import os

import pytest
from telegram_bot.vpn_service.api_models import AWgConfigModel
from telegram_bot.vpn_service.service import VPNService
from telegram_bot.vpn_service.tests.test_data import test_awg_config_data_dict


@pytest.fixture
def awg_config_object():
    return AWgConfigModel(**test_awg_config_data_dict)


class TestVPNService:
    @pytest.mark.asyncio
    async def test_create_file_by_config(self, awg_config_object):
        vpn_service = VPNService()
        file_path = await vpn_service.create_file_by_config(awg_config_object)

        # checking the file:
        with open(file_path, "r") as f:
            content = f.read()

        assert '[Interface]' in content
        assert '[Peer]' in content
        # removing the file
        os.remove(file_path)



