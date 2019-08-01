import subprocess
import requests

class IPMonitor:
    def __init__(self, hosts: list):
        self.hosts = hosts
    
    def check_addresses(self) -> list:
        response = []
        for host in self.hosts:
            dns_result = subprocess.check_output(['dig', '+short', host, '@8.8.8.8']).decode('UTF-8').strip('\n')
            ip_result = requests.get('http://icanhazip.com').content.decode('UTF-8').strip('\n')
            if dns_result != ip_result:
                response.append(f"IP Address mismatch DNS has {dns_result}, direct IP check has {ip_result}")
        return response
    def run(self) -> list:
        return self.check_addresses()