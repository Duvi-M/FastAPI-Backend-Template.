import os
import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def _set_env() -> None:
    # En CI ya vienen, pero esto ayuda localmente
    os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
    os.environ.setdefault("ENV", "test")
    os.environ.setdefault("DEBUG", "false")


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac