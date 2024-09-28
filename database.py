from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from app_env import AppEnv
from app_env import env

db = engine.create_engine(
    f"postgresql://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}",
    echo=(env.APP_ENV),
    pool_pre_ping=True,
)

vectordb_conn_str = f"postgresql+psycopg://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"

Session = sessionmaker(db)