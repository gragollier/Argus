from abc import ABC, abstractmethod, abstractstaticmethod


class BaseModule(ABC):
    @abstractmethod
    def run(self) -> list:
        pass

    @abstractstaticmethod
    def setup(hosts: list) -> list:
        pass
