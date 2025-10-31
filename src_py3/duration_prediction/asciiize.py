from num2words import num2words

import re
from typing import Callable
from num2words import num2words


# ----------------------------------------------------------------------
# 1. Build a converter that knows how to turn a matched string into words
# ----------------------------------------------------------------------
def _make_num2words_replacer(
    lang: str = "en",
    to: str = "cardinal",   # "cardinal" | "ordinal" | "year" | ...
    **num2words_kwargs,
) -> Callable[[re.Match], str]:
    """
    Return a replacement function suitable for re.sub.

    Parameters
    ----------
    lang : str
        Language passed to num2words (default "en").
    to : str
        What kind of word to generate (default "cardinal").
    **num2words_kwargs
        Any extra arguments accepted by num2words (e.g. `prefer` for ordinals).

    Returns
    -------
    Callable[[re.Match], str]
        Function that receives a Match object and returns the spelled-out version.
    """
    def replacer(match: re.Match) -> str:
        num_str = match.group(0)          # the original token, e.g. "-42.5e3"
        # ------------------------------------------------------------------
        # 1. Parse the token into a Python number (int or float)
        # ------------------------------------------------------------------
        try:
            # Scientific notation → float, otherwise try int first
            if "e" in num_str.lower() or "E" in num_str:
                num = float(num_str)
            else:
                # int() ignores trailing dots/comma if they are not part of the number
                num = int(num_str.replace(",", ""))
        except ValueError:
            # Fallback – return the original token unchanged
            return num_str

        # ------------------------------------------------------------------
        # 2. Convert the Python number to words
        # ------------------------------------------------------------------
        # num2words works with int, float, Decimal, etc.
        try:
            spelled = num2words(num, lang=lang, to=to, **num2words_kwargs)
        except Exception as exc:          # pragma: no cover
            # If num2words chokes, keep the original token
            return num_str

        # ------------------------------------------------------------------
        # 3. Preserve punctuation that was attached to the number
        # ------------------------------------------------------------------
        # e.g. "42." → "forty-two."   or   "42," → "forty-two,"
        before = match.group("before") or ""
        after  = match.group("after")  or ""
        return before + spelled + after

    return replacer


# ----------------------------------------------------------------------
# 2. The public function
# ----------------------------------------------------------------------
def numbers_to_words(
    text: str,
    *,
    lang: str = "en",
    to: str = "cardinal",
    **num2words_kwargs,
) -> str:
    """
    Replace every numeric token in *text* with its spoken form.

    Parameters
    ----------
    text : str
        Input string that may contain numbers.
    lang, to, **num2words_kwargs
        Forwarded to `num2words`.

    Returns
    -------
    str
        The original text with numbers spelled out.

    Examples
    --------
    >>> numbers_to_words("I have 42 apples, 3.14 pies and -7 oranges.")
    'I have forty-two apples, three point one four pies and minus seven oranges.'
    """
    # ------------------------------------------------------------------
    # Regex explanation (named groups):
    #   (?P<before>[.,;:!?])?   optional punctuation **before** the number
    #   (?P<num>[-+]?\d[\d,]*(\.\d+)?([eE][-+]?\d+)?)
    #       the actual number (int, float, scientific, commas as thousands)
    #   (?P<after>[.,;:!?])?    optional punctuation **after** the number
    # ------------------------------------------------------------------
    number_pattern = re.compile(
        r"""(?P<before>[.,;:!?])?      # punctuation glued to the left
            (?P<num>
                [-+]?\d[\d,]*              # integer part, optional sign & commas
                (\.\d+)?                   # optional decimal part
                ([eE][-+]?\d+)?            # optional scientific notation
            )
            (?P<after>[.,;:!?])?       # punctuation glued to the right
        """,
        re.VERBOSE,
    )

    replacer = _make_num2words_replacer(lang=lang, to=to, **num2words_kwargs)
    return number_pattern.sub(replacer, text)

def asciiize(text):
    partially_clean = text.encode("ascii", "ignore").decode("ascii")

    return numbers_to_words(partially_clean)


if __name__ == "__main__":

    with open("/Users/neurorobots/Desktop/repos/uq-neuro-nao/src_py3/duration_prediction/texts/raw_verification_text_block.txt", 'r') as file:
        text = file.read()

    fully_clean = asciiize(text)

    try:
        with open("/Users/neurorobots/Desktop/repos/uq-neuro-nao/src_py3/duration_prediction/texts/verification_text_block.txt", "w", encoding="ascii") as f:
            f.write(fully_clean)
        print("File saved successfully!")
    except Exception as e:
        print("Error saving file:", e)

    #print(fully_clean)  # Output: "Python is easy to learn  but sometimes tricky !"   