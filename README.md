# CaterIQ — AI Search Engine & Catering Intelligence Studio

> **Course:** Artificial Intelligence Lab (Semester Project)  
> **Student:** Rayyan Mustafa  
> **Registration Number:** 2312335  
> **Scope:** Weeks 1–5 Uninformed Search (BFS & DFS)  
> **Tech Stack:** 100% Pure Python (No SQL/Databases, No JavaScript, No Complex ORMs)  

---

## 🌟 Project Overview

**CaterIQ** is a pure Python application developed for the Artificial Intelligence Lab semester project. It formulates and solves real-world catering optimization challenges using classical **uninformed state-space search algorithms**:

| Real-World Problem | Course Topic | Algorithm | Data Structure |
|---|---|---|---|
| **Allergen Safe-Path Finder**<br>Find the minimal number of ingredient swaps to make a recipe safe for allergic guests. | Uninformed Search (Lab 04) | **Breadth-First Search (BFS)** | FIFO Queue (`collections.deque`) + Visited Set |
| **Menu Constraint Solver**<br>Assemble a 3-course package (Starter, Main, Dessert) within budget and dietary limits. | Uninformed Search (Lab 05) | **Depth-First Search (DFS) with Pruning** | LIFO Stack (`list.pop()`) + Branch-and-Bound Pruning |

---

## 📁 Repository Structure

```text
CaterIQ/
├── streamlit_app.py           # Streamlit Pure Python Interactive UI
├── data.py                    # In-memory domain knowledge graph (Lists & Dictionaries)
├── requirements.txt           # Minimal dependency: streamlit
├── ai_engine/
│   ├── search/
│   │   ├── core.py            # Problem, Node, SearchResult base classes
│   │   ├── bfs.py             # Breadth-First Search implementation
│   │   └── dfs.py             # Depth-First Search with backtracking and pruning
│   └── problems/
│       ├── allergen_substitution.py # BFS problem formulation
│       └── menu_constraints.py      # DFS problem formulation
└── README.md
```

---

## 🚀 How to Run (1 Single Command)

### 1. Install Dependency
```powershell
pip install -r requirements.txt
```

### 2. Launch the Application
```powershell
streamlit run streamlit_app.py
```
> The application will automatically open in your default browser at **[http://localhost:8501](http://localhost:8501)**.

---

## 🧠 Academic Explanation for the Instructor

### 1. How the Algorithms Connect to Class Topics
- **Weeks 1 & 2 (OOP & Data Structures)**:
  - Formulated in [ai_engine/search/core.py](ai_engine/search/core.py) using the classic Russell & Norvig `Problem` and `Node` abstractions.
  - Domain state space stored in [data.py](data.py) using pure Python `list`, `dict`, `set`, and `tuple`. Zero database overhead.
- **Week 4 (Breadth-First Search)**:
  - Implemented in [ai_engine/search/bfs.py](ai_engine/search/bfs.py).
  - Uses a FIFO queue (`collections.deque`).
  - Applied to the allergen substitution graph in [ai_engine/problems/allergen_substitution.py](ai_engine/problems/allergen_substitution.py).
  - Mathematically guarantees finding the shortest swap chain.
- **Week 5 (Depth-First Search with Pruning)**:
  - Implemented in [ai_engine/search/dfs.py](ai_engine/search/dfs.py).
  - Uses a LIFO stack (`list.pop()`).
  - Applied to 3-course package constraint satisfaction in [ai_engine/problems/menu_constraints.py](ai_engine/problems/menu_constraints.py).
  - Early branch pruning discards branches as soon as partial cost exceeds the budget, drastically reducing node expansions.
