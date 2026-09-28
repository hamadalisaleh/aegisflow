from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse

router = APIRouter(tags=["Agents"])

@router.post("/projects/{project_id}/agents", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(project_id: str, agent_in: AgentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    agent = Agent(
        **agent_in.model_dump(),
        project_id=project_id
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.get("/projects/{project_id}/agents", response_model=List[AgentResponse])
def get_project_agents(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db.query(Agent).filter(Agent.project_id == project_id).all()

@router.get("/agents/{id}", response_model=AgentResponse)
def get_agent(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(Agent).join(Project).filter(Agent.id == id, Project.owner_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.patch("/agents/{id}", response_model=AgentResponse)
def update_agent(id: str, agent_in: AgentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(Agent).join(Project).filter(Agent.id == id, Project.owner_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    update_data = agent_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
        
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/agents/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(Agent).join(Project).filter(Agent.id == id, Project.owner_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return None