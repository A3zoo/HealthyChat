from uuid import UUID
from fastapi import APIRouter, Header, HTTPException
from typing import List, Dict, Any
from events.event_handlers import notifications_store

router = APIRouter()


@router.get("/notifications", tags=["Notifications"])
async def get_notifications(
    user_id: UUID = Header(..., description="User ID"),
    limit: int = 10,
) -> Dict[str, Any]:
    """
    Lấy danh sách notifications cho user (Event-Driven Architecture Demo)
    
    Notifications được tạo tự động thông qua event handlers khi:
    - Có tin nhắn mới từ bot
    - Tạo chat mới
    - Hoàn thành dự đoán bệnh tim
    """
    user_id_str = str(user_id)
    notifications = notifications_store.get(user_id_str, [])
    
    # Trả về notifications mới nhất
    return {
        "user_id": user_id_str,
        "notifications": notifications[-limit:],
        "total": len(notifications),
    }


@router.delete("/notifications", tags=["Notifications"])
async def clear_notifications(
    user_id: UUID = Header(..., description="User ID"),
) -> Dict[str, str]:
    """Xóa tất cả notifications của user"""
    user_id_str = str(user_id)
    if user_id_str in notifications_store:
        notifications_store[user_id_str] = []
    
    return {"message": "Notifications cleared"}


@router.get("/notifications/unread-count", tags=["Notifications"])
async def get_unread_count(
    user_id: UUID = Header(..., description="User ID"),
) -> Dict[str, int]:
    """Lấy số lượng notifications chưa đọc"""
    user_id_str = str(user_id)
    notifications = notifications_store.get(user_id_str, [])
    
    return {
        "user_id": user_id_str,
        "unread_count": len(notifications),
    }

