import heapq
from core import heuristic, parse_problem

def search(nodes, graph, origin, destinations):
    order = 0             # creation order, used to break ties
    nodes_created = 1     # the origin counts as created
    g = 0
    f = g + heuristic(origin, destinations, nodes)

    # each entry: (f, node, order, g, path)
    frontier = [(f, origin, order, g, [origin])]

    entry = heapq.heappop(frontier)
    print(entry)

if __name__ == "__main__":
    nodes = parse_problem("tests/test_01.txt")
    search(nodes, {}, 2, [5, 4])