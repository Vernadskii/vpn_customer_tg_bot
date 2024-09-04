import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_back_project.settings')
django.setup()

from telegram.ext import Application

from telegram import Update

from django_back_project.settings import TELEGRAM_TOKEN
from telegram_bot.dispatcher import setup_handlers


def run_polling(tg_token: str = TELEGRAM_TOKEN):
    """ Run bot in polling mode """
    application = Application.builder().token(tg_token).build()

    setup_handlers(application)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run_polling()