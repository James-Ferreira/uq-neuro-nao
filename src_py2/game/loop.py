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

    def initialise(self):
        self.save.start_time = time.time()
        return "hint"

    def hint(self):
        self.save.pprint_state()

        active_team = self.save.get_active_team()
        inactive_team = self.save.get_inactive_team()

        already_hinted = self.save.get_curr_round_hints()
        already_guessed = self.save.get_curr_round_guesses()

        target_word = self.save.get_target_word()
        try:
            target_with_quadrants = self.save.targets_with_quadrants.get(target_word)
            self.orchestrate.before_hint(active_team, inactive_team, already_hinted, target_with_quadrants)

            hint = active_team.produce_hint(target_word, already_hinted, already_guessed)
            self.save.record_hint(active_team.team_name, hint)

            print("[{}] {} hinted '{}'".format(
            active_team.team_name,
            active_team.get_hinter().name,
            hint,
            ))

            return "guess"
        except ValueError as e:
            self.save.reject_round()
            return "hint"

    def guess(self):
        active_team = self.save.get_active_team()
        inactive_team = self.save.get_inactive_team()

        already_hinted = self.save.get_curr_round_hints()
        already_guessed = self.save.get_curr_round_guesses()
        try:
            active_team = self.save.get_active_team()
            self.orchestrate.before_guess(active_team, inactive_team)
            guess = active_team.produce_guess(self.save.get_target_word(), already_hinted, already_guessed)
            self.save.record_guess(active_team.team_name, guess)

            print("[{}] {} guessed '{}'".format(
            active_team.team_name,
            active_team.get_guesser().name,
            guess,
            ))

            return "evaluate"
        except ValueError as e:
            self.save.reject_round()
            return "hint"

    def evaluate(self):
        active_team = self.save.get_active_team()
        inactive_team = self.save.get_inactive_team()
        guess = self.save.get_latest_guess()
        target_word = self.save.get_target_word()

        print("Evaluating (guess={}) (target={})".format(guess, target_word))

        isActuallyCorrect = guess == target_word
        status = self.orchestrate.before_evaluate(active_team, inactive_team, isActuallyCorrect, guess)

        if (status == "correct"):
            self.save.calculate_score(active_team.team_name)

            info = "of '{} by {} from {}".format(
            guess,
            active_team.get_guesser().name,
            active_team.team_name
            )
            print(colored("✓ Correct guess", 'green') + ' ' + info)
        elif status == "incorrect":
            info = "of '{} by {} from {}".format(
            guess,
            active_team.get_guesser().name,
            active_team.team_name
            )
            print(colored("✘ Incorrect guess", 'red') + ' ' + info)
        else:
            print(colored("✘ Rejected Round", 'yellow'))
            self.save.reject_round()

        if(self.save.isFinished(isActuallyCorrect)):
            self.orchestrate.end_of_game(self.save, active_team, inactive_team)
            return "end_of_game"
        
        if(isActuallyCorrect):
            self.save.next_round()
        else:
            self.save.next_turn()

        return "hint"

    def end_of_game(self):
        self.save.end_time = time.time()
        self.save.export_save()
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