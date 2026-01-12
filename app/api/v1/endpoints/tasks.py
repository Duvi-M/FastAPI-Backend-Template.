from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut
from app.services.tasks import TasksService

router = APIRouter()


@router.post("/", response_model=TaskOut)
async def create_task(
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await TasksService(db).create_task(title=payload.title, owner_id=user.id)


@router.get("/", response_model=list[TaskOut])
async def my_tasks(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await TasksService(db).list_my_tasks(owner_id=user.id)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await TasksService(db).delete_my_task(task_id=task_id, owner_id=user.id)
    return {"ok": True}