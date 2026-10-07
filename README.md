# EduGenie – Gemini-powered learning assistant

FastAPI + HTML/CSS app: Q&A, explanations, quizzes, summaries, learning paths.

## Run locally
1. Get a free API key at https://aistudio.google.com/apikey
2. Setup:
   ```
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env             # then paste your key into .env
   uvicorn main:app --reload
   ```
3. Open http://127.0.0.1:8000

Optional: set `USE_LOCAL_MODEL=1` (and `pip install transformers torch`) to run
LaMini-Flan-T5-783M locally for explanations, as in the original report.

## Deploy on Render (free)
1. Push this folder to a GitHub repo (`.env` is git-ignored, so your key stays private).
2. Render.com → New → Web Service → connect the repo.
3. Build command: `pip install -r requirements.txt`
   Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Environment → add `GEMINI_API_KEY` = your key. Deploy.
(`render.yaml` and `Procfile` are included for one-click / Railway / Heroku-style hosts.)

## Endpoints
GET /qa?question=… · POST /explain {topic} · POST /quiz {text} ·
POST /summarize {text} · GET /learn/recommendations?topic=…
