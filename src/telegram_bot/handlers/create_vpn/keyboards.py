from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.handlers.onboarding.static_text import HELP, MAIN_MENU, ONBOARDING_BUTTONS_QUERY


def make_keyboard_for_create_vpn_command() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(HELP, callback_data=ONBOARDING_BUTTONS_QUERY[HELP]),
        ],
        [
            InlineKeyboardButton(MAIN_MENU, callback_data=ONBOARDING_BUTTONS_QUERY[MAIN_MENU]),
        ],
    ]

    return InlineKeyboardMarkup(buttons)