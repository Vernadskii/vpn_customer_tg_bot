"""Telegram event handlers."""

from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
)

from telegram_bot.handlers.start import start_conversation


def setup_handlers(app: Application):
    """Adding handlers for events from Telegram."""

    # onboarding
    app.add_handler(start_conversation)