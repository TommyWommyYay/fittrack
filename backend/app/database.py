import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Falls back to a local SQLite file when DATABASE_URL is not set (local dev).
# In production (Render), DATABASE_URL points at the managed Postgres instance.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./fittrack.db")

# Render's Postgres connection strings use the legacy "postgres://" scheme,
# which SQLAlchemy 1.4+ no longer recognizes — normalize it.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite requires this flag for use with FastAPI's threaded request handling;
# Postgres does not need or accept it.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency that provides a database session per request and closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
