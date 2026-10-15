import pytest 
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker 
from sqlalchemy.pool import NullPool
import os 
from dotenv import load_dotenv 


load_dotenv(".env.test")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is missing")

os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.database import Base, get_db 
from app.main import app


# Create Async test engine
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(
    expire_on_commit=False,
    autoflush=False,
    bind=test_engine
)


# Fixture to prepare fresh DB for tests
@pytest.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


# Yields a DB session to our test
@pytest.fixture 
async def db_session():
    async with TestingSessionLocal() as session:
        yield session 
    

# Yields a fake web browser (AsyncClient) that points to our test database 
@pytest.fixture
async def client(db_session):
    # override fastapi's db dependency to use our test session
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db 

    # Create async test client
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    # Clean up after test finishes 
    app.dependency_overrides.clear()
