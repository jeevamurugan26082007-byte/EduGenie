import json
import re
from gemini_client import ask


def clean_json_block(text: str) -> str:
    """Remove ```json fences if the model adds them."""
    return re.sub(r"```(?:json)?\n(.*?)```", r"\1", text, flags=re.DOTALL).strip()


def generate_quiz(text: str) -> list:
    prompt = f"""You are a quiz generator.
From the following topic or passage, create 3 multiple-choice questions. Each needs:
- "question": the question text
- "options": a list of exactly 4 plausible options
- "answer": the correct answer, which must exactly match one of the options

Return only valid JSON, like:
[{{"question": "What is ...?", "options": ["A", "B", "C", "D"], "answer": "A"}}]

Topic or passage:
{text}"""
    quiz = json.loads(clean_json_block(ask(prompt, json_mode=True)))
    for q in quiz:
        if q["answer"] not in q["options"]:
            raise ValueError("Model returned an answer that is not in the options. Please try again.")
    return quiz
