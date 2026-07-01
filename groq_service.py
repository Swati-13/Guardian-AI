import json
import logging
import os
from typing import Dict, Optional

from dotenv import load_dotenv
from groq import Groq

from constants import GROQ_MODERATION_PROMPT

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

_groq_client: Optional[Groq] = None


def _get_groq_client() -> Groq:
    global _groq_client

    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            logger.error("GROQ_API_KEY not found in environment")
            raise ValueError(
                "API key not configured. Please set GROQ_API_KEY in .env file"
            )

        _groq_client = Groq(api_key=api_key)
        logger.info("Groq client initialized successfully")

    return _groq_client


async def moderate_content(text: str) -> Dict:
    try:
        client = _get_groq_client()

        logger.info("Calling Groq API...")
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": GROQ_MODERATION_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
            max_tokens=500,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
        )

        response_text = completion.choices[0].message.content
        logger.debug(f"Raw API response: {response_text}")

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            raise ValueError(f"Invalid JSON response from Groq API: {str(e)}")

        result = {
            "should_block": data.get("should_block", False),
            "scores": data.get("scores", {}),
            "flagged_words": data.get("flagged_words", []),
        }

        return result

    except ValueError:
        raise

    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"Groq API error: {str(e)}", exc_info=True)

        if "api_key" in error_msg or "unauthorized" in error_msg or "401" in error_msg:
            raise ValueError("Invalid Groq API key or authentication failed")
        elif "timeout" in error_msg:
            raise TimeoutError("Groq API request timed out. Please try again.")
        elif "connection" in error_msg or "network" in error_msg:
            raise ConnectionError(
                "Cannot connect to Groq API. Please check your internet connection."
            )
        else:
            raise Exception(f"Groq API error: {str(e)}")
