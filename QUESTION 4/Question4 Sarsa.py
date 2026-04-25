import random
from collections import defaultdict

ACTIONS = ["north", "south", "east", "west"]

DIRS = {
    "north": (-1, 0),
    "south": (1, 0),
    "east": (0, 1),
    "west": (0, -1),
}

class GridworldSARSA:
    def __init__(self, n_rows=5, n_cols=5, gamma=0.9, alpha=0.1, epsilon=0.2, episodes=5000):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.episodes = episodes

        self.special_rewards = {"A": 10, "B": 5}
        
        self.state_A = (0, 0)
        self.state_B = (0, 4)

        # Q(s,a)
        self.Q = defaultdict(float)

    def in_bounds(self, r, c):
        return 0 <= r < self.n_rows and 0 <= c < self.n_cols

    def reward_and_next_state(self, state, action):
        """
        Deterministic transition:
        - If action would take agent off-grid:
            reward = -1, next_state = state
        - Otherwise:
            reward = special reward if next_state is A or B, else 0
        """
        r, c = state
        dr, dc = DIRS[action]
        nr, nc = r + dr, c + dc

        if not self.in_bounds(nr, nc):
            return -1, state

        next_state = (nr, nc)

        if next_state == self.state_A:
            return self.special_rewards["A"], next_state
        if next_state == self.state_B:
            return self.special_rewards["B"], next_state

        return 0, next_state

    def epsilon_greedy_action(self, state):
        """Choose action using epsilon-greedy w.r.t Q."""
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)
       
        qs = [self.Q[(state, a)] for a in ACTIONS]
        max_q = max(qs)
        best_actions = [a for a in ACTIONS if self.Q[(state, a)] == max_q]
        return random.choice(best_actions)

    def train_sarsa(self, verbose=False):
        states = [(r, c) for r in range(self.n_rows) for c in range(self.n_cols)]

        for ep in range(self.episodes):
            
            s = random.choice(states)

            a = self.epsilon_greedy_action(s)

            
            horizon = self.n_rows * self.n_cols * 2

            for _ in range(horizon):
                r, s2 = self.reward_and_next_state(s, a)
                a2 = self.epsilon_greedy_action(s2)

                # SARSA update:
              
                old = self.Q[(s, a)]
                target = r + self.gamma * self.Q[(s2, a2)]
                self.Q[(s, a)] = old + self.alpha * (target - old)

                s, a = s2, a2

            if verbose and (ep + 1) % 1000 == 0:
                print(f"Episode {ep+1}/{self.episodes} done.")

    def compute_value_function(self):
        """V(s)=max_a Q(s,a)."""
        V = [[0.0 for _ in range(self.n_cols)] for _ in range(self.n_rows)]
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                s = (r, c)
                V[r][c] = max(self.Q[(s, a)] for a in ACTIONS)
        return V

    def compute_policy_arrows(self):
        """
        Return arrows for each cell indicating optimal actions.
        If multiple actions are equally optimal, we keep multiple arrows.
        """
        arrow_map = {
            "north": "↑",
            "south": "↓",
            "west": "←",
            "east": "→"
        }

        policy = [["" for _ in range(self.n_cols)] for _ in range(self.n_rows)]
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                s = (r, c)
                qs = {a: self.Q[(s, a)] for a in ACTIONS}
                max_q = max(qs.values())
                best = [a for a in ACTIONS if qs[a] == max_q]

              
                policy[r][c] = " ".join(arrow_map[a] for a in best) #Joining Arrrows here  
        return policy


def format_value_grid(V):
   
    for row in V:
        print(" ".join(f"{x:.2f}" for x in row))

def print_policy(policy):
    #  grid print
    for row in policy:
        print("  ".join(cell if cell != "" else "·" for cell in row))


if __name__ == "__main__":
    print("Initializing Gridworld...")
    env = GridworldSARSA(
        n_rows=5,
        n_cols=5,
        gamma=0.9,
        alpha=0.1,
        epsilon=0.2,
        episodes=5000
    )

    print("Grid size:", f"{env.n_rows}x{env.n_cols}")
    print("\nSpecial_rewards =", {"A": 10, "B": 5})
    print(f"Starting Q-learning with parameters:\nγ = {env.gamma}\nα = {env.alpha}")

    print(f"Episodes = {env.episodes}\n")
    env.train_sarsa(verbose=True)

    print("Evaluating optimal value function and policy...")
    V = env.compute_value_function()
    policy = env.compute_policy_arrows()

    print("\nOptimal Value Function:")
    format_value_grid(V)

    print("\nOptimal Policy (arrows):")
    print_policy(policy)
