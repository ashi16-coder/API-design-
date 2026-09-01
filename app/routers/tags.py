from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, Tag
from app.schemas import TagCreate, TagResponse

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", response_model=TagResponse, status_code=201)
def create_tag(body: TagCreate, db: Session = Depends(get_db)):
    if db.query(Tag).filter_by(name=body.name).first():
        raise HTTPException(409, "Tag name already exists")
    tag = Tag(name=body.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.get("", response_model=list[TagResponse])
def list_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(404, "Tag not found")
    db.delete(tag)
    db.commit()
