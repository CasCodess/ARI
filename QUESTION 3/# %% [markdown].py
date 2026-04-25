# %% [markdown]
# # Question 2 – CSP Telecommunication Tower Placement
# This notebook solves a Constraint Satisfaction Problem (CSP) using Backtracking, MRV, and Forward Checking.

# %%
import matplotlib.pyplot as plt

# %%

class Telecom_CSP_Solver:
    def __init__(self, size, mountains):
        self.size = size
        self.mountains = set(mountains)
        self.towers = 8

        self.variables = [f"T{i}" for i in range(1, self.towers + 1)]

        self.domain = {
            var: [
                (r, c)
                for r in range(size)
                for c in range(size)
                if (r, c) not in self.mountains
            ]
            for var in self.variables
        }

    def is_consistent(self, assignment, cell):
        r, c = cell

        for (ar, ac) in assignment.values():
            if ar == r or ac == c:
                return False
            if abs(ar - r) <= 1 and abs(ac - c) <= 1:
                return False

        return True

    def select_unassigned_variable(self, assignment):
        unassigned = [v for v in self.variables if v not in assignment]

        def score(var):
            return len(self.domain[var])

        return min(unassigned, key=score)

    def forward_check(self, assignment):
        new_domain = {}

        for var in self.variables:
            if var not in assignment:
                filtered = [
                    cell for cell in self.domain[var]
                    if self.is_consistent(assignment, cell)
                ]

                if not filtered:
                    return None

                new_domain[var] = filtered

        return new_domain

    def backtrack(self, assignment):
        if len(assignment) == self.towers:
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.domain[var]:
            if self.is_consistent(assignment, value):
                assignment[var] = value

                new_domain = self.forward_check(assignment)

                if new_domain is not None:
                    old_domain = self.domain
                    self.domain = new_domain

                    result = self.backtrack(assignment)

                    if result:
                        return result

                    self.domain = old_domain

                del assignment[var]

        return None


# %%

def draw_grid(solution, mountains):
    size = 10
    fig, ax = plt.subplots()

    for i in range(size + 1):
        ax.plot([0, size], [i, i], 'k')
        ax.plot([i, i], [0, size], 'k')

    for (r, c) in mountains:
        ax.text(c + 0.5, size - r - 0.5, "M",
                ha='center', va='center',
                color='brown', fontweight='bold')

    for var, (r, c) in solution.items():
        ax.text(c + 0.5, size - r - 0.5, "T",
                ha='center', va='center',
                color='blue', fontweight='bold')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("CSP Tower Placement")

    plt.show()


# %%

def solve(mountains):
    solver = Telecom_CSP_Solver(10, mountains)
    solution = solver.backtrack({})

    if solution:
        print("Solution Found:\n")
        for k, v in solution.items():
            print(k, "->", v)

        draw_grid(solution, mountains)
    else:
        print("No solution found")


# %%
solve([(0,0),(1,1),(9,9)])

# %%
solve([(2,2),(2,3),(3,2),(3,3),(7,8),(8,7),(8,8)])

# %%

solve([
    (0,5),(1,5),(2,5),(3,5),(4,5),
    (5,0),(5,1),(5,2),(5,3),(5,4)
])



