from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
import logging

logger = logging.getLogger(__name__)

config = dotenv_values(".env")

DB_ENGINE_LOG = config["DB_ENGINE_LOG"] == "1"
PG_USER = config["PG_USER"]
PG_PASS = config["PG_PASS"]
PG_SERVER = config["PG_SERVER"]
PG_PORT = config["PG_PORT"]
PG_DB = config["PG_DB"]

# PostgreSQL async
PG_ASYNC_SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_SERVER}:{PG_PORT}/{PG_DB}"
)

pg_async_engine = create_async_engine(
    PG_ASYNC_SQLALCHEMY_DATABASE_URL, echo=DB_ENGINE_LOG, pool_size=40, max_overflow=0
)
pg_async_session = sessionmaker(
    pg_async_engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()
