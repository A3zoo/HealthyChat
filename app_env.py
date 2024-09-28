import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(".env")

class AppEnv(BaseModel):
    TOGETHER_API_KEY: str
    APP_ENV: bool
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DEBUG: bool

env = AppEnv.model_validate(os.environ)