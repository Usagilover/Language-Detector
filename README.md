# Signal Decoder — Language Detector on Railway

A small Flask web app that wraps your `lang_detector.pkl` model (char-level
TF-IDF + calibrated linear SVM, 20 languages) behind a web UI and a JSON API,
ready to deploy on [Railway](https://railway.app).

```
lang-detector-app/
├── app.py              Flask app: loads the model, serves the UI + API
├── model/
│   └── lang_detector.pkl
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── requirements.txt
├── runtime.txt          pins Python 3.11
├── Procfile             tells Railway how to start the app
├── railway.json          explicit build/start/healthcheck config
└── .gitignore
```

## Run it locally first (optional, but recommended)

```bash
cd lang-detector-app
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 — type a sentence, hit **Transmit**.

## Deploy to Railway

You'll need a free [Railway](https://railway.app) account. Two ways to ship it:

### Option A — Railway CLI (fastest)

```bash
npm install -g @railway/cli
cd lang-detector-app
railway login
railway init          # creates a new Railway project
railway up            # uploads this folder and builds it
```

Once it's built, run `railway domain` to generate a public `*.up.railway.app`
URL (or add one from the dashboard under **Settings → Networking**).

### Option B — GitHub + Railway dashboard

1. Push this folder to a new GitHub repo:
   ```bash
   cd lang-detector-app
   git init
   git add .
   git commit -m "Language detector app"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```
   The model file is ~80 MB. That's under GitHub's 100 MB hard limit so a
   normal push will work, but if you'd rather not store a binary that size
   in git, see **"Keeping the repo light"** below.
2. In Railway: **New Project → Deploy from GitHub repo** → pick the repo.
3. Railway detects `requirements.txt` + `Procfile` automatically (Nixpacks)
   and builds it. No extra config needed — `railway.json` is already there
   to set the start command and a `/health` healthcheck.
4. Under **Settings → Networking**, click **Generate Domain** to get a
   public URL.

Either way, Railway sets a `PORT` environment variable automatically —
`app.py` and the `Procfile` already read it, so you don't need to set
anything yourself.

## Keeping the repo light (optional)

If you don't want an 80 MB binary in git history, store the model outside
the repo and point `MODEL_PATH` at it instead:

- Upload `lang_detector.pkl` somewhere with a direct download URL (e.g. a
  private S3/R2 bucket, a GitHub Release asset, Hugging Face Hub).
- In Railway, add an environment variable `MODEL_URL` with that link, and
  add a few lines to `app.py` to download it to `/tmp/lang_detector.pkl` on
  startup if it isn't already cached, then set `MODEL_PATH` to that path.
- Or use [Git LFS](https://git-lfs.com) for the `.pkl` file — Railway's
  Nixpacks builder supports LFS-tracked files out of the box.

For a single ~80 MB file, committing it directly (as set up here) is the
simplest path and is fine for a personal/demo project.

## API

```
POST /api/detect
Content-Type: application/json

{ "text": "Bonjour, comment ça va?" }
```

```json
{
  "text": "Bonjour, comment ça va?",
  "detected": { "code": "fr", "name": "French", "confidence": 0.98 },
  "top": [
    { "code": "fr", "name": "French", "confidence": 0.98 },
    { "code": "tr", "name": "Turkish", "confidence": 0.01 }
  ]
}
```

`GET /health` returns `{"status": "ok", "languages": 20}` — used by
Railway's healthcheck.

## Updating the model later

Drop a new `lang_detector.pkl` into `model/`, commit, push (or `railway up`
again) — `app.py` loads whatever is at `MODEL_PATH` on startup, no code
changes needed as long as the new model is the same kind of scikit-learn
`Pipeline` with `.predict_proba()` and `.classes_`.
