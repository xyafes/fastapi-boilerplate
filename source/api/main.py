from typing import Annotated, AsyncGenerator, List, Optional
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import RegisterTortoise

from source.models import User, UserMessage
from source.api.schemas import UserCreate, UserResponse, MessageCreate, MessageResponse, UserWithMessages
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
    "http://localhost:8000",  # This is can be only frontend URL
    # "*",  Allow all origins, Everyone can access
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
    logging.info("%s %s %s", request.method, request.url, request.client.host)
    return await call_next(request)


@app.get("/healthcheck")
async def healthcheck():
    """Health check endpoint."""
    return JSONResponse(content={"status": "ok"}, status_code=200)


@app.post("/create_user", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate) -> UserResponse:
    """Create a new user."""
    return await User.create(**user.model_dump())

@app.get("/get_user", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    """Get a user by ID."""
    return await User.get(user_id=user_id)

@app.get("/get_user_messages", response_model=UserWithMessages)
async def get_user_messages(user_id: int) -> UserWithMessages:
    """Get all messages for a user."""
    user = await User.get(user_id=user_id).prefetch_related("messages")
    return user

@app.post("/create_message", response_model=MessageResponse, status_code=201)
async def create_message(message: MessageCreate) -> MessageResponse:
    """Create a new message for a user."""
    user = await User.get(user_id=message.user_id)
    return await UserMessage.create(user=user, message=message.message)

@app.get("/get_all_users", response_model=List[UserResponse])
async def get_all_users() -> List[UserResponse]:
    """Get all users."""
    return await User.all()

@app.get("/get_all_messages", response_model=List[MessageResponse])
async def get_all_messages() -> List[MessageResponse]:
    """Get all messages."""
    return await UserMessage.all()

@app.delete("/delete_user", status_code=204)
async def delete_user(user_id: int):
    """Delete a user by ID."""
    user = await User.get(user_id=user_id)
    await user.delete()

@app.delete("/delete_message", status_code=204)
async def delete_message(message_id: int):
    """Delete a message by ID."""
    message = await UserMessage.get(id=message_id)
    await message.delete()