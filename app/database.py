import os 

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession 
from sqlalchemy.orm import declarative_base 


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# Create AsyncEngine 
engine = create_async_engine(
    url=DATABASE_URL,
    echo=True
)


# Create Async session maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


Base = declarative_base()

# Dependency for getting Async session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

        