from telebot import TeleBot
from telebot.types import Message
from src.db.models import SessionLocal, Task, User
from src.utils import update_task_status
from src.utils import setup_logger

logger = setup_logger("user", "logs/user.log")


def register_user_handlers(bot: TeleBot):
    @bot.message_handler(commands=["user_tasks"])
    def user_tasks(message: Message):
        session = SessionLocal()
        try:
            user_id = message.from_user.id
            tasks = session.query(Task).filter_by(
                assigned_user_id=user_id).all()
            print(tasks)
            if not tasks:
                bot.reply_to(message, "No tasks found.")
                return

            response = "\n".join(
                [
                    f"{task.task_id}.{task.task_description} - {task.status.value}"
                    for task in tasks
                ]
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

            try:
                task_id = int(args[1])  # Ensure task_id is an integer
            except ValueError:
                bot.reply_to(
                    message, "Invalid task ID. Please enter a valid number.")
                return

            new_status = args[2].strip().upper()

            logger.info(f"User {message.from_user.username} requested to update task {
                        task_id} status to {new_status}")
            print(f"Task ID: {task_id}, New Status: {new_status}")

            if update_task_status(task_id, new_status, session):
                logger.info(f"Task {task_id} status updated successfully.")
                bot.reply_to(message, "Task status updated successfully!")
            else:
                logger.error(f"Error updating task {task_id} status.")
                bot.reply_to(message, "Invalid task ID or status.")
        finally:
            session.close()

    @bot.message_handler(commands=["add"])
    def add_user(message: Message):
        session = SessionLocal()
        try:
            user_id = message.from_user.id
            username = message.from_user.username or f"user_{user_id}"

            existing_user = session.query(
                User).filter_by(user_id=user_id).first()
            if existing_user:
                bot.reply_to(message, f"User {
                             username} is already in the database.")
                return

            is_admin = message.chat.type == "private"

            new_user = User(user_id=user_id, username=username,
                            is_admin=is_admin)
            session.add(new_user)
            session.commit()

            logger.info(
                f"User {username} added successfully. Admin: {is_admin}")

            bot.reply_to(message, f"User {
                         username} added successfully. Admin: {is_admin}")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
        finally:
            session.close()
