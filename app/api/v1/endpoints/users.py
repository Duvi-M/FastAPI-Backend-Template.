from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import require_role
from app.schemas.user import UserCreate, UserOut
from app.services.users import UsersService

router = APIRouter()


@router.get("/", response_model=list[UserOut], dependencies=[Depends(require_role("admin"))])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await UsersService(db).list_users()


@router.post("/", response_model=UserOut, dependencies=[Depends(require_role("admin"))])
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UsersService(db).create_user(
        email=payload.email,
        password=payload.password,
        role=payload.role,
    )