from sqlalchemy.orm import Session
from src.db.models import User, Task, TaskStatus


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
