import os
import warnings

import joblib
from flask import Flask, jsonify, render_template, request

# The model was trained on an older scikit-learn version. Loading it on a
# newer version prints a harmless compatibility warning — silence it so it
# doesn't clutter the Railway logs.
warnings.filterwarnings("ignore", message=".*InconsistentVersionWarning.*")
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

APP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.environ.get("MODEL_PATH", os.path.join(APP_DIR, "model", "lang_detector.pkl"))

LANG_NAMES = {
    "ar": "Arabic", "bg": "Bulgarian", "de": "German", "el": "Greek",
    "en": "English", "es": "Spanish", "fr": "French", "hi": "Hindi",
    "it": "Italian", "ja": "Japanese", "nl": "Dutch", "pl": "Polish",
    "pt": "Portuguese", "ru": "Russian", "sw": "Swahili", "th": "Thai",
    "tr": "Turkish", "ur": "Urdu", "vi": "Vietnamese", "zh": "Chinese",
}

app = Flask(__name__)

print(f"Loading model from {MODEL_PATH} ...")
model = joblib.load(MODEL_PATH)
MODEL_LANGS = list(model.classes_)
print(f"Model loaded. Languages supported: {MODEL_LANGS}")


def lang_label(code: str) -> str:
    return LANG_NAMES.get(code, code)


@app.route("/")
def index():
    return render_template("index.html", langs=[
        {"code": c, "name": lang_label(c)} for c in sorted(MODEL_LANGS, key=lang_label)
    ])


@app.route("/health")
def health():
    return jsonify(status="ok", languages=len(MODEL_LANGS))


@app.route("/api/detect", methods=["POST"])
def detect():
    payload = request.get_json(silent=True) or {}
    text = (payload.get("text") or "").strip()

    if not text:
        return jsonify(error="Send some text to decode."), 400
    if len(text) < 2:
        return jsonify(error="Need at least a couple of characters to get a signal."), 400

    proba = model.predict_proba([text])[0]
    ranked = sorted(zip(model.classes_, proba), key=lambda x: -x[1])

    top = ranked[0]
    results = [
        {"code": code, "name": lang_label(code), "confidence": round(float(p), 4)}
        for code, p in ranked[:5]
    ]

    return jsonify(
        text=text,
        detected={"code": top[0], "name": lang_label(top[0]), "confidence": round(float(top[1]), 4)},
        top=results,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
