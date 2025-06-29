from flask import Flask, request, jsonify
import os
import whisper
import time
import ollama
import string

app = Flask(__name__)

print("Loading Whisper model...")
model = whisper.load_model("small")
print("Whisper model loaded.")

print("Loading Ollama model...")
client = ollama.Client(
    host="http://localhost:11434"
)
print("Ollama model loaded.")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
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

@app.route('/converse', methods=['POST'])
def converse():
    data = request.get_json()
    if not data or 'transcription' not in data:
        return jsonify({'error': 'No transcription provided'}), 400

    transcript = data['transcription']

    prompt=f"You are a conversation partner, named 'Robot', who responds succintly to 'Speaker'. The conversation transcript is as follows:\n " + transcript
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