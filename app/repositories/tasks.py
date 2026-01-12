from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TasksRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, *, title: str, owner_id: int) -> Task:
        task = Task(title=title, owner_id=owner_id)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def list_by_owner(self, owner_id: int) -> list[Task]:
        q = await self.db.execute(select(Task).where(Task.owner_id == owner_id))
        return list(q.scalars().all())

    async def get_by_id(self, task_id: int) -> Task | None:
        q = await self.db.execute(select(Task).where(Task.id == task_id))
        return q.scalar_one_or_none()

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.commit()