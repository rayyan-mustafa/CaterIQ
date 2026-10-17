"""Module C1 — Menu Optimizer (A* Search with Admissible Heuristic).

Finds the optimal value-for-money package balancing price and guest appeal.
Uses an admissible heuristic (sum of minimum possible step costs for remaining slots)
which guarantees that A* returns the optimal package.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Tuple
from ai_engine.search.core import Problem, SearchResult
from ai_engine.search.astar import astar_search
from ai_engine.problems.menu_constraints import Dish


@dataclass(frozen=True)
class OptimizerState:
    """State for menu optimization search."""

    slot_index: int
    chosen_dishes: Tuple[Dish, ...]


class MenuOptimizerProblem(Problem[OptimizerState, Dish]):
    """A* formulation for menu optimization."""

    def __init__(
        self,
        slots: Sequence[str],
        dishes: Sequence[Dish],
        max_budget: float,
        appeal_weight: float = 10.0,
        min_vegetarian: int = 0,
        min_gluten_free: int = 0,
    ) -> None:
        self.slots = list(slots)
        self.max_budget = max_budget
        self.appeal_weight = appeal_weight
        self.min_vegetarian = min_vegetarian
        self.min_gluten_free = min_gluten_free

        # Group candidates by course slot category
        self.category_map: Dict[str, List[Dish]] = {}
        for d in dishes:
            self.category_map.setdefault(d.category.lower(), []).append(d)

        # Precompute the minimum possible step cost for each slot for admissible heuristic
        self.min_step_cost_per_slot: List[float] = []
        for slot in self.slots:
            candidates = self.category_map.get(slot.lower(), [])
            if candidates:
                min_c = min(
                    d.price_per_head + self.appeal_weight * (1.0 - d.popularity_score)
                    for d in candidates
                )
                self.min_step_cost_per_slot.append(min_c)
            else:
                self.min_step_cost_per_slot.append(0.0)

    def initial_state(self) -> OptimizerState:
        return OptimizerState(slot_index=0, chosen_dishes=())

    def is_goal(self, state: OptimizerState) -> bool:
        if state.slot_index != len(self.slots):
            return False

        # Budget constraint
        total_price = sum(d.price_per_head for d in state.chosen_dishes)
        if total_price > self.max_budget:
            return False

        # Dietary constraints
        veg_count = sum(1 for d in state.chosen_dishes if d.is_vegetarian or d.is_vegan)
        if veg_count < self.min_vegetarian:
            return False

        gf_count = sum(1 for d in state.chosen_dishes if d.is_gluten_free)
        if gf_count < self.min_gluten_free:
            return False

        return True

    def actions(self, state: OptimizerState) -> List[Dish]:
        if state.slot_index >= len(self.slots):
            return []

        target_slot = self.slots[state.slot_index].lower()
        candidates = self.category_map.get(target_slot, [])

        # Prune running budget violation
        running_price = sum(d.price_per_head for d in state.chosen_dishes)
        selected_ids = {d.id for d in state.chosen_dishes}

        valid_actions: List[Dish] = []
        for d in candidates:
            if d.id in selected_ids:
                continue
            if running_price + d.price_per_head <= self.max_budget:
                valid_actions.append(d)
        return valid_actions

    def result(self, state: OptimizerState, action: Dish) -> OptimizerState:
        return OptimizerState(
            slot_index=state.slot_index + 1,
            chosen_dishes=state.chosen_dishes + (action,),
        )

    def step_cost(
        self,
        state: OptimizerState,
        action: Dish,
        next_state: OptimizerState,
    ) -> float:
        """Step cost: price + appeal_weight * (1 - popularity).

        Lower price and higher popularity reduce step cost.
        """
        return action.price_per_head + self.appeal_weight * (1.0 - action.popularity_score)

    def heuristic(self, state: OptimizerState) -> float:
        """Admissible heuristic: sum of minimum possible step costs for remaining slots.

        Since no future dish can cost less than the minimum in its category,
        h(state) <= true remaining cost, ensuring A* admissibility.
        """
        remaining_idx = state.slot_index
        return sum(self.min_step_cost_per_slot[remaining_idx:])


def optimize_menu_package(
    slots: List[str],
    dishes: List[Dict[str, Any]],
    max_budget: float,
    appeal_weight: float = 10.0,
    min_vegetarian: int = 0,
    min_gluten_free: int = 0,
) -> Dict[str, Any]:
    """Helper entry point for API to execute A* menu optimization."""
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

    problem = MenuOptimizerProblem(
        slots=slots,
        dishes=dish_objs,
        max_budget=max_budget,
        appeal_weight=appeal_weight,
        min_vegetarian=min_vegetarian,
        min_gluten_free=min_gluten_free,
    )

    res: SearchResult = astar_search(problem)

    if not res.found or not res.solution_path:
        return {
            "found": False,
            "package": None,
            "nodes_expanded": res.nodes_expanded,
            "runtime_ms": res.runtime_ms,
            "message": "No menu combination found that meets budget and dietary constraints.",
        }

    final_state: OptimizerState = res.solution_path[-1]
    chosen = [
        {
            "id": d.id,
            "name": d.name,
            "category": d.category,
            "price_per_head": d.price_per_head,
            "popularity_score": d.popularity_score,
            "is_vegetarian": d.is_vegetarian,
            "is_gluten_free": d.is_gluten_free,
        }
        for d in final_state.chosen_dishes
    ]

    total_price = sum(d.price_per_head for d in final_state.chosen_dishes)
    avg_popularity = (
        sum(d.popularity_score for d in final_state.chosen_dishes) / len(chosen)
        if chosen
        else 0.0
    )

    return {
        "found": True,
        "dishes": chosen,
        "total_price_per_head": round(total_price, 2),
        "average_popularity": round(avg_popularity, 2),
        "evaluation_score": round(res.total_cost or 0.0, 2),
        "nodes_expanded": res.nodes_expanded,
        "nodes_generated": res.nodes_generated,
        "runtime_ms": res.runtime_ms,
    }
