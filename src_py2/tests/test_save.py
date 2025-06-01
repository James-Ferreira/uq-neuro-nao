import unittest
from game.team import Team
from game.save import Save
from game.player import Player, Variant
from game.round import Round
from pprint import pprint

class TestSave(unittest.TestCase):

    def setUp(self):
        self.team1 = Team("Bros", [Player("Mario", Variant.AUTO), Player("Luigi", Variant.AUTO)])
        self.team2 = Team("Princesses", [Player("Peach", Variant.AUTO), Player("Daisy", Variant.AUTO)])
        self.max_rounds = 6
        self.max_turns = 5
        self.target_words = [f"target{i}" for i in range(self.max_rounds + 1)]
        self.save_game = Save(self.team1, self.team2, self.target_words, self.max_rounds, self.max_turns)

    def test_set_round(self):
        self.assertEqual(self.save_game.current_round, 1)
        self.save_game.set_round(2)
        self.assertEqual(self.save_game.current_round, 2)
        self.save_game.set_round(3)
        self.assertEqual(self.save_game.current_round, 3)

    def test_next_turn(self):
        self.assertEqual(self.save_game.current_round, 1)
        self.assertEqual(self.save_game.current_turn, 1)

        for round_num in range(1, self.max_rounds + 1):
            for turn_num in range(1, self.max_turns + 1):
                print("\n({}, {}) ({}, {})".format(round_num, turn_num, self.save_game.current_round, self.save_game.current_turn))

                self.assertEqual(self.save_game.current_round, round_num)
                self.assertEqual(self.save_game.current_turn, turn_num)

                self.save_game.next_turn()

    def test_record_score(self):
        self.save_game.set_round_score(self.team1.team_name, 10)
        self.assertEqual(self.save_game.rounds[1].team1["score"], 10)

        self.save_game.set_round_score(self.team1.team_name, 5)
        self.assertEqual(self.save_game.rounds[1].team1["score"], 5)

        self.save_game.set_round_score(self.team2.team_name, 7)
        self.assertEqual(self.save_game.rounds[1].team2["score"], 7)
       
    def test_record_hint(self):
        self.save_game.record_hint(self.team1.team_name, "hint1")
        self.assertEqual(self.save_game.rounds[1].team1["hints"], ["hint1"])
        self.save_game.record_hint(self.team1.team_name, "hint2")
        self.assertEqual(self.save_game.rounds[1].team1["hints"], ["hint1", "hint2"])

        self.save_game.record_hint(self.team2.team_name, "hintA")
        self.assertEqual(self.save_game.rounds[1].team2["hints"], ["hintA"])

    def test_record_guess(self):
        self.save_game.record_guess(self.team1.team_name, "guess1")
        self.assertEqual(self.save_game.rounds[1].team1["guesses"], ["guess1"])
        self.save_game.record_guess(self.team1.team_name, "guess2")
        self.assertEqual(self.save_game.rounds[1].team1["guesses"], ["guess1", "guess2"])

        self.save_game.record_guess(self.team2.team_name, "guessA")
        self.assertEqual(self.save_game.rounds[1].team2["guesses"], ["guessA"])

        self.save_game.set_round(2)

        self.save_game.record_guess(self.team1.team_name, "guess3")
        self.assertEqual(self.save_game.rounds[2].team1["guesses"], ["guess3"])
        self.assertEqual(self.save_game.rounds[1].team1["guesses"], ["guess1", "guess2"])

    def test_get_round_scores(self):
        
        for i in range(self.max_rounds):
            active_team_name = self.save_game.get_active_team().team_name
            self.save_game.record_hint(active_team_name, "hint1")
            self.save_game.record_guess(active_team_name, "guess1")
            self.save_game.set_round_score(active_team_name, 5)
            self.save_game.next_round()

        expected_scores = {
            1: Round(1, self.team1, self.team2, self.target_words[0], team1_score=5, team1_hints=["hint1"], team1_guesses=["guess1"]),
            2: Round(2, self.team1, self.team2, self.target_words[1], team2_score=5, team2_hints=["hint1"], team2_guesses=["guess1"]),
            3: Round(3, self.team1, self.team2, self.target_words[2], team1_score=5, team1_hints=["hint1"], team1_guesses=["guess1"]),
            4: Round(4, self.team1, self.team2, self.target_words[3], team2_score=5, team2_hints=["hint1"], team2_guesses=["guess1"]),
            5: Round(5, self.team1, self.team2, self.target_words[4], team1_score=5, team1_hints=["hint1"], team1_guesses=["guess1"]),
            6: Round(6, self.team1, self.team2, self.target_words[5], team2_score=5, team2_hints=["hint1"], team2_guesses=["guess1"]),
        }

        self.assertEqual(self.save_game.rounds, expected_scores)

    def test_get_current_round_info(self):
        expected = Round(1, self.team1, self.team2, self.target_words[0])
        self.assertEqual(self.save_game.get_curr_round(), expected)
        
        self.save_game.record_hint(self.team1.team_name, "hint1")
        self.save_game.record_guess(self.team1.team_name, "guess1")
        self.save_game.set_round_score(self.team1.team_name, 3)

        expected = Round(1, self.team1, self.team2, self.target_words[0], team1_score=3, team1_hints=["hint1"], team1_guesses=["guess1"])

        self.assertEqual(self.save_game.get_curr_round(), expected)

    def test_get_active_team(self):
        expected_team = self.team1

        self.assertEqual(self.save_game.get_active_team(), expected_team)

        for round_num in range(1, self.max_rounds + 1):
            expected_team = self.team1 if round_num % 2 == 1 else self.team2
            for turn_num in range(1, self.max_turns + 1):
                active_team = self.save_game.get_active_team()
                print("\n({}, {}) Active Team={}".format(round_num, turn_num, active_team.team_name))
                self.assertEqual(active_team, expected_team)
                expected_team = self.team2 if expected_team == self.team1 else self.team1
                self.save_game.next_turn()

    def test_next_target_word(self):
        for i in range(1, self.max_rounds + 1):
            cr = self.save_game.get_curr_round()
            self.assertEqual(self.save_game.current_round, i)
            self.assertEqual(cr.target_word, self.target_words[i - 1])
            self.save_game.next_round()

    def test_get_latest_guess(self):
            active_team_name = self.save_game.get_active_team().team_name
            self.assertEqual(self.save_game.current_round, 1)

            self.save_game.record_guess(active_team_name, "guess1")
            self.assertEqual(self.save_game.get_latest_guess(), "guess1")

            self.save_game.record_guess(active_team_name, "guess2")
            self.assertEqual(self.save_game.get_latest_guess(), "guess2")


    def test_round_reject(self):
        expected_base = Round(1, self.team1, self.team2, self.target_words[0])

        self.assertEqual(self.save_game.get_curr_round(), expected_base)
        
        self.save_game.record_hint(self.team1.team_name, "hint1")
        self.save_game.record_guess(self.team1.team_name, "guess1")
        self.save_game.set_round_score(self.team1.team_name, 3)
        expected_to_reject = Round(1, self.team1, self.team2, self.target_words[0], team1_score=3, team1_hints=["hint1"], team1_guesses=["guess1"])
        self.assertEqual(self.save_game.get_curr_round(), expected_to_reject)

        self.assertEqual(self.save_game.current_round, 1)
        self.assertEqual(self.save_game.get_target_word(), self.target_words[0])

        self.save_game.reject_round()
        self.assertEqual(self.save_game.current_round, 1)
        self.assertEqual(self.save_game.get_target_word(), self.target_words[1])

        self.save_game.current_round 
        expected_reset = Round(1, self.team1, self.team2, self.target_words[1])
        self.assertEqual(self.save_game.get_curr_round(), expected_reset)

        self.assertEqual(self.save_game.rejected, [expected_to_reject])


if __name__ == '__main__':
    unittest.main()