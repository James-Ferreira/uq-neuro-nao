import requests
import os

API_BASE = os.getenv("UQ_PY3_API", "http://localhost:5001")

def transcribe_filepath(filepath):
    # relies on the api having access to the same file system
    api_url = API_BASE.rstrip("/") + "/transcribe/filepath"

    if not os.path.exists(filepath):
        print("Audio file not found at {}".format(filepath))
        return None

    try:
        response = requests.post(api_url, json={
            'filepath': filepath
        })
        response.raise_for_status()
        transcription_data = response.json()
        transcription = transcription_data.get('transcription')

        if transcription:
            print("Transcribed '{}'".format(transcription))
            return transcription
        else:
            print("Error: API returned empty transcription.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error calling transcription API. Did you TURN ON python3!?!: {}".format(e))
        return None
    except IOError as e:
        print("Error opening audio file: {}".format(e))
        return None


def transcribe_file(filepath):
    api_url = API_BASE.rstrip("/") + "/transcribe/file"

    if not os.path.exists(filepath):
        print("Audio file not found at {}".format(filepath))
        return None

    try:
        with open(filepath, 'rb') as audio_file:
            files = {'audio': (os.path.basename(filepath), audio_file, 'audio/wav')}
            response = requests.post(api_url, files=files)
            response.raise_for_status()
            transcription_data = response.json()
            transcription = transcription_data.get('transcription')

            if transcription:
                print("Transcribed '{}'".format(transcription))
                return transcription
            else:
                print("Error: API returned empty transcription.")
                return None

    except requests.exceptions.RequestException as e:
        print("Error calling transcription API: {}".format(e))
        return None
    except IOError as e:
        print("Error opening audio file: {}".format(e))
        return None

DEBUG = False

def reply(
    transcript,
    model,
    interlocutor,
    type,
    turn_count,
    prompt=None,
    history=None,
    watchdog_mode=False,
    ephemeral_system=None,
):
    api_url = API_BASE.rstrip("/") + "/converse"
    safe_interlocutor = None if interlocutor is None else str(interlocutor).strip() or None

    payload = {
        'model': model,
        'turn_count': turn_count,
    }
    if safe_interlocutor:
        payload['interlocutor'] = safe_interlocutor

    if watchdog_mode:
        payload["watchdog_mode"] = True
    if ephemeral_system:
        payload["ephemeral_system"] = ephemeral_system

    # Preferred new path: structured history + current prompt (or watchdog generation)
    if prompt is not None or history is not None or watchdog_mode:
        payload['history'] = history or []
        if prompt is not None:
            payload['prompt'] = prompt
    else:
        # Backward-compatible legacy path: labeled transcript string
        payload['transcription'] = transcript

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        data = response.json()
        if DEBUG:
            print("JSON DATA: {}".format(data))
        reply = data.get('response')
        reply_segments_list = data.get('segments_list')
        if DEBUG:
            print("REPLY_SEGMENTS_LIST: {}".format(reply_segments_list))

        if reply:
            if type == str:
                if DEBUG:
                    print("Reply '{}'".format(reply))
                return reply
            elif type == list:
                if DEBUG:
                    print("Reply '{}'".format(reply))
                return reply_segments_list
        else:
            print("Error: API returned empty reply.")
            return None
    except Exception as e:
        print("Error calling reply API: {}".format(e))
        return None
