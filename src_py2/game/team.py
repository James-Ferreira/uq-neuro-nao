from game.player import Roles
from game.robot_player import RobotPlayer
from robot.audio_manager import sound_library
import time

class Team(object):
    def __init__(self, team_name, players):
        if len(players) != 2:
            raise ValueError("A team must have exactly two members")
        self.team_name = team_name
        self.players = players
        self._assign_initial_roles()

    def _assign_initial_roles(self):
        self.players[0].assign_role(Roles.HINTER)
        self.players[1].assign_role(Roles.GUESSER)

    def rotate_role(self):
        if self.players[0].get_role() == Roles.HINTER:
            self.players[0].assign_role(Roles.GUESSER)
            self.players[1].assign_role(Roles.HINTER)
        else:
            self.players[0].assign_role(Roles.HINTER)
            self.players[1].assign_role(Roles.GUESSER)

    def get_hinter(self):
        for player in self.players:
            if player.get_role() == Roles.HINTER:
                return player
        return None

    def get_guesser(self):
        for player in self.players:
            if player.get_role() == Roles.GUESSER:
                return player
        return None
    
    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    def __str__(self):
        hinter = self.get_hinter()
        guesser = self.get_guesser()
        return "Team: {} Hinter: {} Guesser: {}".format(self.team_name, hinter, guesser)

    def produce_hint(self, target_word, already_hinted, already_guessed):
        hinter = self.get_hinter()
        guesser = self.get_guesser()
        isRobotGuesser = isinstance(guesser, RobotPlayer)
        isRobotHinter = isinstance(hinter, RobotPlayer)

        speech_delay = 0.3
        if isRobotHinter:
            if isRobotGuesser:
                guesser.nao.tts.say("{}. I am ready to guess".format(hinter.name))
                guesser.nao.mm.use_motion_library("ready_to_guess")

            hinter.nao.tts.say("Ok {}, I shall think about your hint".format(guesser.name))
            hinter.nao.audio_player.post.playFile(sound_library["thinking"])
            hinter.nao.leds.post.fadeRGB('FaceLeds', 0xFFC0CB, 0.1)
            hint = hinter.generate_hint(target_word, already_hinted, already_guessed)
            hinter.nao.audio_player.stopAll()
            hinter.nao.leds.post.fadeRGB("FaceLeds", 0xFFFFFF, 0.1)


            hinter.nao.tts.say("The hint is: {}".format(hint))

            if isRobotGuesser:
                time.sleep(speech_delay)
                guesser.nao.tts.say("Did you say: {}".format(hint))
                time.sleep(speech_delay)
                hinter.nao.tts.say("Yes, I did")
            else:
                confirmed = False
                while not confirmed:
                    hinter.nao.tts.post.say("Do you understand the hint? Press my hand for yes, or my foot for no.")
                    confirmed = hinter.nao.tm.wait_for_touch_confirm()

                    if not confirmed:
                        hinter.nao.tts.say("Okay, let me spell it out for you.")
                        for letter in hint:
                            hinter.nao.tts.say(str(letter.lower()))
                            time.sleep(0.3)
                        hinter.nao.tts.say(str(hint))
 
            return hint

        if not isRobotHinter:
            if isRobotGuesser:
                guesser.nao.tts.say('I am ready to guess')
                guesser.nao.tts.say('You have 5 seconds to think of your hint')
                guesser.nao.audio_player.post.playFile(sound_library["thinking"])
                time.sleep(5)
                guesser.nao.audio_player.stopAll()
                transcript = guesser.nao.am.listen_until_confirmed(5)
                return transcript

        return hinter.generate_hint(target_word, already_hinted)
    
    def produce_guess(self, target_word, already_hinted, already_guessed):
        guesser = self.get_guesser()
        hinter = self.get_hinter()
        isRobotGuesser = isinstance(guesser, RobotPlayer)
        isRobotHinter = isinstance(hinter, RobotPlayer)

        speech_delay = 0.3

        if isRobotGuesser:
            guesser.nao.tts.post.say("I shall now think about my guess")
            guess = guesser.generate_guess(target_word, already_hinted, already_guessed)
            guesser.nao.tts.say("My guess is {}".format(guess))

            if isRobotHinter:
                time.sleep(speech_delay)
                hinter.nao.tts.say("Did you guess {}".format(guess))
                time.sleep(speech_delay)
                guesser.nao.tts.say("Yes")
            else:
                confirmed = False
                while not confirmed:
                    guesser.nao.tts.post.say("Do you understand the guess? Press my hand for yes, or my foot for no.")
                    confirmed = guesser.nao.tm.wait_for_touch_confirm()

                    if not confirmed:
                        guesser.nao.tts.say("Okay, let me spell it out for you.")
                        for letter in guess:
                            guesser.nao.tts.say(str(letter.lower()))
                            time.sleep(0.3)
                        guesser.nao.tts.say(str(guess))

            return guess

        if not isRobotGuesser and isRobotHinter:
            hinter.nao.tts.say("You have 5 seconds to think of your guess")
            hinter.nao.audio_player.post.playFile(sound_library["thinking"])
            time.sleep(5)
            hinter.nao.audio_player.stopAll()
            transcript = hinter.nao.am.listen_until_confirmed(5)
            return transcript
        
        if not isRobotGuesser and not isRobotHinter:
            guess = raw_input("Type guess: ")  # type: ignore (suppressess superfluous warning)
            return guess

        return guesser.generate_guess(target_word, already_guessed)