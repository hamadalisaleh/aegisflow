from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.task import Task, TaskRun
from app.schemas.task import TaskCreate, TaskResponse, TaskRunResponse
from app.api.auth import get_current_user
from app.models.user import User
from datetime import datetime

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_task = Task(
        title=task_in.title,
        input_data=task_in.input_data,
        project_id=task_in.project_id,
        agent_id=task_in.agent_id,
        priority=task_in.priority,
        created_by=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Task).filter(Task.created_by == current_user.id).all()

@router.post("/{id}/run", response_model=TaskRunResponse)
def trigger_task_run(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == id, Task.created_by == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_run = TaskRun(
        task_id=task.id,
        status="running",
        started_at=datetime.utcnow()
    )
    task.status = "running"
    db.add(new_run)
    db.commit()
    db.refresh(new_run)
    return new_run