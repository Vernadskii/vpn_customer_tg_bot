"""Telegram event handlers."""

from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
)

from telegram_bot.handlers.onboarding import handlers as onboarding_handlers
from telegram_bot.handlers.onboarding.static_text import CALLBACK_PATTERN as ONBOARDING_CALLBACK_PATTERN


def setup_handlers(app: Application):
    """Adding handlers for events from Telegram."""

    # onboarding
    app.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    app.add_handler(CallbackQueryHandler(onboarding_handlers.handler_main_menu, pattern=ONBOARDING_CALLBACK_PATTERN))

