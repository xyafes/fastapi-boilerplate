from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class UserBase(BaseModel):
    user_id: int = Field(..., description="Unique identifier for the user")
    username: str = Field(..., description="Username of the user", min_length=1, max_length=255)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    created_at: datetime

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    message: str = Field(..., description="Message content", min_length=1)


class MessageCreate(MessageBase):
    user_id: int = Field(..., description="ID of the user who created the message")


class MessageResponse(MessageBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserWithMessages(UserResponse):
    messages: List[MessageResponse]

    class Config:
        from_attributes = True