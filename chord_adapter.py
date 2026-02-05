# chord_adapter.py
import random
from interfaces import DHTInterface
from chord import ChordNode


class ChordAdapter(DHTInterface):
    def __init__(self):
        self.nodes = []
        self.last_hops = 0
        self.m = 16
        self.stabilize_rounds = 6

    def build(self, nodes: int):
        if nodes <= 0:
            raise ValueError("nodes must be > 0")

        first = ChordNode("node_0", self.m)
        first.join(None)
        self.nodes = [first]

        for i in range(1, nodes):
            new_node = ChordNode(f"node_{i}", self.m)
            bootstrap = random.choice(self.nodes)
            new_node.join(bootstrap)
            self.nodes.append(new_node)

            self._stabilize_all(rounds=2)

        self._stabilize_all(rounds=self.stabilize_rounds)
        print(f"Chord Network built with {nodes} nodes (m={self.m}).")

    def _stabilize_all(self, rounds=1):
        for _ in range(rounds):
            for n in self.nodes:
                n.stabilize()
            for n in self.nodes:
                n.fix_fingers()

    def _get_random_node(self):
        return random.choice(self.nodes)

    def insert(self, key, value):
        start_node = self._get_random_node()
        hops = {"hops": 0}
        start_node.put(str(key), value, hops=hops)
        self.last_hops = hops["hops"]
        return True

    def lookup(self, key):
        start_node = self._get_random_node()
        hops = {"hops": 0}
        value = start_node.get(str(key), hops=hops)
        self.last_hops = hops["hops"]
        return value

    def update(self, key, value):
        self.delete(key)
        self.insert(key, value)

    def delete(self, key):
        start_node = self._get_random_node()
        hops = {"hops": 0}
        ok = start_node.delete_key(str(key), hops=hops)
        self.last_hops = hops["hops"]
        return ok

    def node_join(self, node_name):
        new_node = ChordNode(str(node_name), self.m)
        bootstrap = random.choice(self.nodes) if self.nodes else None
        new_node.join(bootstrap)
        self.nodes.append(new_node)

        self.last_hops = 0
        self._stabilize_all(rounds=3)

    def node_leave(self, node_name):
        name = str(node_name)
        target = None
        for n in self.nodes:
            if getattr(n, "name", None) == name:
                target = n
                break

        if target is None:
            self.last_hops = 0
            return False

        target.leave()
        self.nodes.remove(target)

        self.last_hops = 0
        self._stabilize_all(rounds=3)
        return True

    def get_hops(self):
        return self.last_hops
