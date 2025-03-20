import logging
from typing import Literal

import aiohttp
from aiohttp import ClientTimeout, ClientError, ClientResponseError
from pydantic import ValidationError

from django_module.django_back_project import settings
from telegram_bot.vpn_service.api_models import AWgConfigModel
from telegram_bot.vpn_service.tests.test_data import test_config

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


class ConfigCreateError(Exception):
    """Custom exception for configuration fetch errors."""
    pass


class VPNService:
    _session = None  # singleton session

    def __init__(self, config_type: Literal['awg'] = 'awg'):
        self._base_url = settings.VPN_SERVICE_URL
        self._config_type = config_type
        self.api_version = "v1"
        if self._session is None:  # initialize only for first time
            self._session = aiohttp.ClientSession(
                base_url=self._base_url,
                timeout=ClientTimeout(total=10),  # 10 seconds for request timeout
            )

    async def close_session(self):  # TODO: add invoking at shutdown
        if self._session:
            await self._session.close()
            self._session = None

    async def create_config(self):
        create_url = f"/api/{self.api_version}/config"
        payload = {'proto': self._config_type}  # sets protocol type
        try:
            async with self._session.post(create_url, data=payload) as response:
                data = await response.json()

                if response.status not in (200, 201):
                    # TODO: add logging
                    # logger.error(f"Failed to fetch config: {response.status} - {await response.text()}")
                    print(f"Error creating a new config. Status:{response.status}, data: {data}")
                    # raise ConfigCreateError(f"Error creating a new config: {response.status}, {data}")
                    return None

                return AWgConfigModel(**data)
        except ClientTimeout:
            print(f"Timeout occurred while trying to reach {create_url}")
        except (ClientError, ClientResponseError) as e:
            print(f"HTTP error occurred: {e.status} {e.message} when accessing {create_url}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        finally:
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

async def get_config() -> AWgConfigModel:
        return AWgConfigModel(**test_config['example'])
