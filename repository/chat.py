from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from database import Session

from models.chat import (
    CreateChatModel,
    Chat,
    ChatModel,
)
from events.event_bus import event_bus
from events.event_models import ChatCreatedEvent

def create_chat(payload: CreateChatModel) -> ChatModel:
    with Session() as session:
        chat = Chat(
            name = payload.name,user_id=payload.user_id
        )
        session.add(chat)
        session.commit()
        session.refresh(chat)

        chat_model = ChatModel.model_validate(chat)
        
        # Publish event - Event-Driven Architecture
        event = ChatCreatedEvent(
            chat_id=chat_model.id,
            user_id=payload.user_id,
            chat_name=payload.name,
        )
        event_bus.publish(event)
        
        return chat_model


def get_chat(chat_id: UUID) -> Optional[ChatModel]:
    with Session() as session:
        stmt = select(Chat).where(
            Chat.id == chat_id,
        )
        chat = session.scalars(stmt).one_or_none()

        if chat is None:
            raise HTTPException(status_code=404, detail="Chat not found")

        return ChatModel.model_validate(chat)
    