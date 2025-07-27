import re

def refine_text(text):
    if not text:
        return ""

    text = re.sub(r'\s+', ' ', text).strip()

    # Prefer 2 sentence extract
    sentences = re.split(r'(?<=[.!?]) +', text)
    if len(sentences) >= 2:
        return " ".join(sentences[:2]).strip()

    # Fallback to first 2–3 lines
    lines = text.split("\n")
    return "\n".join(lines[:3]).strip()
