import os, time, json
import src_py2.api.transcribe as transcribe


def _list_input_jobs(outbox_dir):
    # only process published files (not .tmp)
    names = [n for n in os.listdir(outbox_dir) if n.endswith(".input.json")]
    names.sort()
    return names


def _write_json_atomic(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2)
    os.rename(tmp, path)


class NaoJobConsumer(object):
    def __init__(self, convo, model="gesturizer2:latest", interlocutor="Dude"):
        """
        convo: an instance of your existing NAO-side ConversationManager (or equivalent)
               that defines speak_n_gest_next_level(...)
        """
        self.convo = convo
        self.robot = getattr(convo, "robot", None)  # optional, handy for debugging
        self.model = model
        self.interlocutor = interlocutor
        self.transcript = ""  # persistent session transcript

    def handle_input_job(self, job):
        """
        job: dict from turn_XXXX.input.json
        Returns a result dict (for writing a done/ack file).
        """
        turn_id = job.get("turn_id")
        user_text = job.get("user") or ""

        # Always produce an ack, even on empty speech
        result = {
            "version": 1,
            "kind": "done",
            "turn_id": turn_id,
            "ok": False,
            "error": None,
            "robot": job.get("robot"),
            "user": user_text,
            "ai_segments_list": None,
        }

        if not user_text.strip():
            # Nothing to do: no LLM call, no motion
            result["ok"] = True
            return result

        # Update running transcript for context
        self.transcript += "Speaker: {}\n".format(user_text)

        # Get gesturized segments list from your local Py3 API via transcribe.reply
        try:
            segments_list = transcribe.reply(
                self.transcript,
                self.model,
                self.interlocutor,
                list
            )
        except Exception as e:
            result["error"] = "transcribe.reply raised: {}".format(e)
            return result

        if not segments_list:
            result["error"] = "No segments_list returned"
            return result

        # Speak + gesture (delegate to your existing conversation manager)
        try:
            self.convo.speak_n_gest_next_level(segments_list)
        except Exception as e:
            result["error"] = "speak_n_gest_next_level raised: {}".format(e)
            return result

        # Append robot text to transcript (your segments_list carries segment strings)
        try:
            robot_text = " ".join([seg[0] for seg in segments_list if seg and seg[0]])
            self.transcript += "Robot: {}\n".format(robot_text)
        except Exception:
            # Not fatal; transcript is just context
            pass

        result["ai_segments_list"] = segments_list
        result["ok"] = True
        return result

    def run_job_worker(self, session_dir, poll_sec=0.05):
        """
        Watches sessions/<session_id>/robot_outbox for turn_XXXX.input.json
        Writes results to sessions/<session_id>/robot_inbox/turn_XXXX.done.json
        """
        outbox_dir = os.path.join(session_dir, "robot_outbox")
        inbox_dir = os.path.join(session_dir, "robot_inbox")

        if not os.path.isdir(outbox_dir):
            raise RuntimeError("Outbox not found: {}".format(outbox_dir))
        if not os.path.isdir(inbox_dir):
            os.makedirs(inbox_dir)

        processed = set()

        print("NAO job worker started")
        print("  session_dir: {}".format(session_dir))
        print("  outbox_dir:  {}".format(outbox_dir))
        print("  inbox_dir:   {}".format(inbox_dir))

        while True:
            try:
                jobs = _list_input_jobs(outbox_dir)
                for name in jobs:
                    if name in processed:
                        continue

                    job_path = os.path.join(outbox_dir, name)
                    with open(job_path, "r") as f:
                        job = json.load(f)

                    turn_id = job.get("turn_id")
                    print("Processing turn {}".format(turn_id))

                    result = self.handle_input_job(job)

                    done_name = "turn_{:04d}.done.json".format(int(turn_id))
                    done_path = os.path.join(inbox_dir, done_name)
                    _write_json_atomic(done_path, result)

                    processed.add(name)

                time.sleep(poll_sec)

            except KeyboardInterrupt:
                print("Worker exiting (KeyboardInterrupt).")
                break
            except Exception as e:
                print("Worker loop error: {}".format(e))
                time.sleep(0.5)
