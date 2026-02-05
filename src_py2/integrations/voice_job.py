import os, time, json
import src_py2.api.transcribe as transcribe


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


class NaoJobConsumer(object):
    def __init__(self, convo, model="gesturizer2:latest", interlocutor="Dude", include_segments=False):
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
            self.convo.speak_n_gest_next_level(segments_list)
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

        print("NAO job worker started")
        print("session_dir: {}".format(session_dir))
        print("inbox_dir: {}".format(inbox_dir))
        print("outbox_dir: {}".format(outbox_dir))
        print("include_segments: {}".format(self.include_segments))

        while True:
            try:
                jobs = _list_input_jobs(inbox_dir)
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

                    print("Processing turn {}".format(turn_id))

                    result = self.handle_input_job(job)

                    _write_json_atomic(done_path, result)

                    processed.add(name)

                time.sleep(poll_sec)

            except KeyboardInterrupt:
                print("Worker exiting (KeyboardInterrupt).")
                break
            except Exception as e:
                print("Worker loop error: {}".format(e))
                time.sleep(0.5)
