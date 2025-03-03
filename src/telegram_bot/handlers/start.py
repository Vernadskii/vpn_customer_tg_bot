from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

from django_module.apps.users.models import User
from telegram_bot.handlers import static_text
from telegram_bot.handlers.account import handle_top_up_balance, handle_buy_subscription, handle_my_subscription

CHOOSING_START, CHOOSING_LK = range(2)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Личный кабинет", "Инфо"]]
    u, created = await User.get_user_and_created(update, context)

    text = static_text.START_CREATED.format(first_name=u.username) if created \
        else static_text.START_OLD_USER.format(first_name=u.username)

    await update.message.reply_text(
        text=text, reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        ),
    )

    return CHOOSING_START


async def handle_start_selection(update: Update, context: CallbackContext) -> int:
    # Check user choice and navigate to the appropriate state
    choice = update.message.text
    if choice == 'Личный кабинет':
        return await handle_lk(update, context)
    if choice == 'Инфо':
        return await handle_info(update, context)
    return await invalid_input(update, context)


async def handle_account_selection(update: Update, context: CallbackContext) -> int:
    choice = update.message.text
    if choice == 'Пополнить баланс':
        return await handle_top_up_balance(update, context)
    if choice == 'Приобрести ВПН':
        return await handle_buy_subscription(update, context)
    if choice == 'Мои подписки':
        return await handle_my_subscription(update, context)
    return await invalid_input(update, context)


# Handler for "Личный кабинет"
async def handle_lk(update: Update, context: CallbackContext) -> int:
    # Здесь добавьте логику для личного кабинета
    reply_keyboard = [["Пополнить баланс", "Приобрести ВПН", "Мои подписки"]]
    await update.message.reply_text(
        text="Баланс: х\n"
             "Дата окончания подписки: DD-MM-YYYY",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return CHOOSING_LK


# Handler for "Инфо"
async def handle_info(update: Update, context: CallbackContext) -> int:
    # Здесь добавьте логику для информации
    await update.message.reply_text("Вы выбрали Инфо.")
    return ConversationHandler.END


async def invalid_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.edit_text("Invalid input. Write '/start' to initial the bot again.")
    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_command)],
    states={
        CHOOSING_START: [
            MessageHandler(filters.Regex("^(Личный кабинет|Инфо)$"), handle_start_selection),
        ],
        CHOOSING_LK: [
            MessageHandler(filters.Regex("^(Пополнить баланс|Приобрести ВПН|Мои подписки)$"), handle_account_selection),
        ]
    },
    fallbacks=[CommandHandler("cancel", invalid_input)],
)