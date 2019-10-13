from .base_module import BaseModule
import requests
from requests.adapters import HTTPAdapter
from enum import Enum, auto
from typing import Generator, List


class _Type(Enum):
    STATUS_CODE = 'STATUS_CODE'
    RETURN_VALUE = 'RETURN_VALUE'


class HttpMonitor (BaseModule):
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
                session = requests.Session()
                session.mount('https://', HTTPAdapter(max_retries=3))
                session.mount('http://', HTTPAdapter(max_retries=3))
                res = session.get(host)
                if (res.status_code != self.goal):
                    response.append(f"HttpMonitor expected a response code of {self.goal} for {host}, but got {res.status_code}")
            except requests.exceptions.ConnectionError as error:
                response.append(f"HttpMonitor error: {error}")
        return response

    
    def _returnValueCheck(self) -> list:
        return []
    
    @staticmethod
    def setup(hosts: dict) -> list:
        result = []
        for host in hosts.values():
            result.append(HttpMonitor(host['hosts'], _Type(host['type']), host['goal']))
        return result


