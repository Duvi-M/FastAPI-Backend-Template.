from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.api.deps import require_role
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter()


@router.get("/", response_model=list[UserOut], dependencies=[Depends(require_role("admin"))])
async def list_users(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User))
    return q.scalars().all()


@router.post("/", response_model=UserOut, dependencies=[Depends(require_role("admin"))])
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    # valida duplicados
    q = await db.execute(select(User).where(User.email == payload.email))
    if q.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user