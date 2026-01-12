from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.api.deps import require_role
from app.core.security import hash_password
from app.models.user import User

router = APIRouter()

@router.get("/", dependencies=[Depends(require_role("admin"))])
async def list_users(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User))
    return q.scalars().all()

@router.post("/", dependencies=[Depends(require_role("admin"))])
async def create_user(payload: dict, db: AsyncSession = Depends(get_db)):
    # payload: {"email": "...", "password": "...", "role": "user"}
    user = User(
        email=payload["email"],
        hashed_password=hash_password(payload["password"]),
        role=payload.get("role", "user"),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user