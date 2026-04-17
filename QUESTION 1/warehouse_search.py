import heapq
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# ─────────────────────────────────────────────
#  NODE CLASS
# ─────────────────────────────────────────────
class Node:
    """
    Represents a single state in the search tree.

    Attributes:
        state  : (row, col) grid coordinate
        parent : the Node we arrived from (None for the start node)
        action : direction string taken to reach this node
        g      : path cost from the start node to this node (number of steps)
    """

    def __init__(self, state, parent, action, g):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g  # g(n) — cost so far

    # heapq compares elements; if priorities tie we fall back to comparing
    # Nodes, so we need __lt__ to avoid a TypeError.
    def __lt__(self, other):
        return self.g < other.g


# ─────────────────────────────────────────────
#  WAREHOUSE CLASS
# ─────────────────────────────────────────────
class Warehouse:
    """
    Reads and models the warehouse grid, and exposes two informed
    search algorithms: Greedy Best-First Search and A* Search.

    Grid legend (in the .txt file):
        #  – shelving unit / wall (impassable)
        A  – charging station (start)
        B  – product bin (goal)
        ' '– open aisle (passable)
    """

    def __init__(self, filename: str):
        self.walls = set()
        self.start = None
        self.goal = None
        self._parse(filename)

    # ── File Parsing ──────────────────────────
    def _parse(self, filename: str):
        with open(filename) as f:
            lines = f.read().splitlines()

        self.height = len(lines)
        self.width = max(len(line) for line in lines)

        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch == "#":
                    self.walls.add((r, c))
                elif ch == "A":
                    self.start = (r, c)
                elif ch == "B":
                    self.goal = (r, c)

        if self.start is None or self.goal is None:
            raise ValueError("warehouse.txt must contain both 'A' (start) and 'B' (goal).")

        print(f"Parsed warehouse: {self.height} rows × {self.width} cols")
        print(f"  Start (A) : {self.start}")
        print(f"  Goal  (B) : {self.goal}")
        print(f"  Walls     : {len(self.walls)} cells\n")

    # ── Neighbour Expansion ───────────────────
    def neighbors(self, state):
        """
        Returns a list of (action, new_state) tuples for all valid moves
        from *state*. A move is valid when the target cell is inside the
        grid and is not a wall.
        """
        row, col = state
        candidates = [
            ("up",    (row - 1, col)),
            ("down",  (row + 1, col)),
            ("left",  (row,     col - 1)),
            ("right", (row,     col + 1)),
        ]
        return [
            (action, s)
            for action, s in candidates
            if 0 <= s[0] < self.height
            and 0 <= s[1] < self.width
            and s not in self.walls
        ]

    # ── Heuristic: Euclidean Distance ─────────
    def _heuristic(self, state):
        """h(n) = Euclidean distance from *state* to the goal."""
        x1, y1 = state
        x2, y2 = self.goal
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # ── Solve ─────────────────────────────────
    def solve(self, algorithm: str = "astar"):
        """
        Finds the shortest path from start (A) to goal (B).

        Parameters
        ----------
        algorithm : "greedy"  →  priority = h(n)
                    "astar"   →  priority = g(n) + h(n)

        Returns
        -------
        path     : list of (row, col) from start to goal (inclusive)
        explored : set of all (row, col) states that were popped from
                   the frontier during the search
        """
        algorithm = algorithm.lower()
        if algorithm not in ("greedy", "astar"):
            raise ValueError("algorithm must be 'greedy' or 'astar'")

        start_node = Node(state=self.start, parent=None, action=None, g=0)

        # Priority queue: (priority, counter, node)
        # counter breaks ties so Node.__lt__ is rarely needed.
        counter = 0
        frontier = []
        h0 = self._heuristic(self.start)
        priority = h0 if algorithm == "greedy" else 0 + h0
        heapq.heappush(frontier, (priority, counter, start_node))

        explored = set()
        frontier_states = {self.start}  # fast membership test

        while frontier:
            _, _, node = heapq.heappop(frontier)
            frontier_states.discard(node.state)

            # ── Goal test ──
            if node.state == self.goal:
                path = self._reconstruct_path(node)
                print(f"[{algorithm.upper()}] Solution found!")
                print(f"  Path length : {len(path)} steps")
                print(f"  States explored : {len(explored)}\n")
                return path, explored

            # ── Already visited? ──
            if node.state in explored:
                continue
            explored.add(node.state)

            # ── Expand ──
            for action, state in self.neighbors(node.state):
                if state in explored or state in frontier_states:
                    continue
                new_g = node.g + 1
                h = self._heuristic(state)
                priority = h if algorithm == "greedy" else new_g + h
                counter += 1
                child = Node(state=state, parent=node, action=action, g=new_g)
                heapq.heappush(frontier, (priority, counter, child))
                frontier_states.add(state)

        print(f"[{algorithm.upper()}] No solution found.")
        return None, explored

    # ── Path Reconstruction ───────────────────
    def _reconstruct_path(self, node):
        """Walk parent pointers back to the start and reverse."""
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    # ── Visualisation ─────────────────────────
    def visualize(self, path, explored, filename="warehouse_path.png", algorithm="astar"):
        """
        Exports a colour-coded PNG of the warehouse.

        Colour legend
        -------------
        Black       – shelving units (walls)
        White       – open aisles (unexplored)
        Light blue  – explored states (not on final path)
        Yellow      – optimal path
        Green       – start (A)
        Red         – goal  (B)
        """
        # Build a numeric grid: 0=open, 1=wall, 2=explored, 3=path, 4=start, 5=goal
        grid = np.zeros((self.height, self.width), dtype=int)

        for (r, c) in self.walls:
            grid[r, c] = 1
        if explored:
            for (r, c) in explored:
                if grid[r, c] == 0:
                    grid[r, c] = 2
        if path:
            for (r, c) in path:
                grid[r, c] = 3
        if self.start:
            grid[self.start[0], self.start[1]] = 4
        if self.goal:
            grid[self.goal[0], self.goal[1]] = 5

        # Custom colour map
        cmap = plt.cm.colors.ListedColormap([
            "white",       # 0 – open aisle
            "#2b2b2b",     # 1 – wall
            "#aed6f1",     # 2 – explored
            "#f9e547",     # 3 – optimal path
            "#27ae60",     # 4 – start A
            "#e74c3c",     # 5 – goal  B
        ])

        fig, ax = plt.subplots(figsize=(max(8, self.width * 0.5),
                                        max(6, self.height * 0.5)))
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=5, interpolation="nearest")

        # Label A and B
        ax.text(self.start[1], self.start[0], "A", ha="center", va="center",
                fontsize=9, fontweight="bold", color="white")
        ax.text(self.goal[1], self.goal[0], "B", ha="center", va="center",
                fontsize=9, fontweight="bold", color="white")

        # Grid lines
        ax.set_xticks(np.arange(-0.5, self.width, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.height, 1), minor=True)
        ax.grid(which="minor", color="grey", linewidth=0.3)
        ax.tick_params(which="both", bottom=False, left=False,
                       labelbottom=False, labelleft=False)

        # Legend
        patches = [
            mpatches.Patch(color="#27ae60",  label="Start (A)"),
            mpatches.Patch(color="#e74c3c",  label="Goal (B)"),
            mpatches.Patch(color="#f9e547",  label="Optimal path"),
            mpatches.Patch(color="#aed6f1",  label="Explored (not on path)"),
            mpatches.Patch(color="#2b2b2b",  label="Shelving unit (wall)"),
            mpatches.Patch(color="white",    label="Open aisle", ec="grey"),
        ]
        ax.legend(handles=patches, loc="upper right",
                  fontsize=7, framealpha=0.9)

        ax.set_title(
            f"Warehouse AGV Navigation – {algorithm.upper()}\n"
            f"Path length: {len(path) if path else 'N/A'} steps  |  "
            f"States explored: {len(explored)}",
            fontsize=10
        )

        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Image saved → {filename}")


# ─────────────────────────────────────────────
#  MAIN — run both algorithms and compare
# ─────────────────────────────────────────────
if __name__ == "__main__":
    WAREHOUSE_FILE = "warehouse.txt"

    wh = Warehouse(WAREHOUSE_FILE)

    # ── Greedy Best-First Search ──
    print("=" * 50)
    print("Running: GREEDY BEST-FIRST SEARCH")
    print("=" * 50)
    greedy_path, greedy_explored = wh.solve(algorithm="greedy")
    wh.visualize(greedy_path, greedy_explored,
                 filename="warehouse_path_greedy.png",
                 algorithm="greedy")

    # ── A* Search ──
    print("=" * 50)
    print("Running: A* SEARCH")
    print("=" * 50)
    astar_path, astar_explored = wh.solve(algorithm="astar")
    wh.visualize(astar_path, astar_explored,
                 filename="warehouse_path.png",
                 algorithm="astar")

    # ── Comparison ──
    print("=" * 50)
    print("COMPARISON SUMMARY")
    print("=" * 50)
    print(f"{'Algorithm':<12} {'Path Length':>12} {'States Explored':>16}")
    print("-" * 42)
    gl = len(greedy_path) if greedy_path else "N/A"
    ge = len(greedy_explored)
    al = len(astar_path) if astar_path else "N/A"
    ae = len(astar_explored)
    print(f"{'Greedy':<12} {str(gl):>12} {str(ge):>16}")
    print(f"{'A*':<12} {str(al):>12} {str(ae):>16}")
