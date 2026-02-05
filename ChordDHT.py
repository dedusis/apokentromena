class ChordDHT(DHTInterface):
    def __init__(self, m: int):
        self.m = m
        self.nodes: List[ChordNode] = []
        self._last_hops = 0

    def build(self, nodes: int):
        self.nodes = create_network(nodes, self.m)

    def insert(self, key, value):
        entry = random.choice(self.nodes)
        hops = {"hops": 0}
        entry.put(key, value, hops)
        self._last_hops = hops["hops"]

    def lookup(self, key):
        entry = random.choice(self.nodes)
        hops = {"hops": 0}
        value = entry.get(key, hops)
        self._last_hops = hops["hops"]
        return value

    def delete(self, key):
        entry = random.choice(self.nodes)
        hops = {"hops": 0}
        entry.delete_key(key, hops)
        self._last_hops = hops["hops"]

    def node_join(self, node=None):
        # wrapper γύρω από eval_join ή join logic
        pass

    def node_leave(self, node=None):
        pass

    def get_hops(self):
        return self._last_hops
