from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    input_data: str
    agent_id: str | None = None
    priority: str = "medium"

class TaskCreate(TaskBase):
    project_id: str

class TaskResponse(TaskBase):
    id: str
    project_id: str
    status: str
    created_by: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class TaskRunResponse(BaseModel):
    id: str
    task_id: str
    attempt: int
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None

    class Config:
        from_attributes = True