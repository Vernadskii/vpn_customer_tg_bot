import os, django

from logging_config import tgbot_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_module.django_back_project.settings')
django.setup()

import asyncio
from telegram.ext import Application
from telegram import Update

from telegram_bot.vpn_service.service import VPNService
from django_module.django_back_project.settings import TELEGRAM_TOKEN
from telegram_bot.dispatcher import setup_handlers

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

# filterwarnings(
#     action="ignore",
#     message=r"*If 'per_message=False', 'CallbackQueryHandler' will not be tracked for every message*",
#     category=PTBUserWarning,
# )


async def run_polling(tg_token: str = TELEGRAM_TOKEN):
    """Run bot in polling mode asynchronously."""
    application = Application.builder().token(tg_token).build()

    setup_handlers(application)
    await application.initialize()
    await application.start()
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    tgbot_logger.info("Bot has been started in polling mode...")

    try:
        await asyncio.Event().wait()  # Wait indefinitely until manually stopped
    except asyncio.CancelledError:
        tgbot_logger.info("Bot is shutting down...")  # Handle the cancellation gracefully
    finally:
        # Ensure the bot is stopped gracefully
        await VPNService().close_session()
        await application.stop()
        tgbot_logger.info("Bot has been stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(run_polling())
    except (KeyboardInterrupt, SystemExit):
        tgbot_logger.info("Bot process interrupted.")
