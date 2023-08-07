from pwnlib.elf import ELF

class ContextType:
    binary: ELF
    def update(self, arch: str) -> None: ...

context: ContextType = ...
