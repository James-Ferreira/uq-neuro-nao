# -*- coding: utf-8 -*-

import time
from game.save import Save
from game.team import Team
from termcolor import colored
from game.robot_player import RobotPlayer

class Loop:
    def __init__(self, initial_state, save, orchestrate):
        self.current_state = initial_state
        self.save = save
        self.orchestrate = orchestrate
        self.states = {
            "initialise": self.initialise,
            "hint": self.hint,
            "guess": self.guess,
            "evaluate": self.evaluate,
            "end_of_game": self.end_of_game,
        }
        self.p1_name = ""
        self.p2_name = ""

    def initialise(self):
        print("🔸 initialising, waiting for head touch activation")
        #todo: set game start time
        #todo: word quadrants
        #todo: demo round
        p1_name, p2_name = self.orchestrate.simple_welcome()
        self.orchestrate.simple_hobby(p1_name, p2_name)

        # hacky to get p1 and p2 name ovewr to outro, without looking through team obj
        self.p1_name = p1_name
        self.p2_name = p2_name
        return "hint"

    def hint(self):
        self.save.pprint_state()

        active_team = self.save.get_active_team()
        try:
            hint = active_team.produce_hint(self.save.get_target_word(), self.save.get_curr_round_hints(), self.save.get_curr_round_guesses())
            self.save.record_hint(active_team.team_name, hint)

            print("Hint of '{}' by {} from {}".format(
            hint,
            active_team.get_hinter().name,
            active_team.team_name
            ))

            return "guess"
        except ValueError as e:
            self.save.reject_round()
            return "hint"

    def guess(self):
        try:
            active_team = self.save.get_active_team()
            guess = active_team.produce_guess(self.save.get_target_word(), self.save.get_curr_round_hints(), self.save.get_curr_round_guesses())
            self.save.record_guess(active_team.team_name, guess)

            print("Guess of '{}' by {} from {}".format(
            guess,
            active_team.get_guesser().name,
            active_team.team_name
            ))

            return "evaluate"
        except ValueError as e:
            self.save.reject_round()
            return "hint"

    def evaluate(self):
        #todo: false reject / false confirmation handling 
        active_team = self.save.get_active_team()
        guess = self.save.get_latest_guess()
        isCorrect = active_team.produce_evaluation(self.save.get_target_word(), guess)

        if (isCorrect):
            self.save.calculate_score(active_team.team_name)

            info = "of '{} by {} from {}".format(
            guess,
            active_team.get_guesser().name,
            active_team.team_name
            )
            print(colored("✓ Correct guess", 'green') + ' ' + info)
        else:
            info = "of '{} by {} from {}".format(
            guess,
            active_team.get_guesser().name,
            active_team.team_name
            )
            print(colored("✘ Incorrect guess", 'red') + ' ' + info)

        # add an option to reject an evaluation in the case of speech recognition ai 

        if(self.save.isFinished(isCorrect)):
            return "end_of_game"
        
        if(isCorrect):
            self.save.next_round()
        else:
            self.save.next_turn()

        return "hint"

    def end_of_game(self):
        # pprint.pprint(self.save.get_summary(), depth=5)
        #todo: set game end time
        print(self.save.get_final())
        
        self.orchestrate.simple_outro(self.p1_name, self.p2_name)
        return None

    def run(self):

        while True:
            if self.current_state not in self.states:
                print("Error - Unknown State: {}".format(self.current_state))
                break
            
            transition = self.states[self.current_state]()

            if transition is None:
                print("Exiting")
                break
            
            self.current_state = transition
            time.sleep(0.1)