from game.player import Player, Roles, Variant
from robot_player import RobotPlayer
from robot.audio_manager import sound_library
import time
import random

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

        #todo: announce hinter order
        # if already_hinted.length == 0:
            #if isRobotHinter:
                # hinter.robot.tts.say("The hinters will be: {}: that's me, and: {}.  I will hint first".format(hinter.robot.name, other_team_hinter.name))
            # elif otherTeamRobotHinter
                # other_team_hinter.tts.say("The hinters will be: {} and: {}: that's me.  {} will hint first".format(hinter.exp_name, other_team_hinter.exp_name, hinter.exp_name))
            # elif isRobotGuesser:
                # guesser.tts.say("The {} hinters {} will be: {} and: {}.  {} will hint first.".format(bit_1, bit_2, hinter.exp_name, other_team_hinter.exp_name, hinter.exp_name))
        # todo: if there is a Robot on the inactive team, it should turn to look in the direction of the active team

        if isRobotHinter:
            if already_hinted.length == 0:
                duration = random.uniform(2,5)
                hinter.robot.tts.say("Experimenter. Please show me the target word. Touch my head when you are ready for me to scan.")
                hinter.robot.tm.wait_for_touch_activate()
                hinter.robot.leds.rotateEyes(0x33ECFF, 0.5, duration)
                hinter.robot.tts.say("I see the target word")
                #todo: I see the target word in quadrant x; touch hand to confirm

                #todo: other team looks at word quadrants
                #if hinter.team_condition == "P":
                   # print("Partnered Condition: todo")
                    # if otherTeamHinterIsRobotL
                    #   otherHinter.robot.tts.say("Please let me see the target word, too.  Touch my head when you are ready for me to scan.")  
                    #    otherHinter.robot.tm.wait_for_touch_activate()
                    #    otherHinter.robot.leds.rotateEyes(0x33ECFF, 0.5, duration)
                    #    otherHinter.robot.tts.say("I see the target word in quadrant x; touch hand to confirm
                    # elif otherTeamHinterIsHuman:
                    #   hinter.tts.say("Thank you.  Now you can show the target word to: {}, too:  Touch my head when you are ready to continue.".format(other_team_hinter.exp_name))
                    #   hinter.robot.tm.wait_for_touch_activate()

            if isRobotGuesser:
                guesser.robot.tts.say("{}. I am ready to guess".format(hinter.name))
                guesser.robot.mm.use_motion_library("ready_to_guess")

            hinter.robot.tts.say("Ok {}, I shall think about your hint".format(guesser.name))
            # hinter.robot.audio_player.post.playFile(sound_library["thinking"])
            # hinter.robot.audio_player.stopAll()

            hint = hinter.generate_hint(target_word, already_hinted, already_guessed)
            hinter.robot.tts.say("The hint is: {}".format(hint))

            if isRobotGuesser:
                guesser.robot.tts.say("Did you say: {}".format(hint))
                hinter.robot.tts.say("Yes, I did")
            else:
                confirmed = False
                while not confirmed:
                    hinter.robot.tts.say("Do you understand the hint? Press my hand for yes, and feet for no.")
                    confirmed = hinter.robot.tm.wait_for_touch_confirm(timeout=15)

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
            #todo: point to other team
            guesser.robot.tts.say("I shall now think about my guess")
            guess = guesser.generate_guess(target_word, already_hinted, already_guessed)
            guesser.robot.tts.say("My guess is {}".format(guess))

            if isRobotHinter:
                hinter.robot.tts.say("Did you guess {}".format(guess))
                guesser.robot.tts.say("Yes")
            else: #isHumanHinter

                confirmed = False
                while not confirmed:
                    guesser.robot.tts.say("Do you understand the guess? Press my hand for yes, and feet for no.")
                    confirmed = guesser.robot.tm.wait_for_touch_confirm(timeout=15)

                    if not confirmed:
                        guesser.robot.tts.say("Okay, let me spell it out for you.")
                        for letter in guess:
                            guesser.robot.tts.say(str(letter.lower()))
                            time.sleep(0.3)
                        guesser.robot.tts.say(str(guess))

            return guess

        if not isRobotGuesser:
            if isRobotHinter:
                hinter.robot.tts.say("You have 5 seconds to think of your guess")
                # todo: figure out the start_pos time of this file
                # hinter.robot.audio_player.playFileFromPosition(sound_library["thinking"], start, vol, 0)
                transcript = hinter.robot.am.listen_until_confirmed(5)
                return transcript
            
        return guesser.generate_guess(target_word, already_guessed)

    def produce_evaluation(self, target_word, guess):
        hinter = self.get_hinter()
        guesser = self.get_guesser()
        isRobotGuesser = isinstance(guesser, RobotPlayer)
        isRobotHinter = isinstance(hinter, RobotPlayer)
        isCorrect = guess == target_word

        print("Evaluating (guess={}) (target={})".format(guess, target_word))
        if isRobotGuesser:
            guesser.robot.tts.say("Is {} the right word?".format(guess))
            guesser.robot.tts.say("Press me hand for yes, or my feet for no.")
            confirmed = guesser.robot.tm.wait_for_touch_confirm(timeout=15)
            if not confirmed:
                guesser.robot.tts.say("Oh thats disappointing")
                return False
            else:
                guesser.robot.audio_player.playFile(sound_library["correct_sound_a"])
                guesser.robot.tts.say("Woohoo!")
                return True


        if isRobotHinter:
            if isCorrect:
                hinter.robot.tts.say("How delightful. You are correct")
            else:
                hinter.robot.tts.say("How disappointing. You are incorrect")

            # else:
            #     guesser.robot.tts.say("Am I correct?")
            #     transcript = guesser.robot.am.listen(5)
            #     if transcript.contains("no"):
            #         return ValueError("Rejected")


        return isCorrect