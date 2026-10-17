"""Module B — Menu Constraint Solver (DFS with Backtracking).

Solves multi-course package building subject to budget limits and dietary rules.
Implements both plain DFS and early-pruned DFS for benchmark comparison.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple
from ai_engine.search.core import Problem, SearchResult
from ai_engine.search.dfs import depth_first_search


@dataclass(frozen=True)
class Dish:
    """A dish candidate for menu slots."""

    id: str
    name: str
    category: str  # starter, main, dessert, drink, side
    price_per_head: float
    cost_per_head: float = 0.0
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_halal: bool = True
    popularity_score: float = 0.5


# State: tuple of chosen Dish objects
MenuState = Tuple[Dish, ...]


class MenuConstraintProblem(Problem[MenuState, Dish]):
    """DFS Problem formulation for menu package assembly under constraints.

    State: tuple of chosen Dish objects (one per slot).
    Action: Dish to place in the next slot.
    Goal: All slots filled and all hard constraints met.
    """

    def __init__(
        self,
        slots: Sequence[str],  # e.g. ["starter", "main", "dessert"]
        dishes: Sequence[Dish],
        max_budget: float,
        min_vegetarian: int = 0,
        min_gluten_free: int = 0,
        min_vegan: int = 0,
    ) -> None:
        self.slots = list(slots)
        self.max_budget = max_budget
        self.min_vegetarian = min_vegetarian
        self.min_gluten_free = min_gluten_free
        self.min_vegan = min_vegan

        # Group candidates by category
        self.category_map: Dict[str, List[Dish]] = {}
        for d in dishes:
            self.category_map.setdefault(d.category.lower(), []).append(d)

    def initial_state(self) -> MenuState:
        return ()

    def is_goal(self, state: MenuState) -> bool:
        """Check if all slots are filled and all constraints satisfied."""
        if len(state) != len(self.slots):
            return False

        # Budget constraint
        total_price = sum(d.price_per_head for d in state)
        if total_price > self.max_budget:
            return False

        # Vegetarian constraint
        veg_count = sum(1 for d in state if d.is_vegetarian or d.is_vegan)
        if veg_count < self.min_vegetarian:
            return False

        # Gluten-free constraint
        gf_count = sum(1 for d in state if d.is_gluten_free)
        if gf_count < self.min_gluten_free:
            return False

        # Vegan constraint
        vegan_count = sum(1 for d in state if d.is_vegan)
        if vegan_count < self.min_vegan:
            return False

        return True

    def actions(self, state: MenuState) -> List[Dish]:
        """Available dishes for the next unfilled course slot."""
        curr_idx = len(state)
        if curr_idx >= len(self.slots):
            return []

        target_category = self.slots[curr_idx].lower()
        candidates = self.category_map.get(target_category, [])

        # Filter out already selected dishes to avoid duplicates
        selected_ids = {d.id for d in state}
        return [d for d in candidates if d.id not in selected_ids]

    def result(self, state: MenuState, action: Dish) -> MenuState:
        """Append chosen dish to the partial menu state."""
        return state + (action,)

    def prune(self, state: MenuState) -> bool:
        """Early constraint pruning hook.

        Returns True to cut branch immediately if hard constraints cannot be satisfied.
        """
        # 1. Budget overrun pruning: If current partial cost already exceeds budget
        running_price = sum(d.price_per_head for d in state)
        if running_price > self.max_budget:
            return True

        # 2. Dietary reachability pruning: If remaining slots cannot supply missing items
        remaining_slots = len(self.slots) - len(state)

        veg_so_far = sum(1 for d in state if d.is_vegetarian or d.is_vegan)
        if veg_so_far + remaining_slots < self.min_vegetarian:
            return True

        gf_so_far = sum(1 for d in state if d.is_gluten_free)
        if gf_so_far + remaining_slots < self.min_gluten_free:
            return True

        return False


def solve_menu_constraints(
    slots: List[str],
    dishes: List[Dict[str, Any]],
    max_budget: float,
    min_vegetarian: int = 0,
    min_gluten_free: int = 0,
    min_vegan: int = 0,
    use_pruning: bool = True,
    find_all: bool = False,
    max_solutions: int = 3,
) -> Dict[str, Any]:
    """Helper entry point for API to execute DFS menu constraint solving."""
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

    res: SearchResult = depth_first_search(
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
    final_packages = []
    if find_all and "all_solutions" in res.metadata:
        paths = res.metadata["all_solutions"]
    else:
        paths = [res.solution_path]

    for p in paths:
        final_state: MenuState = p[-1]
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

    return {
        "found": True,
        "packages": final_packages,
        "nodes_expanded": res.nodes_expanded,
        "nodes_generated": res.nodes_generated,
        "runtime_ms": res.runtime_ms,
        "pruning_enabled": use_pruning,
    }
