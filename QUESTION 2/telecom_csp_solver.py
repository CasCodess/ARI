import matplotlib.pyplot as plt


class Telecom_CSP_Solver:
    def __init__(self, size, mountains):
        self.size = size
        self.mountains = set(mountains)
        self.towers = 8

        self.variables = [f"T{i}" for i in range(1, self.towers + 1)]

        self.domain = {
            var: [(r, c)
                  for r in range(size)
                  for c in range(size)
                  if (r, c) not in self.mountains]
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

        return min(unassigned, key=lambda var: len(self.domain[var]))

    # -------------------------
    # FORWARD CHECKING
    # -------------------------
    def forward_check(self, var, value):
        new_domain = {}

        for v in self.variables:
            if v != var:
                new_domain[v] = [
                    cell for cell in self.domain[v]
                    if self.is_consistent({var: value}, cell)
                ]

                if not new_domain[v]:
                    return None

        return new_domain

    # -------------------------
    # BACKTRACKING
    # -------------------------
    def backtrack(self, assignment):
        if len(assignment) == self.towers:
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.domain[var]:

            if self.is_consistent(assignment, value):

                assignment[var] = value

                old_domain = self.domain
                new_domain = self.forward_check(var, value)

                if new_domain is not None:
                    self.domain = new_domain

                    result = self.backtrack(assignment)
                    if result:
                        return result

                assignment.pop(var)
                self.domain = old_domain

        return None


# -------------------------
# VISUALISATION FUNCTION
# -------------------------
def draw_grid(solution, mountains):
    size = 10
    fig, ax = plt.subplots()

    for i in range(size + 1):
        ax.plot([0, size], [i, i], 'k')
        ax.plot([i, i], [0, size], 'k')

    for (r, c) in mountains:
        ax.text(c + 0.5, size - r - 0.5, "M",
                ha='center', va='center',
                color='brown', fontsize=12, fontweight='bold')

    for (var, (r, c)) in solution.items():
        ax.text(c + 0.5, size - r - 0.5, "T",
                ha='center', va='center',
                color='blue', fontsize=12, fontweight='bold')

    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Telecom CSP Tower Placement")

    plt.show()


# -------------------------
# MAIN RUN FUNCTION
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