from uuid import UUID
from fastapi import APIRouter, Query, Body, HTTPException, Header
from typing import List, Optional
from datetime import datetime, timezone
from fastapi.security import HTTPBasic
from typing import Annotated
from models.message import MessageModel, CreateMessageModel
from services.chat_with_AI import chat as create_chat_message_with_chatbot
from repository.message import list_messages

router = APIRouter()
security = HTTPBasic()

@router.post(
    "/message/create",
    tags=["Messages"],
    response_model=MessageModel,
)
async def create_chat_message(
    body: Annotated[
        CreateMessageModel,
        Body(
            examples=[
                {
                    "chat_id": "",
                    "user_id": "",
                    "content": "string"
                }
            ],
        ),
    ],
):
    return create_chat_message_with_chatbot(body)

@router.get(
    "/messages/list/{chat_id}", tags=["Messages"]
)
async def list_chat_messages(
    chat_id: UUID,
    user_id: UUID = Header(...),
    limit: int = Query(20, ge=1),
    cursor: Optional[str] = Query(None),
):
    created_at = datetime.now(tz=timezone.utc)
    if cursor:
        created_at = dateutil.parser.isoparse(cursor)
    res = list_messages(chat_id, user_id, limit, created_at)
    if res is None:
        raise HTTPException(status_code=404, detail="Messages not found")
    return res