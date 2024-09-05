from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.handlers.onboarding.static_text import CREATE_VPN, MY_VPN, \
    MY_BALANCE, DEPOSIT, PRICE, HELP, REFERRAL, MAIN_MENU, ONBOARDING_BUTTONS_QUERY


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(CREATE_VPN, callback_data=ONBOARDING_BUTTONS_QUERY[CREATE_VPN]),
            InlineKeyboardButton(MY_VPN, callback_data=ONBOARDING_BUTTONS_QUERY[MY_VPN]),
        ],
        [
            InlineKeyboardButton(MY_BALANCE, callback_data=ONBOARDING_BUTTONS_QUERY[MY_BALANCE]),
            InlineKeyboardButton(DEPOSIT, callback_data=ONBOARDING_BUTTONS_QUERY[DEPOSIT]),
        ],
        [
            InlineKeyboardButton(PRICE, callback_data=ONBOARDING_BUTTONS_QUERY[PRICE]),
            InlineKeyboardButton(HELP, callback_data=ONBOARDING_BUTTONS_QUERY[HELP]),
        ],
        [
            InlineKeyboardButton(REFERRAL, callback_data=ONBOARDING_BUTTONS_QUERY[REFERRAL]),
        ]
    ]

    return InlineKeyboardMarkup(buttons)
