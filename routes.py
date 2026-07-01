import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from constants import MESSAGE_CONTENT_BLOCKED, MESSAGE_CONTENT_SAFE, MESSAGE_EMPTY_TEXT
from groq_service import moderate_content
from response_handler import APIResponse
from utils import clean_text

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter()


class TextPayload(BaseModel):
    text: str


@router.post("/analyze")
async def analyze_text(payload: TextPayload):
    try:
        logger.info("\n" + "=" * 70)
        logger.info("NEW REQUEST RECEIVED - /analyze endpoint")
        logger.info("=" * 70)

        text = payload.text
        text = clean_text(text)

        if not text:
            logger.warning("Empty text received")
            response = APIResponse.error(MESSAGE_EMPTY_TEXT)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content=response.to_dict()
            )

        logger.info(f"Input text length: {len(text)} characters")
        logger.info(
            f"Input text: '{text[:200]}...'"
            if len(text) > 200
            else f"Input text: '{text}'"
        )

        # groq_service.py
        result = await moderate_content(text)

        message = (
            MESSAGE_CONTENT_BLOCKED if result["should_block"] else MESSAGE_CONTENT_SAFE
        )

        logger.info(f"Should block: {result['should_block']}")
        logger.info(f"Message: {message}")
        logger.info("=" * 70 + "\n")

        response = APIResponse.success(result, message)
        return JSONResponse(status_code=status.HTTP_200_OK, content=response.to_dict())

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        response = APIResponse.error(str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=response.to_dict()
        )

    except TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
        response = APIResponse.error(str(e))
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, content=response.to_dict()
        )

    except ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        response = APIResponse.error(str(e))
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=response.to_dict()
        )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        response = APIResponse.error(f"Internal server error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.to_dict(),
        )
