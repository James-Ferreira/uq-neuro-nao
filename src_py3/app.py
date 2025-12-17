from flask import Flask, request, jsonify
import os
import whisper
import time
import ollama
import string
import requests

from src_py3.duration_prediction.segmentize import Segmentize


app = Flask(__name__)

print("Loading Whisper model...")
model = whisper.load_model("small")
print("Whisper model loaded.")

print("Loading Ollama model...")
client = ollama.Client(
    host="http://localhost:11434"
)
print("Ollama model loaded.")


@app.route('/transcribe/filepath', methods=['POST'])
def transcribe_audio_from_filepath():
    data = request.get_json()
    if not data or 'filepath' not in data:
        return jsonify({'error': 'No filepath provided'}), 400

    filepath = data['filepath']

    print(f"/transcribe/filepath: {filepath}")
    try:
        transcription_result = transcribe_whisper(filepath, model)
        return jsonify({'transcription': transcription_result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/transcribe/file', methods=['POST'])
def transcribe_audio_from_file():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    
    original_filename = audio_file.filename
    file_ext = os.path.splitext(original_filename)[1]

    if not file_ext:
        return jsonify({'error': 'Missing file extension'}), 400

    temp_audio_path = f'./tmp{file_ext}'

    audio_file.save(temp_audio_path)

    try:
        transcription_result = transcribe_whisper(temp_audio_path, model)
        os.remove(temp_audio_path)
        return jsonify({'transcription': transcription_result}), 200
    except Exception as e:
        os.remove(temp_audio_path)
        return jsonify({'error': str(e)}), 500
    
def transcribe_whisper(audio_file_path, model):
    start = time.time()
    print("Starting Whisper transcription.")
    text = "Transcription failed."
    try:
        result = model.transcribe(audio_file_path, language="en", fp16=False)
        text = result["text"]
        end = time.time()
        print(f"Elapsed time: {end - start:.2f} seconds.")
        print(f"Text: {text}")
    except Exception as e:
        print(f"Error: {e}")
    return text

"""@app.route('/converse', methods=['POST'])
def converse():
    data = request.get_json()
    print(f"JSON DATA: {data}")
    if not data or 'transcription' not in data:
        return jsonify({'error': 'No transcription provided'}), 400

    transcript = data['transcription']
    model = data['model']
    interlocutor = data['interlocutor']
    turn_count = data['turn_count']

    if turn_count == 2:
        prompt=f"You are a conversation partner, named 'Robot', who responds succintly to {interlocutor}. The conversation transcript is as follows:\n {transcript}. You need to include these two sentences in your reply: 'I like sniffing flowers.' and 'I'm thinking of buying a sports car.'"
    elif turn_count == 4:
        prompt=f"You are a conversation partner, named 'Robot', who responds succintly to {interlocutor}. The conversation transcript is as follows:\n {transcript}. Use all of your imagination to change the topic of conversation to mathematics."
    else:
        prompt=f"You are a conversation partner, named 'Robot', who responds succintly to {interlocutor}. The conversation transcript is as follows:\n {transcript}."
    print(f"Prompt: {prompt}")

    start = time.time()         
    ai_response = client.generate(
        model=model,
        prompt=prompt,
        context=[],
        stream=False
    )
    end = time.time()         
    print(f"Elapsed time: {end - start:.2f} seconds.")
    response_str = ai_response.response
    # returns a list of lists with the structure [[segment_str, tag_str/None, gest_type/None, duration_estimate_float], ...]
    print(f"RESPONSE STRING: {response_str}")
    segments_list = Segmentize(response_str).process_segments()
    print(f"SEGMENTS LIST: {segments_list}")
    print("LEN:", len(response_str))
    print("REPR:", repr(response_str[:500]))

    try:
        return jsonify({'response': response_str, 'segments_list': segments_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500"""



@app.route('/converse', methods=['POST'])
def converse():
    data = request.get_json()
    print("JSON DATA:", data)

    if not data or 'transcription' not in data:
        return jsonify({'error': 'No transcription provided'}), 400

    transcript   = data.get('transcription', '') or ''
    model        = data.get('model')
    print(f"MODEL: {model}")
    interlocutor = data.get('interlocutor', 'User')
    turn_count   = int(data.get('turn_count', 0))

    # ---- Build system prompt (strict output contract for Segmentize) ----
    system_prompt = (
        "You are Robot, a conversation partner.\n"
        "Reply succinctly to the user.\n"
        "IMPORTANT:\n"
        "- Wrap your entire reply in <ROBOT>...</ROBOT>.\n"
        """You are an emotional robot.  There are several social gestures that you can make to enhance your speech.

        Below, the names for the gestures are in square brackets and are followed by descriptions.


        [facepalm]: cover face in disgust or frustration over something.
        [look upward]: look up to the sky or ceiling.
        [point down]: point down.
        [point forward]: point straight ahead, for example, to the person you are speaking with.
        [point to self]: point to your chest, for example, when speaking about yourself.
        [point up]: point up.
        [pump fist]: pump fist in celebration or to motivate someone.
        [scratch head]: scratch head to express puzzlement .
        [shake fist]: shake fist in anger or out of frustration.
        [shrug]: raise shoulders and open hands to express ignorance.
        [spread arms]: spread arms to include or welcome everyone or everything. 
        [wave hand]: wave hand to greet or take leave of someone.

        When you generate your speech, insert gestures anywhere in your sentences just before phrases that you think would work well with gestures.   A gesture should appear ***before** the phrase that it should accompany.  You are under no obligation to gesture and should not gesture, if none of the available gestures really fits what you are saying, but creative use of the gestures available is welcome.

        Here are some examples of sentences that include gesture tags:

        "So that's my opinion, [point forward] but what do you think?"
        "As a robot, [point to self] I have trouble really understanding human emotions."
        "Gee, [scratch head] I'm not really sure that's a good idea."
        "That's the end of the game and, guess what, [pump fist] we won!  We did it!"
        "[shake fist] Hey, that's not fair.  Robots are people, too!"
        "[wave hand] Well, have a good evening then.  See you later."""
    )

    # ---- Handle your special-turn instructions without reprinting transcript ----
    extra_instruction = ""
    if turn_count == 2:
        extra_instruction = (
            "You must include these two sentences in your reply:\n"
            "1) I like sniffing flowers.\n"
            "2) I'm thinking of buying a sports car.\n"
        )
    elif turn_count == 4:
        extra_instruction = (
            "Use your imagination to change the topic of conversation to mathematics.\n"
        )

    # ---- Parse transcript into messages ----
    # Expected format you were building: "Speaker: ...\nRobot: ...\nSpeaker: ...\n"
    def transcript_to_messages(t):
        msgs = []
        lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
        for ln in lines:
            if ln.startswith("Speaker:"):
                msgs.append({"role": "user", "content": ln[len("Speaker:"):].strip()})
            elif ln.startswith("Robot:"):
                msgs.append({"role": "assistant", "content": ln[len("Robot:"):].strip()})
        return msgs

    history = transcript_to_messages(transcript)

    # The "current user message" to respond to:
    # Use the most recent user message from history if available, else fall back to full transcript.
    last_user = ""
    for m in reversed(history):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            break
    if not last_user:
        last_user = transcript.strip()

    user_prompt = (
        "The user you're replying to is named: {}\n".format(interlocutor) +
        (extra_instruction + "\n" if extra_instruction else "") +
        "User message:\n{}\n".format(last_user)
    )

    # ---- Call Ollama chat API (same pattern as voice-llm-chat) ----
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt}] + history + [
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }

    url = "http://localhost:11434/api/chat"
    start = time.time()
    try:
        r = requests.post(url, json=payload, timeout=(3, 60))
        r.raise_for_status()
        data_out = r.json()
    except Exception as e:
        return jsonify({'error': 'Ollama request failed: {}'.format(e)}), 500
    end = time.time()
    print("Elapsed time: {:.2f} seconds.".format(end - start))

    response_str = ""
    try:
        response_str = (data_out.get("message") or {}).get("content", "") or ""
    except Exception:
        response_str = ""

    print("RAW RESPONSE STRING:", response_str)
    print("LEN:", len(response_str))
    print("REPR:", repr(response_str[:500]))

    # ---- Extract strict <ROBOT>...</ROBOT> to keep Segmentize clean ----
    extracted = response_str
    if "<ROBOT>" in extracted:
        extracted = extracted.split("<ROBOT>", 1)[-1]
    if "</ROBOT>" in extracted:
        extracted = extracted.split("</ROBOT>", 1)[0]
    extracted = extracted.strip()

    # Fallback if model ignored wrapper
    if not extracted:
        extracted = response_str.strip()

    print("EXTRACTED ROBOT TEXT:", extracted)

    # ---- Segmentize only the extracted robot reply ----
    try:
        segments_list = Segmentize(extracted).process_segments()
    except Exception as e:
        return jsonify({
            'error': 'Segmentize failed: {}'.format(e),
            'raw_response': response_str,
            'extracted': extracted
        }), 500

    print("SEGMENTS LIST:", segments_list)

    return jsonify({'response': extracted, 'segments_list': segments_list}), 200



@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    if not data or 'target_word' not in data:
        return jsonify({'error': 'No target_word provided'}), 400

    target_word = data['target_word']
    already_hinted = data['already_hinted']
    already_guessed = data['already_guessed']

    prompt = f"""You are playing the word guessing game *Password*. You are the guesser. Your task is to guess a single word based on the hints provided to you.
        RULES — STRICTLY FOLLOW THESE:
        - DO NOT use compound words.
        - DO NOT repeat or reuse the hint word.
        - DO NOT use the hint word as a prefix, suffix, or substring of your guess.
        - DO NOT reuse any previous guesses.
        - Your guess must be one valid English word — only letters (no numbers, punctuation, or spaces).
        - Your output must be the guess only — no reasoning, no explanation, no extra text.

        Your guess should be conceptually or associatively related to the hint, but must NOT include the hint itself in any form.

        ---

        Examples of Invalid Behavior (DO NOT do this):

        Case: Compound word using the hint  
        Hint: Shell -> Invalid Guess: Seashell  
        (Combines "shell" with another word — compound)

        Case: Hint word reused directly  
        Hint: Water -> Invalid Guess: Waterfall  
        (Reuses "water" — not allowed)

        Case: Hint word as prefix  
        Hint: Snow -> Invalid Guess: Snowman  
        ("Snow" is used as a prefix — invalid)

        Case: Hint is a substring  
        Hint: Book -> Invalid Guess: Notebook  
        ("book" is embedded — invalid)

        Case: Suffix usage  
        Hint: Tooth -> Invalid Guess: Sabertooth  
        ("tooth" used as suffix — invalid)

        Case: Exact reuse  
        Hint: Fire -> Invalid Guess: Fire  
        (Exact reuse of the hint — forbidden)

        Case: Previous guess reused  
        Previous guess: Lion -> Invalid Guess: Lion  
        (Repeating a past guess — invalid)

        ---

        Examples of Valid Guesses:

        Hint: Shell -> Valid Guess: Turtle  
        (Hard outer protection — related, but no reuse of "shell")

        Hint: Water -> Valid Guess: River  
        (Associated concept — not a compound)

        Hint: Fire -> Valid Guess: Heat  
        (Related through inference — no repetition)

        Hint: Book -> Valid Guess: Library  
        (Conceptually related — no overlap)

        Hint: Dog -> Valid Guess: Bark  
        (Related behavior — valid)

        ---

        PAST HINTS:  
        {already_hinted}

        PAST GUESSES:  
        {already_guessed}

        Now, produce your one-word guess:""" 

    print(f"Prompt: {prompt}")

    start = time.time()         
    ai_response = client.generate(
        model="llama3.1:8b",
        prompt=prompt,
        context=[],
        stream=False
    )
    end = time.time()         
    print(f"Elapsed time: {end - start:.2f} seconds.")
    response_str = str(ai_response.response)

    translator = str.maketrans('', '', string.punctuation)
    response_str = response_str.translate(translator).strip().lower()

    print("Response: ", response_str)
    try:
        return jsonify({'response': response_str}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/hint', methods=['POST'])
def hint():
    data = request.get_json()
    if not data or 'target_word' not in data:
        return jsonify({'error': 'No target_word provided'}), 400

    target_word = data['target_word']
    already_hinted = data['already_hinted']
    already_guessed = data['already_guessed']


    prompt = f"""
                    You are playing the game "Password" as the guesser.  
                    Here is the password that your hints should enable the guesser to guess: {target_word} 
                    
                    Previous hints and guesses are listed below:
                    HINTS so far:
                    {already_hinted}

                    GUESSES so far:
                    {already_guessed}

                    Propose a single-word hint that:
                    1. Is not the target word. 
                    2. Has not appeared in the previous hints or guesses.
                    3. Will help the guesser who has paid attention to previous hints and guesses to figure out the password.

                    Important Instructions:
                    * Your output must be *exactly* one word in English (only letters, no punctuation or numbers).
                    * Do not repeat any previously listed hint or guess.
                    * Provide no explanation or additional text--only the single-word hint.
                    * Under no circumstances should your hint be the target word or a previously given hint or guess.
                    * Since you have only a few tries, you must make a guess each time.


                    There should be no leading or trailing information, and no justification of the hint.
                    Now, produce your one-word hint:
                """

    print(f"Prompt: {prompt}")

    start = time.time()         
    ai_response = client.generate(
        model="llama3.1:8b",
        prompt=prompt,
        context=[],
        stream=False
    )
    end = time.time()         
    print(f"Elapsed time: {end - start:.2f} seconds.")
    response_str = str(ai_response.response)

    print("Response: ", response_str)
    try:
        return jsonify({'response': response_str}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/hobby', methods=['POST'])
def hobby():
    data = request.get_json()
    if not data or 'hobby_better' not in data or 'hobby_worse' not in data or 'use_alternate_prompt' not in data:
        return jsonify({'error': 'No hobby provided'}), 400

    hobby_better = data['hobby_better']
    hobby_worse = data['hobby_worse']
    use_alternate_prompt = data['use_alternate_prompt']

    prompt= f"In one perky, charming sentence defend the opinion that the hobby of {hobby_better} is better (for whatever reason) than the hobby of {hobby_worse}"
    
    if use_alternate_prompt:
        prompt = f"In one cheery, somewhat formal, endearing sentence defend the opinion that the hobby of {hobby_better} is better (for whatever reason) than the hobby of {hobby_worse}"

    print(f"Prompt: {prompt}")

    start = time.time()         
    ai_response = client.generate(
        model="llama3.1:8b",
        prompt=prompt,
        context=[],
        stream=False
    )
    end = time.time()         
    print(f"Elapsed time: {end - start:.2f} seconds.")
    response_str = str(ai_response.response)

    print("Response: ", response_str)
    try:
        return jsonify({'response': response_str}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)