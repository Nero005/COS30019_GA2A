import re
import sys


def parse_problem(filename):
    nodes = {}   #node (x, y)
    edges = {}   #node (neighbour, cost)
    origin = None
    destinations = []
    section = None

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Nodes:"):
                section = "nodes"
            elif line.startswith("Edges:"):
                section = "edges"
            elif line.startswith("Origin:"):
                section = "origin"
            elif line.startswith("Destinations:"):
                section = "dest"
            elif section == "nodes": 
                n, x, y = map(int, re.findall(r"\d+", line))
                nodes[n] = (x, y)
            elif section == "edges": 
                a, b, cost = map(int, re.findall(r"\d+", line))
                edges.setdefault(a, []).append((b, cost))
            elif section == "origin":
                origin = int(line)
            elif section == "dest": 
                destinations = [int(d) for d in line.split(";")]
    return nodes, edges, origin, destinations


def dfs(nodes, edges, origin, destinations):

    created = 1                      #1 for origin
    frontier = [[origin]]            #stack, each entry is a full path

    while frontier:
        path = frontier.pop()        #newest = deepest
        node = path[-1]

        if node in destinations:
            return node, created, path

        for nxt, _cost in reversed(sorted(edges.get(node, []))):
            if nxt in path:          #avoid cycles along branch
                continue
            created += 1
            frontier.append(path + [nxt])

    return None, created, None


def main():
    if len(sys.argv) != 2:
        print("Usage: python dfs.py <filename>")
        return
    filename = sys.argv[1]

    nodes, edges, origin, destinations = parse_problem(filename)
    goal, created, path = dfs(nodes, edges, origin, destinations)

    print(f"{filename} DFS")
    if goal is None:
        print(f"No goal is reachable; {created}")
    else:
        print(f"{goal} {created}")
        print(" ".join(map(str, path)))


if __name__ == "__main__":
    main()
