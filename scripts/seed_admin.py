import asyncio
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.security import hash_password
from app.models.user import User

DATABASE_URL = os.environ.get("DATABASE_URL")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123456")


async def main() -> None:
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is missing in env")

    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async with SessionLocal() as db:
        q = await db.execute(select(User).where(User.email == ADMIN_EMAIL))
        exists = q.scalar_one_or_none()

        if exists:
            print(f"Admin already exists: {ADMIN_EMAIL}")
            return

        user = User(
            email=ADMIN_EMAIL,
            hashed_password=hash_password(ADMIN_PASSWORD),
            role="admin",
            is_active=True,
        )
        db.add(user)
        await db.commit()
        print(f"Admin created: {ADMIN_EMAIL}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())