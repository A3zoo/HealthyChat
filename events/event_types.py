from enum import Enum


class EventType(str, Enum):
    """Các loại events trong hệ thống"""
    
    MESSAGE_CREATED = "message.created"
    CHAT_CREATED = "chat.created"
    HEART_PREDICTION_COMPLETED = "heart_prediction.completed"
    MEDICINE_RECOMMENDED = "medicine.recommended"
    FAQ_ANSWERED = "faq.answered"

