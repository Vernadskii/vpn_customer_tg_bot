from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding.static_text import CREATE_VPN, MY_VPN, \
    MY_BALANCE, DEPOSIT, PRICE, HELP, REFERRAL


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(CREATE_VPN, callback_data=CREATE_VPN),
            InlineKeyboardButton(MY_VPN, callback_data=MY_VPN),
        ],
        [
            InlineKeyboardButton(MY_BALANCE, callback_data=MY_BALANCE),
            InlineKeyboardButton(DEPOSIT, callback_data=DEPOSIT),
        ],
        [
            InlineKeyboardButton(PRICE, callback_data=PRICE),
            InlineKeyboardButton(HELP, callback_data=HELP),
        ],
        [
            InlineKeyboardButton(REFERRAL, callback_data=REFERRAL),
        ]
    ]

    return InlineKeyboardMarkup(buttons)
