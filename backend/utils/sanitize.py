import re
import unicodedata


def sanitize_text(text: str) -> str:
    """Normalize AI text for reliable plain-text/document export."""
    text = unicodedata.normalize("NFKC", text)
    replacements = {
        "“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-",
        "•": "-", "…": "...", "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def split_terms(terms: str) -> list[str]:
    return [part.strip(" -\t") for part in terms.split(";") if part.strip()]
