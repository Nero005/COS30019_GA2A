import re
import sys


def parse_problem(filename):
    """Read the problem file -> (nodes, edges, origin, destinations)."""
    nodes = {}   # node id -> (x, y)
    edges = {}   # node id -> list of (neighbour, cost)
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
            elif section == "nodes":            # e.g. 1: (4,1)
                n, x, y = map(int, re.findall(r"\d+", line))
                nodes[n] = (x, y)
            elif section == "edges":            # e.g. (2,1): 4
                a, b, cost = map(int, re.findall(r"\d+", line))
                edges.setdefault(a, []).append((b, cost))
            elif section == "origin":
                origin = int(line)
            elif section == "dest":             # e.g. 5; 4
                destinations = [int(d) for d in line.split(";")]
    return nodes, edges, origin, destinations


def dfs(nodes, edges, origin, destinations):

    created = 1                      # root counts as a created node
    frontier = [[origin]]            # stack; each entry is a full path

    while frontier:
        path = frontier.pop()        # newest = deepest
        node = path[-1]

        if node in destinations:
            return node, created, path

        for nxt, _cost in reversed(sorted(edges.get(node, []))):
            if nxt in path:          # avoid cycles along this branch
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
