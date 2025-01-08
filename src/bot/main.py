import os
from telebot import TeleBot
from dotenv import load_dotenv
from admin import register_admin_handlers
from user import register_user_handlers

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

# Register command handlers from separate modules
register_admin_handlers(bot)
register_user_handlers(bot)


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
    bot.infinity_polling()
