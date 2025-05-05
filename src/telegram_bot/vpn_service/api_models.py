from pydantic import BaseModel, constr, ConfigDict
from typing import List


class AWGInterface(BaseModel):
    PrivateKey: constr(min_length=44, max_length=44)  # WireGuard keys are base64-encoded and 44 characters long
    Address: str  # It could be more specific
    h1: int
    h2: int
    h3: int
    h4: int
    jc: int
    jmax: int
    jmin: int
    s1: int
    s2: int


class Peer(BaseModel):
    PublicKey: constr(min_length=44, max_length=44)  # Same as the private key
    AllowedIPs: List[str]  # You can add custom validation if you want stricter control over CIDR
    Endpoint: str  # It's a combination of an IP and a port, so a stricter format could be added via validation
    PersistentKeepalive: int | None = 25


class AWgConfigModel(BaseModel):
    config_id: int
    Interface: AWGInterface
    Peer: Peer

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "Interface": {
                "Address": "10.0.0.7/32",
                "h1": 1227045251,
                "h2": 1227045252,
                "h3": 1227045253,
                "h4": 1227045254,
                "jc": 10,
                "jmax": 30,
                "jmin": 20,
                "PrivateKey": "IPSgpX3YmAsARgs1Fd5KGEoFZzfj3nQ0SMHiG9zHXEE=",
                "s1": 100,
                "s2": 110
            },
            "Peer": {
                "PublicKey": "uMnvozNSuNG6pRbzL7jViHTECIhEzsD/GxMSvY5lBzM=",
                "AllowedIPs": ["10.0.0.0/24"],
                "Endpoint": "194.135.17.31:51000",
                "PersistentKeepalive": 25,
            },
        }
    )
