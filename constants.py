"""
Constants for Groq API integration
Contains moderation prompt and response messages
"""

# Response Messages
MESSAGE_CONTENT_BLOCKED = "Content contains toxic language and should be blocked."
MESSAGE_CONTENT_SAFE = "Content is safe."
MESSAGE_API_ERROR = "Failed to analyze text. Please try again later."
MESSAGE_INVALID_INPUT = "Invalid input. Text is required."
MESSAGE_EMPTY_TEXT = "Text cannot be empty."

GROQ_MODERATION_PROMPT = """Content moderation classifier. Return ONLY valid JSON:

{
  "should_block": <true|false>,
  "scores": {
    "TOXICITY": <0-1>,
    "INSULT": <0-1>,
    "PROFANITY": <0-1>,
    "IDENTITY_ATTACK": <0-1>,
    "THREAT": <0-1>
  },
  "flagged_words": ["word1", "word2"],
}

BLOCK: Direct personal attacks, severe insults, aggressive profanity, real threats, hate speech (race/religion/gender/nationality/disability/orientation), dehumanizing language.

ALLOW: Technical content (code/SQL/scripts), criticism/complaints, negative opinions, frustration, educational content, sarcasm, debates, disagreements.

Analyze INTENT not keywords. Score 0.7+ blocks. Prefer allowing borderline cases. JSON only."""
