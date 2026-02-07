import random
from interfaces import DHTInterface
from pastry_network import PastryNetwork, make_id
from pastry_node import PastryNode
class PastryAdapter(DHTInterface):
    def __init__(self):
        self.network = PastryNetwork()
        self.last_hops = 0 

    def build(self, nodes: int):
        for i in range(nodes):
            node_id = make_id(f"node_{i}")
            new_node = PastryNode(self.network, node_id)
            self.network.add_node(new_node)
            self.network.rebuild()
        print(f"Pastry Network built with {nodes} nodes.")

    def _get_random_node(self):
        all_ids = list(self.network.nodes.keys())
        return self.network.nodes[random.choice(all_ids)]

    def insert(self, key, value):
            start_node = self._get_random_node()
            _, hops = start_node.insert(key, value)
            self.last_hops = hops
            return True

    def lookup(self, key):
            start_node = self._get_random_node()
            value, _, hops = start_node.find_key(key)
            self.last_hops = hops
        
            if isinstance(value, list) and value:
                return value[-1] 
            return value

    def update(self, key, value):
        self.delete(key)
        self.insert(key, value)

    def delete(self, key):
            start_node = self._get_random_node()
            _, _, hops = start_node.delete(key)
            self.last_hops = hops
            return True

    def node_join(self, node_name):
            new_id = make_id(node_name)
            new_node = PastryNode(self.network, new_id)
            self.network.join(new_node)
            self.last_hops = 0
        

    def node_leave(self, node_name):
            target_id = make_id(node_name)
            self.network.leave(target_id)
            self.last_hops = 0

    def get_hops(self):
        return self.last_hops