import asyncio
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_back_project.settings')
django.setup()

from telegram.ext import Application
from telegram import Update

from django_back_project.settings import TELEGRAM_TOKEN
from telegram_bot.dispatcher import setup_handlers


async def run_polling(tg_token: str = TELEGRAM_TOKEN):
    """Run bot in polling mode asynchronously."""
    application = Application.builder().token(tg_token).build()

    setup_handlers(application)
    await application.initialize()
    await application.start()
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    print("Bot is running in polling mode...")

    try:
        # Wait indefinitely until manually stopped
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        # Handle the cancellation gracefully
        print("Bot is shutting down...")
    finally:
        # Ensure the bot is stopped gracefully
        await application.stop()
        print("Bot has been stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(run_polling())
    except (KeyboardInterrupt, SystemExit):
        print("Bot process interrupted.")
