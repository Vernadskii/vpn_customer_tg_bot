import aiofiles

from telegram_bot.vpn_service.api_models import WgConfigModel

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


async def create_config_file_async(file_path: str, config: WgConfigModel) -> None:
    """Asynchronously create a config file and write content to it."""
    interface_str = (
        "[Interface]\n"
        f"PrivateKey = {config.Interface.PrivateKey}\n"
        f"Address = {config.Interface.Address}\n"
        "MTU = 1280\n"  # static value
        "DNS = 1.1.1.1,1.0.0.1\n"  # static value
    )

    peer_str = (
        "\n[Peer]\n"
        f"PublicKey = {config.Peer.PublicKey}\n"
        f"AllowedIPs = {','.join(config.Peer.AllowedIPs)}\n"
        f"Endpoint = {config.Peer.Endpoint}\n"
        f"PersistentKeepalive = {config.Peer.PersistentKeepalive}\n"
    )

    async with aiofiles.open(file_path, 'w') as file:
        await file.write(interface_str + peer_str)

    # logger.info(f"File created: {file_path}")
