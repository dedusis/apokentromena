import hashlib

def make_id(text: str)-> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()

def id_to_number(h):
    return int (h,16)

def prefix_length(a:str, b:str)->int:
    length = 0
    for i in range(min(len(a),len(b))):
        if a[i]==b[i]:
            length += 1
        else:
            break
    return length



class PastryNetwork:
        
    def __init__(self):
        self.nodes = {}

    def add_node(self,node):
        self.nodes[node.node_id]=node

    def remove_node(self,node_id):
        if node_id in self.nodes:
            del self.nodes[node_id]

    def sort_nodes(self):
        return sorted(self.nodes.keys(), key=lambda x : int(x,16))
    
    def route(self,start_id,target_id):
        current = start_id
        hops = 0
        while True:
            node = self.nodes[current]
            next_node = node.next_hop(target_id)
            if next_node == current:
                break
            current = next_node
            hops += 1
        return current,hops
    
    def rebuild(self):
        for i in self.nodes.values():
            i.build_leafs()

        for i in self.nodes.values():
            i.build_table()
            
    def join(self, node):
        self.add_node(node)
        self.rebuild()

    def leave(self, node_id):
        self.remove_node(node_id)
        self.rebuild()
 

