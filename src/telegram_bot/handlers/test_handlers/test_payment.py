from telegram import Update, SuccessfulPayment, Message, Chat, User
from telegram.ext import CallbackContext

import datetime as dt

from telegram_bot.handlers.account import successful_payment_callback


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
