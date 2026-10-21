import sys
import importlib
import matplotlib.pyplot as plt
from core import parse_problem
from search import METHODS

RAD = 0.1  # how much two-way edges curve apart

def draw(nodes, graph, origin, destinations, path, title, out):
    fig, ax = plt.subplots(figsize=(7, 7))

    # edges: gray normally, red and thick if on the found path
    for a in graph:
        for b, cost in graph[a]:
            x1, y1 = nodes[a]
            x2, y2 = nodes[b]
            on_path = (a in path and b in path
                       and path.index(b) == path.index(a) + 1)
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->",
                                        color="red" if on_path else "gray",
                                        lw=3 if on_path else 1,
                                        shrinkA=14, shrinkB=14,
                                        connectionstyle="arc3,rad=" + str(RAD)))
            # edge cost label, placed on the curve
            lx = (x1 + x2) / 2 + 0.5 * RAD * (y2 - y1)
            ly = (y1 + y2) / 2 - 0.5 * RAD * (x2 - x1)
            ax.text(lx, ly, str(cost), fontsize=8, ha="center", va="center",
                    bbox=dict(facecolor="white", edgecolor="none", pad=1))

    # nodes: green = origin, orange = destination, pink = on path
    for n, (x, y) in nodes.items():
        if n == origin:
            colour = "lightgreen"
        elif n in destinations:
            colour = "orange"
        elif n in path:
            colour = "lightpink"
        else:
            colour = "lightgray"
        ax.scatter(x, y, s=700, c=colour, edgecolors="black", zorder=3)
        ax.text(x, y, str(n), ha="center", va="center", fontweight="bold", zorder=4)

    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)
    ax.set_title(title)
    xs = [p[0] for p in nodes.values()]
    ys = [p[1] for p in nodes.values()]
    ax.set_xlim(min(xs) - 1, max(xs) + 1)
    ax.set_ylim(min(ys) - 1, max(ys) + 1)
    plt.savefig(out, dpi=150)   # saved image can go into the report
    plt.show()

def main():
    if len(sys.argv) != 3:
        print("Usage: python visualize.py <filename> <method>")
        return
    filename = sys.argv[1]
    method = sys.argv[2].upper()
    if method not in METHODS:
        print("Unknown method: " + method)
        return

    nodes, graph, origin, destinations = parse_problem(filename)
    algorithm = importlib.import_module(METHODS[method])
    goal, nodes_created, path = algorithm.search(nodes, graph, origin, destinations)

    title = method + ": goal " + str(goal) + ", nodes created " + str(nodes_created)
    draw(nodes, graph, origin, destinations, path, title, "vis_" + method + ".png")

main()