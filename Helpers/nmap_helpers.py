

from typing import List
import re


class NmapSensitizer:

    def __nmap_ports_sensitizer(self, text: str, lined_text: List[str]) -> list:
        pattern = r'(?P<port>\d+/\w+)\s+(?P<state>\w+)\s+(?P<service>\S+)(?:(?=\n[^\n]*?\S)|\s+(?P<version>\S+))?'

        matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)

        results = []
        # Extracting and printing results
        for match in matches:
            flag = False
            port = str(match[0]).split("/")
            result = {
                "portid": port[0],
                "protocol": port[1],
                "state": match[1],
                "service": {
                    "name": match[2],
                    "version": match[3],
                },
                "vulnerabilities": []
            }
            pattern = '|'.join(re.escape(option)
                               for option in ["open", "closed", "filtered"])

            # Check if the string contains one of the options
            if not re.search(pattern, result["state"]):
                continue
            for line in lined_text:
                if line.startswith(f"{result['portid']}/{result['protocol']}") and not flag:
                    flag = True
                    continue

                if flag:
                    if line.startswith("|"):
                        result["vulnerabilities"].append(
                            line.strip("|").strip("_").strip(" "))
                    else:
                        break
            results.append(result)

        return results

    def __nmap_os_sensitizer(self, text: List[str]) -> list:

        # line= line.replace("Aggressive OS guesses:", "")
        pattern = r'(?:Aggressive OS guesses: |)([\w\s.-]+) \((\d+%)\)'
        matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
        results = []
        for match in matches:
            results.append({
                "os": match[0].strip(),
                "accuracy": match[1],
            })

        return results

    @staticmethod
    def sensitize(text: str) -> dict:
        nmap = NmapSensitizer()
        lined_text = list(map(str.strip, text.split("\n")))
        return {
            "os": nmap.__nmap_os_sensitizer(text),
            "ports": nmap.__nmap_ports_sensitizer(text, lined_text),
        }
