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
from events.event_bus import event_bus
from events.event_models import MessageCreatedEvent
from events.event_types import EventType


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
        session.refresh(user_message)
        
        message_model = MessageModel.model_validate(user_message)
        
        # Publish event - Event-Driven Architecture
        event = MessageCreatedEvent(
            chat_id=payload.chat_id,
            user_id=payload.user_id,
            message_id=message_model.id,
            content=payload.content,
            is_bot_message=(payload.user_id is None),
        )
        event_bus.publish(event)
        
        return message_model
