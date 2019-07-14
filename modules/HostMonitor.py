import subprocess

class HostMonitor:
    history = {}
    def __init__(self, hosts: list, username: str, password: str):
        self.hosts = hosts
        self.username = username
        self.password = password

        print("Running initial power state check")
        for host in hosts:
            self.history[host] = check_power_state(host, username, password)


    def run(self) -> list:
        response = []
        for host in self.hosts:
            current_state = check_power_state(host, self.username, self.password)
            print(current_state)
            if self.history[host] != current_state:
                response.append(f"Host {host} power state changed from {self.history[host]} to {current_state}")
                self.history[host] = current_state
        return response


def check_power_state(host: str, username: str, password: str) -> str:
    try:
        raw_result = str(subprocess.check_output(['ipmitool', '-I', 'lanplus', '-H', host, '-U', username, '-P', password, 'power', 'status']))
        return raw_result[-6:-3].strip()
    except subprocess.CalledProcessError as error:
        print(f"Error checking power state of {host}: {error}")
        return f"An error occurred trying to check the power state of {host}"