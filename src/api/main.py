from fastapi import FastAPI,  Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.models import SessionLocal, User, Task
from src.utils import setup_logger

logger = setup_logger("api", "logs/api.log")

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/telebot/users")
def fetch_users(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching users from the database.")
        users = db.query(User).all()
        logger.info(f"Fetched {len(users)} users.")
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api/v1/telebot/tasks")
def fetch_tasks(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching tasks from the database.")
        tasks = db.query(Task).all()
        logger.info(f"Fetched {len(tasks)} tasks.")
        return tasks
    except Exception as e:
        logger.error(f"Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
