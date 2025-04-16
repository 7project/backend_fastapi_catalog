from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import quote_plus
from config import settings
from sqlalchemy.ext.asyncio import AsyncAttrs


password = quote_plus(settings.DB_PASSWORD)
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{password}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine,
                                       autoflush=False,
                                       autocommit=False,
                                       expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    pass
