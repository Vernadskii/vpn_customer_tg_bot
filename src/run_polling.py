import asyncio
import os, django

from telegram_bot.vpn_service.service import VPNService

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_module.django_back_project.settings')
django.setup()

from telegram.ext import Application
from telegram import Update

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
    print("Bot is running in polling mode...")

    try:
        await asyncio.Event().wait()  # Wait indefinitely until manually stopped
    except asyncio.CancelledError:
        print("Bot is shutting down...")  # Handle the cancellation gracefully
    finally:
        # Ensure the bot is stopped gracefully
        await application.stop()
        print("Bot has been stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(run_polling())
    except (KeyboardInterrupt, SystemExit):
        VPNService().close_session()
        print("Bot process interrupted.")
