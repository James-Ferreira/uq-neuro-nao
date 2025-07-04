import os
import api.transcribe as transcribe
import time
import string

class AudioManager:
    # todo (?): rename robot arg to nao ?
    def __init__(self, robot):
        self.nao = robot

    def pitch_change(self):
        current_pitch = self.nao.tts.getParameter('pitchShift')
        print("Current pitch: {}".format(current_pitch))
        print("Pitch range: 0.5 - 4")
        user_input = raw_input("Please enter a value for pitch: ")  # type: ignore (suppressess superfluous warning)
        self.nao.tts.setParameter("pitchShift", float(user_input))

    def set_pitch(self, value):
        self.nao.tts.setParameter("pitchShift", float(value))

    def set_volume(self, value):
        self.nao.audio_player.setMasterVolume(float(value))

    def stop_rec(self):
        # Needed because any break in a recording script will cause the recording not to stop, even when command window closed??
        self.nao.audio_recorder.stopMicrophonesRecording()

    # add parameter for announcing, "I'm listening"?
    def listen(self, duration):
        try:
            self.nao.tts.say("I'm listening.")
            self.nao.audio_player.post.playFile(sound_library["start_listening"])
            
            self.nao.leds.post.fadeRGB("AllLeds", 0xFF0000, 0.1)
            audio_path = "/tmp/recorded_speech.wav"
            self.record_audio(duration, audio_path)
            self.nao.leds.post.fadeRGB("AllLeds", 0xFFFFFF, 0.1)

            if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
                raise ValueError("Zero-length audio can cause recognition failure or hang")

            self.nao.audio_player.post.playFile(sound_library["stop_listening"])

            transcription = transcribe.transcribe_filepath(audio_path)
            if transcription:
                # self.nao.leds.post.fadeRGB("AllLeds", 0x00FF00, 0.1)
                # self.nao.tts.say("I think you said: " + str(transcription))
                # self.nao.leds.post.fadeRGB("AllLeds", 0xFFFFFF, 0.1)

                return clean_string(transcription)
            else:
                raise ValueError("Transcription was empty or failed.")
            
        except Exception as e:
            print("Listening error: %s " % (e))
            self.nao.tts.say("I'm sorry, I didn't catch that. Please say it again.")
        
        self.nao.tts.say("Sorry, I couldn't understand. Let's try again later.")

    def listen_until_confirmed(self, duration=2.5):
        while True:
            try:
                self.nao.audio_player.post.playFile(sound_library["start_listening"])
                self.nao.tts.say("I'm listening")
                self.nao.leds.post.fadeRGB("FaceLeds", 0x00FF00, 0.1)

                audio_path = "/tmp/recorded_speech.wav"
                self.record_audio(duration, audio_path)
                self.nao.leds.post.fadeRGB("FaceLeds", 0xFFFFFF, 0.1)

                if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
                    raise ValueError("Zero-length audio can cause recognition failure or hang")

                # removing .post from below to see if that stops speech from occuring as end sound plays
                self.nao.audio_player.playFile(sound_library["stop_listening"])

                transcription = transcribe.transcribe_filepath(audio_path)
                if not transcription:
                    raise ValueError("Transcription was empty or failed.")

                cleaned_input = clean_string(transcription)

                self.nao.tts.post.say(
                    "I heard {}. Is that correct? "
                    "Press my hand for yes, or my foot for no.".format(cleaned_input))
                
                confirmed = self.nao.tm.wait_for_touch_confirm()

                if confirmed:
                    self.nao.tts.say("Confirmed.")
                    return cleaned_input
                else:
                    self.nao.tts.say("Okay, let's try again.")
            
            except Exception as e:
                print("Listening error: %s" % e)
                self.nao.tts.say("I'm sorry, I didn't catch that.")
                self.nao.tts.say("Let's try again.")    

    def converse(self, rounds=3):
        transcription = ""

        for i in range(rounds):
            try:
                print("Listening...")
                input = self.listen(5)
                if not input:
                    print("No input received.")
                    continue


                self.nao.tts.post.say(
                "I heard {}. Is that correct? "
                "Press my hand for yes, or my foot for no.".format(input))
                confirmed = self.nao.tm.wait_for_touch_confirm()
                if not confirmed:
                    self.nao.tts.say("REJECTED")
                    continue

                self.nao.tts.say("CONFIRMED")

                transcription += "Speaker: {}\n".format(input)

                ai_reply = transcribe.reply(transcription)
                if ai_reply:
                    self.nao.tts.say(str(ai_reply))
                    transcription += "Robot: {}\n".format(ai_reply)
                else:
                    print("AI did not return a reply.\n")

            except Exception as e:
                print("Error during conversation round {}: {}".format(i + 1, e))
                continue
        return transcription

    def record_audio(self, duration, output_path, playback=False):
        self.stop_rec()

        internal_path = '/home/nao/recordings/audio/audio_recording.wav'
        
        # channels can be =
        # [1, 0, 0, 0] for left microphone only
        # [0, 1, 0, 0] for right microphone only
        # [0, 0, 1, 0] for front microhpone only
        # [0, 0, 0, 1] for rear microhpone only
        # [1, 1, 1, 1] for all microphnes
        channels = [0, 0, 1, 0]
        
        self.nao.audio_recorder.startMicrophonesRecording(internal_path, 'wav', 16000, channels)
        print('Audio recording started.')
        
        time.sleep(float(duration))

        self.nao.audio_recorder.stopMicrophonesRecording()
        print('Audio recording stopped.')

        if playback == True:
            self.nao.audio_player.playFile(internal_path)
            
        self.nao.download_file_from_nao(remote_file_path=internal_path, local_file_path=output_path)

def clean_string(text):
    text = text.strip()
    return ''.join([c for c in text.lower() if c == ' ' or (c not in string.punctuation and c not in string.whitespace.replace(' ', ''))])

sound_library = {
    "start_listening": "/home/nao/AUDIO/listen_start.mp3",
    "stop_listening": "/home/nao/AUDIO/listen_stop2.mp3",
    "thinking_human": "/home/nao/AUDIO/thinking_human2.mp3",
    "victory_path": "/home/nao/AUDIO/we_won_1.mp3",
    "correct_sound_a": "/home/nao/AUDIO/correct_4-10.mp3", #3.5s
    "incorrect_sound_a": "/home/nao/AUDIO/incorrect_2-3.mp3", #2.3s
    "correct_sound_b": "/home/nao/AUDIO/correct_1-5.mp3", #1.5s
    "incorrect_sound_b": "/home/nao/AUDIO/incorrect_1-05.mp3", #1.05s
    "thinking": "/home/nao/AUDIO/thinking_3.mp3",
    "scanning": "/home/nao/AUDIO/scanning_3.mp3",
}