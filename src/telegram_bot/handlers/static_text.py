#### STATES ####
# start.py
CHOOSING_START, CHOOSING_ACCOUNT_ACTION, CHOOSING_INFO = range(3)
# info.py
BACK_TO_INFO = range(100, 101)
BACK_TO_ACCOUNT = range(120, 121)
STOPPING = range(400, 401)
CHOOSING_PRICE, BUYING_STATE = range(150, 152)

#### TEXT AND CALLBACKS ####
START_OVER = "START_FLAG"
BACK = "Назад"
BACK_CALLBACK = "BACK_CALLBACK"
BACK_INFO_CALLBACK = "BACK_INFO_CALLBACK"
BACK_ACCOUNT_CALLBACK = "BACK_ACCOUNT_CALLBACK"
STOP_TEXT = "Диалог сброшен\nЧтобы начать заново введите команду /start"

START_CREATED = "Привет {first_name}, рад видеть тебя!"
START_OLD_USER = "Добро пожаловать снова, {first_name}!"

PERSONAL_ACCOUNT_BUTTON = "Личный кабинет 👤"
PERSONAL_ACCOUNT_CALLBACK = "personal_account"

INFO_BUTTON = "Инфо ℹ️"
INFO_CALLBACK = "info"

# account.py
BUY_VPN_BUTTON = "Приобрести ВПН 🌐"
BUY_VPN_CALLBACK = "buy_vpn"

MY_SUBSCRIPTIONS_BUTTON = "Мои подписки 🧮"
MY_SUBSCRIPTIONS_CALLBACK = "my_subscriptions"

PRICE_1_MONTH = 1
BUY_1_MONTH = '1 месяц'
BUY_1_MONTH_CALLBACK = '1_month_callback'
PRICE_3_MONTH = 150
BUY_3_MONTH = '3 месяца'
BUY_3_MONTH_CALLBACK = '3_month_callback'
PRICE_6_MONTH = 300
BUY_6_MONTH = '6 месяцев'
BUY_6_MONTH_CALLBACK = '6_month_callback'

BUY_CALLBACK_PATTERN = f"^({BUY_1_MONTH_CALLBACK}|{BUY_3_MONTH_CALLBACK}|{BUY_6_MONTH_CALLBACK})$"

# info.py
ABOUT_US_BUTTON = "О нас ℹ️"
ABOUT_US_CALLBACK = "about_us"

HOW_TO_USE_BUTTON = "Как пользоваться 📖"
HOW_TO_USE_CALLBACK = "how_to_use"

SUPPORT_BUTTON = "Поддержка 💬"
SUPPORT_CALLBACK = "support"
