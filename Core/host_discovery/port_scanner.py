import re
from typing import List
import nmap3

import time
import subprocess
from Helpers import NmapSensitizer

nmap = nmap3.NmapScanTechniques()



def extract_ports(results) -> List[str]:
    live_ips = []
    # print(results)
    for ip, details in results.items():

        if not details.get('ports', []):
            return live_ips

        for port_info in details.get('ports', []):
            port_id = port_info.get('portid', '')
            state = port_info.get('state', '')
            service_name = port_info.get('service', {}).get('name', '')

            if state == "open":
                live_ips.append(
                    f"[+] Port: {port_id}, State: {state}, Service Name: {service_name}")
            elif state == "filtered" or state == "closed":
                live_ips.append(
                    f"[-] Port: {port_id}, State: {state}, Service Name: {service_name}")
            else:
                live_ips.append(
                    f"[?] Port: {port_id}, State: {state}, Service Name: {service_name}")
    return live_ips


def match_state(state: int, portList: List[int]):
    # After checking the scan type check for the following:
    match state:
        case 1:
            ports = '-p-'
        case 2:
            ports = '-p'
            ports += ",".join(list(map(lambda num: str(num), portList)))
        case 3:
            ports = '--top-ports '
            ports += f"{portList[0]}"
    # print(ports)
    return ports


def port_scanner(target: str, switch: int, portsType: int, portList: List[int]):


    match switch:
        case 1:
            ports = match_state(portsType, portList)
            results = nmap.nmap_syn_scan(
                target, args=f"-Pn -T5 {ports}")

        case 2:
            ports = match_state(portsType, portList)
            results = nmap.nmap_tcp_scan(
                target, args=f"-Pn -T5 {ports}")

        case 3:
            ports = match_state(portsType, portList)
            results = nmap.nmap_fin_scan(
                target, args=f"-Pn -T5 {ports}")
        case 4:
            ports = match_state(portsType, portList)
            results = subprocess.run(
                f"nmap {target} -T5 -Pn -sA {ports}", shell=True, capture_output=True, text=True)
            results = {target: NmapSensitizer.sensitize(results.stdout)}
        case 5:
            ports = match_state(portsType, portList)
            results = nmap.nmap_udp_scan(
                target, args=f"-Pn -T5 {ports}")

    return extract_ports(results)


if __name__ == "__main__":
    port_scanner("meemdtt.com", 4, 3, [300])
