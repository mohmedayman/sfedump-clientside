from typing import List
import nmap3
import subprocess
from Helpers import NmapSensitizer
nmap = nmap3.Nmap()


def service_scanner(target: str, method: int):

    if method == 1:  # Service Detection

        prog = "-sV"

    elif method == 2:  # Vulnerability Detection
        prog = "-sC"

    elif method == 3:  # os detection
        prog = "-O"

    else:  # aggressive
        prog = "-A"

    results = subprocess.run(
        f"nmap -T5 -Pn {prog} {target}", shell=True, capture_output=True, text=True)

    if results.returncode > 0:
        raise Exception(results.stderr)

    results = NmapSensitizer.sensitize(results.stdout)

    return results


if __name__ == "__main__":
    print(service_scanner("chat.openai.com", 2))
