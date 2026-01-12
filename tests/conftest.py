import os
import pytest
import httpx

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def _set_env() -> None:
    os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
    os.environ.setdefault("ENV", "test")
    os.environ.setdefault("DEBUG", "false")


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac