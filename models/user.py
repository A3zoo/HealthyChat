from datetime import datetime, timezone
from .base import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import UUID, DateTime, Text, String
import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict

class User(Base):
    __tablename__: str = "users"  # type: ignore

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    ip_address: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    password: Mapped[str] = mapped_column(String(61), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=(lambda: datetime.now(tz=timezone.utc))
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=(lambda: datetime.now(tz=timezone.utc)),
        onupdate=(lambda: datetime.now(tz=timezone.utc)),
    )


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    ip_address: str
    email: Optional[str]
    password: Optional[str]
    created_at: datetime
    updated_at: datetime


class CreateUserModel(BaseModel):
    ip_address: str
    email: Optional[str]
    password: Optional[str]


class UserReponseModel(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    ip_address: str
    created_at: datetime
    updated_at: datetime
