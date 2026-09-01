from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    body: str


class CommentResponse(BaseModel):
    id: int
    body: str
    task_id: int
    author_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
