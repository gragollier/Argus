from .base_module import BaseModule
import subprocess
import paramiko

class HostMonitor(BaseModule):
    history = {}
    def __init__(self, hosts: list, username: str, password: str, chassis: str = None, fan_threshold: int = None):
        self.hosts = hosts
        self.username = username
        self.password = password
        self.chassis = chassis
        self.fan_threshold = fan_threshold

        print("Running initial power state check")
        for host in hosts:
            self.history[host] = check_power_state(host, username, password)

    def check_power(self) -> list:
        response = []
        for host in self.hosts:
            current_state = check_power_state(host, self.username, self.password)
            if self.history[host] != current_state:
                response.append(f"Host {host} power state changed from {self.history[host]} to {current_state}")
                self.history[host] = current_state
        return response

    # This is incredibly forced for my usage, but that's fine for now
    def check_fan_speed(self) -> list:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(self.chassis, username=self.username, password=self.password)
        _, std_out, _ = ssh_client.exec_command('getsensorinfo')

        cleaned_output = map(lambda x: int(x.split()[4]), std_out.readlines()[2:11])
        response = filter(lambda x: x > self.fan_threshold, cleaned_output)

        ssh_client.close()
        return map(lambda x: f"Fan speed above threshold, fan speed is {x}", response)

    def run(self) -> list:
        response = self.check_power()
        if self.fan_threshold:
            response.extend(self.check_fan_speed())
        return response

    @staticmethod
    def setup(hosts: dict) -> list:
        host_monitors = []
        for host_type in hosts:
            host_config = hosts[host_type]
            if host_type == 'm1000e':
                host_monitors.append(HostMonitor(host_config['hosts'], host_config['username'], host_config['password'], chassis=host_config['chassis'], fan_threshold=host_config['fan_threshold']))
            else:
                host_monitors.append(HostMonitor(host_config['hosts'], host_config['username'], host_config['password']))
        return host_monitors


def check_power_state(host: str, username: str, password: str) -> str:
    try:
        raw_result = str(subprocess.check_output(['ipmitool', '-I', 'lanplus', '-H', host, '-U', username, '-P', password, 'power', 'status']))
        return raw_result[-6:-3].strip()
    except subprocess.CalledProcessError as error:
        print(f"Error checking power state of {host}: {error}")
        return f"An error occurred trying to check the power state of {host}"