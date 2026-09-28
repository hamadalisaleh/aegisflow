from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.task import Task, TaskRun
from app.schemas.task import TaskCreate, TaskResponse, TaskRunResponse
from app.agents.repo_analyzer import RepositoryAnalyzerAgent

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(
        title=task_in.title,
        input_data=task_in.input_data,
        project_id=task_in.project_id,
        agent_id=task_in.agent_id,
        created_by=current_user.id,
        status="pending",
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("", response_model=List[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = db.query(Task).filter(Task.created_by == current_user.id).all()
    return tasks


@router.get("/{id}", response_model=TaskResponse)
def get_task(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == id, Task.created_by == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/{id}/run", response_model=TaskRunResponse)
def trigger_task_run(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == id, Task.created_by == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # إنشاء سجل تشغيل جديد
    new_run = TaskRun(
        task_id=task.id,
        status="running",
        started_at=datetime.utcnow(),
    )
    db.add(new_run)
    db.commit()

    # تشغيل الوكيل RepositoryAnalyzerAgent لتحليل محتوى المهمة
    try:
        analyzer = RepositoryAnalyzerAgent()
        result = analyzer.analyze(task.input_data)

        new_run.status = "completed"
        new_run.completed_at = datetime.utcnow()
        new_run.error_message = result["summary"]  # حفظ التقرير الناتج
        task.status = "completed"
    except Exception as e:
        new_run.status = "failed"
        new_run.completed_at = datetime.utcnow()
        new_run.error_message = str(e)
        task.status = "failed"

    db.commit()
    db.refresh(new_run)
    return new_run