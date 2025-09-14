import os
import asyncio
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = (os.getenv("POSTGRES_HOST"))
DB_PORT = int(os.getenv("POSTGRES_PORT"))
DB_NAME = os.getenv("TARGET_DB")


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db_pool: asyncpg.pool.Pool | None = None

async def init_db_pool():
    """
    Функция вызывается при старте приложения, создаёт пул asyncpg.
    """
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            dsn=DATABASE_URL,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        print(db_pool)

async def close_db_pool():
    """
    Закрытие пула при остановке приложения.
    """
    global db_pool
    if db_pool:
        await db_pool.close()
        db_pool = None
