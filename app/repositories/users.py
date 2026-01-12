from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UsersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        q = await self.db.execute(select(User).where(User.email == email))
        return q.scalar_one_or_none()

    async def list_all(self) -> list[User]:
        q = await self.db.execute(select(User))
        return list(q.scalars().all())

    async def create(self, *, email: str, hashed_password: str, role: str = "user") -> User:
        user = User(email=email, hashed_password=hashed_password, role=role)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user