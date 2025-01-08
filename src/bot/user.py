from telebot import TeleBot
from telebot.types import Message
from src.db.models import SessionLocal, Task, TaskStatus
from src.utils import update_task_status


def register_user_handlers(bot: TeleBot):
    @bot.message_handler(commands=["user_tasks"])
    def user_tasks(message: Message):
        session = SessionLocal()
        try:
            user_id = message.from_user.id
            tasks = session.query(Task).filter_by(
                assigned_user_id=user_id).all()
            if not tasks:
                bot.reply_to(message, "No tasks found.")
                return

            response = "\n".join(
                [f"{i+1}. {task.task_description} - {task.status.value}" for i,
                    task in enumerate(tasks)]
            )
            bot.reply_to(message, response)
        finally:
            session.close()

    @bot.message_handler(commands=["update_status"])
    def update_status(message: Message):
        session = SessionLocal()
        try:
            args = message.text.split(" ", 2)
            if len(args) < 3:
                bot.reply_to(
                    message, "Usage: /update_status <task_id> <new_status>")
                return

            task_id = int(args[1])
            new_status = args[2].lower()

            task = session.query(Task).filter_by(id=task_id).first()
            if not task or new_status not in TaskStatus.__members__:
                bot.reply_to(message, "Invalid task ID or status.")
                return

            task.status = TaskStatus[new_status.upper()]
            session.commit()
            bot.reply_to(message, f"Task status updated to {new_status}.")
        finally:
            session.close()
