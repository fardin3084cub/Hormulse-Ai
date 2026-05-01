"""
app/database.py — Async SQLAlchemy + SQLite/Postgres
"""
 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings
 
settings = get_settings()
 
engine = create_async_engine(
    settings.database_url,
    echo=settings.env == "development",
    # SQLite specific
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)
 
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
 
 
class Base(DeclarativeBase):
    pass
 
 
async def init_db():
    """Create all tables on startup."""
    # Import all models so Base knows about them
    from app.models import user, log, chat_message, plan  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
 
 
async def get_db():
    """Dependency: yields an async DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
