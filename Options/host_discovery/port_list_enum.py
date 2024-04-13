from enum import Enum


class PortListTypeEnum(Enum):
    top = "top"
    values = "values"

    def __int__(cls):
        match cls:
            case cls.top:
                return 3
            case _:
                return 2
