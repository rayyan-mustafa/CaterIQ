# CaterIQ — Archived Architecture & Advanced Modules Reference

> **Document Purpose**: Comprehensive technical reference and blueprint for all decoupled components from earlier project iterations (Weeks 6–7 Advanced AI Search, FastAPI REST Backend, SQLite Database, and Next.js 14 Frontend).
> **Student Attribution**: Rayyan Mustafa (Reg: 2312335) — AI Lab Semester Project
> **Active Production State**: The active repository is strictly simplified to **Weeks 1–5 (Pure Python + Streamlit + In-Memory `data.py`)**. This file serves as the single source of truth should any advanced modules be rebuilt under the new streamlined infrastructure.

---

## 1. Executive Summary of Archived Components

| Component | Original Location | Description | Key Technologies / Algorithms |
| :--- | :--- | :--- | :--- |
| **Informed Search (A*)** | `archive_weeks_6_7/ai_engine/search/astar.py` | Cost-optimal state-space search with admissible heuristics | $f(n) = g(n) + h(n)$, `heapq` priority queue |
| **Greedy Best-First** | `archive_weeks_6_7/ai_engine/search/greedy.py` | Purely heuristic-driven state-space exploration | $f(n) = h(n)$, `heapq` priority queue |
| **Adversarial Search** | `archive_weeks_6_7/ai_engine/search/adversarial.py` | 2-player zero-sum game tree search | Minimax, Alpha-Beta Pruning ($\alpha \ge \beta$ cutoffs) |
| **Menu Optimizer** | `archive_weeks_6_7/ai_engine/problems/menu_optimizer.py` | A* search balancing dish price and popularity appeal | Admissible remaining slot cost heuristic |
| **Delivery Routing** | `archive_weeks_6_7/ai_engine/problems/delivery_routing.py` | Vehicle route planning for event catering vans | Great-circle Haversine distance heuristic |
| **Bid Pricing Game** | `archive_weeks_6_7/ai_engine/problems/bid_pricing.py` | Adversarial pricing advisor against a rival catering firm | Minimax with alpha-beta pruning, profit margin utility |
| **FastAPI REST API** | `archive_fullstack_version/backend/` | RESTful API with SQLite & SQLAlchemy ORM | FastAPI, Pydantic v2, SQLAlchemy, Uvicorn |
| **Next.js Frontend** | `archive_fullstack_version/frontend/` | Multi-page fullstack web interface | Next.js 14 (App Router), React, Tailwind CSS |
| **Database Seeders** | `scripts/seed_data.py` | SQLite database population with catering domain models | SQLAlchemy sessions, relational foreign keys |

---

## 2. Advanced Search Algorithms (Weeks 6–7)

### A. A* Search (`astar.py`)
- **Evaluation Function**: $f(n) = g(n) + h(n)$
  - $g(n)$: Exact accumulated cost from the initial state to node $n$.
  - $h(n)$: Admissible (never overestimates) heuristic estimate of cost from $n$ to the nearest goal state.
- **Optimality**: Guaranteed to return the lowest-cost solution when $h(n)$ is admissible and consistent.
- **Python Implementation Blueprint**:
```python
import heapq, time
from ai_engine.search.core import Node, Problem, SearchResult

def astar_search(problem: Problem, max_depth: int = None) -> SearchResult:
    start_time = time.perf_counter()
    initial = problem.initial_state()
    root = Node(state=initial, path_cost=0.0, heuristic_value=problem.heuristic(initial))
    
    # Priority Queue stores tuples: (f_cost, node)
    frontier = [(root.path_cost + root.heuristic_value, root)]
    best_g = {initial: 0.0}
    nodes_expanded = 0

    while frontier:
        f_cost, node = heapq.heappop(frontier)

        # Goal test on node expansion guarantees cost optimality
        if problem.is_goal(node.state):
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return SearchResult(
                solution_path=node.state_path(),
                total_cost=node.path_cost,
                nodes_expanded=nodes_expanded,
                runtime_ms=elapsed,
                found=True
            )

        if node.path_cost > best_g.get(node.state, float("inf")):
            continue

        nodes_expanded += 1
        for action, next_state, step_cost in problem.successors(node.state):
            new_g = node.path_cost + step_cost
            if new_g < best_g.get(next_state, float("inf")):
                best_g[next_state] = new_g
                h_val = problem.heuristic(next_state)
                child = Node(state=next_state, parent=node, action=action, path_cost=new_g, heuristic_value=h_val)
                heapq.heappush(frontier, (new_g + h_val, child))

    return SearchResult(solution_path=[], found=False)
```

---

### B. Greedy Best-First Search (`greedy.py`)
- **Evaluation Function**: $f(n) = h(n)$
- **Characteristics**: Fast exploration towards the perceived goal, but not guaranteed to find the lowest-cost path.
- **Priority Queue Entry**: `(h(node.state), node)`

---

### C. Adversarial Minimax & Alpha-Beta Search (`adversarial.py`)
- **Application**: 2-Player zero-sum game tree search where **MAX** is our catering business and **MIN** is a rival firm bidding on the same client event.
- **Alpha-Beta Pruning Optimization**:
  - $\alpha$: Highest (best) value that MAX has found so far across the search tree.
  - $\beta$: Lowest (best) value that MIN has found so far across the search tree.
  - **Pruning Condition**: Whenever $\beta \le \alpha$, the remaining child branches are safely pruned without altering the final minimax decision.
- **Python Implementation Blueprint**:
```python
def alpha_beta_search(state, max_depth=4):
    nodes_evaluated = 0
    pruned_branches = 0

    def _max_value(curr_state, depth, alpha, beta):
        nonlocal nodes_evaluated, pruned_branches
        nodes_evaluated += 1
        if depth >= max_depth or curr_state.is_terminal():
            return curr_state.utility("MAX"), None

        best_val, best_action = float("-inf"), None
        for move in curr_state.legal_moves():
            next_state = curr_state.make_move(move)
            val, _ = _min_value(next_state, depth + 1, alpha, beta)
            if val > best_val:
                best_val, best_action = val, move
            if best_val >= beta:
                pruned_branches += 1
                return best_val, best_action  # Beta cutoff
            alpha = max(alpha, best_val)
        return best_val, best_action

    def _min_value(curr_state, depth, alpha, beta):
        nonlocal nodes_evaluated, pruned_branches
        nodes_evaluated += 1
        if depth >= max_depth or curr_state.is_terminal():
            return curr_state.utility("MAX"), None

        best_val, best_action = float("inf"), None
        for move in curr_state.legal_moves():
            next_state = curr_state.make_move(move)
            val, _ = _max_value(next_state, depth + 1, alpha, beta)
            if val < best_val:
                best_val, best_action = val, move
            if best_val <= alpha:
                pruned_branches += 1
                return best_val, best_action  # Alpha cutoff
            beta = min(beta, best_val)
        return best_val, best_action

    val, move = _max_value(state, 0, float("-inf"), float("inf"))
    return {"best_move": move, "expected_payoff": val, "nodes_evaluated": nodes_evaluated, "pruned": pruned_branches}
```

---

## 3. Advanced Catering Domain Formulations (Weeks 6–7)

### A. Delivery Vehicle Routing (`delivery_routing.py`)
- **Problem**: Finding the fastest delivery route for catering vans between commercial kitchens, cold storage depots, and client wedding venues.
- **Graph Topology**: City street graph with edge weights representing travel time in minutes.
- **Heuristic**: Straight-line Great-Circle distance via the Haversine formula divided by maximum vehicle speed:
$$d = 2r \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)$$
$$h(n) = \frac{d(\text{location}_n, \text{destination})}{v_{\max}}$$
- **Admissibility**: Because straight-line travel is strictly shorter than any road network path, $h(n)$ never overestimates, guaranteeing A* finds the fastest route.

### B. Menu Value Optimization (`menu_optimizer.py`)
- **Problem**: Finding an optimal 3-course menu that maximizes guest appeal while staying strictly within budget.
- **Objective Function (Cost)**:
$$\text{Cost} = \text{Price} + w \times (1.0 - \text{Popularity})$$
- **Admissible Heuristic**: Sum of the minimum possible step costs for all remaining unfilled course slots.

### C. Competitive Bid Pricing Game (`bid_pricing.py`)
- **State Vector**: `(round_num, our_price, competitor_price, our_cost, headcount, quality_ratings)`
- **Available Actions**: Price percentage adjustments ($\pm 10\%, \pm 5\%, 0\%$).
- **Utility Function**:
$$\text{Utility} = P(\text{Win}) \times (\text{Price} - \text{Cost}) \times \text{Headcount}$$
where $P(\text{Win})$ is modeled as a sigmoid probability over price and quality score differences.

---

## 4. Fullstack Web Architecture (Decoupled & Archived)

### A. Backend: FastAPI REST Service (`backend/`)
- **Framework**: FastAPI (Python 3.10+) with Uvicorn ASGI server.
- **Database**: SQLite (`cateriq.db`) with SQLAlchemy ORM models:
  - `Dish`: Name, category (starter, main, dessert), price per head, dietary flags (vegetarian, vegan, gluten-free, halal).
  - `Event`: Client name, event date, headcount, dietary constraints, budget cap.
  - `Order`: Linked event ID, selected menu items, status (draft, confirmed, completed).
- **Archived Endpoints**:
  - `POST /api/v1/search/bfs`: Triggers allergen safe-path graph substitution.
  - `POST /api/v1/search/dfs`: Solves 3-course menu constraints with branch pruning.
  - `GET /api/v1/dishes`: Returns catalog of candidate dishes.
  - `GET /api/v1/events`: Retrieves catering bookings and dietary restrictions.

### B. Frontend: Next.js 14 App Router (`frontend/`)
- **Framework**: Next.js 14 (React 18, TypeScript) with Tailwind CSS.
- **UI Components**:
  - `AISearchStudio.tsx`: Interactive dashboard to configure BFS and DFS search parameters.
  - `EventManagement.tsx`: Grid of upcoming catering bookings.
  - `DishCatalog.tsx`: Filterable card layout of dishes with dietary tags.

---

## 5. Utility & Report Scripts Reference (`scripts/`)

| Script Name | Purpose & Functionality |
| :--- | :--- |
| `create_cateriq_report.py` | Generates the formal assignment Word document (`Project_1_CaterIQ_Rayyan_Mustafa_2312335.docx`) according to academic guidelines. |
| `generate_report_assets.py` | Generates algorithmic state-space diagrams, search tree graphs, and benchmark plots embedded into reports. |
| `seed_data.py` | Populated the historical SQLite `cateriq.db` database using SQLAlchemy ORM models. |
| `generate_data.py` | Synthesizes synthetic event profiles and ingredient combinations for stress testing. |

---

## 6. How to Re-Integrate If Needed in the Future

If you ever wish to upgrade CaterIQ to include Weeks 6–7 or fullstack endpoints:
1. **To Add A* or Minimax**:
   - Create `ai_engine/search/astar.py` and `ai_engine/search/adversarial.py` using the clean blueprints in Section 2.
   - Add a new tab in `app.py` for informed search or competitive pricing.
2. **To Add REST Endpoints**:
   - Install `fastapi` and `uvicorn`.
   - Wrap the functions from `ai_engine` in FastAPI route handlers that return JSON responses.
3. **Data Independence**:
   - All models can directly read from `data.py`, keeping the project 100% free of database lock-in.
