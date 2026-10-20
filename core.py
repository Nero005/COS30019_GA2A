import math

def heuristic(node, destinations, nodes):
    x1, y1 = nodes[node]
    return min(math.dist((x1, y1), nodes[d]) for d in destinations)

def parse_problem(filename):
    nodes = {}
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
                #looks like "1: (4,1)"
                label, coords  = line.split(":")
                x, y = coords.strip().strip("()").split(",")
                nodes[int(label)] = (int(x), int(y))

    return nodes