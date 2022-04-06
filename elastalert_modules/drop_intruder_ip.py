import ipaddress
from math import exp
from elastalert.enhancements import BaseEnhancement, DropMatchException
from elastalert import util


class DropIntruderIOIP(BaseEnhancement):
    # This enhancement ensures we don't alert on Intruder.IO IP's
    # which frequently scan our Infra.
    def process(self, match):
        whitelisted = self.generate_trusted_ips()
        
        if match["source"]["ip"] in whitelisted:
            raise DropMatchException()

    def generate_trusted_ips(self):
        all_ips = ["139.162.214.111"]
        ranges = [
            "35.177.219.0/26",
            "3.9.159.128/25",
            "18.168.180.128/25",
            "18.168.224.128/25",
            "54.93.254.128/26",
            "18.194.95.64/26",
            "3.124.123.128/25",
            "3.67.7.128/25",
            "203.12.218.0/24",
        ]

        for range in ranges:
            expanded = [str(ip) for ip in ipaddress.IPv4Address(range)]
            all_ips.extend(expanded)
        return all_ips
