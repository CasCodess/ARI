#  Artificial Intelligence Assignment

## Search, Optimisation, and Reinforcement Learning

---

## Group Information

**Group Name:
**Members:

---

## Assignment Overview

This project covers four key areas of Artificial Intelligence:

1. Search Algorithms
2. Constraint Satisfaction Problems (CSP)
3. Game Playing (Adversarial Search)
4. Reinforcement Learning

All solutions are implemented in Python and organised into separate folders per question.

---

## Repository Structure

```bash
.
├── QUESTION 1/
│   ├── Question_1_Warehouse_Search.ipynb
│   ├── warehouse_search.py
│   ├── warehouse.txt
│   ├── warehouse_path.png
│   ├── warehouse_path_greedy.png
│   └── README.md
│
├── QUESTION 2/
│   ├── Question2.ipynb
│   ├── telecom_csp_solver.py
│   ├── test_level1.py
│   ├── test_level2.py
│   ├── test_level3.py
│   └── README.md
│
├── QUESTION 3/
│   ├── tictactoe.py
│   ├── runner_gui.py
│   └── README.md
│
├── QUESTION 4/
│   ├── Question4_Sarsa.py
│   └── README.md
│
└── README.md
```

---

# Question 1: Warehouse Search (Informed Search)

### Description

A warehouse robot must navigate from a **start point (A)** to a **goal (B)** while avoiding obstacles.

### Algorithms Used

* Greedy Best-First Search
* A* Search

### Heuristic

Euclidean Distance:

$$
h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}
$$

### Output

* `warehouse_path.png` → A* result
* `warehouse_path_greedy.png` → Greedy result

---

# Question 2: Telecommunication Tower Placement (CSP)

### Description

Place 8 towers on a 10×10 grid while satisfying spatial and terrain constraints.

### Techniques Used

* Backtracking
* Minimum Remaining Values (MRV)
* Forward Checking

### Constraints

* No same row or column
* No adjacent placement (including diagonals)
* No placement on mountain cells

### Test Files

* `test_level1.py` (Easy)
* `test_level2.py` (Medium)
* `test_level3.py` (Hard)

---

# Question 3: Tic Tac Toe (Game Playing)

### Description

Implementation of a Tic Tac Toe AI system.

### Features

* Game logic (`tictactoe.py`)
* GUI interface (`runner_gui.py`)

---

# Question 4: SARSA (Reinforcement Learning)

### Description

Implementation of the SARSA algorithm for learning optimal policies.

---

  How to Run

### Question 1:

```bash
python warehouse_search.py
```

### Question 2:

```bash
python test_level1.py
python test_level2.py
python test_level3.py
```

### Question 3:

```bash
python runner_gui.py
```

### Question 4:

```bash
python Question4_Sarsa.py
```

---

  Final Submission

* Jupyter Notebooks for all questions
* Python implementations
* Visual outputs
* PDF version of notebook *(submitted separately)*
* GitHub repository link

---

## Notes

* Each group member contributed via GitHub commits
* The project follows modular and structured design
* All solutions align with lecture methodologies





