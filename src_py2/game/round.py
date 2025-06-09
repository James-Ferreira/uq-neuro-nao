class Round:
    def __init__(
            self,
            round_number,
            team_1,
            team_2,
            target_word=None,
            team_1_score=0,
            team_1_hints=None,
            team_1_guesses=None,
            team_2_score=0,
            team_2_hints=None,
            team_2_guesses=None
    ):
        self.round_number = round_number
        self.target_word = target_word
        
        self.team_1 = {
            "team_name": team_1.team_name,
            "score": team_1_score,
            "hints": team_1_hints if team_1_hints is not None else [],
            "guesses": team_1_guesses if team_1_guesses is not None else []
        }
        
        self.team_2 = {
            "team_name": team_2.team_name,
            "score": team_2_score,
            "hints": team_2_hints if team_2_hints is not None else [],
            "guesses": team_2_guesses if team_2_guesses is not None else []
        }

    def reset(self):
        self.target_word = None
        self.team_1["score"] = 0
        self.team_1["hints"] = []
        self.team_1["guesses"] = []
        self.team_2["score"] = 0
        self.team_2["hints"] = []
        self.team_2["guesses"] = []

    def __eq__(self, other):
        if isinstance(other, Round):
            return (
                self.round_number == other.round_number and
                self.target_word == other.target_word and
                self.team_1["team_name"] == other.team_1["team_name"] and
                self.team_1["score"] == other.team_1["score"] and
                self.team_1["hints"] == other.team_1["hints"] and
                self.team_1["guesses"] == other.team_1["guesses"] and
                self.team_2["team_name"] == other.team_2["team_name"] and
                self.team_2["score"] == other.team_2["score"] and
                self.team_2["hints"] == other.team_2["hints"] and
                self.team_2["guesses"] == other.team_2["guesses"]
            )
        return False
