from enum import Enum


class IndexedEnum(Enum):
    @classmethod
    def values(cls):
        return list(cls)

    def __init__(self, *args):
        self.ordinal = len(type(self))

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.ordinal
