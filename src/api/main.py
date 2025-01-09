from fastapi import FastAPI,  Depends
from sqlalchemy.orm import Session
from src.db.models import SessionLocal, User, Task

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/telebot/users")
def fetch_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.get("/api/v1/telebot/tasks")
def fetch_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks
