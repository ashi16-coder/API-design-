from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, tasks, tags, comments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(tags.router)
app.include_router(comments.router)
