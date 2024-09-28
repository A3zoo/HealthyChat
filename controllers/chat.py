from uuid import UUID
from aiohttp import payload
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional, Annotated
from datetime import datetime, timezone
from models.chat import (
    ChatModel,
    CreateChatModel,
    CreateChatResponseModel,
)
from repository.chat import create_chat, get_chat

router = APIRouter()


@router.post(
    "/chats",
    status_code=200,
    tags=["Chat"],
    description="Create a new chat",
)
def _create_chat(
    payload: CreateChatModel,
):
    return create_chat(payload)


@router.get(
    "/chats/get/{chat_id}",
    status_code=200,
    tags=["Chat"],
    description="Get a chat",
)
def _get_chat(chat_id: UUID) -> ChatModel | None:
    return get_chat(chat_id)
