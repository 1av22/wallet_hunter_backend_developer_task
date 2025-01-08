from sqlalchemy import create_engine, Column, Integer, String, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
import os

load_dotenv(dotenv_path="config/.env")
Base = declarative_base()


class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)


class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True)
    assigned_user_id = Column(Integer, ForeignKey(
        "users.user_id"), nullable=False)
    task_description = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
