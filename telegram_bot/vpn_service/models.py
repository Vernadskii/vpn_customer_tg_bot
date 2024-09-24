from pydantic import BaseModel, constr, ConfigDict
from typing import List


class Interface(BaseModel):
    PrivateKey: constr(min_length=44, max_length=44)  # WireGuard keys are base64-encoded and 44 characters long
    Address: str  # It could be more specific


class Peer(BaseModel):
    PublicKey: constr(min_length=44, max_length=44)  # Same as the private key
    AllowedIPs: List[str]  # You can add custom validation if you want stricter control over CIDR
    Endpoint: str  # It's a combination of an IP and a port, so a stricter format could be added via validation
    PersistentKeepalive: int


class WgConfigModel(BaseModel):
    Interface: Interface
    Peer: Peer

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "Interface": {
                    "PrivateKey": "IPSgpX3YmAsARgs1Fd5KGEoFZzfj3nQ0SMHiG9zHXEE=",
                    "Address": "10.0.0.7/32"
                },
                "Peer": {
                    "PublicKey": "uMnvozNSuNG6pRbzL7jViHTECIhEzsD/GxMSvY5lBzM=",
                    "AllowedIPs": ["10.0.0.0/24"],
                    "Endpoint": "194.135.17.31:51000",
                    "PersistentKeepalive": 25,
                },
            }
        }
    )
