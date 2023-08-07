from collections.abc import Callable
from typing import Type
from types import TracebackType

class tube:
    def interactive(self, prompt: str = ...) -> None: ...
    def recv(self, numb: int = ..., timeout: int = ...) -> bytes: ...
    def recvS(self, numb: int = ..., timeout: int = ...) -> str: ...
    def recvb(self, numb: int = ..., timeout: int = ...) -> bytearray: ...
    def recvall(self) -> bytes: ...
    def recvallS(self) -> str: ...
    def recvallb(self) -> bytearray: ...
    def recvline(self, keepends: bool = ..., timeout: int = ...) -> bytes: ...
    def recvlineS(self, keepends: bool = ..., timeout: int = ...) -> str: ...
    def recvlineb(self, keepends: bool = ..., timeout: int = ...) -> bytearray: ...
    def recvline_contains(
        self,
        items: bytes | list[str] | tuple[str, ...],
        keepends: bool = ...,
        timeout: int = ...,
    ) -> bytes: ...
    def recvline_containsS(
        self,
        items: bytes | list[str] | tuple[str, ...],
        keepends: bool = ...,
        timeout: int = ...,
    ) -> str: ...
    def recvline_containsb(
        self,
        items: bytes | list[str] | tuple[str, ...],
        keepends: bool = ...,
        timeout: int = ...,
    ) -> bytearray: ...
    def recvline_endswith(
        self,
        delims: bytes | list[str] | tuple[str, ...],
        keepends: bool = ...,
        timeout: int = ...,
    ) -> bytes: ...
    def recvline_endswithS(
        self,
        delims: bytes | list[str] | tuple[str, ...],
        keepends: bool = ...,
        timeout: int = ...,
    ) -> str: ...
    def recvline_endswithb(
        self,
        delims: bytes | list[str] | tuple[str, ...],
        keepends: bool = ...,
        timeout: int = ...,
    ) -> bytearray: ...
    def recvline_pred(
        self, pred: Callable[[str], bool], keepends: bool = ...
    ) -> bytes: ...
    def recvline_regex(
        self, regex: bytes, exact: bool = ..., keepends: bool = ..., timeout: int = ...
    ) -> bytes: ...
    def recvline_regexS(
        self, regex: bytes, exact: bool = ..., keepends: bool = ..., timeout: int = ...
    ) -> str: ...
    def recvline_regexb(
        self, regex: bytes, exact: bool = ..., keepends: bool = ..., timeout: int = ...
    ) -> bytearray: ...
    def recvline_startswith(
        self,
        delims: bytes | list[bytes] | tuple[bytes, ...],
        keepends: bool = ...,
        timeout: int = ...,
    ) -> bytes: ...
    def recvline_startswithS(
        self,
        delims: bytes | list[bytes] | tuple[bytes, ...],
        keepends: bool = ...,
        timeout: int = ...,
    ) -> str: ...
    def recvline_startswithb(
        self,
        delims: bytes | list[bytes] | tuple[bytes, ...],
        keepends: bool = ...,
        timeout: int = ...,
    ) -> bytearray: ...
    def recvlines(
        self, numlines: int, keepends: bool = ..., timeout: int = ...
    ) -> list[bytes]: ...
    def recvlinesS(
        self, numlines: int, keepends: bool = ..., timeout: int = ...
    ) -> list[str]: ...
    def recvlinesb(
        self, numlines: int, keepends: bool = ..., timeout: int = ...
    ) -> list[bytearray]: ...
    def recvn(self, numb: int, timeout: int = ...) -> bytes: ...
    def recvnS(self, numb: int, timeout: int = ...) -> str: ...
    def recvnb(self, numb: int, timeout: int = ...) -> bytearray: ...
    def recvpred(self, pred: Callable[[bytes], bool], timeout: int = ...) -> bytes: ...
    def recvpredS(self, pred: Callable[[bytes], bool], timeout: int = ...) -> str: ...
    def recvpredb(
        self, pred: Callable[[bytes], bool], timeout: int = ...
    ) -> bytearray: ...
    def recvregex(
        self, regex: bytes, exact: bool = ..., timeout: int = ...
    ) -> bytes: ...
    def recvregexS(
        self, regex: bytes, exact: bool = ..., timeout: int = ...
    ) -> str: ...
    def recvregexb(
        self, regex: bytes, exact: bool = ..., timeout: int = ...
    ) -> bytearray: ...
    def recvrepeat(self, timeout: int = ...) -> bytes: ...
    def recvrepeatS(self, timeout: int = ...) -> str: ...
    def recvrepeatb(self, timeout: int = ...) -> bytearray: ...
    def recvuntil(
        self,
        delims: bytes | list[bytes] | tuple[bytes, ...],
        drop: bool = ...,
        timeout: int = ...,
    ) -> bytes: ...
    def recvuntilS(
        self,
        delims: bytes | list[bytes] | tuple[bytes, ...],
        drop: bool = ...,
        timeout: int = ...,
    ) -> str: ...
    def recvuntilb(
        self,
        delims: bytes | list[bytes] | tuple[bytes, ...],
        drop: bool = ...,
        timeout: int = ...,
    ) -> bytearray: ...
    def send(self, data: bytes) -> bytes: ...
    def sendafter(
        self,
        delim: bytes | list[bytes] | tuple[bytes, ...],
        data: bytes,
        timeout: int = ...,
    ) -> bytes: ...
    def sendline(self, data: bytes) -> bytes: ...
    def sendlineafter(
        self,
        delim: bytes | list[bytes] | tuple[bytes, ...],
        data: bytes,
        timeout: int = ...,
    ) -> bytes: ...
    def sendlinethen(
        self,
        delim: bytes | list[bytes] | tuple[bytes, ...],
        data: bytes,
        timeout: int = ...,
    ) -> bytes: ...
    def sendthen(
        self,
        delim: bytes | list[bytes] | tuple[bytes, ...],
        data: bytes,
        timeout: int = ...,
    ) -> bytes: ...
    def settimeout(self, timeout: int) -> None: ...
    read = recv
    readS = recvS
    readb = recvb
    readall = recvall
    readallS = recvallS
    readallb = recvallb
    readline = recvline
    readlineS = recvlineS
    readlineb = recvlineb
    readline_contains = recvline_contains
    readline_containsS = recvline_containsS
    readline_containsb = recvline_containsb
    readline_endswith = recvline_endswith
    readline_endswithS = recvline_endswithS
    readline_endswithb = recvline_endswithb
    readline_pred = recvline_pred
    readline_regex = recvline_regex
    readline_regexS = recvline_regexS
    readline_regexb = recvline_regexb
    readline_startswith = recvline_startswith
    readline_startswithS = recvline_startswithS
    readline_startswithb = recvline_startswithb
    readlines = recvlines
    readlinesS = recvlinesS
    readlinesb = recvlinesb
    readn = recvn
    readnS = recvnS
    readnb = recvnb
    readpred = recvpred
    readpredS = recvpredS
    readpredb = recvpredb
    readregex = recvregex
    readregexS = recvregexS
    readregexb = recvregexb
    readrepeat = recvrepeat
    readrepeatS = recvrepeatS
    readrepeatb = recvrepeatb
    readuntil = recvuntil
    readuntilS = recvuntilS
    readuntilb = recvuntilb
    write = send
    writeafter = sendafter
    writeline = sendline
    wrtielineafter = sendlineafter
    writelinethen = sendlinethen
    writethen = sendthen

    def __enter__(self) -> tube: ...
    def __exit__(
        self,
        __exc_type: Type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
        /,
    ) -> None: ...
    def close(self) -> None: ...
