from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, CallbackContext, \
    CallbackQueryHandler

from django_module.apps.users.models import User
from telegram_bot.handlers import static_text
from telegram_bot.handlers.account import handle_account_selection
from telegram_bot.handlers.info import handle_info_selection


CHOOSING_START, CHOOSING_ACCOUNT, CHOOSING_INFO = range(3)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton(static_text.PERSONAL_ACCOUNT_BUTTON, callback_data=static_text.PERSONAL_ACCOUNT_CALLBACK)],
        [InlineKeyboardButton(static_text.INFO_BUTTON, callback_data=static_text.INFO_CALLBACK)]
    ]

    u, created = await User.get_user_and_created(update, context)

    text = static_text.START_CREATED.format(first_name=u.username) if created \
        else static_text.START_OLD_USER.format(first_name=u.username)

    await update.message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    return CHOOSING_START


async def handle_start_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()  # Подтверждаем получку, чтобы избежать "зависания" у пользователя
    choice = query.data

    if choice == "personal_account":
        return await handle_account(update, context)
    elif choice == "info":
        return await handle_info(update, context)


async def handle_account(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton(static_text.TOP_UP_ACCOUNT_BUTTON, callback_data=static_text.TOP_UP_ACCOUNT_CALLBACK),
            InlineKeyboardButton(static_text.BUY_VPN_BUTTON, callback_data=static_text.BUY_VPN_CALLBACK)
        ],
        [
            InlineKeyboardButton(static_text.MY_SUBSCRIPTIONS_BUTTON, callback_data=static_text.MY_SUBSCRIPTIONS_CALLBACK)
        ]
    ]

    await update.callback_query.message.reply_text(
        text="Баланс: х\nДата окончания подписки: DD-MM-YYYY",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return CHOOSING_ACCOUNT


async def handle_info(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton(static_text.ABOUT_US_BUTTON, callback_data=static_text.ABOUT_US_CALLBACK),
            InlineKeyboardButton(static_text.PRICING_BUTTON, callback_data=static_text.PRICING_CALLBACK),
        ],
        [
            InlineKeyboardButton(static_text.HOW_TO_USE_BUTTON, callback_data=static_text.HOW_TO_USE_CALLBACK),
            InlineKeyboardButton(static_text.SUPPORT_BUTTON, callback_data=static_text.SUPPORT_CALLBACK),
        ]
    ]

    await update.callback_query.message.reply_text(
        text="Выберите раздел:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return CHOOSING_INFO


async def invalid_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.edit_text("Invalid input. Write '/start' to initial the bot again.")
    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_command)],
    states={
        CHOOSING_START: [CallbackQueryHandler(handle_start_selection)],
        CHOOSING_ACCOUNT: [CallbackQueryHandler(handle_account_selection)],
        CHOOSING_INFO: [CallbackQueryHandler(handle_info_selection)]
    },
    fallbacks=[
        CommandHandler("start", start_command),  # Обработка команды /start в fallback
        CommandHandler("cancel", invalid_input),
    ],
)
