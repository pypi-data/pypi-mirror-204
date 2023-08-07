from typing import Literal, Any
from collections.abc import Callable, Iterable

def p8(
    number: int,
    sign: Literal["signed", "unsigned"] = ...,
    endian: Literal["little", "big"] = ...,
) -> bytes: ...

p16 = p8
p32 = p8
p64 = p8

def pack(
    number: int,
    word_size: int = ...,
    sign: Literal["signed", "unsigned"] = ...,
    endian: Literal["little", "big"] = ...,
) -> bytes: ...
def u8(
    number: bytes,
    sign: Literal["signed", "unsigned"] = ...,
    endian: Literal["little", "big"] = ...,
) -> int: ...

u16 = u8
u32 = u8
u64 = u8

def unpack(
    number: bytes,
    word_size: int = ...,
    sign: Literal["signed", "unsigned"] = ...,
    endian: Literal["little", "big"] = ...,
) -> int: ...
def flat(
    args: dict[int, bytes | int | list[int]],
    preprocessor: Callable[[Any], bytes] = ...,
    length: int = ...,
    filler: Iterable[bytes] = ...,
    word_size: int = ...,
    endianness: Literal["little", "big"] = ...,
    sign: bool = ...,
) -> bytes: ...

fit = flat
