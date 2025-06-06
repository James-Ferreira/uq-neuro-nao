from game.round import Round
from termcolor import colored
import copy

class Save(object):
    def __init__(self, team1, team2, target_words, max_rounds=3, max_turns=3):
        self.team1 = team1
        self.team2 = team2
        self.target_words = target_words
        self.max_rounds = max_rounds
        self.max_turns = max_turns
        self.current_round = 1
        self.current_turn = 1
        self.start_time = 0
        self.end_time = 0
        self.rounds = {
            i: Round(i, team1, team2) for i in range(1, max_rounds + 1)
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
            self.team1.rotate_role()
            self.team2.rotate_role()

    def get_curr_round(self):
        return self.rounds[self.current_round]

    def get_curr_round_hints(self):
        cr = self.get_curr_round()
        all_round_hints = cr.team1["hints"] + cr.team2["hints"]
        return all_round_hints

    def get_curr_round_guesses(self):
        cr = self.get_curr_round()
        all_round_hints = cr.team1["guesses"] + cr.team2["guesses"]
        return all_round_hints

    def reject_round(self):
        cr = self.get_curr_round()
        self.rejected.append(copy.deepcopy(cr))
        cr.reset()
        
        self.set_turn(1)
        self.next_target_word()

    #todo: write test
    def isFinished(self, isCorrect):
         if((isCorrect and self.max_rounds == self.current_round) or (self.max_rounds == self.current_round and self.max_turns == self.current_turn)):
            return True
         
    def get_active_team(self):
        if self.current_round % 2 == 1:
            starting_team = self.team1
            other_team = self.team2
        else:
            starting_team = self.team2
            other_team = self.team1

        if self.current_turn % 2 == 1:
            return starting_team
        else:
            return other_team

    
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
            
            if team_name == self.team1.team_name:
                round.team1["score"] = score
            elif team_name == self.team2.team_name:
                round.team2["score"] = score
            else:
                raise ValueError("Invalid team name: {}".format(team_name))
        else:
            raise ValueError("Round {} does not exist.".format(self.current_round))

    def get_score(self, team_name):
        if self.team1.team_name == team_name:
            return sum(round.team1["score"] for round in self.rounds.values())
        elif self.team2.team_name == team_name:
            return sum(round.team2["score"] for round in self.rounds.values())
        return -1 

    ### HINTS & GUESSES ###

    def record_hint(self, team_name, hint):
        if self.current_round in self.rounds:
            cr = self.get_curr_round()
            
            if team_name == self.team1.team_name:
                cr.team1["hints"].append(hint)
            elif team_name == self.team2.team_name:
                cr.team2["hints"].append(hint)
            else:
                raise ValueError("Invalid team name: {}".format(team_name))
        else:
            raise ValueError("Round {} does not exist.".format(self.current_round))
        
    def record_guess(self, team_name, guess):
        if self.current_round in self.rounds:
            cr = self.get_curr_round()

            if team_name == self.team1.team_name:
                cr.team1["guesses"].append(guess)
            elif team_name == self.team2.team_name:
                cr.team2["guesses"].append(guess)
            else:
                raise ValueError("Invalid team name")

    def get_latest_guess(self):
        cr = self.get_curr_round()
        active_team = self.get_active_team().team_name
        if cr.team1["team_name"] == active_team:
            guesses = cr.team1["guesses"]
        elif cr.team2["team_name"] == active_team:
            guesses = cr.team2["guesses"]

        if not guesses:
            return None

        return guesses[-1]
    

    ### PRETTY PRINT ###
    def pprint_state(self):
        team1_score =self.get_score(self.team1.team_name)
        team2_score =self.get_score(self.team2.team_name)
        round_str = colored('ROUND', 'cyan') + ' ' + colored(str(self.current_round), 'yellow') + '/' + str(self.max_rounds)
        turn_str = colored('Turn', 'cyan') + ' ' + colored(str(self.current_turn), 'yellow') + '/' + str(self.max_turns)
        score_str = colored(self.team1.team_name + ':', 'cyan') + ' ' + str(team1_score) + ' points  ' + \
                    colored(self.team2.team_name + ':', 'cyan') + ' ' + str(team2_score) + ' points'

        hinter_str = colored('(Hinter: ' + self.get_active_team().get_hinter().name + ')', 'magenta')
        print(round_str + '  ' + turn_str + '  ' + score_str + ' ' + hinter_str)

    def get_final(self):
        team1_total = self.get_score(self.team1.team_name)
        team2_total = self.get_score(self.team2.team_name)

        if team1_total > team2_total:
            winner = self.team1.team_name
            loser = self.team2.team_name
            winner_score = team1_total
            loser_score = team2_total
        elif team2_total > team1_total:
            winner = self.team2.team_name
            loser = self.team1.team_name
            winner_score = team2_total
            loser_score = team1_total
        else:
            return "-*-*-*-Tie! Both teams have {} pts -*-*-*-".format(team1_total)

        return "-*-*-*- Winner: {} ({}) pts, Loser: {} ({}) pts -*-*-*-".format(winner, winner_score, loser, loser_score)
