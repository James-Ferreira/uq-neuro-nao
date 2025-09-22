import src_py2.api.transcribe as transcribe
import os
import random
import string
import time

class AudioManagerDuo:
    def __init__(self, listener, speaker):
        self.listener = listener
        self.speaker = speaker

    def clean_string(self, text):
        text = text.strip()
        return ''.join([c for c in text.lower() if c == ' ' or (c not in string.punctuation and c not in string.whitespace.replace(' ', ''))])

    def stop_rec(self):
        # Needed because any break in a recording script will cause the recording not to stop, even when command window closed??
        self.listener.nao.audio_recorder.stopMicrophonesRecording()

    def record_audio(self, to_say="My name is Benjamin.", playback=False):
        try:
            # SETUP
            self.stop_rec()
            internal_path = '/home/nao/recordings/audio/audio_recording.wav'
            output_path = "/tmp/recorded_speech.wav"
            channels = [0, 0, 1, 0]

            # START RECORDING
            self.listener.nao.leds.post.fadeRGB("AllLeds", 0xFF0000, 0.1)
            self.listener.nao.audio_recorder.startMicrophonesRecording(internal_path, 'wav', 16000, channels)
            print('Audio recording started.')
            
            # SPEAKER SPEAKS
            time.sleep(random.uniform(0.5, 2))
            self.speaker.nao.tts.say(to_say)
            time.sleep(random.uniform(0.5, 2))

            # STOP LISTENING
            self.listener.nao.audio_recorder.stopMicrophonesRecording()
            self.listener.nao.leds.post.fadeRGB("AllLeds", 0xFFFFFF, 0.1)
            print('Audio recording stopped.')

            # should this be checking the output_path or the input path?
            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                raise ValueError("Zero-length audio can cause recognition failure or hang")

            if playback == True:
                self.listener.nao.audio_player.playFile(internal_path)
                
            self.listener.nao.download_file_from_nao(remote_file_path=internal_path, local_file_path=output_path)

            transcription = transcribe.transcribe_filepath(output_path)

            if transcription:
                self.listener.nao.tts.say("I think you said: " + str(transcription))  # todo: comment/delete this after testing...
                return self.clean_string(transcription)
            else: raise ValueError("Transcription was empty or failed.")
            
        except Exception as e:
            print("Listening error: %s " % (e))
            self.listener.nao.tts.say("I'm sorry, I didn't catch that. Please say it again.")
        
        self.listener.nao.tts.say("Sorry, I couldn't understand. Let's try again later.")
