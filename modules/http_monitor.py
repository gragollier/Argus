import requests
from enum import Enum, auto
from typing import Generator, List


class _Type(Enum):
    STATUS_CODE = 'STATUS_CODE'
    RETURN_VALUE = 'RETURN_VALUE'


class HttpMonitor:
    def __init__(self, hosts: list, kind: _Type, goal: str):
        self.hosts = hosts
        self.type = kind
        self.goal = goal

        
    def run(self) -> list:
        if self.type == _Type.STATUS_CODE:
            return self._statusCodeCheck()
        elif self.type == _Type.RETURN_VALUE:
            return self._returnValueCheck()

    def _statusCodeCheck(self) -> list:
        response = []
        for host in self.hosts:
            try:
                res = requests.get(host)
                if (res.status_code != self.goal):
                    response.append(f"HttpMonitor expected a response code of {self.goal} for {host}, but got {res.status_code}")
            except requests.exceptions.ConnectionError as error:
                response.append(f"HttpMonitor error: {error}")
        return response

    
    def _returnValueCheck(self) -> list:
        return []
    
    @staticmethod
    def setup(hosts: list) -> list:
        result = []
        for host in hosts:
            result.append(HttpMonitor(host['hosts'], _Type(host['type']), host['goal']))
        return result


