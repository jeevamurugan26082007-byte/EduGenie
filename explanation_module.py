"""Concept explanations.

Default: Gemini (works on any host, no GPU/RAM needed).
Local mode: set USE_LOCAL_MODEL=1 to run LaMini-Flan-T5-783M on your own machine
(needs `pip install transformers torch`, ~3 GB download, not suited to free cloud hosts).
"""
import os
from gemini_client import ask

_tok = _model = None


def _local_explain(topic: str) -> str:
    global _tok, _model
    if _model is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        name = "MBZUAI/LaMini-Flan-T5-783M"
        _tok = AutoTokenizer.from_pretrained(name)
        _model = AutoModelForSeq2SeqLM.from_pretrained(name)
    inputs = _tok(f"Explain the concept of '{topic}' in a simple and clear way for a school student.",
                  return_tensors="pt")
    out = _model.generate(**inputs, max_new_tokens=150, temperature=0.7,
                          top_k=50, top_p=0.95, do_sample=True)
    return _tok.decode(out[0], skip_special_tokens=True)


def explain_topic(topic: str) -> str:
    if os.getenv("USE_LOCAL_MODEL") == "1":
        return _local_explain(topic)
    return ask(f"Explain the concept of '{topic}' in a simple and clear way for a school student. "
               "Keep it under 150 words.")
