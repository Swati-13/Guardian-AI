import re

import emoji


def clean_text(text: str) -> str:
    """
    Cleans the input text before sending to the Groq API.

    Steps:
    1. Strip leading/trailing spaces
    2. Remove emojis and symbols
    3. Remove URLs, special chars, and extra spaces
    4. Convert to lowercase
    """
    if not text or not isinstance(text, str):
        return ""

    # Remove emojis
    text = emoji.replace_emoji(text, replace="")

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Remove non-alphanumeric characters except spaces and basic punctuation
    text = re.sub(r"[^a-zA-Z0-9\s.,!?']", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Strip and lowercase
    text = text.strip().lower()

    return text
