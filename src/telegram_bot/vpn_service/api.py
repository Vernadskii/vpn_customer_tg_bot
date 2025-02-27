import logging

import aiohttp
from pydantic import ValidationError
from django_back_project import settings
from telegram_bot.vpn_service.models import WgConfigModel
from telegram_bot.vpn_service.tests.test_data import test_config

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


class ConfigFetchError(Exception):
    """Custom exception for configuration fetch errors."""
    pass


# async def get_config() -> WgConfigModel | None:
#     """Fetch VPN config from vpn service."""
#     url = f"{settings.VPN_SERVICE_URL}/api/config"
#
#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.post(url) as response:
#                 if response.status != 200:
#                     logger.error(f"Failed to fetch config: {response.status} - {await response.text()}")
#                     raise ConfigFetchError(f"Error fetching config: {response.status}")
#
#                 data = await response.json()
#                 return WgConfigModel(**data)
#
#         except (aiohttp.ClientError, ValidationError) as e:
#             logger.error("An error occurred: %s", e)
#             return None

async def get_config() -> WgConfigModel:
        return WgConfigModel(**test_config['example'])
