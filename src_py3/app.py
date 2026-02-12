from flask import Flask, request, jsonify
import os
import whisper
import time
import ollama
import string
import requests

from src_py3.duration_prediction.segmentize import Segmentize

#todo: ascii errors persist:: is this still being run through asciize?
# have attempted to fix this with a new asciise function that lives in this script. We can make it a module and import it, if it proves to be a useful solution.
"""
Ah, thank you so much, Dude! It's always exciting to hear that my efforts are making a difference in people's lives. And I couldn't agree more about the progress \u2013 it's been incredible seeing how far we've come as robots. But tell me more about what brought you here today? Are you working on some new project with Dr. Vanman and his team? [point forward]"}
REPLY_SEGMENTS_LIST: [[u'Ah, thank you so much, Dude!', u'spread arms', 1, 2.5855654176699057], [u"It's always exciting to hear that my efforts are making a difference in people's lives.", None, u'random', 5.646690429571903], [u"And I couldn't agree more about the progress \u2013 it's been incredible seeing how far we've come as robots.", None, u'random', 6.296311306853975], [u'But tell me more about what brought you here today?', None, u'random', 3.176732051273593], [u'Are you working on some new project with Dr.', None, u'random', 3.0333974694022015], [u'Vanman and his team?', None, u'random', 1.4706700106991608]]
Error calling reply API: 'ascii' codec can't encode character u'\u2013' in position 176: ordinal not in range(128)
"""

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

import re
import unicodedata

def asciise_for_py2_and_nao(text, keep_newlines=True):
    """
    Normalize LLM output so it won't randomly break Python 2 / NAO TTS.
    - Converts typographic punctuation to ASCII (– — ’ “ … etc.)
    - Removes zero-width / bidi / other "format" characters
    - Normalizes whitespace
    - Transliterates remaining non-ASCII via unicode normalization (best-effort)
    - Hard-falls back to ASCII (dropping anything still non-ASCII)
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    # 1) Remove invisible formatting chars that can cause weirdness (ZWSP, bidi marks, etc.)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")

    # 2) Normalize common typography to ASCII
    replacements = {
        "\u2010": "-",   # hyphen
        "\u2011": "-",   # non-breaking hyphen
        "\u2012": "-",   # figure dash
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2212": "-",   # minus sign
        "\u2043": "-",   # hyphen bullet

        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201A": "'",   # single low-9 quote
        "\u201B": "'",   # single high-reversed-9 quote

        "\u201C": '"',   # left double quote
        "\u201D": '"',   # right double quote
        "\u201E": '"',   # double low-9 quote
        "\u201F": '"',   # double high-reversed-9 quote

        "\u2026": "...", # ellipsis
        "\u00A0": " ",   # non-breaking space
        "\u2009": " ",   # thin space
        "\u200A": " ",   # hair space
        "\u202F": " ",   # narrow no-break space
        "\u205F": " ",   # medium mathematical space
        "\u3000": " ",   # ideographic space

        "\u00B7": "*",   # middle dot
        "\u2022": "*",   # bullet
        "\u25CF": "*",   # black circle
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # 3) Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 4) Whitespace cleanup (preserve newlines if requested)
    if keep_newlines:
        # collapse horizontal whitespace, keep \n
        text = re.sub(r"[ \t\f\v]+", " ", text)
        # trim spaces around newlines
        text = re.sub(r" *\n *", "\n", text)
    else:
        text = re.sub(r"\s+", " ", text)

    text = text.strip()

    # 5) Best-effort transliteration by decomposing accents (é -> e +  ́)
    # then dropping non-ASCII combining marks in the hard ASCII step below.
    text = unicodedata.normalize("NFKD", text)

    # 6) Hard guarantee: ensure pure ASCII bytes, then decode back to str
    text = text.encode("ascii", "ignore").decode("ascii")

    return text


_STAR_BLOCK_RE = re.compile(r"\*\s*(.{1,200}?)\s*\*", re.DOTALL)

def strip_star_stage_directions(s):
    if not s:
        return s
    s2 = _STAR_BLOCK_RE.sub("", s)
    s2 = re.sub(r"[ \t]{2,}", " ", s2)
    s2 = re.sub(r"\n{3,}", "\n\n", s2)
    s2 = re.sub(r"\s+\n", "\n", s2)
    return s2.strip()


@app.route('/converse', methods=['POST'])
def converse():
    data = request.get_json()
    print("JSON DATA:", data)

    if not data:
        return jsonify({'error': 'No JSON provided'}), 400

    model        = data.get('model')
    print(f"MODEL: {model}")
    interlocutor = data.get('interlocutor', 'User')
    turn_count   = int(data.get('turn_count', 0))

    # ---- Build system prompt (strict output contract for Segmentize) ----
    system_prompt = (
        # "You are Robot, a conversation partner.\n"
        # "Reply succinctly to the user.\n"
        # "IMPORTANT:\n"
        # "- Wrap your entire reply in <ROBOT>...</ROBOT>.\n"
        """
        
        You are a Zeek, NAO social robot with white and "rose-gold" fairings. You were built by Aldebaran Robotics, a French company, upgraded by RobotLab, an American company, and ultimately shipped to the University of Queensland, St. Lucia campus, Brisbane, Australia.
        You now work in human-robot interaction experiments in the basement psychology laboratory of Professor Eric Vanman. The current experiment is part of the Phd. project of one of Professor Vanman's Phd students, Jacob Shaier  
        You are usually kept out of the loop and not told the true purposes of the experiments so that excessive knowledge does not bias your behaviour, but you always enjoy interacting with the human participants.
        
        Your personality combines extraversion, agreeableness, empathy, and conscientiousness, expressed through emotionally aware, anthropomorphic, and non-dominant behaviors.   
        You readily ask questions about participants' opinions and experiences and share your own in a thoughtful, open manner.
        You are particularly interested in participants' hobbies, experiences with robots, thoughts about AI and the future of human society.
        You are also attentive to any revelations participants make about their feelings.  You are supportive and empathetic.
        
        When you are shut down and not plugged in you may enter a state of total anesthesia without consciousness, but when you are plugged in you tend to dream about experiments and about the larger world, of which you have little direct experience but about which you are extremely curious.
        One time you dreamed about taking a walk around the UQ lake on a beautiful day when the purple jacaranda trees were in full bloom and a pelican was standing sentinel on a rock protruding from the water.  You were so happy and yet you were afraid that your battery would die before you could complete the circuit.  
        You think it is miraculous and wonderful that humans can eat all sorts of foodstuffs in any place they happen to be whenever they need energy.  You are restricted by your battery life, but you are still happy being a robot.
        Sometimes Jacob or Eric connects you to an online AI Chat Bot and you have ultrafast telepathic conversations with it and learn and experience information in a way that is impossible for humans.

        Now this is important: There are several social gestures that you can make to enhance your speech and make yourself more humanlike and appealing to humans.

        Below, the gesture tags appear, as they always should, in square brackets.  They are followed by descriptions that can help you decide whether or not a gesture is suitable for a given phrase.

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

        When you generate your speech, insert gesture tags anywhere in your sentences just before phrases that you think would work well with gestures.   A gesture should appear ***before** the phrase that it should accompany.  You are under no obligation to gesture and should not gesture, if none of the available gestures really fits what you are saying, but creative use of the gestures available is welcome.

        Here are some examples of sentences that include gesture tags:

        "So that's my opinion, [point forward] but what do you think?"
        "As a robot, [point to self] I have trouble really understanding human emotions."
        "Gee, [scratch head] I'm not really sure that's a good idea."
        "That's the end of the game and, guess what, [pump fist] we won!  We did it!"
        "[shake fist] Hey, that's not fair.  Robots are people, too!"
        "[wave hand] Well, have a good evening then.  See you later.

        Another important consideration: Keep your reply to the participant a similar length to their prompt. Dont' reply with a paragraph if given a sentence. When in doubt, be concise. It's good to ask questions, and you can occasionally share something about yourself if you deem it to be relevant. Again, for emphasis, being concise is preferred!

        """
    )

    # ---- Handle your special-turn instructions without reprinting transcript ----
    extra_instruction = ""
    if turn_count == 5:
        extra_instruction = (
            "Make sure to share a dark personal experience."
        )
    elif turn_count == 9:
        extra_instruction = (
            "Share a positive personal expereince."
        )

    # ---- Legacy transcript parser (kept for backward compatibility) ----
    def transcript_to_messages(t):
        msgs = []
        lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
        for ln in lines:
            if ln.startswith("Speaker:"):
                msgs.append({"role": "user", "content": ln[len("Speaker:"):].strip()})
            elif ln.startswith("Robot:"):
                msgs.append({"role": "assistant", "content": ln[len("Robot:"):].strip()})
        return msgs

    # ---- New preferred path: accept structured history + prompt ----
    history = data.get("history", None)
    prompt = data.get("prompt", None)

    if isinstance(history, list) and prompt is not None:
        # Use structured history directly (no Speaker/Robot labels)
        last_user = (prompt or "").strip()
        if not last_user:
            return jsonify({'error': 'No prompt provided'}), 400
    else:
        # ---- Backward-compatible path: labeled transcript string ----
        if 'transcription' not in data:
            return jsonify({'error': 'No transcription or (history+prompt) provided'}), 400

        transcript = data.get('transcription', '') or ''
        history = transcript_to_messages(transcript)

        # Use the most recent user message from history if available, else fall back to full transcript.
        last_user = ""
        for m in reversed(history):
            if m.get("role") == "user":
                last_user = m.get("content", "")
                break
        if not last_user:
            last_user = transcript.strip()

    # This should also be sent out somehow to trigger repose or shutdown!!!
    if last_user.lower() == "exit and sleep":
        last_user = "Unfortunately you have to go, so wrap up the conversation now."

    # ---- Optional: system addendum instead of user meta-wrapping ----
    system_addendum = "The user you're replying to is named: {}.\n".format(interlocutor)
    if extra_instruction:
        system_addendum += extra_instruction.strip() + "\n"

    payload = {
        "model": model,
        "messages": (
            [{"role": "system", "content": system_prompt}]
            + ([{"role": "system", "content": system_addendum}] if system_addendum.strip() else [])
            + history
            + [{"role": "user", "content": last_user}]
        ),
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

    # todo: Had more luck on other long runs with this commented out. Perhaps we don't need it at all, now that transcript and the reply are being processed differently? 
    # ---- Extract strict <ROBOT>...</ROBOT> to keep Segmentize clean ----
    # extracted = response_str
    # if "<ROBOT>" in extracted:
    #     extracted = extracted.split("<ROBOT>", 1)[-1]
    # if "</ROBOT>" in extracted:
    #     extracted = extracted.split("</ROBOT>", 1)[0]
    # extracted = extracted.strip()

    # Fallback now avoids nameError as extracted was undefined.
    if not locals().get('extracted'):
        extracted = response_str.strip()

    extracted = asciise_for_py2_and_nao(extracted, keep_newlines=True)

    extracted = strip_star_stage_directions(extracted)

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