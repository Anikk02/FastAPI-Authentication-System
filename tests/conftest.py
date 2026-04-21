import os
import sys
import asyncio
import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base, get_db
from app.main import app

# ✅ Async test DB
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test_auth.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ✅ Override dependency
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

# ✅ Create & drop tables async
@pytest.fixture(scope="function")
async def client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)