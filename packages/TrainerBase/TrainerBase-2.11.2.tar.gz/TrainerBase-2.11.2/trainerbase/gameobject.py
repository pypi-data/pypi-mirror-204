from uuid import uuid4
from typing import Self
from collections.abc import Callable

from trainerbase.memory import Address, make_address, pm


class GameObject:
    DPG_TAG_PREFIX = "object__"
    DPG_TAG_POSTFIX_IS_FROZEN = "__frozen"
    DPG_TAG_POSTFIX_GETTER = "__getter"
    DPG_TAG_POSTFIX_SETTER = "__setter"

    updated_objects: list[Self] = []

    def __init__(
        self,
        address: Address | int,
        pm_read: Callable,
        pm_write: Callable,
        frozen=None,
    ):
        GameObject.updated_objects.append(self)

        self.address = make_address(address)
        self.frozen = frozen
        self.pm_read = pm_read
        self.pm_write = pm_write

        dpg_tag = f"{GameObject.DPG_TAG_PREFIX}{uuid4()}"
        self.dpg_tag_frozen = f"{dpg_tag}{GameObject.DPG_TAG_POSTFIX_IS_FROZEN}"
        self.dpg_tag_getter = f"{dpg_tag}{GameObject.DPG_TAG_POSTFIX_GETTER}"
        self.dpg_tag_setter = f"{dpg_tag}{GameObject.DPG_TAG_POSTFIX_SETTER}"

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f" at {hex(self.address.resolve())}:"
            f" value={self.value},"
            f" frozen={self.frozen},"
            f" dpg_tag_frozen={self.dpg_tag_frozen},"
            f" dpg_tag_getter={self.dpg_tag_getter}"
            f" dpg_tag_setter={self.dpg_tag_setter}"
            ">"
        )

    def after_read(self, value):
        return value

    def before_write(self, value):
        return value

    @property
    def value(self):
        return self.after_read(self.pm_read(self.address.resolve()))

    @value.setter
    def value(self, new_value):
        self.pm_write(self.address.resolve(), self.before_write(new_value))


class GameInt(GameObject):
    def __init__(self, pointer: Address | int):
        super().__init__(
            pointer,
            pm.read_int,
            pm.write_int,
        )


class GameFloat(GameObject):
    def __init__(self, pointer: Address | int):
        super().__init__(
            pointer,
            pm.read_float,
            pm.write_float,
        )

    def before_write(self, value):
        return float(value)


class GameByte(GameObject):
    def __init__(self, pointer: Address | int):
        super().__init__(pointer, pm.read_char, pm.write_char)

    def before_write(self, value: int):
        return value.to_bytes(1, "little").decode()

    def after_read(self, value):
        return int.from_bytes(value.encode(), "little")
