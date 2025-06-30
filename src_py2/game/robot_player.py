from game.player import Player
from robot.nao_robot import NAORobot
from api.dialog import generate_ai_guess, generate_ai_hint, generate_hobby_opinion

class RobotPlayer(Player):
    def __init__(self, name, variant, ip_address, pitch, team_condition, orientation, reversed, user='nao', pword='nao', port=9559):
        super(RobotPlayer, self).__init__(name, variant)
        self.nao = NAORobot(name, ip_address, port, user, pword, reversed)
        self.robot = self.nao
        self.ip_address = ip_address
        self.team_condition = team_condition #todo: enforce P or O
        self.orientation = orientation #todo: enforce L or R
        self.nao.am.set_pitch(pitch)

    def generate_guess(self, target_word, already_hinted, already_guessed):
        return generate_ai_guess(target_word, already_hinted, already_guessed)
    
    def generate_hint(self, target_word, already_hinted, already_guessed):
        return generate_ai_hint(target_word, already_hinted, already_guessed)

    def generate_opinion(self, hobby_better, hobby_worse, use_alternate_prompt):
        return generate_hobby_opinion(hobby_better, hobby_worse, use_alternate_prompt)
