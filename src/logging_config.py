import logging
# import os
#
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_module.django_back_project.settings')
# django.setup()

# Get the logger for your application, such as 'my_app' as defined in settings.py
tgbot_logger = logging.getLogger('tg_bot')

# Example logging in your application
tgbot_logger.debug("This is a debug message from my app.")
tgbot_logger.info("This is an info message from my app.")

aiohttp_logger = logging.getLogger("aiohttp.client")
# Suppress the 'Unclosed client session' warnings from aiohttp
aiohttp_logger.addFilter(lambda record: "Unclosed client session" not in record.getMessage())