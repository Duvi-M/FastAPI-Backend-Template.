from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories.tasks import TasksRepository


class TasksService:
    def __init__(self, db: AsyncSession):
        self.tasks = TasksRepository(db)

    async def create_task(self, *, title: str, owner_id: int) -> Task:
        return await self.tasks.create(title=title, owner_id=owner_id)

    async def list_my_tasks(self, *, owner_id: int) -> list[Task]:
        return await self.tasks.list_by_owner(owner_id)

    async def delete_my_task(self, *, task_id: int, owner_id: int) -> None:
        task = await self.tasks.get_by_id(task_id)
        if not task or task.owner_id != owner_id:
            raise HTTPException(status_code=404, detail="Task not found")
        await self.tasks.delete(task)