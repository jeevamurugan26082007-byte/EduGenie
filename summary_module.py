from gemini_client import ask


def summarize_text(text: str) -> str:
    return ask(f"Summarize the following text in simple language:\n\n{text}")
