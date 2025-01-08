from .user import register_user_handlers
from .admin import register_admin_handlers
from src.db.models import SessionLocal, User
import os
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

register_admin_handlers(bot)
register_user_handlers(bot)


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(
        message, "Welcome to the Task Assignment Bot! Use /help for commands.")


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(
        message, "Available Commands:\n/admin_assign\n/user_tasks\n/update_status")


@bot.message_handler(content_types=["new_chat_members"])
def add_group_admins(message):
    admins = bot.get_chat_administrators(message.chat.id)
    session = SessionLocal()
    try:
        for admin in admins:
            user = session.query(User).filter_by(user_id=admin.user.id).first()
            if not user:
                new_user = User(
                    user_id=admin.user.id,
                    username=admin.user.username or admin.user.first_name,
                    is_admin=True,
                )
                session.add(new_user)
        session.commit()
        bot.reply_to(message, "Group admins have been added to the database.")
    except Exception as e:
        bot.reply_to(message, f"Error adding admins: {e}")
    finally:
        session.close()


@bot.message_handler(content_types=["new_chat_members"])
def add_all_members(message):
    chat_id = message.chat.id
    session = SessionLocal()
    try:
        # Add new members who just joined
        for new_member in message.new_chat_members:
            user_data = new_member
            # Check if user already exists in the database
            existing_user = session.query(User).filter_by(
                user_id=user_data.id).first()
            if not existing_user:
                new_user = User(
                    user_id=user_data.id,
                    username=user_data.username or user_data.first_name,
                    is_admin=False,  # New members are not admins by default
                )
                session.add(new_user)
        session.commit()
        bot.reply_to(message, "New members have been added to the database.")
    except Exception as e:
        bot.reply_to(message, f"Error adding members: {e}")
    finally:
        session.close()


@bot.message_handler(content_types=["new_chat_members"])
def add_group_members(message):
    session = SessionLocal()
    try:
        # Fetch all members of the group
        chat_members = bot.get_chat_administrators(message.chat.id)
        for member in chat_members:
            user = session.query(User).filter_by(
                user_id=member.user.id).first()
            if not user:
                new_user = User(
                    user_id=member.user.id,
                    username=member.user.username or member.user.first_name,
                    is_admin=member.status == "administrator" or member.status == "creator",
                )
                session.add(new_user)
        session.commit()
        bot.reply_to(message, "Group members have been added to the database.")
    except Exception as e:
        bot.reply_to(message, f"Error adding members: {e}")
    finally:
        session.close()


@bot.message_handler(content_types=["new_chat_members"])
def add_new_member(message):
    session = SessionLocal()
    try:
        for new_member in message.new_chat_members:
            user = session.query(User).filter_by(user_id=new_member.id).first()
            if not user:
                new_user = User(
                    user_id=new_member.id,
                    username=new_member.username or new_member.first_name,
                    is_admin=False,  # New members are not admins by default
                )
                session.add(new_user)
        session.commit()
        bot.reply_to(message, "New member(s) have been added to the database.")
    except Exception as e:
        bot.reply_to(message, f"Error adding new members: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
