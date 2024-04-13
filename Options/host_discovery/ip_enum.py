from enum import Enum


class IPScannerEnum(Enum):
    arp = "arp"
    icmp = "icmp"
    no_dns = "no_dns"
    

    def __int__(cls):
        match cls:
            case cls.arp:
                return 2
            case cls.icmp:
                return 1
          
            case _:
                return 3
