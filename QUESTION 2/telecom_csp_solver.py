import matplotlib.pyplot as plt


class Telecom_CSP_Solver:
    def __init__(self, size, mountains):
        self.size = size
        self.mountains = set(mountains)
        self.towers = 8

        self.variables = [f"T{i}" for i in range(1, self.towers + 1)]

        # Domain: all valid cells excluding mountains
        self.domain = {
            var: [
                (r, c)
                for r in range(size)
                for c in range(size)
                if (r, c) not in self.mountains
            ]
            for var in self.variables
        }

    # -------------------------
    # CONSTRAINT CHECK
    # -------------------------
    def is_consistent(self, assignment, cell):
        r, c = cell

        for (ar, ac) in assignment.values():

            # same row or column
            if ar == r or ac == c:
                return False

            # adjacency + diagonal restriction
            if abs(ar - r) <= 1 and abs(ac - c) <= 1:
                return False

        return True

    # -------------------------
    # MRV HEURISTIC
    # -------------------------
def select_unassigned_variable(self, assignment):
    unassigned = [v for v in self.variables if v not in assignment]

    # MRV + Degree heuristic (tie-breaker)
    def score(var):
        return (len(self.domain[var]),
                -sum(1 for v in self.variables if v not in assignment))

    return min(unassigned, key=score)

    # -------------------------
    # FORWARD CHECKING (FIXED)
    # -------------------------
def forward_check(self, assignment):
    new_domain = {}

    for var in self.variables:
        if var not in assignment:
            filtered = []

            for cell in self.domain[var]:
                if self.is_consistent(assignment, cell):
                    filtered.append(cell)

            if not filtered:
                return None

            new_domain[var] = filtered

    return new_domain

    # -------------------------
    # BACKTRACKING SEARCH
    # -------------------------
    def backtrack(self, assignment):

        if len(assignment) == self.towers:
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.domain[var]:

            if self.is_consistent(assignment, value):

                # assign
                assignment[var] = value

                # forward checking with updated assignment
                new_domain = self.forward_check(assignment)

                if new_domain is not None:
                    old_domain = self.domain
                    self.domain = new_domain

                    result = self.backtrack(assignment)

                    if result:
                        return result

                    self.domain = old_domain

                # undo assignment
                del assignment[var]

        return None


# -------------------------
# VISUALISATION
# -------------------------
def draw_grid(solution, mountains):
    size = 10
    fig, ax = plt.subplots()

    # grid lines
    for i in range(size + 1):
        ax.plot([0, size], [i, i], 'k')
        ax.plot([i, i], [0, size], 'k')

    # mountains
    for (r, c) in mountains:
        ax.text(
            c + 0.5, size - r - 0.5, "M",
            ha='center', va='center',
            color='brown', fontsize=12, fontweight='bold'
        )

    # towers
    for var, (r, c) in solution.items():
        ax.text(
            c + 0.5, size - r - 0.5, "T",
            ha='center', va='center',
            color='blue', fontsize=12, fontweight='bold'
        )

    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Telecom CSP Tower Placement (10x10 Grid)")

    plt.show()


# -------------------------
# SOLVE FUNCTION
# -------------------------
def solve(mountains):
    solver = Telecom_CSP_Solver(10, mountains)
    solution = solver.backtrack({})

    if solution:
        print("\nSolution Found:\n")
        for k, v in solution.items():
            print(f"{k} -> {v}")

        draw_grid(solution, mountains)
    else:
        print("No solution found")