from fastapi import Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError
from pydantic import ValidationError

from source.settings import fastapi_logger as logging

async def doesnotexist_exception_handler(request: Request, exc: DoesNotExist):
    """Handle DoesNotExist exceptions."""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"},
    )

async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    return JSONResponse(
        status_code=409,
        content={"detail": "Database integrity error. The resource may already exist."},
    )

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logging.error("Unexpected error: %s", str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )