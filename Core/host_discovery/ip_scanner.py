import nmap3

nmap = nmap3.NmapHostDiscovery()


def extract_live_ips(results):
    res = []
    if results:
        for ip_address, result in results.items():
            if not isinstance(result, dict):
                continue
            
            try:
                if result.get('state', {}).get('state') == 'up':
                    res.append(f"{ip_address} is up")
            except Exception as e:
                print(e)
                continue

    return res


def ip_scanner(target: str, switch: int):

    results = None
    match switch:
        case 1:
            # Ping Sweep (Disable Port Scanning)
            results = nmap.nmap_no_portscan(target, args=f"-T5")
        case 2:
            results = nmap.nmap_arp_discovery(
                target, args=f"-T5")  # Arp Discovery
        case 3:
            results = nmap.nmap_disable_dns(
                target, args=f"-T5")  # No DNS Resolution

    return extract_live_ips(results)


if __name__ == "__main__":
    ip_scanner()
