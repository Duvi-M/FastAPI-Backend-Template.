from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.repositories.users import UsersRepository
from app.models.user import User


class UsersService:
    def __init__(self, db: AsyncSession):
        self.users = UsersRepository(db)

    async def list_users(self) -> list[User]:
        return await self.users.list_all()

    async def create_user(self, *, email: str, password: str, role: str) -> User:
        exists = await self.users.get_by_email(email)
        if exists:
            raise HTTPException(status_code=409, detail="Email already exists")

        return await self.users.create(
            email=email,
            hashed_password=hash_password(password),
            role=role,
        )