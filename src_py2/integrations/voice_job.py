import os, time, json, re
from datetime import datetime
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


def _list_system_jobs(inbox_dir):
    if not os.path.isdir(inbox_dir):
        return []
    names = [n for n in os.listdir(inbox_dir) if n.endswith(".json")]
    names.sort()
    return names


def _write_json_atomic(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
    os.rename(tmp, path)


def _write_text_atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(text)
    os.rename(tmp, path)


def _now_iso_local():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _parse_iso_local(text):
    if not text:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(str(text), fmt)
        except Exception:
            pass
    return None


def _seconds_between(start_text, end_text):
    start_dt = _parse_iso_local(start_text)
    end_dt = _parse_iso_local(end_text)
    if start_dt is None or end_dt is None:
        return None
    delta = (end_dt - start_dt).total_seconds()
    if delta < 0:
        return 0.0
    return float(delta)


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


def _dialogue_line(turn_id, speaker, text):
    return 'turn_{} {}: {}'.format(str(turn_id), speaker, json.dumps("" if text is None else str(text), ensure_ascii=False))


def _count_words(text):
    return len(re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*", str(text or "")))


def _load_watchdog_prompts(session_dir):
    event_path = os.path.join(session_dir, "watchdog_events.jsonl")
    prompts_by_turn = {}

    if not os.path.isfile(event_path):
        return prompts_by_turn

    with open(event_path, "r") as f:
        for raw_line in f:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                payload = json.loads(raw_line)
            except Exception:
                continue

            if payload.get("event") != "watchdog_prompt":
                continue

            turn_ref = payload.get("turn_ref")
            if turn_ref is None:
                continue

            try:
                turn_ref = int(turn_ref)
            except Exception:
                continue

            prompts_by_turn.setdefault(turn_ref, []).append(payload.get("ai", ""))

    return prompts_by_turn


def _rewrite_session_dialogue(session_dir):
    inbox_dir = os.path.join(session_dir, "robot_inbox")
    outbox_dir = os.path.join(session_dir, "robot_outbox")
    dialogue_path = os.path.join(session_dir, "session_dialogue.txt")
    watchdog_prompts = _load_watchdog_prompts(session_dir)

    turn_ids = set()

    if os.path.isdir(inbox_dir):
        for name in os.listdir(inbox_dir):
            match = re.match(r"turn_(\d+)_input\.json$", name)
            if match:
                turn_ids.add(int(match.group(1)))

    if os.path.isdir(outbox_dir):
        for name in os.listdir(outbox_dir):
            match = re.match(r"turn_(\d+)_output\.json$", name)
            if match:
                turn_ids.add(int(match.group(1)))

    lines = []
    for turn_id in sorted(turn_ids):
        input_path = os.path.join(inbox_dir, "turn_{:04d}_input.json".format(turn_id))
        output_path = os.path.join(outbox_dir, "turn_{:04d}_output.json".format(turn_id))

        user_text = ""
        ai_text = ""

        if os.path.isfile(input_path):
            with open(input_path, "r") as f:
                input_payload = json.load(f)
            user_text = input_payload.get("user", "")

        if os.path.isfile(output_path):
            with open(output_path, "r") as f:
                output_payload = json.load(f)
            ai_text = output_payload.get("ai", "")

        if not str(user_text or "").strip() and not str(ai_text or "").strip():
            continue

        lines.append(_dialogue_line(turn_id, "user", user_text))
        lines.append(_dialogue_line(turn_id, "robot", ai_text))

        for idx, watchdog_text in enumerate(watchdog_prompts.get(turn_id, []), start=1):
            lines.append(_dialogue_line("{}_{}".format(turn_id, idx), "watchdog", watchdog_text))

    text = "\n".join(lines)
    if text:
        text += "\n"
    _write_text_atomic(dialogue_path, text)


def _write_language_metrics_summary(session_dir):
    inbox_dir = os.path.join(session_dir, "robot_inbox")
    outbox_dir = os.path.join(session_dir, "robot_outbox")
    summary_path = os.path.join(session_dir, "session_language_metrics.json")

    turn_ids = set()
    if os.path.isdir(inbox_dir):
        for name in os.listdir(inbox_dir):
            match = re.match(r"turn_(\d+)_input\.json$", name)
            if match:
                turn_ids.add(int(match.group(1)))
    if os.path.isdir(outbox_dir):
        for name in os.listdir(outbox_dir):
            match = re.match(r"turn_(\d+)_output\.json$", name)
            if match:
                turn_ids.add(int(match.group(1)))

    total_words = 0
    spoken_turns = 0
    total_speaking_time_sec = 0.0
    latency_vals = []

    for turn_id in sorted(turn_ids):
        input_path = os.path.join(inbox_dir, "turn_{:04d}_input.json".format(turn_id))
        output_path = os.path.join(outbox_dir, "turn_{:04d}_output.json".format(turn_id))

        input_payload = {}
        output_payload = {}

        if os.path.isfile(input_path):
            try:
                with open(input_path, "r") as f:
                    input_payload = json.load(f)
            except Exception:
                input_payload = {}

        if os.path.isfile(output_path):
            try:
                with open(output_path, "r") as f:
                    output_payload = json.load(f)
            except Exception:
                output_payload = {}

        word_count = _count_words(input_payload.get("user", ""))
        if word_count <= 0:
            continue

        spoken_turns += 1
        total_words += word_count

        try:
            duration_sec = float(input_payload.get("participant_duration_sec") or 0.0)
        except Exception:
            duration_sec = 0.0
        if duration_sec > 0:
            total_speaking_time_sec += duration_sec

        try:
            latency_sec = output_payload.get("latency_sec")
            if latency_sec is not None:
                latency_sec = float(latency_sec)
                if latency_sec >= 0:
                    latency_vals.append(latency_sec)
        except Exception:
            pass

    summary = {
        "updated_at": _now_iso_local(),
        "spoken_turn_count": spoken_turns,
        "total_words": total_words,
        "mean_words_per_turn": (float(total_words) / float(spoken_turns)) if spoken_turns else None,
        "total_speaking_time_sec": total_speaking_time_sec,
        "word_rate_wps": (float(total_words) / float(total_speaking_time_sec)) if total_speaking_time_sec > 0 else None,
        "latency_turn_count": len(latency_vals),
        "mean_latency_sec": (sum(latency_vals) / float(len(latency_vals))) if latency_vals else None,
    }

    try:
        _write_json_atomic(summary_path, summary)
    except Exception as e:
        print("Session language metrics write failed: {}".format(e))


def _as_bool(value, default=False):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    text = str(value).strip().lower()
    if text in ("1", "true", "t", "yes", "y", "on"):
        return True
    if text in ("0", "false", "f", "no", "n", "off", ""):
        return False
    return default


class NaoJobConsumer(object):
    def __init__(
        self,
        convo,
        model="gesturizer2:latest",
        interlocutor=None,
        include_segments=False,
        special_commands=None,
        watchdog_cfg=None,
        session_end_cfg=None,
        require_enter_before_speak=False,
        require_enter_for_watchdog=False,
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
        self.turn_count = 0
        self.current_turn_id = None
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
        self._input_attempt_in_progress = False
        self._watchdog_total = 0
        self._watchdog_consecutive_without_user = 0
        self._watchdog_due_mono = None
        self._watchdog_event_path = None
        self._watchdog_summary_path = None
        self._last_robot_finish_at = None

        session_end_cfg = session_end_cfg or {}
        self.session_end_enabled = bool(session_end_cfg.get("enabled", False))
        self.session_end_after_sec = float(session_end_cfg.get("after_sec", 0.0))
        self.session_end_use_model_closing_instruction = _as_bool(
            session_end_cfg.get("use_model_closing_instruction", False), False
        )
        self.session_end_model_closing_instruction = str(
            session_end_cfg.get("model_closing_instruction", "")
        ).strip()
        self.session_end_append_final_line = _as_bool(
            session_end_cfg.get("append_final_line", True), True
        )
        self.session_end_final_line = str(session_end_cfg.get("final_line", "")).strip()
        self.session_end_action = str(session_end_cfg.get("action", "")).strip() or None
        self.session_end_stop_worker = _as_bool(session_end_cfg.get("stop_worker", True), True)
        self._session_started_mono = _now_watchdog_clock()
        self._session_started_at = _now_iso_local()
        self._session_end_announced = False
        self._session_end_turn_id = None
        self._session_end_armed = False
        self._session_end_armed_at = None
        self._session_end_armed_turn_id = None
        self._session_should_stop_worker = False
        self._session_end_summary_path = None

        self.require_enter_before_speak = _as_bool(require_enter_before_speak, False)
        self.require_enter_for_watchdog = _as_bool(require_enter_for_watchdog, False)

        env_gate = os.getenv("NAO_REQUIRE_ENTER_BEFORE_SPEAK")
        if env_gate is not None:
            self.require_enter_before_speak = _as_bool(env_gate, self.require_enter_before_speak)

        env_watchdog_gate = os.getenv("NAO_REQUIRE_ENTER_FOR_WATCHDOG")
        if env_watchdog_gate is not None:
            self.require_enter_for_watchdog = _as_bool(
                env_watchdog_gate, self.require_enter_for_watchdog
            )

    def _wait_for_operator_enter(self, source_label):
        if not self.require_enter_before_speak:
            return
        if source_label == "watchdog" and not self.require_enter_for_watchdog:
            return

        prompt = (
            "\n[operator_gate] Reply is ready ({src}). "
            "Press Enter in this terminal to execute robot speech/gestures... "
        ).format(src=source_label)

        try:
            raw_input(prompt)
        except EOFError:
            print("[operator_gate] stdin unavailable; continuing without Enter confirmation.")
        except Exception as e:
            print("[operator_gate] Enter gate failed ({}); continuing.".format(e))

    def _release_turn_gate_if_held(self, reason):
        """
        Release bumper turn gate when no robot speech will run.
        speak_n_gest_next_level() normally releases this in finally, but early-return
        paths (empty input, generation errors) need a manual release to avoid deadlock.
        """
        if not hasattr(self.convo, "turn_gate"):
            return
        gate = self.convo.turn_gate
        if not gate.locked():
            return
        try:
            gate.release()
            self.convo.turn_in_progress = False
            print("Turn gate released without robot speech: {}".format(reason))
            try:
                self.convo.set_ready_mode()
            except Exception as led_error:
                print("WARN: set_ready_mode failed after gate release: {}".format(led_error))
        except Exception as e:
            print("WARN: could not release turn gate ({}): {}".format(reason, e))

    def _estimate_script_duration(self, text):
        words = [w for w in (text or "").strip().split() if w]
        return max(2.5, 0.45 * len(words))

    def _handle_system_say_job(self, job):
        text = (job.get("text") or "").strip()
        result = {
            "kind": "say",
            "created_at": _now_iso_local(),
            "source": job.get("source"),
            "text": text,
            "ok": False,
            "skipped": False,
        }

        if not text:
            result["skipped"] = True
            result["error"] = "empty system say text"
            return result

        if hasattr(self.convo, "turn_gate") and not self.convo.turn_gate.acquire(False):
            return None

        self.convo.turn_in_progress = True

        segments_list = [[text, None, None, self._estimate_script_duration(text)]]
        try:
            self._wait_for_operator_enter("system_say")
            self.convo.speak_n_gest_next_level(segments_list, leds=True)
            self._note_robot_utterance_finished()
            result["ok"] = True
            result["robot_finish_at"] = self._last_robot_finish_at
            result["ai_duration_sec"] = _segments_to_duration_sec(segments_list)
            return result
        except Exception as e:
            self._release_turn_gate_if_held("system_say_error")
            result["error"] = "system say failed: {}".format(e)
            return result

    def handle_system_job(self, job):
        kind = str(job.get("kind") or "").strip().lower()
        if kind == "say":
            return self._handle_system_say_job(job)
        return {
            "kind": kind,
            "created_at": _now_iso_local(),
            "ok": False,
            "skipped": True,
            "error": "unknown system job kind: {}".format(kind or "(missing)"),
        }

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
        self._wait_for_operator_enter("special_command")
        self.convo.speak_n_gest_next_level(scripted_segments, leds=True)
        try:
            self._perform_robot_action(action)

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
        result["robot_finish_at"] = self._last_robot_finish_at
        return result

    def _perform_robot_action(self, action):
        if action == "repose":
            if self.robot is None or getattr(self.robot, "mm", None) is None:
                raise RuntimeError("robot motion manager unavailable")
            self.robot.mm.repose(False)
            return
        if action == "shutdown":
            if self.robot is None:
                raise RuntimeError("robot unavailable")
            if not getattr(self.robot, "usrnme", None) or not getattr(self.robot, "pword", None):
                raise RuntimeError("robot SSH credentials missing (usrnme/pword)")
            self.robot.shutdown()
            return
        raise RuntimeError("unknown special action: {}".format(action))

    def _session_elapsed_sec(self):
        return max(0.0, _now_watchdog_clock() - self._session_started_mono)

    def _is_session_end_due(self):
        if not self.session_end_enabled:
            return False
        if self._session_end_announced:
            return False
        if self.session_end_after_sec <= 0:
            return False
        return self._session_elapsed_sec() >= self.session_end_after_sec

    def _append_session_final_line(self, segments_list):
        if (not self.session_end_append_final_line) or (not self.session_end_final_line):
            return segments_list
        merged = list(segments_list or [])
        merged.append(
            [
                self.session_end_final_line,
                None,
                None,
                self._estimate_script_duration(self.session_end_final_line),
            ]
        )
        return merged

    def _mark_session_end_announced(self, turn_id):
        self._session_end_announced = True
        self._session_end_turn_id = turn_id
        self._session_should_stop_worker = self.session_end_stop_worker
        self._write_session_end_summary()

    def _arm_session_end(self, turn_id=None):
        if self._session_end_armed:
            return
        self._session_end_armed = True
        self._session_end_armed_at = _now_iso_local()
        self._session_end_armed_turn_id = turn_id
        self._write_session_end_summary()

    def _write_session_end_summary(self):
        if not self._session_end_summary_path:
            return
        summary = {
            "updated_at": _now_iso_local(),
            "enabled": self.session_end_enabled,
            "after_sec": self.session_end_after_sec,
            "use_model_closing_instruction": self.session_end_use_model_closing_instruction,
            "model_closing_instruction": self.session_end_model_closing_instruction,
            "append_final_line": self.session_end_append_final_line,
            "final_line": self.session_end_final_line,
            "action": self.session_end_action,
            "stop_worker": self.session_end_stop_worker,
            "session_started_at": self._session_started_at,
            "session_elapsed_sec": self._session_elapsed_sec(),
            "session_end_armed": self._session_end_armed,
            "session_end_armed_at": self._session_end_armed_at,
            "session_end_armed_turn_id": self._session_end_armed_turn_id,
            "session_end_announced": self._session_end_announced,
            "session_end_turn_id": self._session_end_turn_id,
            "session_should_stop_worker": self._session_should_stop_worker,
        }
        try:
            _write_json_atomic(self._session_end_summary_path, summary)
        except Exception as e:
            print("Session end summary write failed: {}".format(e))

    def _note_robot_utterance_finished(self):
        self._last_robot_finish_mono = _now_watchdog_clock()
        self._last_robot_finish_at = _now_iso_local()
        if self.watchdog_enabled and int(self.turn_count or 0) >= self.watchdog_activate_after_turn:
            self._watchdog_due_mono = self._last_robot_finish_mono + self.watchdog_interval_sec

    def _note_input_job_seen(self):
        self._last_input_job_seen_mono = _now_watchdog_clock()
        # A fresh user attempt is underway; do not fire watchdog until robot speaks again.
        self._watchdog_due_mono = None

    def note_input_attempt_started(self):
        self._input_attempt_in_progress = True

    def note_input_attempt_finished(self):
        self._input_attempt_in_progress = False

    def _on_nonempty_user_turn(self):
        self.turn_count = int(self.turn_count or 0) + 1
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
            return False
        if self._input_attempt_in_progress:
            return False
        if int(self.turn_count or 0) < self.watchdog_activate_after_turn:
            return False
        if self._last_robot_finish_mono is None:
            return False
        if self._watchdog_consecutive_without_user >= self.watchdog_max_consecutive:
            return False
        if self._watchdog_due_mono is None:
            self._watchdog_due_mono = self._last_robot_finish_mono + self.watchdog_interval_sec
        if _now_watchdog_clock() < self._watchdog_due_mono:
            return False

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
            return False

        if not segments_list:
            self._watchdog_due_mono = _now_watchdog_clock() + self.watchdog_interval_sec
            self._write_watchdog_event({
                "ts": _now_iso_local(),
                "event": "watchdog_empty_generation",
                "watchdog_total_before": self._watchdog_total,
                "consecutive_without_user_before": self._watchdog_consecutive_without_user,
            })
            return False

        try:
            self._wait_for_operator_enter("watchdog")
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
            return False

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
            "robot_finish_at": self._last_robot_finish_at,
        })
        return True

    def handle_input_job(self, job):
        """
        job: dict from turn_XXXX_input.json
        Returns a result dict (for writing an output file).
        Success is indicated by the absence of an "error" key.
        """
        turn_id = job.get("turn_id")
        user_text = job.get("user") or ""
        recording_started_at = job.get("recording_started_at")

        self.current_turn_id = turn_id
        latency_sec = _seconds_between(self._last_robot_finish_at, recording_started_at)

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
            "latency_sec": latency_sec,
        }
        if self.session_end_enabled:
            result["session_elapsed_sec"] = self._session_elapsed_sec()

        # Empty input: still produce a valid output record (no error)
        if not user_text.strip():
            self._release_turn_gate_if_held("empty_user_text")
            result["watchdog_total_so_far"] = self._watchdog_total
            result["watchdog_consecutive_without_user"] = self._watchdog_consecutive_without_user
            return result

        matched_command = self._match_special_command(user_text)
        if matched_command:
            try:
                result = self._run_special_command(matched_command, result)
            except Exception as e:
                self._release_turn_gate_if_held("special_command_error")
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

        session_end_due = False
        if self.session_end_enabled:
            if self._session_end_armed:
                session_end_due = True
            elif self._is_session_end_due():
                self._arm_session_end(turn_id=turn_id)
                result["session_end_armed_this_turn"] = True
        session_end_ephemeral_system = None
        if (
            session_end_due
            and self.session_end_use_model_closing_instruction
            and self.session_end_model_closing_instruction
        ):
            session_end_ephemeral_system = self.session_end_model_closing_instruction
            result["session_end_model_closing_instruction_applied"] = True

        # Get gesturized segments list from local Py3 API
        try:
            segments_list = transcribe.reply(
                "",
                self.model,
                self.interlocutor,
                list,
                int(self.turn_count or 0) + 1,
                prompt=user_text,
                history=self.history,
                ephemeral_system=session_end_ephemeral_system,
            )
        except Exception as e:
            self._release_turn_gate_if_held("transcribe_reply_error")
            result["error"] = "transcribe.reply raised: {}".format(e)
            return result

        if not segments_list:
            self._release_turn_gate_if_held("empty_segments_list")
            result["error"] = "No segments_list returned"
            return result

        if (not session_end_due) and self._is_session_end_due():
            if not self._session_end_armed:
                self._arm_session_end(turn_id=turn_id)
                result["session_end_armed_after_generation"] = True
        if session_end_due:
            segments_list = self._append_session_final_line(segments_list)
            result["session_end_due_before_reply"] = True

        # Speak + gesture
        try:
            self._wait_for_operator_enter("turn_reply")
            self.convo.speak_n_gest_next_level(segments_list, leds=True)
        except Exception as e:
            self._release_turn_gate_if_held("speak_n_gest_error")
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
        result["robot_finish_at"] = self._last_robot_finish_at
        result["watchdog_total_so_far"] = self._watchdog_total
        result["watchdog_consecutive_without_user"] = self._watchdog_consecutive_without_user
        if self.session_end_enabled:
            result["session_elapsed_sec"] = self._session_elapsed_sec()

        # Optional debugging payload
        if self.include_segments:
            result["ai_segments_list"] = segments_list

        if session_end_due:
            result["session_end_triggered"] = True
            result["session_end_stop_worker"] = self.session_end_stop_worker
            result["session_end_action"] = self.session_end_action

            action_error = None
            if self.session_end_action:
                try:
                    self._perform_robot_action(self.session_end_action)
                except Exception as e:
                    action_error = str(e)
                    print("Session end action failed: {}".format(e))
            if action_error:
                result["session_end_action_error"] = action_error

            self._mark_session_end_announced(turn_id)

        return result

    def run_job_worker(self, session_dir, poll_sec=0.05):
        """
        Watches sessions/<session_id>/robot_inbox for turn_XXXX_input.json
        Writes results to sessions/<session_id>/robot_outbox/turn_XXXX_output.json
        """
        inbox_dir = os.path.join(session_dir, "robot_inbox")
        outbox_dir = os.path.join(session_dir, "robot_outbox")
        system_inbox_dir = os.path.join(session_dir, "robot_system_inbox")
        system_done_dir = os.path.join(session_dir, "robot_system_done")

        if not os.path.isdir(inbox_dir):
            raise RuntimeError("Inbox not found: {}".format(inbox_dir))
        if not os.path.isdir(outbox_dir):
            os.makedirs(outbox_dir)
        if not os.path.isdir(system_inbox_dir):
            os.makedirs(system_inbox_dir)
        if not os.path.isdir(system_done_dir):
            os.makedirs(system_done_dir)

        processed = set()
        known_inputs = set()
        self._watchdog_event_path = os.path.join(session_dir, "watchdog_events.jsonl")
        self._watchdog_summary_path = os.path.join(session_dir, "watchdog_summary.json")
        self._session_end_summary_path = os.path.join(session_dir, "session_end_summary.json")
        self._write_watchdog_summary()
        self._write_session_end_summary()
        _write_language_metrics_summary(session_dir)

        print("NAO job worker started")

        while True:
            try:
                system_jobs = _list_system_jobs(system_inbox_dir)
                for name in system_jobs:
                    job_path = os.path.join(system_inbox_dir, name)
                    try:
                        with open(job_path, "r") as f:
                            job = json.load(f)
                    except Exception as e:
                        print("System job read failed ({}): {}".format(name, e))
                        continue

                    result = self.handle_system_job(job)
                    if result is None:
                        continue

                    done_path = os.path.join(system_done_dir, name)
                    _write_json_atomic(done_path, result)
                    try:
                        os.remove(job_path)
                    except Exception as e:
                        print("System job cleanup failed ({}): {}".format(name, e))

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
                    _rewrite_session_dialogue(session_dir)
                    _write_language_metrics_summary(session_dir)

                    user_text = _single_line(job.get("user", ""))
                    ai_text = _single_line(result.get("ai", ""))
                    print("Turn {} | Participant: {} | Robot: {}".format(turn_id, user_text, ai_text))

                    processed.add(name)
                    if result.get("session_end_triggered") and self._session_should_stop_worker:
                        print("Session end condition met at turn {}. Exiting worker.".format(turn_id))
                        return

                if self._maybe_fire_watchdog():
                    _write_language_metrics_summary(session_dir)
                time.sleep(poll_sec)

            except KeyboardInterrupt:
                print("Worker exiting (KeyboardInterrupt).")
                break
            except Exception as e:
                print("Worker loop error: {}".format(e))
                time.sleep(0.5)
