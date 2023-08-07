def asm(
    code: str,
    vma: int = ...,
    extract: bool = ...,
    shared: bool = ...,
    **kwargs: dict[str, str]
) -> bytes: ...
def disasm(
    data: bytes,
    vma: int = ...,
    extract: bool = ...,
    shared: bool = ...,
    **kwargs: dict[str, str]
) -> str: ...
