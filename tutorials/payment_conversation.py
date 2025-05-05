import logging
from telegram import Update, LabeledPrice
from telegram.ext import Application, CommandHandler, MessageHandler, filters, PreCheckoutQueryHandler, CallbackContext, \
    ConversationHandler

from tutorials import TEST_TOKEN

# Вставьте сюда ваш токен
TOKEN = TEST_TOKEN

CHOOSING_START, PAYMENT_STATE = 1, 2

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Выберите команду /buy для покупки.")
    return CHOOSING_START


async def buy(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    title = "Название товара"
    description = "Описание товара"
    payload = "Custom-Payload"
    currency = "XTR"  # Используем Telegram Stars (XTR)
    price = 1  # Цена в XTR
    prices = [LabeledPrice("Название товара", int(price))]

    await context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token="",  # Пустой токен для цифровых товаров
        currency=currency,
        prices=prices,
        start_parameter="start_parameter"
    )
    return PAYMENT_STATE


async def precheckout_callback(update: Update, context: CallbackContext):
    query = update.pre_checkout_query
    if False:
        await query.answer(ok=False, error_message="Что-то пошло не так...")
    await query.answer(ok=True)


async def successful_payment_callback(update: Update, context: CallbackContext):
    payment = update.message.successful_payment
    await update.message.reply_text(f"Спасибо за выбор!")


async def help(update: Update, context: CallbackContext):
    await update.message.reply_text(f"Проверка выполнена")
    return CHOOSING_START


def main():
    application = Application.builder().token(TEST_TOKEN).build()

    start_conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_START: [
                CommandHandler("buy", buy),
            ],
            PAYMENT_STATE: [
                MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback),
                CommandHandler("help", help),
            ],
        },
        fallbacks=[],
    )

    application.add_handler(start_conversation)
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.run_polling()


if __name__ == '__main__':
    main()
