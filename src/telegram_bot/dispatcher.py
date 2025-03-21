"""Telegram event handlers."""
import json
import os

from dateutil.relativedelta import relativedelta
from telegram import Update, SuccessfulPayment, Message, Chat, User
from telegram.error import TelegramError
from telegram.ext import (
    Application, MessageHandler, PreCheckoutQueryHandler, CallbackContext, filters, CommandHandler,
)
import datetime as dt
from django_module.apps.vpn.models import Subscription, Client, PaymentHistory, Config
from django_module.django_back_project.settings import ENV
from telegram_bot.handlers.start import start_conversation
from telegram_bot.vpn_service.service import VPNService


async def notify_admin_users(context: CallbackContext, message: str):
    admin_clients = await Client.get_admin_clients()
    # Iterate over the admin clients and send a message
    for client in admin_clients:
        try:
            await context.bot.send_message(chat_id=client.chat_id, text=message)
        except TelegramError as e:
            print(f"Failed to send message to {client.chat_id}: {e}")


async def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    if False:
        await query.answer(ok=False, error_message="Что-то пошло не так...")
    await query.answer(ok=True)


async def successful_payment_callback(update: Update, context: CallbackContext):
    payment = update.message.successful_payment
    months_amount = json.loads(payment.invoice_payload)['months_amount']
    client, _ = await Client.get_client_or_create(update.effective_user.to_dict())
    subscription = Subscription.objects.create(
        client=client, start_date=dt.date.today(), end_date=dt.date.today()+relativedelta(month=months_amount),
        amount=months_amount,
    )
    PaymentHistory.objects.create(
        client=client, payment_date=dt.datetime.now(), transaction_id=payment.telegram_payment_charge_id,
        amount=payment.total_amount
    )
    config = await VPNService().create_config()
    if config is None:
        await update.message.reply_text(
            f"Платеж успешно выполнен! В данный момент возникли технические сложности, "
            f"с вами свяжется специалист поддержки при первой возможности"
        )
        await notify_admin_users(
            context, f"Клиент {client.username} заплатил, но не получил конфиг так как VPN сервис оказался недоступен."
        )
        return

    config_file_path = await VPNService.create_file_by_config(config)
    Config.objects.create(data=config.model_dump(), activated=True, vpn_id=config.config_id, subscription=subscription)
    await context.bot.send_document(
        update.effective_user.id,
        caption=f'Это ваш персональный файл конфигурации VPN. Он действует до {subscription.end_date}',
        document=config_file_path,
    )
    os.remove(config_file_path)
    await update.message.reply_text(f"Спасибо за выбор!")


async def test_successful_payment(update: Update, context: CallbackContext):
    fake_payment = SuccessfulPayment(
        currency="XTR",
        total_amount=50,  # 50 stars
        invoice_payload='{"months_amount": 1}',  # Симуляция подписки на 1 месяц
        telegram_payment_charge_id="TEST_CHARGE_ID",
        provider_payment_charge_id="TEST_PROVIDER_ID"
    )

    # Создаем объект Message с успешным платежом
    fake_message = Message(
        message_id=9999,
        date=dt.datetime.now(),
        chat=Chat(id=update.effective_chat.id, type="private"),
        from_user=User(
            id=update.effective_user.id,
            is_bot=False,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
        ),
        successful_payment=fake_payment
    )

    # Создаем новый Update с этим сообщением
    fake_update = Update(update_id=update.update_id, message=fake_message)

    # Вызываем обработчик успешного платежа
    await successful_payment_callback(fake_update, context)


def setup_handlers(app: Application):
    """Adding handlers for events from Telegram."""

    # onboarding
    app.add_handler(start_conversation)
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback),)

    if ENV in ('local', 'test'):
        app.add_handler(CommandHandler("test_payment", test_successful_payment))