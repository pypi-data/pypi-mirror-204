from typing import Literal
from collections.abc import Callable

class FmtStr:
    def __init__(
        self,
        execute_fmt: Callable[[bytes], bytes],
        offset: int = ...,
        padlen: int = ...,
        numbwritten: int = ...,
    ) -> None: ...
    def execute_writes(self) -> None: ...
    def write(self, addr: int, data: int) -> None: ...
    offset: int

def fmtstr_payload(
    offset: int,
    writes: dict[int, int],
    numbwritten: int = ...,
    write_size: Literal["byte", "short", "int"] = ...,
    overflows: int = ...,
    stategy: Literal["fast", "small"] = ...,
) -> bytes: ...
