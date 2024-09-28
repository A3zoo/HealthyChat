from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import select
from database import Session
from models.message import (
    Message,
    MessageModel,
    CreateMessageModel
)

from models.chat import Chat


def get_messages(chat_id: UUID, limit: int) -> list[MessageModel]:
    with Session() as session:
        stmt = (
            select(Message)
            .where(
                Message.chat_id == chat_id,
            )
            .order_by(Message.created_at.desc())
            .limit(limit)
        )

        message_seq = session.scalars(stmt).all()
        return [MessageModel.model_validate(message) for message in message_seq]


def list_messages(
    chat_id: UUID, limit: int, created_at: datetime
):
    with Session() as session:
        chat_stmt = select(Chat).where(Chat.id == chat_id)
        chat = session.scalars(chat_stmt).one_or_none()
        if chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")

        stmt = (
            select(Message)
            .where(
                Message.chat_id == chat_id,
            )
            .order_by(Message.created_at.desc())
            .limit(limit)
            .filter(Message.created_at < created_at)
        )
        messages = session.scalars(stmt).all()

        list_chat_messages = [MessageModel.model_validate(message) for message in messages]
        return list_chat_messages


def create_message(payload: CreateMessageModel) -> Optional[MessageModel]:
    with Session() as session:
        user_message = Message(**payload.model_dump())
        session.add(user_message)
        session.commit()
        return MessageModel.model_validate(user_message)
