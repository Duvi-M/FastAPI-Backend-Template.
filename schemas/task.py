from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class TaskOut(BaseModel):
    id: int
    title: str
    owner_id: int

    model_config = {"from_attributes": True}