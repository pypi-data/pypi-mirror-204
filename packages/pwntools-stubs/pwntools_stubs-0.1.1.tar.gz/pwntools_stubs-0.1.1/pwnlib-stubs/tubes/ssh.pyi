from pwnlib.tubes.tube import tube

class ssh(tube):
    def __init__(
        self,
        user: str = ...,
        host: str = ...,
        port: int = ...,
        password: str = ...,
        key: str = ...,
        keyfile: str = ...,
        proxy_command: str = ...,
        proxy_sock: str = ...,
        level: int = ...,
        cache: bool = ...,
        ssh_agent: bool = ...,
        ignore_config: bool = ...,
    ) -> None: ...
