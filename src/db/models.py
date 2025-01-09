from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy import Enum as SQLAlchemyENUM
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from enum import Enum
import os

load_dotenv(dotenv_path="config/.env")
Base = declarative_base()


class TaskStatus(Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(BigInteger, primary_key=True, index=True)
    # Updated to BigInteger
    assigned_user_id = Column(BigInteger, nullable=False)
    task_description = Column(String, nullable=False)
    status = Column(SQLAlchemyENUM(TaskStatus), default=TaskStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
