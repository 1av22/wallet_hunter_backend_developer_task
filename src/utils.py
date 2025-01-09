import logging
from sqlalchemy.orm import Session
from src.db.models import User, Task, TaskStatus
import os


def is_admin(username: int, session: Session) -> bool:
    user = session.query(User).filter_by(username=username).first()
    return user.is_admin if user else False


def update_task_status(task_id: int, new_status: str, session: Session) -> bool:
    # Normalize the user input by converting it to lowercase
    normalized_status = new_status.strip().lower()

    # Check if the status exists in TaskStatus enum
    if normalized_status not in TaskStatus.__members__:
        print(f"Invalid status: {new_status}")
        return False

    # Retrieve the task
    task = session.query(Task).filter_by(task_id=task_id).first()
    if not task:
        print(f"Task ID {task_id} not found.")
        return False

    # Update the task status
    task.status = TaskStatus[normalized_status]
    session.commit()
    return True


def setup_logger(name: str, log_file: str, level=logging.INFO):
    # Create the logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir) and log_dir != '':
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
