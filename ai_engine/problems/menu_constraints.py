"""Module B — Menu Constraint Solver (DFS with Backtracking).

Solves multi-course package building subject to budget limits and dietary rules.
Implements both plain DFS and early-pruned DFS for benchmark comparison.
"""

from dataclasses import dataclass
from ai_engine.search.core import Problem, SearchResult
from ai_engine.search.dfs import depth_first_search


@dataclass(frozen=True)
class Dish:
    """Represents a dish option for a menu course."""
    id: str
    name: str
    category: str  # starter, main, dessert
    price_per_head: float
    cost_per_head: float = 0.0
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_halal: bool = True
    popularity_score: float = 0.5


class MenuConstraintProblem(Problem):
    """DFS Problem formulation for menu package assembly under constraints.

    State: tuple of chosen Dish objects so far (e.g., (Starter, Main)).
    Action: Next Dish candidate to add.
    Goal: All course slots filled AND all budget/dietary constraints satisfied.
    """

    def __init__(self, slots, dishes, max_budget, min_vegetarian=0, min_gluten_free=0, min_vegan=0):
        self.slots = list(slots)
        self.max_budget = float(max_budget)
        self.min_vegetarian = int(min_vegetarian)
        self.min_gluten_free = int(min_gluten_free)
        self.min_vegan = int(min_vegan)

        # Group dish candidates by category (starter, main, dessert)
        self.category_map = {}
        for d in dishes:
            cat = d.category.lower()
            self.category_map.setdefault(cat, []).append(d)

    def initial_state(self):
        """Initial state is an empty menu tuple."""
        return ()

    def is_goal(self, state):
        """Returns True if all course slots are filled and all rules are satisfied."""
        # 1. Must have all courses selected (e.g. Starter, Main, Dessert)
        if len(state) != len(self.slots):
            return False

        # 2. Total price must be within budget
        total_price = sum(d.price_per_head for d in state)
        if total_price > self.max_budget:
            return False

        # 3. Vegetarian count check
        veg_count = sum(1 for d in state if d.is_vegetarian or d.is_vegan)
        if veg_count < self.min_vegetarian:
            return False

        # 4. Gluten-free count check
        gf_count = sum(1 for d in state if d.is_gluten_free)
        if gf_count < self.min_gluten_free:
            return False

        # 5. Vegan count check
        vegan_count = sum(1 for d in state if d.is_vegan)
        if vegan_count < self.min_vegan:
            return False

        return True

    def actions(self, state):
        """Returns candidates for the next unfilled course slot."""
        curr_idx = len(state)
        if curr_idx >= len(self.slots):
            return []  # All slots already filled

        # What course are we picking next? (e.g., "starter", "main", or "dessert")
        target_category = self.slots[curr_idx].lower()
        candidates = self.category_map.get(target_category, [])

        # Avoid choosing duplicate dishes
        selected_ids = {d.id for d in state}
        return [d for d in candidates if d.id not in selected_ids]

    def result(self, state, action):
        """Append the chosen dish to the current menu state."""
        return state + (action,)

    def prune(self, state):
        """Early pruning check: returns True to cut this branch immediately."""
        # 1. Budget overrun: If current partial price already exceeds budget, stop!
        running_price = sum(d.price_per_head for d in state)
        if running_price > self.max_budget:
            return True

        # 2. Dietary reachability: If remaining unfilled slots can't supply enough veg/gf dishes
        remaining_slots = len(self.slots) - len(state)

        veg_so_far = sum(1 for d in state if d.is_vegetarian or d.is_vegan)
        if veg_so_far + remaining_slots < self.min_vegetarian:
            return True

        gf_so_far = sum(1 for d in state if d.is_gluten_free)
        if gf_so_far + remaining_slots < self.min_gluten_free:
            return True

        return False


def solve_menu_constraints(
    slots,
    dishes,
    max_budget,
    min_vegetarian=0,
    min_gluten_free=0,
    min_vegan=0,
    use_pruning=True,
    find_all=False,
    max_solutions=3,
):
    """Main helper called by the FastAPI router to solve menu package constraints via DFS."""
    dish_objs = [
        Dish(
            id=d.get("id", str(i)),
            name=d["name"],
            category=d.get("category", "main"),
            price_per_head=float(d.get("price_per_head", 0.0)),
            cost_per_head=float(d.get("cost_per_head", 0.0)),
            is_vegetarian=bool(d.get("is_vegetarian", False)),
            is_vegan=bool(d.get("is_vegan", False)),
            is_gluten_free=bool(d.get("is_gluten_free", False)),
            is_halal=bool(d.get("is_halal", True)),
            popularity_score=float(d.get("popularity_score", 0.5)),
        )
        for i, d in enumerate(dishes)
    ]

    problem = MenuConstraintProblem(
        slots=slots,
        dishes=dish_objs,
        max_budget=max_budget,
        min_vegetarian=min_vegetarian,
        min_gluten_free=min_gluten_free,
        min_vegan=min_vegan,
    )

    res = depth_first_search(
        problem,
        use_pruning=use_pruning,
        find_all=find_all,
        max_solutions=max_solutions,
    )

    if not res.found or not res.solution_path:
        return {
            "found": False,
            "packages": [],
            "nodes_expanded": res.nodes_expanded,
            "nodes_generated": res.nodes_generated,
            "runtime_ms": res.runtime_ms,
            "pruning_enabled": use_pruning,
            "message": "No menu combination satisfies all specified constraints within budget.",
        }

    # Format solution packages
    if find_all and "all_solutions" in res.metadata:
        paths = res.metadata["all_solutions"]
    else:
        paths = [res.solution_path]

    final_packages = []
    for p in paths:
        final_state = p[-1]
        package_dishes = [
            {
                "id": d.id,
                "name": d.name,
                "category": d.category,
                "price_per_head": d.price_per_head,
                "is_vegetarian": d.is_vegetarian,
                "is_gluten_free": d.is_gluten_free,
            }
            for d in final_state
        ]
        total_p = sum(d.price_per_head for d in final_state)
        final_packages.append({
            "dishes": package_dishes,
            "total_price_per_head": round(total_p, 2),
        })

    # Sort packages descending by price so top package best matches the client budget tier
    final_packages.sort(key=lambda p: p["total_price_per_head"], reverse=True)

    return {
        "found": True,
        "packages": final_packages,
        "nodes_expanded": res.nodes_expanded,
        "nodes_generated": res.nodes_generated,
        "runtime_ms": res.runtime_ms,
        "pruning_enabled": use_pruning,
    }
