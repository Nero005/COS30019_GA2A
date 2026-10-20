import heapq
import math
import sys
 
def heuristic(node, destinations, nodes):
    x1, y1 = nodes[node]
    return min(math.dist((x1, y1), nodes[d]) for d in destinations)
 
def parse_problem(filename):
    nodes = {}          # node number: (x, y)
    edges = {}          # node number: list of (neighbour, cost)
    origin = None
    destinations = []
    section = None
 
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
 
            # a heading line switches which section we are reading
            if line == "Nodes:":
                section = "nodes"
            elif line == "Edges:":
                section = "edges"
            elif line == "Origin:":
                section = "origin"
            elif line == "Destinations:":
                section = "destinations"
 
            # a data line, handled by whichever section we are in
            elif section == "nodes":
                # looks like "1: (4,1)"
                label, coords = line.split(":")
                x, y = coords.strip().strip("()").split(",")
                nodes[int(label)] = (int(x), int(y))
 
            elif section == "edges":
                # looks like "(2,1): 4"
                pair, cost = line.split(":")
                a, b = pair.strip().strip("()").split(",")
                edges.setdefault(int(a), []).append((int(b), int(cost)))
 
            elif section == "origin":
                # looks like "2"
                origin = int(line)
 
            elif section == "destinations":
                # looks like "5; 4"
                destinations = [int(d) for d in line.split(";")]
 
    return nodes, edges, origin, destinations

def gbfs(nodes, edges, origin, destinations):
    counter = 0          # insertion order, for chronological tie-breaking
    created = 1          # the root counts as a created node
    frontier = [(heuristic(origin, destinations, nodes), origin, counter, [origin])]
 
    while frontier:
        h, node, _, path = heapq.heappop(frontier)
 
        if node in destinations:
            return node, created, path
 
        for nxt, _cost in sorted(edges.get(node, [])):
            if nxt in path:
                continue
            counter += 1
            created += 1
            heapq.heappush(
                frontier,
                (heuristic(nxt, destinations, nodes), nxt, counter, path + [nxt]),
            )
    return None

def search():
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        return
    filename, method = sys.argv[1], sys.argv[2].upper()
 
    nodes, edges, origin, destinations = parse_problem(filename)
 
    if method != "GBFS":
        print(f"Method {method} not implemented in this file.")
        return
 
    result = gbfs(nodes, edges, origin, destinations)
    print(f"{filename} {method}")
    if result is None:
        print("No goal is reachable; 0")
    else:
        goal, created, path = result
        print(f"{goal} {created}")
        print(" ".join(map(str, path)))

if __name__ == "__main__":
    search()