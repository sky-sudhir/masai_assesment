

from sqlalchemy.ext.asyncio import create_async_engine,  AsyncSession
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from api.config import DATABASE_URL_CONFIG

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URL_CONFIG, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
   
    async with AsyncSessionLocal() as session:
        yield session