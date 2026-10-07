import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
FALLBACKS = [m.strip() for m in os.getenv(
    "GEMINI_FALLBACK_MODELS", "gemini-flash-latest,gemini-flash-lite-latest").split(",") if m.strip()]
_client = None


def ask(prompt: str, json_mode: bool = False) -> str:
    """Send a prompt to Gemini. Retries on overload and falls back to other models."""
    global _client
    if _client is None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")
        _client = genai.Client(api_key=key)

    config = types.GenerateContentConfig(response_mime_type="application/json") if json_mode else None
    last_error = None

    for model in [MODEL] + FALLBACKS:
        for attempt in range(3):
            try:
                return _client.models.generate_content(
                    model=model, contents=prompt, config=config).text.strip()
            except Exception as e:
                last_error = e
                code = getattr(e, "code", None)
                if code in (429, 500, 503, 504):   # busy: wait, then retry
                    time.sleep(2 ** attempt)        # 1s, 2s, 4s
                    continue
                break                               # 404 etc: try the next model
    raise RuntimeError(f"Gemini is busy right now. Please try again in a minute. ({last_error})")