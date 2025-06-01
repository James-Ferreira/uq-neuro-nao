from game.player import Player, Variant
from robot.robot import Robot
import requests

class RobotPlayer(Player):
    def __init__(self, name, variant, ip_address, pitch, team_condition, orientation, reversed, user='nao', pword='nao', port=9559):
        super(RobotPlayer, self).__init__(name, variant)
        self.robot = Robot(name, ip_address, port, user, pword, reversed)
        self.ip_address = ip_address
        self.team_condition = team_condition #todo: enforce P or O
        self.orientation = orientation #todo: enforce L or R
        self.robot.am.set_pitch(pitch)

    def generate_guess(self, target_word, already_hinted, already_guessed):
        # guess = super(RobotPlayer, self).generate_guess(cheat)

        guess = generate_ai_guess(target_word, already_hinted, already_guessed)

        return guess
    
    def generate_hint(self, target_word, already_hinted, already_guessed):
        # hint = super(RobotPlayer, self).generate_hint()
        # self.robot.tts.say("I am {}".format(self.name))
        # self.robot.tts.say("My hint is {}".format(hint)) 
        hint = generate_ai_hint(target_word, already_hinted, already_guessed)

        return hint

    def generate_opinion(self, hobby_better, hobby_worse, use_alternate_prompt):
        return generate_hobby_opinion(hobby_better, hobby_worse, use_alternate_prompt)

def generate_ai_guess(target_word, already_hinted, already_guessed):
    api_url = "http://localhost:5000/guess"

    try:
        response = requests.post(api_url, json={
            'target_word': target_word,
            'already_hinted': already_hinted,
            'already_guessed': already_guessed,
            })
        response.raise_for_status()
        data = response.json()
        reply = data.get('response')

        if reply:
            print("Reply '{}'".format(reply))
            return reply
        else:
            print("Error: API returned empty reply.")
            return None
    except Exception as e:
        print("Error calling reply API: {}".format(e))
        return None

def generate_ai_hint(target_word, already_hinted, already_guessed):
    api_url = "http://localhost:5000/hint"

    try:
        response = requests.post(api_url, json={
            'target_word': target_word,
            'already_hinted': already_hinted,
            'already_guessed': already_guessed,
            })
        response.raise_for_status()
        data = response.json()
        reply = data.get('response')

        if reply:
            print("Reply '{}'".format(reply))
            return reply
        else:
            print("Error: API returned empty reply.")
            return None
    except Exception as e:
        print("Error calling reply API: {}".format(e))
        return None

def generate_hobby_opinion(hobby_better, hobby_worse, use_alternate_prompt):
    api_url = "http://localhost:5000/hobby"

    try:
        response = requests.post(api_url, json={
            'hobby_better': hobby_better,
            'hobby_worse': hobby_worse,
            'use_alternate_prompt': use_alternate_prompt,
            })
        response.raise_for_status()
        data = response.json()
        reply = data.get('response')

        if reply:
            print("Reply '{}'".format(reply))
            return reply
        else:
            print("Error: API returned empty reply.")
            return None
    except Exception as e:
        print("Error calling reply API: {}".format(e))
        return None