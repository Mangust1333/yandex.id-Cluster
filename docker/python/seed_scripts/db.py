from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from sqlalchemy import text

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = (os.getenv("POSTGRES_HOST"))
DB_PORT = int(os.getenv("POSTGRES_PORT"))
DB_NAME = os.getenv("TARGET_DB")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

def get_current_migration_version():
    result = session.execute(text("SELECT version FROM flyway_schema_history ORDER BY installed_rank DESC LIMIT 1"))
    row = result.fetchone()
    return row[0] if row else None