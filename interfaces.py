from abc import ABC, abstractmethod

class DHTInterface(ABC):

    @abstractmethod
    def build(self, nodes: int):
        pass

    @abstractmethod
    def insert(self, key, value):
        pass

    @abstractmethod
    def lookup(self, key):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def node_join(self, node):
        pass

    @abstractmethod
    def node_leave(self, node):
        pass

    @abstractmethod
    def get_hops(self):
        pass
