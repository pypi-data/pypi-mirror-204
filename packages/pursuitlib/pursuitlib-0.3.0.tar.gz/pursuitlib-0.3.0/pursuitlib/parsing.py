from typing import Optional

from decimal import Decimal


def parseint(value, default: Optional[int] = None) -> Optional[int]:
    if value is not None:
        try:
            return int(value)
        except ValueError:
            pass

    return default


def parsefloat(value, default: Optional[float] = None) -> Optional[float]:
    if value is not None:
        try:
            return float(value)
        except ValueError:
            pass

    return default


def parseas(type_name: str, value, default=None):
    if value is not None:
        try:
            if type_name == "str":
                return str(value)
            elif type_name == "int":
                return int(value)
            elif type_name == "float":
                return float(value)
            elif type_name == "Decimal":
                return Decimal(value)
        except ValueError:
            pass

    return default
