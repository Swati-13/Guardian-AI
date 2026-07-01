import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from response_handler import APIResponse
from routes import router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GuardianAI Content Moderation API",
    description="Analyze text for toxic and abusive language using Groq API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(router)


# Global exception handler for HTTP exceptions (404, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions (404, 405, etc.)
    Returns standardized error response
    """
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    logger.error(f"Path: {request.url.path}")

    # Create error message based on status code
    if exc.status_code == 404:
        message = f"Endpoint not found: {request.url.path}"
    elif exc.status_code == 405:
        message = f"Method not allowed: {request.method} on {request.url.path}"
    else:
        message = exc.detail or "HTTP error occurred"

    response = APIResponse.error(message)
    return JSONResponse(status_code=exc.status_code, content=response.to_dict())


# Global exception handler for validation errors (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Handle request validation errors (422) and return friendly messages.
    """
    errors = exc.errors()

    # Default message
    message = "Request validation failed"

    if errors:
        first_error = errors[0]
        loc = first_error.get("loc", [])
        error_type = first_error.get("type", "")
        error_msg = first_error.get("msg", "")

        # Case 1: Missing required field
        if error_type == "value_error.missing":
            field_name = loc[-1] if loc else "field"
            message = f"'{field_name}' field is required"

        # Case 2: JSON decode error (empty body, invalid JSON)
        elif error_type == "json_invalid":
            message = "Request body must be a valid JSON with required fields, Text field is required."

        # Fallback: any other validation error
        else:
            field = " -> ".join(str(l) for l in loc)
            message = f"Validation error in '{field}': {error_msg}"

    response = APIResponse.error(message).to_dict()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=response
    )


# Global exception handler for all other exceptions (500)
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all other unexpected exceptions (500)
    Returns standardized error response
    """
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    logger.error(f"Path: {request.url.path}")

    response = APIResponse.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response.to_dict()
    )


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Content Moderation API server...")
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")
