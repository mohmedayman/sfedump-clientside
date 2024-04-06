

from enum import Enum


class ServiceScannerEnum(Enum):
    service = "service"
    vulnerability = "vulnerability"
    os = "os"
    aggressive = "aggressive"
    

    def __int__(cls):
        match cls:
            case cls.service:
                return 1
            case cls.vulnerability:
                return 2
            case cls.os:
                return 3
            case _:
                return 4
