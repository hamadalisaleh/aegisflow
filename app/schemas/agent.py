from pydantic import BaseModel
from datetime import datetime

class AgentBase(BaseModel):
    name: str
    description: str | None = None
    system_prompt: str
    model_provider: str = "gemini"
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.7
    status: str = "active"

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    system_prompt: str | None = None
    model_provider: str | None = None
    model_name: str | None = None
    temperature: float | None = None
    status: str | None = None

class AgentResponse(AgentBase):
    id: str
    project_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True