from fastapi import APIRouter, Query, Request
from models.user import CreateUserModel
from repository.user import create_user
from typing import Optional

router = APIRouter()


@router.post("/guest_user/create", tags=["User"])
async def create_guest_user(request: Request):
    return create_user(request)
