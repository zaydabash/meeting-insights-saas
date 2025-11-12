from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.models.task import Task, TaskStatus, TaskSource
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.post("", response_model=TaskResponse)
async def create_task(
    request: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    task = Task(
        org_id=current_user.org_id,
        meeting_id=request.meeting_id,
        title=request.title,
        owner_user_id=request.owner_user_id,
        due_date=request.due_date,
        source=TaskSource.INTERNAL,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return TaskResponse.model_validate(task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    request: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.org_id == current_user.org_id,
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    if request.status:
        task.status = request.status
    if request.title:
        task.title = request.title
    if request.due_date:
        task.due_date = request.due_date
    
    from datetime import datetime
    task.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(task)
    
    return TaskResponse.model_validate(task)


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    meeting_id: int = None,
    status: TaskStatus = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    query = db.query(Task).filter(Task.org_id == current_user.org_id)
    
    if meeting_id:
        query = query.filter(Task.meeting_id == meeting_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    return [TaskResponse.model_validate(task) for task in tasks]

