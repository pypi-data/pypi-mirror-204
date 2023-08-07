from pwnlib.tubes.tube import tube
from typing import Literal

class listen(tube):
    def __init__(
        self,
        port: int = ...,
        bindaddr: str = ...,
        fam: Literal["any", "ipv4", "ipv6"] | int = ...,
        typ: Literal["tcp", "udp"] | int = ...,
    ) -> None: ...
