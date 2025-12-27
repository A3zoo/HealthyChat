"""
Event Handlers - Xử lý các events trong hệ thống
"""
import logging
from typing import Dict, Any
from .event_models import (
    BaseEvent,
    MessageCreatedEvent,
    ChatCreatedEvent,
    HeartPredictionCompletedEvent,
)
from .event_types import EventType

logger = logging.getLogger(__name__)


# In-memory store cho notifications (trong production nên dùng Redis hoặc database)
notifications_store: Dict[str, list] = {}


def message_created_handler(event: MessageCreatedEvent) -> None:
    """
    Handler cho event message.created
    Tạo notification và lưu vào store
    """
    logger.info(f"Handling message.created event for chat {event.chat_id}")
    
    notification = {
        "type": "message",
        "chat_id": str(event.chat_id),
        "message_id": str(event.message_id),
        "content": event.content[:100] + "..." if len(event.content) > 100 else event.content,
        "is_bot_message": event.is_bot_message,
        "timestamp": event.timestamp.isoformat(),
    }
    
    # Lưu notification cho user (nếu là bot message)
    if event.is_bot_message and event.user_id:
        user_id = str(event.user_id)
        if user_id not in notifications_store:
            notifications_store[user_id] = []
        notifications_store[user_id].append(notification)
        
        # Giữ lại tối đa 50 notifications
        if len(notifications_store[user_id]) > 50:
            notifications_store[user_id] = notifications_store[user_id][-50:]
    
    logger.info(f"Notification created for user {event.user_id}")


def chat_created_handler(event: ChatCreatedEvent) -> None:
    """
    Handler cho event chat.created
    Log analytics và tạo welcome notification
    """
    logger.info(f"Handling chat.created event for chat {event.chat_id}")
    
    # Analytics logging (có thể gửi đến analytics service)
    logger.info(f"New chat created: {event.chat_name} by user {event.user_id}")
    
    # Tạo welcome notification
    notification = {
        "type": "chat_created",
        "chat_id": str(event.chat_id),
        "message": f"Chào mừng đến với cuộc trò chuyện: {event.chat_name}",
        "timestamp": event.timestamp.isoformat(),
    }
    
    user_id = str(event.user_id)
    if user_id not in notifications_store:
        notifications_store[user_id] = []
    notifications_store[user_id].append(notification)


def heart_prediction_handler(event: HeartPredictionCompletedEvent) -> None:
    """
    Handler cho event heart_prediction.completed
    Tạo notification với kết quả dự đoán
    """
    logger.info(f"Handling heart_prediction.completed event for chat {event.chat_id}")
    
    risk_messages = {
        "low": "Nguy cơ thấp. Tuy nhiên, hãy tiếp tục theo dõi sức khỏe.",
        "medium": "Nguy cơ trung bình. Nên tham khảo ý kiến bác sĩ.",
        "high": "Nguy cơ cao. Khuyến nghị gặp bác sĩ sớm nhất có thể.",
    }
    
    notification = {
        "type": "heart_prediction",
        "chat_id": str(event.chat_id),
        "risk_level": event.risk_level,
        "message": risk_messages.get(event.risk_level, "Đã hoàn thành phân tích."),
        "prediction_result": event.prediction_result,
        "timestamp": event.timestamp.isoformat(),
    }
    
    user_id = str(event.user_id)
    if user_id not in notifications_store:
        notifications_store[user_id] = []
    notifications_store[user_id].append(notification)


def register_handlers(event_bus) -> None:
    """Đăng ký tất cả handlers với event bus"""
    from .event_types import EventType
    
    event_bus.subscribe(EventType.MESSAGE_CREATED, message_created_handler)
    event_bus.subscribe(EventType.CHAT_CREATED, chat_created_handler)
    event_bus.subscribe(EventType.HEART_PREDICTION_COMPLETED, heart_prediction_handler)
    
    logger.info("All event handlers registered")

