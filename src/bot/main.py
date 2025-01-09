import os
from telebot import TeleBot
from dotenv import load_dotenv
from src.bot.admin import register_admin_handlers
from src.bot.user import register_user_handlers
from src.db.models import SessionLocal, User
from src.utils import setup_logger

logger = setup_logger("bot", "logs/bot.log")

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

register_admin_handlers(bot)
register_user_handlers(bot)


def add_bot_admin():
    session = SessionLocal()
    try:
        admin_user_id = 1219117288
        admin_username = "MeDontHaveAUsername"

        existing_user = session.query(User).filter_by(
            user_id=admin_user_id).first()
        if not existing_user:
            new_user = User(
                user_id=admin_user_id,
                username=admin_username,
                is_admin=True,
            )
            session.add(new_user)
            session.commit()
            logger.info(f"Admin {admin_username} added to the database.")
            print(f"Admin {admin_username} added to the database.")
    except Exception as e:
        logger.error(f"Error adding admin: {e}")
        print(f"Error adding admin: {e}")
    finally:
        session.close()


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(
        message, "Welcome to the Task Assignment Bot! Use /help for commands."
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(
        message,
        "Available Commands:\n/admin_assign\n/user_tasks\n/update_status",
    )


if __name__ == "__main__":
    print("Bot is running...")
    add_bot_admin()
    bot.infinity_polling()
