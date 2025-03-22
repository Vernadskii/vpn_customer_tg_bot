from telegram.error import TelegramError
from telegram.ext import CallbackContext

from django_module.apps.vpn.models import Client
from logging_config import tgbot_logger


async def notify_admin_users(context: CallbackContext, message: str):
    """Iterate over the admin clients and send a message to each."""
    async for client in Client.objects.filter(is_admin=True).all():
        try:
            await context.bot.send_message(chat_id=client.chat_id, text=message)
        except TelegramError as e:
            tgbot_logger.error(f"Failed to send message to {client.chat_id}: {e}")
