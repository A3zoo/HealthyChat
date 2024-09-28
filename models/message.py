import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional
from sqlalchemy.types import TypeDecorator, BigInteger
from base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, DateTime, Text, Enum as saEnum, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime, timezone

class Message(Base):
    __tablename__: str = 'message'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    chat_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    is_chatbot: Mapped[bool] = mapped_column(Boolean)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=(lambda: datetime.now(tz=timezone.utc))
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=(lambda: datetime.now(tz=timezone.utc)),
        onupdate=(lambda: datetime.now(tz=timezone.utc)),
    )


class CreateMessageModel(BaseModel):
    chat_id: uuid.UUID
    user_id: Optional[uuid.UUID]
    content: str

class MessageModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    chat_id: uuid.UUID
    user_id: Optional[uuid.UUID]
    content: str
    created_at: datetime
    updated_at: datetime
