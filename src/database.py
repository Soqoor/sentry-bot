from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

# For mysql: mysql://<username>:<password>@<host>:<port>/<db>

engine = create_async_engine(settings.ASYNC_DATABASE_URL)

LocalSession = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# Dependency
async def get_db() -> AsyncSession:
    async with LocalSession() as session:
        yield session
