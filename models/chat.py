from datetime import datetime, timezone
from typing import Optional
from pydantic import ConfigDict, BaseModel
from .base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import UUID, String, DateTime
import uuid

class Chat(Base):
    __tablename__: str = "chats"  # type: ignore
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=(lambda: datetime.now(tz=timezone.utc))
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=(lambda: datetime.now(tz=timezone.utc)),
        onupdate=(lambda: datetime.now(tz=timezone.utc)),
    )

class CreateChatMessageResponseModel(BaseModel):
    id: uuid.UUID
    chat_id: uuid.UUID

class CreateChatModel(BaseModel):
    chat_id: uuid.UUID
    name:str
    user_id: uuid.UUID



class ChatModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class UpdateChatModel(BaseModel):
    id: uuid.UUID
    name: Optional[str] = None
    user_id: Optional[uuid.UUID] = None


class CreateChatResponseModel(BaseModel):
    id: uuid.UUID
    name: str



