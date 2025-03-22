"""Setup handlers."""
from telegram import Update
from telegram.ext import (
    Application, PreCheckoutQueryHandler, CallbackContext, CommandHandler,
)
from django_module.django_back_project.settings import ENV
from telegram_bot.handlers.start import start_conversation
from telegram_bot.handlers.test_handlers.test_payment import test_successful_payment


async def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    if False:
        await query.answer(ok=False, error_message="Что-то пошло не так...")
    await query.answer(ok=True)


def setup_handlers(app: Application):
    """Adding handlers for events from Telegram."""

    # onboarding
    app.add_handler(start_conversation)
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    if ENV in ('local', 'test'):
        app.add_handler(CommandHandler("test_payment", test_successful_payment))
