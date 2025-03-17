from typing import Annotated, AsyncGenerator, Optional
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import RegisterTortoise

from source.models import User, UserMessage
from source.settings import tortoise_orm, debug, fastapi_logger as logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with RegisterTortoise(
        app=app,
        config=tortoise_orm,
        generate_schemas=True,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(
    title="Example API",
    lifespan=lifespan,
    debug=debug,
    summary="Example API for retrieving messages.",
)

origins = [
    # "http://localhost:8000", This is can be only frontend URL
    "*",  # Allow all origins, Everyone can access
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def check_token(request: Request, call_next):
    """Check the token in the Authorization header and log them."""
    logging.info(f"{request.client.host} {request.method} {request.url}")
    logging.info("%s %s %s", request.method, request.url, request.headers)
    return await call_next(request)
