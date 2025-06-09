from game.player import Roles
from robot_player import RobotPlayer
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

        if isRobotHinter:
            if isRobotGuesser:
                guesser.robot.tts.say("{}. I am ready to guess".format(hinter.name))
                guesser.robot.mm.use_motion_library("ready_to_guess")

            hinter.robot.tts.say("Ok {}, I shall think about your hint".format(guesser.name))
            hinter.robot.audio_player.post.playFile(sound_library["thinking"])
            hint = hinter.generate_hint(target_word, already_hinted, already_guessed)
            hinter.robot.audio_player.stopAll()

            hinter.robot.tts.say("The hint is: {}".format(hint))

            if isRobotGuesser:
                guesser.robot.tts.say("Did you say: {}".format(hint))
                hinter.robot.tts.say("Yes, I did")
            else:
                confirmed = False
                while not confirmed:
                    hinter.robot.tts.say("Do you understand the hint? Press my hand for yes, or my foot for no.")
                    confirmed = hinter.robot.tm.wait_for_touch_confirm()

                    if not confirmed:
                        hinter.robot.tts.say("Okay, let me spell it out for you.")
                        for letter in hint:
                            hinter.robot.tts.say(str(letter.lower()))
                            time.sleep(0.3)
                        hinter.robot.tts.say(str(hint))
 
            return hint

        if not isRobotHinter:
            if isRobotGuesser:
                guesser.robot.tts.say('I am ready to guess')
                guesser.robot.tts.say('You have 5 seconds to think of your hint')
                transcript = guesser.robot.am.listen_until_confirmed(5)
                return transcript

        return hinter.generate_hint(target_word, already_hinted)
    
    def produce_guess(self, target_word, already_hinted, already_guessed):
        guesser = self.get_guesser()
        hinter = self.get_hinter()
        isRobotGuesser = isinstance(guesser, RobotPlayer)
        isRobotHinter = isinstance(hinter, RobotPlayer)

        if isRobotGuesser:
            guesser.robot.tts.say("I shall now think about my guess")
            guess = guesser.generate_guess(target_word, already_hinted, already_guessed)
            guesser.robot.tts.say("My guess is {}".format(guess))

            if isRobotHinter:
                hinter.robot.tts.say("Did you guess {}".format(guess))
                guesser.robot.tts.say("Yes")
            else:
                confirmed = False
                while not confirmed:
                    guesser.robot.tts.say("Do you understand the guess? Press my hand for yes, or my foot for no.")
                    confirmed = guesser.robot.tm.wait_for_touch_confirm()

                    if not confirmed:
                        guesser.robot.tts.say("Okay, let me spell it out for you.")
                        for letter in guess:
                            guesser.robot.tts.say(str(letter.lower()))
                            time.sleep(0.3)
                        guesser.robot.tts.say(str(guess))

            return guess

        if not isRobotGuesser and isRobotHinter:
            hinter.robot.tts.say("You have 5 seconds to think of your guess")
            hinter.robot.audio_player.post.playFile(sound_library["thinking"])
            time.sleep(5)
            hinter.robot.audio_player.stopAll()
            transcript = hinter.robot.am.listen_until_confirmed(5)
            return transcript
        
        if not isRobotGuesser and not isRobotHinter:
            guess = raw_input("Type guess: ")
            return guess

        return guesser.generate_guess(target_word, already_guessed)