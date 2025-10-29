# duration_predictor.py
import joblib
import numpy as np
import re
import syllapy
import os

from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple


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

def vectorize(texts: List[str]) -> Tuple[np.ndarray, List[str]]:
    feats = [make_features(s) for s in texts]
    keys = sorted(feats[0].keys())
    X = np.array([[f[k] for k in keys] for f in feats], dtype=float)
    return X, keys

# -------------------------------------------------
# 1. Predictor Class (train once, save, reuse)
# -------------------------------------------------
class DurationPredictor:
    def __init__(self, alpha: float = 1.0):
        self.model = Ridge(alpha=alpha, fit_intercept=True)
        self.scaler = StandardScaler()
        self.keys_ = None
        self.keep_cols_ = None

    def fit(self, texts: List[str], durations: List[float]):
        X, self.keys_ = vectorize(texts)

        # Remove zero-variance features
        var = X.var(axis=0)
        self.keep_cols_ = var > 1e-12
        X = X[:, self.keep_cols_]

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, durations)

    def predict(self, text: str) -> float:
        feats = make_features(text)
        x = np.array([[feats[k] for k in self.keys_]], dtype=float)
        x = x[:, self.keep_cols_]
        x_scaled = self.scaler.transform(x)
        pred = self.model.predict(x_scaled)[0]
        return float(np.clip(pred, 0.1, 30.0))

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self, path)
        print(f"Model saved to {path}")

    @staticmethod
    def load(path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model not found: {path}")
        model = joblib.load(path)
        print(f"Model loaded from {path}")
        return model

# -------------------------------------------------
# 2. Training Script (run once)
# -------------------------------------------------
def train_and_save_model(texts: List[str], durations: List[float], model_path: str = "src_py3/duration_prediction/models/duration_predictor.pkl"):
    predictor = DurationPredictor(alpha=1.0)
    print(f"Training on {len(texts)} samples...")
    predictor.fit(texts, durations)
    predictor.save(model_path)

# -------------------------------------------------
# 3. Prediction Helper (for other scripts)
# -------------------------------------------------
def predict_duration(text: str, model_path: str = "src_py3/duration_prediction/models/duration_predictor.pkl") -> float:
    predictor = DurationPredictor.load(model_path)
    return predictor.predict(text)