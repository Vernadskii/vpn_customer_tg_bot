import hashlib
import logging
from pathlib import Path
from typing import Literal

import aiofiles
import aiohttp
from aiohttp import ClientTimeout, ClientError, ClientResponseError
from pydantic import ValidationError

from django_module.django_back_project import settings
from telegram_bot.vpn_service.api_models import AWgConfigModel

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


class ConfigCreateError(Exception):
    """Custom exception for configuration fetch errors."""
    pass


def hash_id(_id: int) -> str:
    """Хешируем строку с использованием SHA256."""
    hash_object = hashlib.sha256(str(_id).encode())  # Преобразуем строку в байты
    return hash_object.hexdigest()  # Возвращаем хеш как строку


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
                headers={"X-API-Key": settings.VPN_SERVICE_SECRET_KEY}
            )

    async def close_session(self):  # TODO: add invoking at shutdown
        if self._session:
            await self._session.close()
            self._session = None

    async def create_config(self) -> AWgConfigModel:
        """Send a request to vnp-service for creating new config."""
        create_url = f"/api/{self.api_version}/config"
        payload = {'proto': self._config_type}  # sets protocol type
        try:
            async with self._session.post(create_url, json=payload) as response:
                data = await response.json()

                if response.status not in (200, 201):
                    print(f"Error creating a new config. Status:{response.status}, data: {data}")
                    raise ConfigCreateError(f"Error creating a new config: {response.status}, {data}")

                try:
                    return AWgConfigModel(**data)
                except ValidationError as ve:
                    print(f"Validation error: {ve.errors()}")  # TODO: add logging
                    raise ConfigCreateError from ve

        except ClientTimeout as ct:
            print(f"Timeout occurred while trying to reach {create_url}")
            raise ConfigCreateError from ct
        except (ClientError, ClientResponseError) as e:
            print(f"HTTP error occurred: {e.status} {e.message} when accessing {create_url}")
            raise ConfigCreateError from e
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            raise ConfigCreateError from e

    def deactivate_config(self):
        pass

    def activate_config(self):
        pass

    @staticmethod
    async def create_file_by_config(config: AWgConfigModel):
        """Asynchronously create a config file and write content to it. Returns the path to the file."""
        INTERFACE_TMP = (
            "[Interface]\n" +
            f"PrivateKey = {config.Interface.PrivateKey}\n" +
            f"Address = {config.Interface.Address}\n" +
            f"Jc = {config.Interface.jc}\n" +
            f"Jmin = {config.Interface.jmin}\n" +
            f"Jmax = {config.Interface.jmax}\n" +
            f"S1 = {config.Interface.s1}\n" +
            f"S2 = {config.Interface.s2}\n" +
            f"H1 = {config.Interface.h1}\n" +
            f"H2 = {config.Interface.h2}\n" +
            f"H3 = {config.Interface.h3}\n" +
            f"H4 = {config.Interface.h4}\n"
        )

        PEER_TMP = (
            "[Peer]\n"
            f"PublicKey = {config.Peer.PublicKey}\n"
            f"AllowedIPs = {','.join(config.Peer.AllowedIPs)}\n"
            f"Endpoint = {config.Peer.Endpoint}\n"
            f"PersistentKeepalive = {config.Peer.PersistentKeepalive}\n"
        )

        file_name = hash_id(config.config_id)[0:20]
        file_path = Path(__file__).parent / file_name  # Получаем путь к текущей директории скрипта и добавляем имя файла

        async with aiofiles.open(file_path, 'w') as file:
            await file.write(INTERFACE_TMP + "\n" + PEER_TMP)

        return file_path
