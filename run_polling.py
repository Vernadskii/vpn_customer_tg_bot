import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from telegram.ext import Application

from telegram import Update

from dtb.settings import TELEGRAM_TOKEN
from tgbot.dispatcher import setup_handlers


def run_polling(tg_token: str = TELEGRAM_TOKEN):
    """ Run bot in polling mode """
    application = Application.builder().token(tg_token).build()

    setup_handlers(application)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run_polling()