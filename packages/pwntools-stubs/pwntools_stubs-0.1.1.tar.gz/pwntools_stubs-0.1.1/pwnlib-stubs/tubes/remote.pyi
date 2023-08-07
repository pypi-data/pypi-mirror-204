from pwnlib.tubes.tube import tube
from typing import Literal, Any
from socket import socket
from ssl import SSLContext

class remote(tube):
    def __init__(
        self,
        host: str,
        port: int,
        fam: Literal["any", "ipv4", "ipv6"] | int = ...,
        typ: Literal["tcp", "udp"] | int = ...,
        ssl: bool = ...,
        sock: socket = ...,
        ssl_context: SSLContext = ...,
        ssl_args: dict[str, Any] = ...,
        sni: bool = ...,
    ) -> None: ...

class connect(remote): ...
