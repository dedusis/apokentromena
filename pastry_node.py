from pastry_network import prefix_length
from pastry_network import make_id
class PastryNode:
    def __init__(self,network,node_id):
        self.network = network
        self.node_id = node_id
        self.leaf_right = []
        self.leaf_left = []
        id_length = 40 #logw sha-1 pou paragei 40 hex xaraktires panta
        self.routing_table = []
        for i in range (id_length):
            self.routing_table.append([None] * 16 )
        self.data = {}

    def build_leafs(self):
        all_ids = [id for id in self.network.sort_nodes()
                   if id != self.node_id] # afairo apo ola ta ids to id tou node 
        
        my_id = int (self.node_id,16)

        left = []
        right =[]

        for id in all_ids:
            if int (id,16) < my_id:
                left.append(id)
            else:
                right.append(id)

        close = 4 #kontinoi 

        self.leaf_left = left [-close:]
        self.leaf_right = right[:close]

    def build_table(self):
         all_ids = [id for id in self.network.sort_nodes()
                   if id != self.node_id]
         id_length = 40
         self.routing_table=[]
         for i in range(id_length):
            self.routing_table.append([None]*16)
         for id in all_ids:
             row=prefix_length(self.node_id,id)
             if row >= id_length:
                 continue
             col= int (id[row],16)

             if self.routing_table[row][col] is None:
                 self.routing_table[row][col] = id
             
    def next_hop(self,target):
        close_nodes = self.leaf_right + [self.node_id] + self.leaf_left
        if len(close_nodes) > 1 :
            target_number = int(target,16)
            closest = close_nodes[0]
            min_distance = abs(int(closest,16)-target_number)

            for i in close_nodes[1:]:
                distance = abs(int(i,16)-target_number)
                if distance < min_distance:
                    closest = i
                    min_distance = distance
            
            values = [int(x,16) for x in close_nodes]# gia na doume an to target einai entos tou leaf set
            if min(values) <= target_number <= max(values):
                return closest
            
        match = prefix_length(self.node_id,target)# alliw koitame ton prefix pinaka
        if match < len(self.node_id):
                    digit = int(target[match],16)
                    next_node = self.routing_table[match][digit]
                    if next_node is not None:
                        return next_node
        return self.node_id
    def insert(self, key, value):
        key_id = make_id(str(key))
        dest_id, hops = self.network.route(self.node_id, key_id)

        dest_node = self.network.nodes[dest_id]
        k = str(key)

        if k not in dest_node.data:
            dest_node.data[k] = []
        dest_node.data[k].append(value)

        return dest_id, hops


    def find_key(self, key):
        key_id = make_id(str(key))
        dest_id, hops = self.network.route(self.node_id, key_id)

        dest_node = self.network.nodes[dest_id]
        value = dest_node.data.get(str(key))

        return value, dest_id, hops

    def delete(self, key):
        key_id = make_id(str(key))
        dest_id, hops = self.network.route(self.node_id, key_id)

        dest_node = self.network.nodes[dest_id]
        existed = str(key) in dest_node.data
        dest_node.data.pop(str(key), None)

        return existed, dest_id, hops

    def update(self, key, value):
        return self.insert(key, value)

             
       
