from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load("lang_detector.pkl")

lang_names = {"en": "English", "es": "Spanish", "fr": "French", "de": "German"}

@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json()
    
    if not data or "text" not in data:
        return jsonify({"error": "Please provide a 'text' field"}), 400
    
    text  = data["text"]
    pred  = model.predict([text])[0]
    proba = model.predict_proba([text])[0]
    score = max(proba)

    return jsonify({
        "language": lang_names[pred],
        "code": pred,
        "confidence": round(score, 4)
    })

@app.route("/")
def home():
    return jsonify({"status": "Language detector is running!"})

if __name__ == "__main__":
    app.run()
