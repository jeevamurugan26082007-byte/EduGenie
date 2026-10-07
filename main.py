from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question_with_gemini
from quiz_module import generate_quiz
from summary_module import summarize_text

app = FastAPI(title="EduGenie")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TopicIn(BaseModel):
    topic: str


class TextIn(BaseModel):
    text: str


@app.exception_handler(Exception)
async def on_error(request: Request, exc: Exception):
    return JSONResponse({"error": f"{type(exc).__name__}: {exc}"}, status_code=500)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/qa")
def qa(question: str = Query(..., min_length=1)):
    return {"answer": answer_question_with_gemini(question)}


@app.post("/explain")
def explain(body: TopicIn):
    return {"topic": body.topic, "explanation": explain_topic(body.topic)}


@app.post("/summarize")
def summarize(body: TextIn):
    return {"summary": summarize_text(body.text)}


@app.post("/quiz")
def quiz(body: TextIn):
    return {"quiz": generate_quiz(body.text)}


@app.get("/learn/recommendations")
def recommendations(topic: str = Query(..., min_length=1)):
    return {"topic": topic, "recommendation": get_learning_recommendations(topic)}
