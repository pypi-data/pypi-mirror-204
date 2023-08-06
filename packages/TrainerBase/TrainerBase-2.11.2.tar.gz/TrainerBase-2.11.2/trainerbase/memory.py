from typing import Self

from pymem import Pymem
from pymem.exception import ProcessNotFound

from config import PROCESS_NAMES


for process_name in PROCESS_NAMES:
    try:
        pm = Pymem(process_name)
    except ProcessNotFound:
        continue
    break
else:
    raise ProcessNotFound(f"not any: {PROCESS_NAMES}")


ARCH = 32 if pm.is_WoW64 else 64
POINTER_SIZE = 4 if pm.is_WoW64 else 8


read_pointer = pm.read_uint if pm.is_WoW64 else pm.read_ulonglong


class Address:
    def __init__(self, address: int, offsets: list[int] = None, add: int = 0):
        self.address = address
        self.offsets = [] if offsets is None else offsets
        self.add = add

    def inherit(self, *, extra_offsets: list = None, new_add: int = None) -> Self:
        new_address = Address(self.address, self.offsets.copy(), self.add)

        if extra_offsets is not None:
            new_address.offsets.extend(extra_offsets)

        if new_add is not None:
            new_address.add = new_add

        return new_address

    def resolve(self):
        pointer = self.address
        for offset in self.offsets:
            pointer = read_pointer(pointer) + offset

        return pointer + self.add


def make_address(address: Address | int):
    if isinstance(address, Address):
        return address

    return Address(address)
