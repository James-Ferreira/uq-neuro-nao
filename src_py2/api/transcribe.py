import requests
import os

def transcribe_filepath(filepath):
    # relies on the api having access to the same file system
    api_url = "http://localhost:5000/transcribe/filepath"

    if not os.path.exists(filepath):
        print("Audio file not found at {}".format(filepath))
        return None

    try:
        response = requests.post(api_url, json={
            'filepath': filepath,
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
        print("Error calling transcription API: {}".format(e))
        return None
    except IOError as e:
        print("Error opening audio file: {}".format(e))
        return None
    

def transcribe_file(filepath):
    api_url = "http://localhost:5000/transcribe/file"

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
    

def reply(transcript, model):
    api_url = "http://localhost:5000/converse"

    try:
        response = requests.post(api_url, json={'transcription': transcript, 'model': model})
        response.raise_for_status()
        data = response.json()
        reply = data.get('response')

        if reply:
            print("Reply '{}'".format(reply))
            return reply
        else:
            print("Error: API returned empty reply.")
            return None
    except Exception as e:
        print("Error calling reply API: {}".format(e))
        return None