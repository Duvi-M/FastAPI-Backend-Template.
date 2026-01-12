from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.repositories.users import UsersRepository
from app.schemas.auth import TokenResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.users = UsersRepository(db)

    async def login(self, *, email: str, password: str) -> TokenResponse:
        user = await self.users.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Bad credentials")

        return TokenResponse(
            access_token=create_access_token(user.email),
            refresh_token=create_refresh_token(user.email),
        )