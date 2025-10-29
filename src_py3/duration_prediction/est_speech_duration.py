import numpy as np
import re
import syllapy
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple

# -------------------------------------------------
# 1. FEATURE EXTRACTOR (unchanged)
# -------------------------------------------------
WORD_RE = re.compile(r"[A-Za-z0-9']+")

def make_features(text: str) -> dict:
    words = WORD_RE.findall(text)
    sylls = syllapy.count(text)
    puncts = {',': text.count(','), '.': text.count('.'),
              ':': text.count(':'), ';': text.count(';'),
              '?': text.count('?'), '!': text.count('!'),
              '…': text.count('…')}

    return {
        "n_chars":          len(text),
        "n_words":          len(words),
        "n_syll":           sylls,
        "mean_word_len":    (sum(map(len, words)) / len(words)) if words else 0,
        "n_commas":         puncts[','],
        "n_periods":        puncts['.'],
        "n_colon_semicolon": puncts[':'] + puncts[';'],
        "n_qe":             puncts['?'] + puncts['!'],
        "n_ellipsis":       puncts['…'],
        "starts_cap":       int(text[:1].isupper()),
        "ends_punct":       int(text[-1] in ".?!"),
    }

# -------------------------------------------------
# 2. VECTORIZER
# -------------------------------------------------
def vectorize(texts: List[str]) -> Tuple[np.ndarray, List[str]]:
    feats = [make_features(s) for s in texts]
    keys  = sorted(feats[0].keys())
    X = np.array([[f[k] for k in keys] for f in feats], dtype=float)
    return X, keys

# -------------------------------------------------
# 3. ROBUST PREDICTOR
# -------------------------------------------------
class DurationPredictor:
    def __init__(self, alpha: float = 1.0):
        self.model   = Ridge(alpha=alpha, fit_intercept=True)
        self.scaler  = StandardScaler()
        self.keys_: List[str] = None

    def fit(self, texts: List[str], durations: List[float]):
        X, self.keys_ = vectorize(texts)

        # ---- 1. Guard against zero-variance columns -----------------
        var = X.var(axis=0)
        keep = var > 1e-12                     # keep only columns with *some* variance
        X = X[:, keep]
        self.keep_cols_ = keep

        # ---- 2. Scale ------------------------------------------------
        X_scaled = self.scaler.fit_transform(X)

        # ---- 3. Train ------------------------------------------------
        self.model.fit(X_scaled, durations)

    def predict(self, text: str) -> float:
        feats = make_features(text)
        x = np.array([[feats[k] for k in self.keys_]], dtype=float)

        # ---- 1. Apply same column-mask as during training ----------
        x = x[:, self.keep_cols_]

        # ---- 2. Scale ------------------------------------------------
        x_scaled = self.scaler.transform(x)

        # ---- 3. Predict ---------------------------------------------
        pred = self.model.predict(x_scaled)[0]

        # ---- 4. Clip to a sane range (optional but helpful) -------
        pred = np.clip(pred, 0.1, 30.0)   # seconds
        return float(pred)
# -------------------------------------------------
# 4. EXAMPLE USAGE
# -------------------------------------------------
if __name__ == "__main__":
    # -----------------------------------------------------------------
    # TRAINING DATA (you will collect many such pairs in practice)
    # -----------------------------------------------------------------
    train_texts = ['Now this is the point. You fancy me mad.', 'Madmen know nothing. But you should have seen me.', 'You should have seen how wisely I proceeded -- with what caution -- with what foresight -- with what dissimulation I went to work!', 'I was never kinder to the old man than during the whole week before I killed him.', 'And every night, about midnight, I turned the latch of his door and opened it -- oh, so gently!', 'And then, when I had made an opening sufficient for my head, I put in a dark lantern, all closed, closed, so that no light shone out;', 'and then I thrust in my head.', 'Oh, you would have laughed to see how cunningly I thrust it in!', 'I moved it slowly -- very, very slowly, so that I might not disturb the old man\xe2\x80\x99s sleep.', 'It took me an hour to place my whole head within the opening so far that I could see him as he lay upon his bed.', 'Ha! -- would a madman have been so wise as this?', 'And then, when my head was well in the room, I undid the lantern cautiously -- oh, so cautiously -- cautiously (for the hinges creaked) -- I undid it just so much that a single thin ray fell upon the vulture eye.', 'And this I did for seven long nights -- every night just at midnight -- but I found the eye always closed;', 'and so it was impossible to do the work;', 'for it was not the old man who vexed me;', 'but his Evil Eye. And every morning, when the day broke, I went boldly into the chamber;', 'and spoke courageously to him, calling him by name in a hearty tone;', 'and inquiring how he had passed the night.', 'So you see he would have been a very profound old man, indeed, to suspect that every night, just at twelve, I looked in upon him while he slept.']
    train_durations = [3.202072858810425, 3.3758039474487305, 8.295403957366943, 5.016243934631348, 6.758117914199829, 10.34211802482605, 1.9351820945739746, 4.092810153961182, 6.8662428855896, 6.645294189453125, 3.4834768772125244, 14.637854814529419, 7.073831081390381, 2.755497932434082, 2.768275022506714, 5.935276985168457, 4.505468130111694, 2.868773937225342, 10.032859086990356]   # seconds, measured from your TTS engine

    # -----------------------------------------------------------------
    # TRAIN THE MODEL (once)
    # -----------------------------------------------------------------
    predictor = DurationPredictor(alpha=1.0)
    predictor.fit(train_texts, train_durations)

    # -----------------------------------------------------------------
    # PREDICT NEW SENTENCES
    # -----------------------------------------------------------------
    new_sentences = [
        "Short.",
        "A longer sentence with commas, periods, and a question?",
        "Wow!!!"
    ]

    for s in new_sentences:
        dur = predictor.predict(s)
        print(f'"{s}"  →  {dur:.3f} s')
