import requests

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