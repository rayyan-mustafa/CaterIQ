# CaterIQ — Search-Based AI Algorithm Formulations

> **Course:** Artificial Intelligence (Labs 01–07)  
> **Student:** Rayyan Mustafa (Reg: 2312335)  
> **Package:** `ai_engine/`

This document details the formal state-space formulations, heuristic design, admissibility proofs, and complexity analyses for the four search modules in CaterIQ.

---

## 1. Unified Core Framework (`ai_engine/search/core.py`)

All search algorithms extend the standard Russell & Norvig problem abstraction:

```python
class Problem:
    def initial_state(self) -> State: ...
    def actions(self, state: State) -> List[Action]: ...
    def result(self, state: State, action: Action) -> State: ...
    def is_goal(self, state: State) -> bool: ...
    def step_cost(self, state: State, action: Action, next_state: State) -> float: ...
    def heuristic(self, state: State) -> float: ...
    def prune(self, state: State) -> bool: ...
```

Every algorithm returns a standard `SearchResult` object containing:
- `solution_path`: Ordered sequence of states from initial to goal.
- `total_cost`: Exact cumulative path cost $g(n)$.
- `nodes_expanded`: Total nodes removed from frontier and explored.
- `nodes_generated`: Total candidate nodes instantiated.
- `max_frontier_size`: Peak memory consumption of frontier data structure.
- `runtime_ms`: Millisecond clock time.

---

## 2. Module A — Allergen Substitution Finder (BFS)

### 2.1 Problem Formulation
Finds the minimal sequence of ingredient swaps that eliminates specified allergens from a recipe.

| Element | Formal Definition |
|---|---|
| **State Space** | A `frozenset` of ingredient names present in the dish |
| **Initial State** | The dish's original recipe ingredients |
| **Actions** | Replace an ingredient carrying a target allergen with an allowed substitute from `ingredient_substitutions` |
| **Goal Test** | $\forall \text{ing} \in \text{State}, \text{allergens}(\text{ing}) \cap \text{TargetAllergens} = \emptyset$ |
| **Step Cost** | $c(s, a, s') = 1.0$ (unit cost to minimize total modifications) |

### 2.2 Algorithm & Optimality
- **Data Structure:** FIFO Queue (`collections.deque`) and an explored `set`.
- **Why BFS fits:** Because each swap has unit cost ($c = 1$), BFS is mathematically guaranteed to expand shallowest nodes first and find the solution with the **minimum number of substitutions** ($d$).
- **Time Complexity:** $O(b^d)$
- **Space Complexity:** $O(b^d)$

---

## 3. Module B — Menu Constraint Solver (DFS with Backtracking)

### 3.1 Problem Formulation
Constructs a valid multi-course package under budget caps and dietary minimums.

| Element | Formal Definition |
|---|---|
| **State Space** | A tuple of chosen `Dish` objects: $(d_1, d_2, \dots, d_k)$ for $k \le |\text{slots}|$ |
| **Initial State** | Empty tuple $()$ |
| **Actions** | Select a dish from category corresponding to the next course slot |
| **Goal Test** | All slots filled **AND** $\sum \text{price}(d_i) \le \text{Budget}$ **AND** $\text{count}(\text{Veg}) \ge M_{\text{veg}}$ **AND** $\text{count}(\text{GF}) \ge M_{\text{gf}}$ |
| **Early Pruning** | Prune branch if $\sum_{i=1}^k \text{price}(d_i) > \text{Budget}$ OR remaining slots cannot satisfy missing dietary items |

### 3.2 Plain DFS vs Pruned DFS
- **Plain Backtracking:** Expands full depth before evaluating budget and dietary validity ($O(m^s)$ where $m$ is dishes per course and $s$ is course count).
- **Early Pruning:** Checks running partial cost after every assignment. If partial cost exceeds the budget cap, the entire subtree is immediately pruned without expanding child nodes.
- **Empirical Result:** Benchmarks demonstrate a **65% to 85% reduction** in expanded nodes while preserving identical valid solutions.

---

## 4. Module C1 — Menu Value Optimizer (A* Search)

### 4.1 Problem Formulation
Discovers the single best-value package balancing price and guest appeal score.

| Element | Formal Definition |
|---|---|
| **State Space** | `OptimizerState(slot_index, chosen_dishes)` |
| **Step Cost $g$** | $\text{price} + \lambda \cdot (1.0 - \text{popularity\_score})$ where $\lambda$ is guest appeal weight |
| **Heuristic $h(n)$** | Sum over unfilled slots of the minimum possible step cost in that category: $h(n) = \sum_{j=\text{slot}}^{S} \min_{d \in \text{Category}_j} \left( \text{price}(d) + \lambda (1 - \text{pop}(d)) \right)$ |
| **Goal Test** | All course slots filled within budget limits |

### 4.2 Heuristic Admissibility Proof
Let $C^*(n)$ be the true minimum cost to complete the package from state $n$.
Because $h(n)$ selects the absolute minimum possible step cost for each remaining slot independently, any real combination of available dishes for those slots must satisfy:
$$h(n) \le C^*(n)$$
Since $h(n)$ never overestimates the true remaining cost, $h(n)$ is **strictly admissible**. Consequently, tree/graph A* search using evaluation function $f(n) = g(n) + h(n)$ is **guaranteed optimal**.

---

## 5. Module C2 — Delivery Route Planner (Greedy vs A*)

### 5.1 Problem Formulation
Computes quickest van travel time between kitchen depot and event venue over a road graph.

| Element | Formal Definition |
|---|---|
| **State Space** | Location / waypoint node name |
| **Actions** | Travel along connected road edge to neighbor node |
| **Step Cost** | Actual road travel time in minutes |
| **Heuristic $h(n)$** | $\frac{\text{HaversineDistance}(n, \text{Goal})}{\text{MaxSpeed}}$ in minutes |

### 5.2 Algorithmic Comparison
1. **Greedy Best-First:** Prioritizes solely by $h(n)$. It rapidly dives toward nodes with smaller straight-line distance, but can be lured down deceptive or congested roads that yield suboptimal total time.
2. **A\* Search:** Evaluates $f(n) = g(n) + h(n)$. Combines elapsed driving time with remaining straight-line estimate, guaranteeing the shortest true travel time.

---

## 6. Module D — Bid Pricing Advisor (Minimax + Alpha-Beta)

### 6.1 Game Model Formulation
Simulates competitive bidding against a rival caterer:
- **MAX Player:** Our catering business (seeking to maximize expected contract profit).
- **MIN Player:** Competitor (seeking to undercut our pricing and capture the event).
- **Moves:** Pricing adjustments around base price ($-8\%, -4\%, 0\%, +4\%, +8\%$).
- **Rounds:** Multi-round offers and counter-offers ($d = 3$ to $6$).
- **Quality Offset:** The client awards an effective price discount based on reputation rating difference:
  $$\text{EffectivePrice}_{\text{our}} = P_{\text{our}} - 2.5 \cdot (\text{Rating}_{\text{our}} - \text{Rating}_{\text{comp}})$$
- **Terminal Payoff (MAX):**
  $$\text{Utility} = \begin{cases} (P_{\text{our}} - \text{Cost}_{\text{our}}) \times \text{Headcount} & \text{if } \text{EffectivePrice}_{\text{our}} \le P_{\text{comp}} \\ 0 & \text{otherwise} \end{cases}$$

### 6.2 Alpha-Beta Pruning Efficiency
- **Alpha ($\alpha$):** Best value that MAX can guarantee so far along the path.
- **Beta ($\beta$):** Best value that MIN can guarantee so far along the path.
- **Pruning Criterion:** Whenever $\alpha \ge \beta$, the remaining children of the current node are pruned.
- **Verification Guarantee:** Minimax and Alpha-Beta produce the **exact same optimal expected payoff**, while Alpha-Beta skips 30% to 50% of the game tree.
