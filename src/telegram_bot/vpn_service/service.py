import logging

import aiohttp
from pydantic import ValidationError
from django_back_project import settings
from telegram_bot.vpn_service.api_models import WgConfigModel
from telegram_bot.vpn_service.tests.test_data import test_config

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


class ConfigCreateError(Exception):
    """Custom exception for configuration fetch errors."""
    pass


class VPNService:

    def __init__(self):
        self.url = settings.VPN_SERVICE_URL

    async def create_config(self):
        post_url = f"{self.url}/api/v1/config"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(post_url) as response:
                    data = await response.json()

                    if response.status != 200:
                        # TODO: add logging
                        # logger.error(f"Failed to fetch config: {response.status} - {await response.text()}")
                        raise ConfigCreateError(f"Error creating a new config: {response.status}, {data}")

                    return WgConfigModel(**data)

            except (aiohttp.ClientError, ValidationError) as e:
                # TODO: add logging
                # logger.error("An error occurred: %s", e)
                return None

    def deactivate_config(self):
        pass

    def activate_config(self):
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
