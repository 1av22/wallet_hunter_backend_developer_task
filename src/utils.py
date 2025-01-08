from sqlalchemy.orm import Session
from src.db.models import User, Task, TaskStatus


def is_admin(user_id: int, session: Session) -> bool:
    user = session.query(User).filter_by(user_id=user_id).first()
    return user.is_admin if user else False


def update_task_status(task_id: int, new_status: str, session: Session) -> bool:
    if new_status not in [status.value for status in TaskStatus]:
        return False

    task = session.query(Task).filter_by(task_id=task_id).first()
    if not task:
        return False

    task.status = TaskStatus(new_status)
    session.commit()
    return True
