from collections import defaultdict

class Frac:
    def __init__(self,num,den):
        d = gcd(num,den)
        num //= d
        den //= d
        self.num = num
        self.den = den
    
    def power_series(self):
        num = self.den
        den = self.den - self.num
        return Frac(num,den)
        
    def __add__(self,other):
        num = self.num*other.den + other.num*self.den
        den = self.den*other.den
        result = Frac(num,den)
        return result
        
    def __mul__(self,other):
        num = self.num*other.num
        den = self.den*other.den
        result = Frac(num,den)
        return result
    
    def __repr__(self):
        return '{}/{}'.format(self.num,self.den)
        
class Edge:
    def __init__(self,i,j):
        self.source = i
        self.range = j
    
    def __str__(self):
        return '{}->{}'.format(self.source,self.range)
    
    def __hash__(self): 
        return self.__str__().__hash__()
    
    __repr__ = __str__
    
class Trail:
    def __init__(self,edges):
        self.indexOf = {}
        self.edges = tuple(edges)
        self.source = edges[0].source
        self.range = edges[-1].range
        self.nodes = [e.source for e in self.edges]+[self.range]
        for i,edge in enumerate(edges):
            self.indexOf[edge] = i
    
    def add_edge(self,edge):
        new_edges = self.edges + (edge,)
        return Trail(new_edges)
    
    def __hash__(self):
        return self.edges.__hash__()
        
    def __str__(self):
        return self.edges.__str__()
        
    def __repr__(self):
        return self.edges.__repr__()

class Graph:
    def __init__(self,m):
        self.nodes = range(len(m))
        self.edges = {}                # map from edges to probabilities
        self.s_inv = defaultdict(list) # inverse of range map
        self.r_inv = defaultdict(list) # inverse of source map
        for i,row in enumerate(m):
            den = sum(row)             # get denominator for edge probabilities
            if den > 0:
                for j,num in enumerate(row):
                    if num > 0:
                        edge = Edge(i,j) 
                        self.edges[edge] = Frac(num,den)  # Add edge and its probability to edge map
                        self.s_inv[i].append(edge)        # Add edge to s_inv of its source
                        self.r_inv[j].append(edge)        # Add edge to r_inv of its range
        self.terminal_nodes = [node for node in self.nodes if node not in self.s_inv]
    
    def get_circuits(self,root):
        n_edges = len(self.edges)
        trails = [Trail([edge]) for edge in self.s_inv[root]] # Start with single edge trails from root
        circuits = defaultdict(set)
        for _ in range(n_edges): # we know a circuit can't be longer that the total number of edges
            new_trails = []      # At each iteration we start a new list and only add non-circuits
            for trail in trails:
                source = trail.range # start at the end of the trail
                for edge in self.s_inv[source]: # iterate through all edges that extend the trail
                    if edge in trail.edges:     # check if new edge creates a circuit
                        index = trail.indexOf[edge]      # where have we seen this edge before?
                        circuit = trail.edges[index:]    # just take the circuit
                        circuits[source].add(circuit)
                    else:
                        new_trail = trail.add_edge(edge) # extend the trail
                        new_trails.append(new_trail)     # pass trail to the next iteration
            trails = new_trails
        return circuits
    
    def get_terminal_paths(self,root):
        n_nodes = len(self.nodes)
        paths = [Trail([edge]) for edge in self.s_inv[root]] # Start with single edge trails from root
        terminal_paths = [path for path in paths if path.range in self.terminal_nodes] # one edge terminal paths
        for _ in range(n_nodes): # we know a path can't be longer than the total number of nodes
            new_paths = []       # At each iteration we start a new list and only add non-circuits
            for path in paths:
                source = path.range # start at the end of the trail
                for edge in self.s_inv[source]: # iterate through all edges that extend the trail
                    r = edge.range
                    if r not in path.nodes:     # check if new edge creates a cycle
                        new_path = path.add_edge(edge)   # extend the path
                        if r in self.terminal_nodes:          # check if path is terminal
                            terminal_paths.append(new_path)
                        else:
                            new_paths.append(new_path)   # pass path to the next iteration 
            paths = new_paths
        return terminal_paths
    
    def get_circuit_values(self,circuits):
        circuit_values = defaultdict(lambda : Frac(1,1)) # initialize map from nodes to circuit values
        for node, circuit_set in circuits.items():
            total_for_node = Frac(0,1) # initialize value for given node
            for circuit in circuit_set:
                single_loop_val = Frac(1,1) # initialize value for given loop
                for edge in circuit:        # multiply edge values
                    edge_val = self.edges[edge]
                    single_loop_val *= edge_val
                total_loop_val = single_loop_val.power_series() # sum over all possible numbers of loops
                total_for_node += total_loop_val                # add to total node value
            circuit_values[node] = total_for_node
        return circuit_values
        
    def get_path_values(self,paths,circuit_values):
        path_values = defaultdict(lambda : Frac(0,1)) # initialize map from nodes to path values
        for path in paths:
            path_value = Frac(1,1)     # initialize value for path
            for edge in path.edges:    # multiply values for all nodes and edges
                source_value = circuit_values[edge.source] 
                edge_value = self.edges[edge]
                path_value *= source_value*edge_value
            path_values[path.range] += path_value
        return path_values
    
    def get_answer(self):
        circuits = self.get_circuits(0)
        terminal_paths = self.get_terminal_paths(0)
        circuit_values = self.get_circuit_values(circuits)
        path_values = self.get_path_values(terminal_paths,circuit_values)
        answer = common(*[path_values[i] for i in sorted(self.terminal_nodes)])
        return answer

def gcd(a,b):
    while b:
        a,b = b,a%b
    return a
        
def common(*fracs):
    first,rest = fracs[0],fracs[1:]
    if len(fracs)==1:
        return [first.num,first.den]
    common_rest = common(*rest)
    den_rest = common_rest[-1]   # get old denominator
    d = gcd(first.den,den_rest)  # gcd of new denominator and old denominator
    a = den_rest//d              # factor to multiply new numerator by
    b = first.den//d             # factor to multiply old numerators by
    cd = (first.den*den_rest)//d # new common denominator
    nums = [a*first.num]+[b*r for r in common_rest[:-1]]+[cd]
    return nums
    
def answer(m):
    graph = Graph(m)
    answer = graph.get_answer()
    return answer
