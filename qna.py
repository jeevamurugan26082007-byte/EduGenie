from gemini_client import ask


def answer_question_with_gemini(question: str) -> str:
    return ask(f"Answer this student's question clearly and concisely:\n\n{question}")
