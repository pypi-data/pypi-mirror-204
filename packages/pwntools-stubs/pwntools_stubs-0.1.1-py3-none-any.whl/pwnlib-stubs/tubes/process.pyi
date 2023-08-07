from pwnlib.tubes.tube import tube
from typing import Any
from collections.abc import Callable

class process(tube):
    def __init__(
        self,
        argv: list[str] = ...,
        shell: bool = ...,
        executable: str = ...,
        cwd: str = ...,
        env: dict[str, str] = ...,
        stdin: int = ...,
        stdout: int = ...,
        stderr: int = ...,
        close_fds: bool = ...,
        preexec_fn: Callable[[], Any] = ...,
        raw: bool = ...,
        aslr: bool = ...,
        setuid: bool = ...,
        where: str = ...,
        display: list[str] = ...,
        alarm: int = ...,
    ) -> None: ...
