# Warehouse Logistics Bot – Search Algorithms

## Course Information

- **Course:** Artificial Intelligence (ARI711S)
- **Assignment:** 1

---

## Project Overview

This project simulates an **Automated Guided Vehicle (AGV)** navigating a warehouse grid from a **start point (A)** to a **goal (B)**.

The system compares two **informed search algorithms**:

- 🔹 **Greedy Best-First Search**
- 🔹 **A\* Search**

The goal is to evaluate:

- Path length
- Number of explored states
- Efficiency vs optimality

---

## Algorithms Explained

### Greedy Best-First Search

- Uses only the heuristic: `h(n)`
- Chooses the node closest to the goal
- Fast, but not always optimal

### A\* Search

- Uses: `f(n) = g(n) + h(n)`
- Combines actual cost + estimated cost
- Guarantees the shortest path

---

## Heuristic Function

Euclidean Distance:

h(n) = √((x₁ - x₂)² + (y₁ - y₂)²)

---

## Project Structure

```
ARI/
│── Question_1_Warehouse_Search.ipynb
│── warehouse_search.py
│── warehouse.txt
│── warehouse_path.png
│── warehouse_path_greedy.png
│── README.md
```

---

## ▶️ How to Run

### Option 1: Jupyter Notebook

1. Open the notebook:

   ```
   Question_1_Warehouse_Search.ipynb
   ```

2. Click **Run All**

---

### Option 2: Python Script

```bash
python warehouse_search.py
```

---

## Test Cases

The system includes:

- Straight-line navigation
- Blocked path (no solution)
- Adjacent start & goal
- Greedy vs A\* comparison

---

## Output

The program generates visualizations:

- 🟩 Start (A)
- 🟥 Goal (B)
- 🟨 Optimal Path
- 🟦 Explored Nodes
- ⬛ Walls

---

## Key Findings

- Greedy is faster but may produce longer paths
- A\* explores more nodes but guarantees optimal results
- Euclidean heuristic ensures A\* optimality

---

## Author

- **Name:**
- **Program:**

---

## Notes

This project demonstrates practical implementation of **search algorithms in AI**, including:

- State space representation
- Heuristic design
- Pathfinding optimization
- Visualization of search processes

---
