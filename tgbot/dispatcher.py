"""Telegram event handlers."""

from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
)

from tgbot.handlers.onboarding import handlers as onboarding_handlers


def setup_handlers(app: Application):
    """Adding handlers for events from Telegram."""

    # onboarding
    app.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    app.add_handler(CallbackQueryHandler(onboarding_handlers.first_menu_button))

