import os, time, json, re
import src_py2.api.transcribe as transcribe


def _now_watchdog_clock():
    mono = getattr(time, "monotonic", None)
    if callable(mono):
        return mono()
    return time.time()


def _list_input_jobs(inbox_dir):
    names = [n for n in os.listdir(inbox_dir) if n.endswith("_input.json")]
    names.sort()
    return names


def _write_json_atomic(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
    os.rename(tmp, path)


def _now_iso_local():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _normalize_command_text(text):
    """
    Lowercase and strip punctuation/whitespace so phrase matching is robust
    to casing, spacing, and symbols.
    """
    if text is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "", str(text).lower())


def _segments_to_text(segments_list):
    parts = []
    for seg in (segments_list or []):
        try:
            txt = seg[0]
        except Exception:
            txt = None
        if txt:
            parts.append(txt)
    return " ".join(parts).strip()


def _segments_to_duration_sec(segments_list):
    total = 0.0
    for seg in (segments_list or []):
        try:
            dur = seg[3]  # expected: [text, gesture, variant, duration]
        except Exception:
            dur = None
        if isinstance(dur, (int, float)):
            total += float(dur)
    return total


def _single_line(text):
    s = (text or "").strip()
    if not s:
        return "(no speech detected)"
    return re.sub(r"\s+", " ", s)


class NaoJobConsumer(object):
    def __init__(
        self,
        convo,
        model="gesturizer2:latest",
        interlocutor="Dude",
        include_segments=False,
        special_commands=None,
        watchdog_cfg=None,
    ):
        """
        convo: your NAO-side ConversationManager (or equivalent) defining speak_n_gest_next_level(...)
        include_segments: if True, write ai_segments_list into output json (for debugging)
        """
        self.convo = convo
        self.robot = getattr(convo, "robot", None)
        self.model = model
        self.interlocutor = interlocutor
        self.include_segments = include_segments

        self.history = []   # [{"role":"user"/"assistant", "content": "..."}]
        self.turn_count = None
        self.special_commands = {
            "gotosleeplittlerobot": {
                "reply_text": "Going to sleep now.",
                "action": "repose",
            },
            "timetoshutdown": {
                "reply_text": "Shutting down now.",
                "action": "shutdown",
            },
        }
        if isinstance(special_commands, dict):
            for command_key, cfg in special_commands.items():
                if not isinstance(cfg, dict):
                    continue
                base = self.special_commands.get(command_key, {})
                merged = {
                    "reply_text": cfg.get("reply_text", base.get("reply_text", "")),
                    "action": cfg.get("action", base.get("action")),
                }
                self.special_commands[command_key] = merged

        watchdog_cfg = watchdog_cfg or {}
        self.watchdog_enabled = bool(watchdog_cfg.get("enabled", False))
        self.watchdog_mode = bool(watchdog_cfg.get("watchdog_mode", True))
        self.watchdog_activate_after_turn = int(watchdog_cfg.get("activate_after_turn", 0))
        self.watchdog_interval_sec = float(watchdog_cfg.get("interval_sec", 30.0))
        self.watchdog_max_consecutive = int(watchdog_cfg.get("max_consecutive_without_user", 2))
        self.watchdog_ephemeral_system = str(
            watchdog_cfg.get(
                "ephemeral_system_prompt",
                "The participant has not spoken recently. Re-engage with one short, warm, context-aware line. "
                "Do not mention silence, timing, or that this is a watchdog prompt.",
            )
        ).strip()
        self.watchdog_legacy_prompt = str(
            watchdog_cfg.get(
                "legacy_prompt",
                "Please re-engage the participant with one short, warm, context-aware line.",
            )
        ).strip()
        self._last_robot_finish_mono = None
        self._last_input_job_seen_mono = None
        self._watchdog_total = 0
        self._watchdog_consecutive_without_user = 0
        self._watchdog_due_mono = None
        self._watchdog_event_path = None
        self._watchdog_summary_path = None

    def _estimate_script_duration(self, text):
        words = [w for w in (text or "").strip().split() if w]
        return max(2.5, 0.45 * len(words))

    def _match_special_command(self, user_text):
        normalized = _normalize_command_text(user_text)
        if not normalized:
            return None
        for key in self.special_commands:
            if key in normalized:
                return key
        return None

    def _run_special_command(self, command_key, result):
        cfg = self.special_commands.get(command_key, {})
        reply_text = cfg.get("reply_text", "")
        action = cfg.get("action")
        duration_est = self._estimate_script_duration(reply_text)
        scripted_segments = [[reply_text, None, None, duration_est]]

        action_log = {
            "command": command_key,
            "action": action,
            "requested_at": _now_iso_local(),
            "ok": False,
            "error": None,
            "completed_at": None,
        }

        t0 = time.time()
        self.convo.speak_n_gest_next_level(scripted_segments, leds=True)
        try:
            if action == "repose":
                if self.robot is None or getattr(self.robot, "mm", None) is None:
                    raise RuntimeError("robot motion manager unavailable")
                self.robot.mm.repose(False)
            elif action == "shutdown":
                if self.robot is None:
                    raise RuntimeError("robot unavailable")
                if not getattr(self.robot, "usrnme", None) or not getattr(self.robot, "pword", None):
                    raise RuntimeError("robot SSH credentials missing (usrnme/pword)")
                self.robot.shutdown()
            else:
                raise RuntimeError("unknown special action: {}".format(action))

            action_log["ok"] = True
        except Exception as e:
            action_log["error"] = str(e)
            raise
        finally:
            action_log["completed_at"] = _now_iso_local()

        elapsed = max(0.0, time.time() - t0)

        result["ai"] = reply_text
        result["ai_duration_sec"] = elapsed
        result["special_command"] = command_key
        result["special_action"] = action_log
        self._note_robot_utterance_finished()
        return result

    def _note_robot_utterance_finished(self):
        self._last_robot_finish_mono = _now_watchdog_clock()
        if self.watchdog_enabled and int(self.turn_count or 0) >= self.watchdog_activate_after_turn:
            self._watchdog_due_mono = self._last_robot_finish_mono + self.watchdog_interval_sec

    def _note_input_job_seen(self):
        self._last_input_job_seen_mono = _now_watchdog_clock()
        # A fresh user attempt is underway; do not fire watchdog until robot speaks again.
        self._watchdog_due_mono = None

    def _on_nonempty_user_turn(self):
        self._watchdog_consecutive_without_user = 0
        self._write_watchdog_summary()

    def _write_watchdog_event(self, payload):
        if not self._watchdog_event_path:
            return
        try:
            with open(self._watchdog_event_path, "a") as f:
                f.write(json.dumps(payload) + "\n")
        except Exception as e:
            print("Watchdog event log write failed: {}".format(e))

    def _write_watchdog_summary(self):
        if not self._watchdog_summary_path:
            return
        summary = {
            "updated_at": _now_iso_local(),
            "watchdog_enabled": self.watchdog_enabled,
            "watchdog_mode": self.watchdog_mode,
            "watchdog_activate_after_turn": self.watchdog_activate_after_turn,
            "watchdog_interval_sec": self.watchdog_interval_sec,
            "watchdog_max_consecutive_without_user": self.watchdog_max_consecutive,
            "watchdog_total": self._watchdog_total,
            "watchdog_consecutive_without_user": self._watchdog_consecutive_without_user,
        }
        try:
            _write_json_atomic(self._watchdog_summary_path, summary)
        except Exception as e:
            print("Watchdog summary write failed: {}".format(e))

    def _generate_watchdog_segments(self):
        turn_ref = int(self.turn_count or 0)
        prompt = None
        if not self.watchdog_mode:
            prompt = self.watchdog_legacy_prompt
        return transcribe.reply(
            "",
            self.model,
            self.interlocutor,
            list,
            turn_ref,
            prompt=prompt,
            history=self.history,
            watchdog_mode=self.watchdog_mode,
            ephemeral_system=self.watchdog_ephemeral_system,
        )

    def _maybe_fire_watchdog(self):
        if not self.watchdog_enabled:
            return
        if int(self.turn_count or 0) < self.watchdog_activate_after_turn:
            return
        if self._last_robot_finish_mono is None:
            return
        if self._watchdog_consecutive_without_user >= self.watchdog_max_consecutive:
            return
        if self._watchdog_due_mono is None:
            self._watchdog_due_mono = self._last_robot_finish_mono + self.watchdog_interval_sec
        if _now_watchdog_clock() < self._watchdog_due_mono:
            return

        try:
            segments_list = self._generate_watchdog_segments()
        except Exception as e:
            self._watchdog_due_mono = _now_watchdog_clock() + self.watchdog_interval_sec
            self._write_watchdog_event({
                "ts": _now_iso_local(),
                "event": "watchdog_generation_error",
                "error": str(e),
                "watchdog_total_before": self._watchdog_total,
                "consecutive_without_user_before": self._watchdog_consecutive_without_user,
            })
            return

        if not segments_list:
            self._watchdog_due_mono = _now_watchdog_clock() + self.watchdog_interval_sec
            self._write_watchdog_event({
                "ts": _now_iso_local(),
                "event": "watchdog_empty_generation",
                "watchdog_total_before": self._watchdog_total,
                "consecutive_without_user_before": self._watchdog_consecutive_without_user,
            })
            return

        try:
            self.convo.speak_n_gest_next_level(segments_list, leds=True)
        except Exception as e:
            self._watchdog_due_mono = _now_watchdog_clock() + self.watchdog_interval_sec
            self._write_watchdog_event({
                "ts": _now_iso_local(),
                "event": "watchdog_speak_error",
                "error": str(e),
                "watchdog_total_before": self._watchdog_total,
                "consecutive_without_user_before": self._watchdog_consecutive_without_user,
            })
            return

        robot_text = _segments_to_text(segments_list)
        dur_sec = _segments_to_duration_sec(segments_list)
        if robot_text:
            self.history.append({"role": "assistant", "content": robot_text})

        self._watchdog_total += 1
        self._watchdog_consecutive_without_user += 1
        self._note_robot_utterance_finished()
        self._write_watchdog_summary()
        self._write_watchdog_event({
            "ts": _now_iso_local(),
            "event": "watchdog_prompt",
            "watchdog_total": self._watchdog_total,
            "watchdog_mode": self.watchdog_mode,
            "watchdog_activate_after_turn": self.watchdog_activate_after_turn,
            "consecutive_without_user": self._watchdog_consecutive_without_user,
            "interval_sec": self.watchdog_interval_sec,
            "max_consecutive_without_user": self.watchdog_max_consecutive,
            "turn_ref": int(self.turn_count or 0),
            "ai": robot_text,
            "ai_duration_sec": dur_sec,
        })

    def handle_input_job(self, job):
        """
        job: dict from turn_XXXX_input.json
        Returns a result dict (for writing an output file).
        Success is indicated by the absence of an "error" key.
        """
        turn_id = job.get("turn_id")
        user_text = job.get("user") or ""

        self.turn_count = turn_id

        # Base result payload (no "ok" field by design)
        result = {
            "model": self.model,
            "robot": job.get("robot"),
            "interlocutor": self.interlocutor,
            "created_at": _now_iso_local(),
            "turn_id": turn_id,
            "user": user_text,
            "ai": "",
            "ai_duration_sec": 0.0,
        }

        # Empty input: still produce a valid output record (no error)
        if not user_text.strip():
            result["watchdog_total_so_far"] = self._watchdog_total
            result["watchdog_consecutive_without_user"] = self._watchdog_consecutive_without_user
            return result

        matched_command = self._match_special_command(user_text)
        if matched_command:
            try:
                result = self._run_special_command(matched_command, result)
            except Exception as e:
                result["error"] = "special command '{}' failed: {}".format(matched_command, e)
                if "special_action" not in result:
                    cfg = self.special_commands.get(matched_command, {})
                    result["special_action"] = {
                        "command": matched_command,
                        "action": cfg.get("action"),
                        "requested_at": _now_iso_local(),
                        "ok": False,
                        "error": str(e),
                        "completed_at": _now_iso_local(),
                    }
                return result

            self.history.append({"role": "user", "content": user_text})
            if result.get("ai"):
                self.history.append({"role": "assistant", "content": result["ai"]})
            self._on_nonempty_user_turn()
            result["watchdog_total_so_far"] = self._watchdog_total
            result["watchdog_consecutive_without_user"] = self._watchdog_consecutive_without_user
            return result

        # Get gesturized segments list from local Py3 API
        try:
            segments_list = transcribe.reply(
                "",
                self.model,
                self.interlocutor,
                list,
                self.turn_count,
                prompt=user_text,
                history=self.history
            )
        except Exception as e:
            result["error"] = "transcribe.reply raised: {}".format(e)
            return result

        if not segments_list:
            result["error"] = "No segments_list returned"
            return result

        # Speak + gesture
        try:
            self.convo.speak_n_gest_next_level(segments_list, leds=True)
        except Exception as e:
            result["error"] = "speak_n_gest_next_level raised: {}".format(e)
            return result

        # Produce trimmed logging outputs
        robot_text = _segments_to_text(segments_list)
        dur_sec = _segments_to_duration_sec(segments_list)

        result["ai"] = robot_text
        result["ai_duration_sec"] = dur_sec

        # Add this user turn to structured history
        self.history.append({"role": "user", "content": user_text})
        # Keep history for context
        if robot_text:
            self.history.append({"role": "assistant", "content": robot_text})
        self._on_nonempty_user_turn()
        self._note_robot_utterance_finished()
        result["watchdog_total_so_far"] = self._watchdog_total
        result["watchdog_consecutive_without_user"] = self._watchdog_consecutive_without_user

        # Optional debugging payload
        if self.include_segments:
            result["ai_segments_list"] = segments_list

        return result

    def run_job_worker(self, session_dir, poll_sec=0.05):
        """
        Watches sessions/<session_id>/robot_inbox for turn_XXXX_input.json
        Writes results to sessions/<session_id>/robot_outbox/turn_XXXX_output.json
        """
        inbox_dir = os.path.join(session_dir, "robot_inbox")
        outbox_dir = os.path.join(session_dir, "robot_outbox")

        if not os.path.isdir(inbox_dir):
            raise RuntimeError("Inbox not found: {}".format(inbox_dir))
        if not os.path.isdir(outbox_dir):
            os.makedirs(outbox_dir)

        processed = set()
        known_inputs = set()
        self._watchdog_event_path = os.path.join(session_dir, "watchdog_events.jsonl")
        self._watchdog_summary_path = os.path.join(session_dir, "watchdog_summary.json")
        self._write_watchdog_summary()

        print("NAO job worker started")

        while True:
            try:
                jobs = _list_input_jobs(inbox_dir)
                for name in jobs:
                    if name in known_inputs:
                        continue
                    known_inputs.add(name)
                    self._note_input_job_seen()
                for name in jobs:
                    if name in processed:
                        continue

                    job_path = os.path.join(inbox_dir, name)
                    with open(job_path, "r") as f:
                        job = json.load(f)

                    turn_id = job.get("turn_id")
                    done_name = "turn_{:04d}_output.json".format(int(turn_id))
                    done_path = os.path.join(outbox_dir, done_name)

                    # Skip if already processed in a previous run
                    if os.path.isfile(done_path):
                        processed.add(name)
                        continue

                    result = self.handle_input_job(job)

                    _write_json_atomic(done_path, result)

                    user_text = _single_line(job.get("user", ""))
                    ai_text = _single_line(result.get("ai", ""))
                    print("Turn {} | Participant: {} | Robot: {}".format(turn_id, user_text, ai_text))

                    processed.add(name)

                self._maybe_fire_watchdog()
                time.sleep(poll_sec)

            except KeyboardInterrupt:
                print("Worker exiting (KeyboardInterrupt).")
                break
            except Exception as e:
                print("Worker loop error: {}".format(e))
                time.sleep(0.5)
