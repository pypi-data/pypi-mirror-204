from pwnlib.context import context as context
from pwnlib.tubes.process import process as process
from pwnlib.tubes.remote import connect as connect, remote as remote
from pwnlib.tubes.ssh import ssh as ssh
from pwnlib import gdb as gdb
from pwnlib.elf import ELF as ELF
from pwnlib.util.cyclic import cyclic as cyclic, cyclic_find as cyclic_find
from pwnlib.util.packing import (
    p8 as p8,
    p16 as p16,
    p32 as p32,
    p64 as p64,
    u8 as u8,
    u16 as u16,
    u32 as u32,
    u64 as u64,
    pack as pack,
    unpack as unpack,
    fit as fit,
    flat as flat,
)
from pwnlib import shellcraft as shellcraft
from pwnlib.asm import asm as asm, disasm as disasm
from pwnlib import log as log
from pwnlib.fiddling import (
    b64d as b64d,
    b64e as b64e,
    rol as rol,
    ror as ror,
    unhex as unhex,
    enhex as enhex,
    xor as xor,
    urldecode as urldecode,
    urlencode as urlencode,
    bits as bits,
    unbits as unbits,
)
from pwnlib.fmtstr import FmtStr as FmtStr, fmtstr_payload as fmtstr_payload
import os as os
import sys as sys
import time as time
import requests as requests
import re as re
import random as random

class _Args:
    def __getitem__(self, key: str) -> str: ...
    def __getattr__(self, key: str) -> str: ...

args: _Args
