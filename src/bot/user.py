from telebot import TeleBot
from telebot.types import Message
from src.db.models import SessionLocal, Task, User
from src.utils import update_task_status


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

            print(f"Task ID: {task_id}, New Status: {new_status}")

            if update_task_status(task_id, new_status, session):
                bot.reply_to(message, "Task status updated successfully!")
            else:
                bot.reply_to(message, "Invalid task ID or status.")
        finally:
            session.close()

    @bot.message_handler(commands=["add"])
    def add_user(message: Message):
        session = SessionLocal()
        try:
            # Retrieve user details from the message
            user_id = message.from_user.id
            username = message.from_user.username or f"user_{user_id}"

            # Check if the user is already in the database
            existing_user = session.query(
                User).filter_by(user_id=user_id).first()
            if existing_user:
                bot.reply_to(message, f"User {
                             username} is already in the database.")
                return

            # Determine if the user is an admin
            # (This is an example; replace it with your logic to check admin status)
            # True if in a private chat, for example
            is_admin = message.chat.type == "private"

            # Add the user to the database
            new_user = User(user_id=user_id, username=username,
                            is_admin=is_admin)
            session.add(new_user)
            session.commit()

            bot.reply_to(message, f"User {
                         username} added successfully. Admin: {is_admin}")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
        finally:
            session.close()
