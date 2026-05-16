from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(DATABASE_URL, echo=settings.environment == "development")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def create_tables():
    try:
        async with engine.begin() as conn:
            from app.models.schemas import Analysis
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified.")
    except Exception as e:
        logger.warning(f"DB init warning (running without DB): {e}")


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
