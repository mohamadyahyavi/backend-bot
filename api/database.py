from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)

# PostgreSQL connection URL
DATABASE_URL = (
    "postgresql+asyncpg://postgres:muhammad99@localhost/shopdb"
)

# Create async SQLAlchemy engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for all models
Base = declarative_base()