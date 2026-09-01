from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db, Task, Tag, User
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, PaginatedResponse, TaskStatus, TaskPriority

router = APIRouter(tags=["tasks"])


def _get_task_or_404(task_id: int, db: Session) -> Task:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@router.post("/users/{user_id}/tasks", response_model=TaskResponse, status_code=201)
def create_task(user_id: int, body: TaskCreate, db: Session = Depends(get_db)):
    if not db.get(User, user_id):
        raise HTTPException(404, "User not found")
    tags = db.query(Tag).filter(Tag.id.in_(body.tag_ids)).all()
    task = Task(**body.model_dump(exclude={"tag_ids"}), owner_id=user_id, tags=tags)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/users/{user_id}/tasks", response_model=PaginatedResponse)
def list_tasks(
    user_id: int,
    db: Session = Depends(get_db),
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tag_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    if not db.get(User, user_id):
        raise HTTPException(404, "User not found")
    q = db.query(Task).filter(Task.owner_id == user_id)
    if status:
        q = q.filter(Task.status == status)
    if priority:
        q = q.filter(Task.priority == priority)
    if tag_id:
        q = q.filter(Task.tags.any(Tag.id == tag_id))
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return _get_task_or_404(task_id, db)


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, body: TaskUpdate, db: Session = Depends(get_db)):
    task = _get_task_or_404(task_id, db)
    data = body.model_dump(exclude_unset=True)
    if "tag_ids" in data:
        task.tags = db.query(Tag).filter(Tag.id.in_(data.pop("tag_ids"))).all()
    for k, v in data.items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = _get_task_or_404(task_id, db)
    db.delete(task)
    db.commit()
