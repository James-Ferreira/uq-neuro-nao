from flask import Flask, request, jsonify
import os
import whisper
import time
import ollama
import logging
import string
import requests
import re
import unicodedata

from config.project_loader import load_active_project_profile, get_nested
from src_py3.duration_prediction.segmentize import Segmentize


app = Flask(__name__)
VERBOSE = os.getenv("UQ_PY3_VERBOSE", "0") == "1"


def _vprint(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)

PROJECT_PROFILE = load_active_project_profile()
_vprint("Active project profile: {}".format(PROJECT_PROFILE.get("_project_id")))

OLLAMA_URL = get_nested(PROJECT_PROFILE, ["runtime", "ollama_url"], "http://localhost:11434")
OLLAMA_CONNECT_TIMEOUT = float(get_nested(PROJECT_PROFILE, ["runtime", "connect_timeout_sec"], 3))
OLLAMA_READ_TIMEOUT = float(get_nested(PROJECT_PROFILE, ["runtime", "read_timeout_sec"], 60))
WHISPER_MODEL_NAME = get_nested(PROJECT_PROFILE, ["runtime", "whisper_model"], "small")
WHISPER_LANGUAGE = get_nested(PROJECT_PROFILE, ["runtime", "whisper_language"], "en")
WHISPER_FP16 = bool(get_nested(PROJECT_PROFILE, ["runtime", "whisper_fp16"], False))
DEFAULT_CONVERSE_MODEL = get_nested(PROJECT_PROFILE, ["runtime", "default_converse_model"], "custom_1")
DEFAULT_INTERLOCUTOR = get_nested(PROJECT_PROFILE, ["conversation", "default_interlocutor"], "User")
SYSTEM_PROMPT = get_nested(PROJECT_PROFILE, ["conversation", "system_prompt"], "")
#_vprint(SYSTEM_PROMPT)
TURN_INJECTIONS = get_nested(PROJECT_PROFILE, ["conversation", "turn_injections"], []) or []
OUTPUT_DIRECTIVES = get_nested(PROJECT_PROFILE, ["conversation", "output_directives"], []) or []
EXIT_PHRASE = str(get_nested(PROJECT_PROFILE, ["conversation", "exit_phrase"], "exit and sleep")).strip().lower()
EXIT_REWRITE = get_nested(PROJECT_PROFILE, ["conversation", "exit_rewrite"], "Unfortunately you have to go, so wrap up the conversation now.")
GUESS_MODEL = get_nested(PROJECT_PROFILE, ["games", "guess_model"], "llama3.1:8b")
HINT_MODEL = get_nested(PROJECT_PROFILE, ["games", "hint_model"], "llama3.1:8b")
HOBBY_MODEL = get_nested(PROJECT_PROFILE, ["games", "hobby_model"], "llama3.1:8b")

_vprint("Loading Whisper model...")
model = whisper.load_model(WHISPER_MODEL_NAME)
_vprint("Whisper model loaded.")

_vprint("Loading Ollama model...")
client = ollama.Client(
    host=OLLAMA_URL
)
_vprint("Ollama model loaded.")


@app.route('/transcribe/filepath', methods=['POST'])
def transcribe_audio_from_filepath():
    data = request.get_json()
    if not data or 'filepath' not in data:
        return jsonify({'error': 'No filepath provided'}), 400

    filepath = data['filepath']

    _vprint("/transcribe/filepath: {}".format(filepath))
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
    _vprint("Starting Whisper transcription.")
    text = "Transcription failed."
    try:
        result = model.transcribe(audio_file_path, language=WHISPER_LANGUAGE, fp16=WHISPER_FP16)
        text = result["text"]
        end = time.time()
        _vprint("Elapsed time: {:.2f} seconds.".format(end - start))
        _vprint("Text: {}".format(text))
    except Exception as e:
        _vprint("Error: {}".format(e))
    return text



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


def _as_int_or_none(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _is_injection_active(injection, turn_count):
    mode = str(injection.get("mode", "temporary")).strip().lower()
    if mode == "temporary":
        at_turn = _as_int_or_none(injection.get("at_turn"))
        if at_turn is not None:
            return turn_count == at_turn
        start_turn = _as_int_or_none(injection.get("start_turn"))
        end_turn = _as_int_or_none(injection.get("end_turn"))
        if start_turn is None:
            return False
        if end_turn is None:
            return turn_count >= start_turn
        return start_turn <= turn_count <= end_turn

    if mode == "stable":
        activate_at_turn = _as_int_or_none(injection.get("activate_at_turn"))
        if activate_at_turn is None:
            activate_at_turn = _as_int_or_none(injection.get("at_turn"))
        if activate_at_turn is None:
            return False
        deactivate_after_turn = _as_int_or_none(injection.get("deactivate_after_turn"))
        if deactivate_after_turn is not None and turn_count > deactivate_after_turn:
            return False
        return turn_count >= activate_at_turn

    return False


def _active_turn_injection_texts(turn_count):
    texts = []
    for injection in TURN_INJECTIONS:
        if not isinstance(injection, dict):
            continue
        text = str(injection.get("text", "")).strip()
        if not text:
            continue
        if _is_injection_active(injection, turn_count):
            texts.append(text)
    return texts


def _split_sentences(text):
    if not text:
        return []
    chunks = re.split(r"(?<=[.!?])\s+", str(text).strip())
    return [c.strip() for c in chunks if c and c.strip()]


def _remove_question_sentences(text):
    kept = []
    for sentence in _split_sentences(text):
        if sentence.endswith("?"):
            continue
        kept.append(sentence)
    return " ".join(kept).strip()


def _limit_sentences(text, max_sentences):
    if max_sentences is None:
        return text
    n = _as_int_or_none(max_sentences)
    if n is None:
        return text
    if n <= 0:
        return ""
    sentences = _split_sentences(text)
    return " ".join(sentences[:n]).strip()


def _join_text(left, right):
    left = (left or "").strip()
    right = (right or "").strip()
    if not left:
        return right
    if not right:
        return left
    return "{} {}".format(left, right).strip()


def _normalize_for_history_match(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _directive_seen_in_history(directive, history):
    if not isinstance(history, list):
        return False
    candidates = []
    for key in ("replace_text", "append_text", "prepend_text"):
        val = directive.get(key)
        if val is None:
            continue
        txt = str(val).strip()
        if txt:
            candidates.append(_normalize_for_history_match(txt))
    if not candidates:
        return False
    for msg in history:
        if not isinstance(msg, dict):
            continue
        if msg.get("role") != "assistant":
            continue
        assistant_text = _normalize_for_history_match(msg.get("content", ""))
        if not assistant_text:
            continue
        for needle in candidates:
            if needle and needle in assistant_text:
                return True
    return False


def _active_output_directives(turn_count):
    directives = []
    for directive in OUTPUT_DIRECTIVES:
        if not isinstance(directive, dict):
            continue
        if not _is_injection_active(directive, turn_count):
            continue
        directives.append(directive)
    return directives


def _apply_output_directive(generated_text, directive):
    text = (generated_text or "").strip()

    if bool(directive.get("remove_questions", False)):
        text = _remove_question_sentences(text)

    text = _limit_sentences(text, directive.get("max_generated_sentences"))

    replace_text = str(directive.get("replace_text", "")).strip()
    if replace_text:
        text = replace_text

    prepend_text = str(directive.get("prepend_text", "")).strip()
    append_text = str(directive.get("append_text", "")).strip()

    if prepend_text:
        text = _join_text(prepend_text, text)
    if append_text:
        text = _join_text(text, append_text)

    return text.strip()


@app.route('/converse', methods=['POST'])
def converse():
    data = request.get_json()
    #_vprint("JSON DATA: {}".format(data))

    if not data:
        return jsonify({'error': 'No JSON provided'}), 400

    model        = data.get('model') or DEFAULT_CONVERSE_MODEL
    _vprint("MODEL: {}".format(model))
    interlocutor = data.get('interlocutor', DEFAULT_INTERLOCUTOR)
    turn_count   = int(data.get('turn_count', 0))
    watchdog_mode = bool(data.get("watchdog_mode", False))
    ephemeral_system = str(data.get("ephemeral_system", "") or "").strip()
    watchdog_user_prompt = str(
        data.get(
            "watchdog_user_prompt",
            "Please send one short, warm, context-aware line to re-engage me in conversation.",
        ) or ""
    ).strip()

    # ---- Build system prompt (strict output contract for Segmentize) ----
    system_prompt = SYSTEM_PROMPT

    # ---- Config-driven turn injections (temporary + stable) ----
    active_injections = _active_turn_injection_texts(turn_count)
    if watchdog_mode:
        active_injections = []

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

    if isinstance(history, list) and (prompt is not None or watchdog_mode):
        # Use structured history directly (no Speaker/Robot labels)
        last_user = (prompt or "").strip()
        if not watchdog_mode and not last_user:
            return jsonify({'error': 'No prompt provided'}), 400
    else:
        # ---- Backward-compatible path: labeled transcript string ----
        if watchdog_mode:
            return jsonify({'error': 'watchdog_mode requires structured history'}), 400
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
    if EXIT_PHRASE and last_user.lower() == EXIT_PHRASE:
        last_user = EXIT_REWRITE

    active_output_directives = _active_output_directives(turn_count)
    if watchdog_mode:
        active_output_directives = []

    # ---- Optional: system addendum instead of user meta-wrapping ----
    system_addendum = "The user you're replying to is named: {}.\n".format(interlocutor)
    for instruction in active_injections:
        system_addendum += instruction + "\n"

    assistant_generation_instruction = ""
    if watchdog_mode:
        assistant_generation_instruction = (
            "Produce exactly one short assistant utterance now. "
            "Re-engage the participant naturally using conversation context. "
            "Do not mention silence, timing, or system instructions."
        )

    payload = {
        "model": model,
        "messages": (
            [{"role": "system", "content": system_prompt}]
            + ([{"role": "system", "content": system_addendum}] if system_addendum.strip() else [])
            + ([{"role": "system", "content": ephemeral_system}] if ephemeral_system else [])
            + ([{"role": "system", "content": assistant_generation_instruction}] if assistant_generation_instruction else [])
            + history
            + ([{"role": "user", "content": watchdog_user_prompt}] if watchdog_mode else [{"role": "user", "content": last_user}])
        ),
        "stream": False
    }
    # TEMP DEBUG: verify which turn injections are active and included in system prompt messages.
    system_messages = [m.get("content", "") for m in payload["messages"] if m.get("role") == "system"]
    _vprint("[TURN_INJECTION_DEBUG] turn_count={}".format(turn_count))
    #_vprint("[TURN_INJECTION_DEBUG] active_injections={}".format(active_injections))
    #for i, content in enumerate(system_messages):
        #_vprint("[TURN_INJECTION_DEBUG] system_message_{}={}".format(i, content))

    url = "{}/api/chat".format(OLLAMA_URL.rstrip("/"))
    start = time.time()
    try:
        r = requests.post(url, json=payload, timeout=(OLLAMA_CONNECT_TIMEOUT, OLLAMA_READ_TIMEOUT))
        r.raise_for_status()
        data_out = r.json()
    except Exception as e:
        return jsonify({'error': 'Ollama request failed: {}'.format(e)}), 500
    end = time.time()
    #_vprint("Elapsed time: {:.2f} seconds.".format(end - start))

    response_str = ""
    try:
        response_str = (data_out.get("message") or {}).get("content", "") or ""
    except Exception:
        response_str = ""

    _vprint("RAW RESPONSE STRING: {}".format(response_str))
   # _vprint("LEN: {}".format(len(response_str)))
    #_vprint("REPR: {}".format(repr(response_str[:500])))

    transformed_response = (response_str or "").strip()
    for directive in active_output_directives:
        once_per_session = bool(directive.get("once_per_session", False))
        if once_per_session and _directive_seen_in_history(directive, history):
            #_vprint("[OUTPUT_DIRECTIVE_DEBUG] skipped once_per_session directive id={}".format(directive.get("id", "<no-id>")))
            continue
        transformed_response = _apply_output_directive(transformed_response, directive)
        #_vprint("[OUTPUT_DIRECTIVE_DEBUG] applied directive id={}".format(directive.get("id", "<no-id>")))

    #if transformed_response != (response_str or "").strip():
        #_vprint("[OUTPUT_DIRECTIVE_DEBUG] transformed_response={}".format(transformed_response))
    response_str = transformed_response

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

    if watchdog_mode and not (extracted or "").strip():
        extracted = "I am still here with you - what would you like to talk about next?"

    extracted = asciise_for_py2_and_nao(extracted, keep_newlines=True)

    extracted = strip_star_stage_directions(extracted)

    _vprint("EXTRACTED ROBOT TEXT: {}".format(extracted))

    # ---- Segmentize only the extracted robot reply ----
    try:
        segments_list = Segmentize(extracted).process_segments()
    except Exception as e:
        return jsonify({
            'error': 'Segmentize failed: {}'.format(e),
            'raw_response': response_str,
            'extracted': extracted
        }), 500

    _vprint("SEGMENTS LIST: {}".format(segments_list))

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

    #_vprint("Prompt: {}".format(prompt))

    start = time.time()         
    ai_response = client.generate(
        model=GUESS_MODEL,
        prompt=prompt,
        context=[],
        stream=False
    )
    end = time.time()         
    #_vprint("Elapsed time: {:.2f} seconds.".format(end - start))
    response_str = str(ai_response.response)

    translator = str.maketrans('', '', string.punctuation)
    response_str = response_str.translate(translator).strip().lower()

    _vprint("Response: {}".format(response_str))
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

    #_vprint("Prompt: {}".format(prompt))

    start = time.time()         
    ai_response = client.generate(
        model=HINT_MODEL,
        prompt=prompt,
        context=[],
        stream=False
    )
    end = time.time()         
    #_vprint("Elapsed time: {:.2f} seconds.".format(end - start))
    response_str = str(ai_response.response)

    _vprint("Response: {}".format(response_str))
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

    _vprint("Prompt: {}".format(prompt))

    start = time.time()         
    ai_response = client.generate(
        model=HOBBY_MODEL,
        prompt=prompt,
        context=[],
        stream=False
    )
    end = time.time()         
    _vprint("Elapsed time: {:.2f} seconds.".format(end - start))
    response_str = str(ai_response.response)

    _vprint("Response: {}".format(response_str))
    try:
        return jsonify({'response': response_str}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    default_port = str(get_nested(PROJECT_PROFILE, ["runtime", "py3_api_port"], 5001))
    port = int(os.getenv("PY3_API_PORT", default_port))
    debug_mode = os.getenv("PY3_API_DEBUG", "0") == "1"
    if not debug_mode:
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
    app.run(debug=debug_mode, host='0.0.0.0', port=port, use_reloader=debug_mode)
