from typing import Callable, Dict, List, Optional
from collections import defaultdict
import logging
from .event_models import BaseEvent

logger = logging.getLogger(__name__)


class EventBus:
    """
    Simple Event Bus implementation cho Event-Driven Architecture.
    Hỗ trợ publish/subscribe pattern.
    """
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._event_history: List[BaseEvent] = []
        self._max_history = 100  # Giữ lại 100 events gần nhất
    
    def subscribe(self, event_type: str, handler: Callable[[BaseEvent], None]) -> None:
        """
        Đăng ký handler cho một loại event
        
        Args:
            event_type: Loại event (ví dụ: "message.created")
            handler: Function sẽ được gọi khi event được publish
        """
        self._subscribers[event_type].append(handler)
        logger.info(f"Subscribed handler for event type: {event_type}")
    
    def unsubscribe(self, event_type: str, handler: Callable[[BaseEvent], None]) -> None:
        """Hủy đăng ký handler"""
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
            logger.info(f"Unsubscribed handler for event type: {event_type}")
    
    def publish(self, event: BaseEvent) -> None:
        """
        Publish một event - tất cả handlers đăng ký sẽ được gọi
        
        Args:
            event: Event object cần publish
        """
        event_type = event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type)
        
        # Lưu vào history
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
        
        logger.info(f"Publishing event: {event_type} (ID: {event.event_id})")
        
        # Gọi tất cả handlers đã đăng ký
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler for {event_type}: {e}", exc_info=True)
        
        # Cũng gọi handlers đăng ký cho "*" (tất cả events)
        all_handlers = self._subscribers.get("*", [])
        for handler in all_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in wildcard event handler: {e}", exc_info=True)
    
    def get_event_history(self, event_type: Optional[str] = None, limit: int = 10) -> List[BaseEvent]:
        """
        Lấy lịch sử events
        
        Args:
            event_type: Lọc theo loại event (None = tất cả)
            limit: Số lượng events trả về
        """
        history = self._event_history
        if event_type:
            history = [e for e in history if str(e.event_type) == event_type]
        
        return history[-limit:]
    
    def clear_history(self) -> None:
        """Xóa lịch sử events"""
        self._event_history.clear()


# Global event bus instance
event_bus = EventBus()

