from abc import ABC
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from .event_types import EventType


class BaseEvent(BaseModel, ABC):
    """Base class cho tất cả events"""
    
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True


class MessageCreatedEvent(BaseEvent):
    """Event được publish khi có tin nhắn mới được tạo"""
    
    event_type: EventType = EventType.MESSAGE_CREATED
    chat_id: UUID
    user_id: Optional[UUID]
    message_id: UUID
    content: str
    is_bot_message: bool = False


class ChatCreatedEvent(BaseEvent):
    """Event được publish khi có chat mới được tạo"""
    
    event_type: EventType = EventType.CHAT_CREATED
    chat_id: UUID
    user_id: UUID
    chat_name: str


class HeartPredictionCompletedEvent(BaseEvent):
    """Event được publish khi hoàn thành dự đoán bệnh tim"""
    
    event_type: EventType = EventType.HEART_PREDICTION_COMPLETED
    chat_id: UUID
    user_id: UUID
    prediction_result: Dict[str, Any]
    risk_level: str  # "low", "medium", "high"


class MedicineRecommendedEvent(BaseEvent):
    """Event được publish khi có gợi ý thuốc"""
    
    event_type: EventType = EventType.MEDICINE_RECOMMENDED
    chat_id: UUID
    user_id: UUID
    medicine_suggestions: list[Dict[str, Any]]
    price_range: Optional[str] = None

