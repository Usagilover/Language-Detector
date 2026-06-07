from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load("lang_detector.pkl")

lang_names = {"en": "English", "es": "Spanish", "fr": "French", "de": "German"}
lang_flags = {"en": "🇬🇧", "es": "🇪🇸", "fr": "🇫🇷", "de": "🇩🇪"}
lang_subtitles = {"en": "Anglo-Saxon roots", "es": "Romance language", "fr": "Langue d'amour", "de": "Germanic tongue"}

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
        "confidence": round(score, 4),
        "flag": lang_flags[pred],
        "subtitle": lang_subtitles[pred]
    })

@app.route("/")
def home():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lingua — Language Detector</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --rose-50:  #fff1f3;
  --rose-100: #ffe4e9;
  --rose-200: #fecdd6;
  --rose-300: #fda4b4;
  --rose-400: #fb6f8a;
  --rose-500: #f43f67;
  --rose-600: #e11d4a;
  --blush:    #fdf2f4;
  --petal:    #fce7ec;
  --cream:    #fffaf9;
  --text-dark:#2d1a20;
  --text-mid: #7a4f5a;
  --text-soft:#b48a94;
}

body {
  font-family: "DM Sans", sans-serif;
  background: var(--blush);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  position: relative;
  overflow-x: hidden;
}

/* Decorative background blobs */
body::before, body::after {
  content: "";
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.45;
  pointer-events: none;
  z-index: 0;
}
body::before {
  width: 500px; height: 500px;
  background: radial-gradient(circle, #fda4b4, #fecdd6);
  top: -120px; right: -100px;
}
body::after {
  width: 400px; height: 400px;
  background: radial-gradient(circle, #fce7ec, #fff1f3);
  bottom: -80px; left: -80px;
}

.wrap {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 520px;
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 36px;
  animation: fadeUp 0.7s ease both;
}
.header .eyebrow {
  display: inline-block;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--rose-400);
  background: var(--rose-100);
  padding: 5px 14px;
  border-radius: 99px;
  margin-bottom: 16px;
}
.header h1 {
  font-family: "Playfair Display", serif;
  font-size: 42px;
  font-weight: 600;
  color: var(--text-dark);
  line-height: 1.1;
  margin-bottom: 10px;
}
.header h1 em {
  font-style: italic;
  color: var(--rose-500);
}
.header p {
  font-size: 14px;
  color: var(--text-soft);
  font-weight: 300;
  letter-spacing: 0.02em;
}

/* Card */
.card {
  background: var(--cream);
  border-radius: 28px;
  padding: 36px;
  border: 1.5px solid var(--rose-200);
  box-shadow:
    0 2px 4px rgba(244,63,103,0.04),
    0 8px 24px rgba(244,63,103,0.08),
    0 32px 64px rgba(244,63,103,0.06);
  animation: fadeUp 0.7s 0.1s ease both;
}

/* Textarea */
.textarea-wrap {
  position: relative;
  margin-bottom: 16px;
}
.textarea-wrap label {
  display: block;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-soft);
  margin-bottom: 10px;
}
textarea {
  width: 100%;
  height: 150px;
  padding: 16px 18px;
  background: var(--blush);
  border: 1.5px solid var(--rose-200);
  border-radius: 16px;
  font-family: "DM Sans", sans-serif;
  font-size: 15px;
  font-weight: 300;
  color: var(--text-dark);
  resize: none;
  outline: none;
  line-height: 1.7;
  transition: border-color 0.2s, box-shadow 0.2s;
}
textarea::placeholder { color: var(--text-soft); }
textarea:focus {
  border-color: var(--rose-300);
  box-shadow: 0 0 0 4px rgba(253,164,180,0.18);
}

/* Button */
button {
  width: 100%;
  padding: 15px;
  background: var(--text-dark);
  color: #fff8f9;
  border: none;
  border-radius: 14px;
  font-family: "DM Sans", sans-serif;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.06em;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  position: relative;
  overflow: hidden;
}
button:hover {
  background: var(--rose-600);
  box-shadow: 0 6px 20px rgba(225,29,74,0.25);
  transform: translateY(-1px);
}
button:active { transform: translateY(0); }
button:disabled { opacity: 0.55; cursor: not-allowed; transform: none; box-shadow: none; }
button .btn-hint {
  position: absolute;
  right: 18px; top: 50%;
  transform: translateY(-50%);
  font-size: 11px;
  opacity: 0.45;
  letter-spacing: 0.04em;
}

/* Result */
.result {
  margin-top: 24px;
  padding: 28px;
  background: var(--petal);
  border-radius: 20px;
  border: 1.5px solid var(--rose-200);
  display: none;
  animation: popIn 0.45s cubic-bezier(0.34,1.56,0.64,1) both;
}
.result.show { display: block; }

.result-top {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 22px;
}
.flag-circle {
  width: 62px; height: 62px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(244,63,103,0.12);
  border: 2px solid var(--rose-200);
}
.result-text h2 {
  font-family: "Playfair Display", serif;
  font-size: 26px;
  font-weight: 600;
  color: var(--text-dark);
  line-height: 1.1;
}
.result-text .sub {
  font-size: 12px;
  color: var(--text-soft);
  font-style: italic;
  margin-top: 3px;
}

/* Confidence bar */
.conf-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.conf-label {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-soft);
}
.conf-pct {
  font-size: 13px;
  font-weight: 500;
  color: var(--rose-500);
}
.bar-bg {
  height: 6px;
  background: var(--rose-200);
  border-radius: 99px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  border-radius: 99px;
  background: linear-gradient(90deg, var(--rose-300), var(--rose-500));
  width: 0%;
  transition: width 0.8s cubic-bezier(0.16,1,0.3,1);
}

/* Language pills */
.pills {
  display: flex;
  gap: 8px;
  margin-top: 20px;
  flex-wrap: wrap;
}
.pill {
  padding: 5px 13px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 400;
  background: white;
  color: var(--text-soft);
  border: 1.5px solid var(--rose-200);
  transition: all 0.2s;
}
.pill.active {
  background: var(--text-dark);
  color: #fff8f9;
  border-color: var(--text-dark);
}

/* Error */
.error {
  margin-top: 14px;
  padding: 12px 16px;
  background: #fff0f2;
  border-radius: 12px;
  border: 1px solid #fecdd6;
  color: var(--rose-600);
  font-size: 13px;
  display: none;
}
.error.show { display: block; }

/* Divider */
.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 20px 0 0;
}
.divider-line { flex: 1; height: 1px; background: var(--rose-200); }
.divider-text { font-size: 11px; color: var(--text-soft); letter-spacing: 0.08em; }

/* Footer */
.footer {
  text-align: center;
  margin-top: 28px;
  font-size: 12px;
  color: var(--text-soft);
  animation: fadeUp 0.7s 0.2s ease both;
}
.footer span { color: var(--rose-400); }

/* Animations */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes popIn {
  from { opacity: 0; transform: scale(0.94); }
  to   { opacity: 1; transform: scale(1); }
}
</style>
</head>
<body>
<div class="wrap">
  <div class="header">
    <span class="eyebrow">AI Powered</span>
    <h1>Detect any <em>language</em></h1>
    <p>Paste text below and let the model identify it instantly</p>
  </div>

  <div class="card">
    <div class="textarea-wrap">
      <label>Your text</label>
      <textarea id="input" placeholder="Type or paste text in any of the four languages…"></textarea>
    </div>

    <button id="btn" onclick="detect()">
      Detect Language
      <span class="btn-hint">Ctrl + Enter</span>
    </button>

    <div class="error" id="error"></div>

    <div class="result" id="result">
      <div class="result-top">
        <div class="flag-circle" id="flag"></div>
        <div class="result-text">
          <h2 id="language"></h2>
          <div class="sub" id="subtitle"></div>
        </div>
      </div>

      <div class="conf-row">
        <span class="conf-label">Confidence</span>
        <span class="conf-pct" id="pct"></span>
      </div>
      <div class="bar-bg"><div class="bar-fill" id="bar"></div></div>

      <div class="divider">
        <div class="divider-line"></div>
        <div class="divider-text">supported languages</div>
        <div class="divider-line"></div>
      </div>
      <div class="pills">
        <span class="pill" id="pill-en">🇬🇧 English</span>
        <span class="pill" id="pill-es">🇪🇸 Spanish</span>
        <span class="pill" id="pill-fr">🇫🇷 French</span>
        <span class="pill" id="pill-de">🇩🇪 German</span>
      </div>
    </div>
  </div>

  <div class="footer">
    Built with <span>♥</span> · 4 languages · ML powered
  </div>
</div>

<script>
  async function detect() {
    const text = document.getElementById("input").value.trim();
    const btn  = document.getElementById("btn");
    const err  = document.getElementById("error");
    const res  = document.getElementById("result");

    err.classList.remove("show");

    if (!text) {
      err.textContent = "Please enter some text first.";
      err.classList.add("show");
      return;
    }

    btn.disabled = true;
    btn.textContent = "Detecting…";

    try {
      const r = await fetch("/detect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      const data = await r.json();
      if (data.error) throw new Error(data.error);

      document.getElementById("flag").textContent     = data.flag;
      document.getElementById("language").textContent = data.language;
      document.getElementById("subtitle").textContent = data.subtitle;
      document.getElementById("pct").textContent      = (data.confidence * 100).toFixed(1) + "%";

      ["en","es","fr","de"].forEach(c => document.getElementById("pill-"+c).classList.remove("active"));
      document.getElementById("pill-"+data.code).classList.add("active");

      res.classList.remove("show");
      void res.offsetWidth;
      res.classList.add("show");
      document.getElementById("bar").style.width = "0%";
      setTimeout(() => {
        document.getElementById("bar").style.width = (data.confidence * 100) + "%";
      }, 80);

    } catch(e) {
      err.textContent = "Something went wrong. Please try again.";
      err.classList.add("show");
    } finally {
      btn.disabled = false;
      btn.textContent = "Detect Language";
      const hint = document.createElement("span");
      hint.className = "btn-hint";
      hint.textContent = "Ctrl + Enter";
      btn.appendChild(hint);
    }
  }

  document.getElementById("input").addEventListener("keydown", e => {
    if (e.key === "Enter" && e.ctrlKey) detect();
  });
</script>
</body>
</html>'''

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
