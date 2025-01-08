from telebot import TeleBot
from telebot.types import Message
from src.db.models import SessionLocal, Task, User
from src.utils import is_admin


def register_admin_handlers(bot: TeleBot):
    @bot.message_handler(commands=["admin_assign"])
    def assign_task(message: Message):
        session = SessionLocal()
        try:
            if not is_admin(message.from_user.id, session):
                bot.reply_to(message, "Unauthorized access.")
                return

            args = message.text.split(" ", 2)
            if len(args) < 3:
                bot.reply_to(
                    message, "Usage: /admin_assign @username Task Description"
                )
                return

            username = args[1].lstrip("@")
            description = args[2]
            user = session.query(User).filter_by(username=username).first()
            if not user:
                bot.reply_to(message, f"User @{username} not found.")
                return

            task = Task(assigned_user_id=user.user_id,
                        task_description=description)
            session.add(task)
            session.commit()
            bot.reply_to(
                message, f"Task assigned to @{username}: {description}")
        finally:
            session.close()
