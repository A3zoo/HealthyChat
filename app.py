from fastapi import FastAPI
from app_env import env
from fastapi.middleware.cors import CORSMiddleware
from controllers import chat, chat_message, user, notifications
from events.event_bus import event_bus
from events.event_handlers import register_handlers

app = FastAPI(debug=env.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register event handlers - Event-Driven Architecture
register_handlers(event_bus)

# Include routers
app.include_router(chat.router, prefix="/api")
app.include_router(chat_message.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")