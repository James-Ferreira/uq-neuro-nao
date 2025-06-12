from game.round import Round
from termcolor import colored
import copy
import pprint
import json
from enum import Enum

class Save(object):
    def __init__(self, team_1, team_2, game_condition, target_words, max_rounds=4, max_turns=6):
        self.team_1 = team_1
        self.team_2 = team_2
        self.game_condition = game_condition
        self.target_words = target_words
        self.max_rounds = max_rounds
        self.max_turns = max_turns
        self.current_round = 1
        self.current_turn = 1
        self.start_time = 0
        self.end_time = 0
        self.rounds = {
            i: Round(i, team_1, team_2) for i in range(1, max_rounds + 1)
        }

        self.rejected = []

        self.set_target_word(target_words[0])


    ### ROUNDS ###
    def set_round(self, round_no):
        if 0 < round_no <= self.max_rounds:
            self.current_round = round_no

    def set_turn(self, turn_no):
        if 0 < turn_no <= self.max_turns:
            self.current_turn = turn_no

    def set_target_word(self, word):
        if self.current_round in self.rounds:
            for round_num, round in self.rounds.items():
                if round.target_word == word:
                    raise ValueError("Target word '{}' already used in round {}".format(word, round_num))
            self.rounds[self.current_round].target_word = word
        else:
            raise ValueError("Round {} does not exist.".format(self.current_round))

    def next_turn(self):
        # self.get_active_team().rotate_role()
        if self.current_turn < self.max_turns:
            self.set_turn(self.current_turn + 1)
        else: 
            self.next_round()

    def next_round(self):
       if self.current_round < self.max_rounds:
            self.set_round(self.current_round + 1)
            self.set_turn(1) 
            self.next_target_word()
            self.team_1.rotate_role()
            self.team_2.rotate_role()

    def get_curr_round(self):
        return self.rounds[self.current_round]

    def get_curr_round_hints(self):
        cr = self.get_curr_round()
        all_round_hints = cr.team_1["hints"] + cr.team_2["hints"]
        return all_round_hints

    def get_curr_round_guesses(self):
        cr = self.get_curr_round()
        all_round_hints = cr.team_1["guesses"] + cr.team_2["guesses"]
        return all_round_hints

    def reject_round(self):
        cr = self.get_curr_round()
        self.rejected.append(copy.deepcopy(cr))
        cr.reset()
        
        self.set_turn(1)
        self.next_target_word()

    def isFinished(self, isCorrect):
         if((isCorrect and self.max_rounds == self.current_round) or (self.max_rounds == self.current_round and self.max_turns == self.current_turn)):
            return True
         
    def get_active_team(self):
        base_team = self.team_1 if self.current_round % 2 == 1 else self.team_2
        alt_team = self.team_2 if base_team == self.team_1 else self.team_1

        return base_team if self.current_turn % 2 == 1 else alt_team

    def get_inactive_team(self):
        active = self.get_active_team()
        return self.team_1 if active == self.team_2 else self.team_2
        
    ### TARGET WORD ###
    def get_target_word(self):
        return self.rounds[self.current_round].target_word
    
    def next_target_word(self):
        used_words = {round_data.target_word for round_data in self.rounds.values() if round_data.target_word}
        rejected_words = {round_data.target_word for round_data in self.rejected if round_data.target_word}
        used_words.update(rejected_words)

        for word in self.target_words:
            if word not in used_words:
                self.set_target_word(word)
                return word

        raise ValueError("No more target words available.")
    
    ### SCORES ###
    def calculate_score(self, team_name):
        score = self.max_turns - self.current_turn
        self.set_round_score(team_name, score)

    def set_round_score(self, team_name, score):
        if self.current_round in self.rounds:
            round = self.rounds[self.current_round]
            
            if team_name == self.team_1.team_name:
                round.team_1["score"] = score
            elif team_name == self.team_2.team_name:
                round.team_2["score"] = score
            else:
                raise ValueError("Invalid team name: {}".format(team_name))
        else:
            raise ValueError("Round {} does not exist.".format(self.current_round))

    def get_score(self, team_name):
        if self.team_1.team_name == team_name:
            return sum(round.team_1["score"] for round in self.rounds.values())
        elif self.team_2.team_name == team_name:
            return sum(round.team_2["score"] for round in self.rounds.values())
        return -1 # error

    ### HINTS & GUESSES ###

    def record_hint(self, team_name, hint):
        if self.current_round in self.rounds:
            cr = self.get_curr_round()
            
            if team_name == self.team_1.team_name:
                cr.team_1["hints"].append(hint)
            elif team_name == self.team_2.team_name:
                cr.team_2["hints"].append(hint)
            else:
                raise ValueError("Invalid team name: {}".format(team_name))
        else:
            raise ValueError("Round {} does not exist.".format(self.current_round))
        
    def record_guess(self, team_name, guess):
        if self.current_round in self.rounds:
            cr = self.get_curr_round()

            if team_name == self.team_1.team_name:
                cr.team_1["guesses"].append(guess)
            elif team_name == self.team_2.team_name:
                cr.team_2["guesses"].append(guess)
            else:
                raise ValueError("Invalid team name")

    def get_latest_guess(self):
        cr = self.get_curr_round()
        active_team = self.get_active_team().team_name
        if cr.team_1["team_name"] == active_team:
            guesses = cr.team_1["guesses"]
        elif cr.team_2["team_name"] == active_team:
            guesses = cr.team_2["guesses"]

        if not guesses:
            return None

        return guesses[-1]
    

    ### PRETTY PRINT ###
    def pprint_state(self):
        team_1_score =self.get_score(self.team_1.team_name)
        team_2_score =self.get_score(self.team_2.team_name)
        round_str = colored('ROUND', 'cyan') + ' ' + colored(str(self.current_round), 'yellow') + '/' + str(self.max_rounds)
        turn_str = colored('Turn', 'cyan') + ' ' + colored(str(self.current_turn), 'yellow') + '/' + str(self.max_turns)
        score_str = colored(self.team_1.team_name + ':', 'cyan') + ' ' + str(team_1_score) + ' points  ' + \
                    colored(self.team_2.team_name + ':', 'cyan') + ' ' + str(team_2_score) + ' points'

        hinter_str = colored('(Hinter: ' + self.get_active_team().get_hinter().name + ')', 'magenta')
        print(round_str + '  ' + turn_str + '  ' + score_str + ' ' + hinter_str)

    def export_save(self):
        print("=== Exporting Save ===\n\n\n\n")
        team_1_total = self.get_score(self.team_1.team_name)
        team_2_total = self.get_score(self.team_2.team_name)
        team_1_outcome = "win" if team_1_total > team_2_total else "tie" if team_1_total == team_2_total else "lose"
        team_2_outcome = "win" if team_1_outcome == "lose" else "tie" if team_1_outcome == "tie" else "lose"        
        
        config_data = {
            "max_rounds": self.max_rounds,
            "max_turns": self.max_turns,
            "game_condition": self.game_condition,
        }

        team_data = {
            "team_1": {
                "name": self.team_1.team_name,
                "players": [{"name": p.name, "variant": p.variant.name} for p in self.team_1.players],
                "score": team_1_total,
                "outcome": team_1_outcome
            },
            "team_2": {
                "name": self.team_2.team_name,
                "players": [{"name": p.name, "variant": p.variant.name} for p in self.team_2.players],
                "score": team_2_total,
                "outcome": team_2_outcome
            },
        }

        round_data = make_json_safe(self.rounds)

        rejected_data = make_json_safe(self.rejected)

        data = {
            "config": config_data,
            "teams": team_data,
            "rounds": round_data,
            "rejected": rejected_data,
            "duration": round(self.end_time - self.start_time, 2)
        }

        if team_1_outcome == "tie":
            print("-*-*-*-Tie! Both teams have {} pts -*-*-*-".format(team_1_total))
        else:
            print("-*-*-*- Team_1: {} ({}) pts, Team_2: {} ({}) pts -*-*-*-".format(
                self.team_1.team_name,
                team_1_total,
                self.team_2.team_name,
                team_2_total,
                ))
            
        pprint.pprint(data, indent=2)

        with open("session_data.json", "w") as f:
            json.dump(data, f, indent=4)

def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, Enum):
        return obj.name
    elif hasattr(obj, "__dict__"):
        return make_json_safe(vars(obj))
    else:
        try:
            json.dumps(obj)
            return obj
        except TypeError:
            return str(obj)