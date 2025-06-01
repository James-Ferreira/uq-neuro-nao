class Round:
    def __init__(
            self,
            round_number,
            team1,
            team2,
            target_word=None,
            team1_score=0,
            team1_hints=None,
            team1_guesses=None,
            team2_score=0,
            team2_hints=None,
            team2_guesses=None
    ):
        self.round_number = round_number
        self.target_word = target_word
        
        self.team1 = {
            "team_name": team1.team_name,
            "score": team1_score,
            "hints": team1_hints if team1_hints is not None else [],
            "guesses": team1_guesses if team1_guesses is not None else []
        }
        
        self.team2 = {
            "team_name": team2.team_name,
            "score": team2_score,
            "hints": team2_hints if team2_hints is not None else [],
            "guesses": team2_guesses if team2_guesses is not None else []
        }

    def reset(self):
        self.target_word = None
        self.team1["score"] = 0
        self.team1["hints"] = []
        self.team1["guesses"] = []
        self.team2["score"] = 0
        self.team2["hints"] = []
        self.team2["guesses"] = []

    def __eq__(self, other):
        if isinstance(other, Round):
            return (
                self.round_number == other.round_number and
                self.target_word == other.target_word and
                self.team1["team_name"] == other.team1["team_name"] and
                self.team1["score"] == other.team1["score"] and
                self.team1["hints"] == other.team1["hints"] and
                self.team1["guesses"] == other.team1["guesses"] and
                self.team2["team_name"] == other.team2["team_name"] and
                self.team2["score"] == other.team2["score"] and
                self.team2["hints"] == other.team2["hints"] and
                self.team2["guesses"] == other.team2["guesses"]
            )
        return False
