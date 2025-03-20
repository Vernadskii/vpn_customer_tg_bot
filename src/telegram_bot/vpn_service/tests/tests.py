import os
import tempfile

import pytest
from telegram_bot.vpn_service.api_models import WgConfigModel
from telegram_bot.vpn_service.tests.test_data import test_config
from telegram_bot.vpn_service.utils import create_config_file_async


@pytest.fixture
def temp_file():
    """Fixture that return file path and remove file at the end."""
    _, temp_path = tempfile.mkstemp()
    yield temp_path
    os.remove(temp_path)  # Teardown: remove the temp file


def test_creation_wg_config_model_instance():
    config = WgConfigModel(**test_config['example'])
    print(config)


@pytest.mark.asyncio
async def test_creation_wg_config_file(temp_file):
    assert os.path.exists(temp_file)
    config = WgConfigModel(**test_config['example'])
    await create_config_file_async(temp_file, config)

    # checking file:
    with open(temp_file, "r") as f:
        content = f.read()

    print(f"\nFile content:\n{content}")
    assert '[Interface]' in content
    assert '[Peer]' in content



