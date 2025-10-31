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
    

def reply(transcript, model, interlocutor, type):
    api_url = "http://localhost:5000/converse"

    try:
        response = requests.post(api_url, json={'transcription': transcript, 'model': model, 'interlocutor': interlocutor})
        response.raise_for_status()
        data = response.json()
        print("JSON DATA: {}".format(data))
        reply = data.get('response')
        reply_segments_list = data.get('segments_list')

        if reply:
            if type == str:
                print("Reply '{}'".format(reply))
                return reply
            elif type == list:
                print("Reply '{}'".format(reply))
                return reply_segments_list
        else:
            print("Error: API returned empty reply.")
            return None
    except Exception as e:
        print("Error calling reply API: {}".format(e))
        return None