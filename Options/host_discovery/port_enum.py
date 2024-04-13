from enum import Enum


class PortScannerEnum(Enum):
    syn = "syn"
    connect = "connect"
    fin = "fin"
    ack = "ack"
    udp = "udp"

    def __int__(cls):
        match cls:
            case cls.syn:
                return 1
            case cls.connect:
                return 2
            case cls.fin:
                return 3
            case cls.ack:
                return 4
            case _:
                return 5
