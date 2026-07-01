import logging
from typing import Any, Dict

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class APIResponse:
    """Standardized API response formatter"""

    def __init__(self, data: Dict[str, Any], status: bool, message: str):
        self.data = data
        self.status = status
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        """Convert response object to dictionary"""
        return {"data": self.data, "status": self.status, "message": self.message}

    @classmethod
    def success(cls, data: Dict[str, Any], message: str):
        logger.info(f"Success Response: {message}")
        logger.debug(f"Response Data: {data}")
        return cls(data=data, status=True, message=message)

    @classmethod
    def error(cls, message: str):
        logger.error(f"Error Response: {message}")
        return cls(data={}, status=False, message=message)
