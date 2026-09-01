from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum, Table
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from datetime import datetime, timezone

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass


task_tags = Table(
    "task_tags", Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    tasks = relationship("Task", back_populates="owner")
    comments = relationship("Comment", back_populates="author")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum("todo", "in_progress", "done"), default="todo")
    priority = Column(Enum("low", "medium", "high"), default="medium")
    due_date = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    owner = relationship("User", back_populates="tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    tasks = relationship("Task", secondary=task_tags, back_populates="tags")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")
