from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, Comment, Task
from app.schemas import CommentCreate, CommentResponse

router = APIRouter(tags=["comments"])

AUTHOR_ID = 1  # Replace with auth dependency when auth is added


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse, status_code=201)
def add_comment(task_id: int, body: CommentCreate, db: Session = Depends(get_db)):
    if not db.get(Task, task_id):
        raise HTTPException(404, "Task not found")
    comment = Comment(body=body.body, task_id=task_id, author_id=AUTHOR_ID)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def list_comments(task_id: int, db: Session = Depends(get_db)):
    if not db.get(Task, task_id):
        raise HTTPException(404, "Task not found")
    return db.query(Comment).filter_by(task_id=task_id).all()


@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(404, "Comment not found")
    if comment.author_id != AUTHOR_ID:
        raise HTTPException(403, "Not allowed to delete this comment")
    db.delete(comment)
    db.commit()
