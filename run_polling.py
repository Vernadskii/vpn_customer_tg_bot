import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from telegram.ext import Application

from telegram import Bot

from dtb.settings import TELEGRAM_TOKEN
from tgbot.dispatcher import setup_handlers


def run_polling(tg_token: str = TELEGRAM_TOKEN):
    """ Run bot in polling mode """
    application = Application.builder().token(tg_token).build()

    setup_handlers(application)

    bot_info = Bot(tg_token).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Polling of '{bot_link}' has started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    application.start_polling()


if __name__ == "__main__":
    run_polling()