from fastapi import FastAPI
from app_env import env
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(env.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

##app.include_router(account.router, prefix="/api")