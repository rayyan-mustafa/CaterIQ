"""Module A — Allergen Substitution Finder (Breadth-First Search).

Finds the minimum number of ingredient swaps required to make a dish
safe from specified guest allergens.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, FrozenSet, List, NamedTuple, Optional, Set, Tuple
from ai_engine.search.core import Problem, SearchResult
from ai_engine.search.bfs import breadth_first_search


class SwapAction(NamedTuple):
    """An ingredient substitution action."""

    replace_ingredient: str
    with_ingredient: str
    cost: float = 1.0

    def __repr__(self) -> str:
        return f"Swap({self.replace_ingredient} -> {self.with_ingredient})"


class AllergenSubstitutionProblem(Problem[FrozenSet[str], SwapAction]):
    """Formal BFS problem for allergen substitution.

    State: frozenset of ingredient names present in the dish.
    Action: SwapAction(from, to) replacing an unsafe or intermediate ingredient.
    Goal: No ingredient in the state contains any of the target allergens.
    """

    def __init__(
        self,
        initial_ingredients: Set[str],
        ingredient_allergens: Dict[str, Set[str]],
        allowed_substitutions: Dict[str, List[Tuple[str, float]]],
        target_allergens: Set[str],
    ) -> None:
        """Initialize the allergen substitution problem.

        Args:
            initial_ingredients: Set of ingredient names initially in the dish.
            ingredient_allergens: Map of ingredient name -> set of allergens it contains.
            allowed_substitutions: Map of ingredient name -> list of (substitute_name, swap_cost).
            target_allergens: Set of allergens to eliminate.
        """
        self._initial = frozenset(initial_ingredients)
        self.ingredient_allergens = {k: set(v) for k, v in ingredient_allergens.items()}
        self.allowed_substitutions = allowed_substitutions
        self.target_allergens = set(target_allergens)

    def initial_state(self) -> FrozenSet[str]:
        return self._initial

    def is_goal(self, state: FrozenSet[str]) -> bool:
        """Check if any ingredient in state has any target allergen."""
        for ing in state:
            contained = self.ingredient_allergens.get(ing, set())
            if not contained.isdisjoint(self.target_allergens):
                return False
        return True

    def actions(self, state: FrozenSet[str]) -> List[SwapAction]:
        """Generate possible substitutions for unsafe ingredients."""
        available_actions: List[SwapAction] = []
        for ing in state:
            contained = self.ingredient_allergens.get(ing, set())
            # We prioritize substituting ingredients that actually carry a target allergen
            if not contained.isdisjoint(self.target_allergens):
                subs = self.allowed_substitutions.get(ing, [])
                for sub, cost in subs:
                    available_actions.append(
                        SwapAction(replace_ingredient=ing, with_ingredient=sub, cost=cost)
                    )
        return available_actions

    def result(self, state: FrozenSet[str], action: SwapAction) -> FrozenSet[str]:
        """Apply the swap action to produce a new state."""
        new_set = set(state)
        new_set.discard(action.replace_ingredient)
        new_set.add(action.with_ingredient)
        return frozenset(new_set)

    def step_cost(
        self,
        state: FrozenSet[str],
        action: SwapAction,
        next_state: FrozenSet[str],
    ) -> float:
        return 1.0  # Unit cost: BFS minimizes number of ingredient changes


@dataclass
class SubstitutionSolution:
    """Friendly output for API and UI presentation."""

    found: bool
    original_ingredients: List[str]
    safe_ingredients: Optional[List[str]]
    swaps_required: List[Dict[str, str]]
    nodes_expanded: int
    runtime_ms: float
    safety_disclaimer: str = (
        "Note: Allergen finder is an AI decision aid. Kitchen staff must verify all physical ingredient packaging."
    )


def find_allergen_substitutions(
    ingredients: List[str],
    ingredient_allergens: Dict[str, List[str]],
    allowed_substitutions: Dict[str, List[Tuple[str, float]]],
    target_allergens: List[str],
    max_depth: int = 5,
) -> SubstitutionSolution:
    """Helper entry point for API to execute BFS allergen substitution."""
    problem = AllergenSubstitutionProblem(
        initial_ingredients=set(ingredients),
        ingredient_allergens={k: set(v) for k, v in ingredient_allergens.items()},
        allowed_substitutions=allowed_substitutions,
        target_allergens=set(target_allergens),
    )

    res: SearchResult = breadth_first_search(problem, max_depth=max_depth)

    if not res.found or res.solution_path is None:
        return SubstitutionSolution(
            found=False,
            original_ingredients=sorted(ingredients),
            safe_ingredients=None,
            swaps_required=[],
            nodes_expanded=res.nodes_expanded,
            runtime_ms=res.runtime_ms,
        )

    final_state = res.solution_path[-1]
    actions: List[SwapAction] = res.metadata.get("actions", [])
    swaps = [
        {"from": a.replace_ingredient, "to": a.with_ingredient}
        for a in actions
    ]

    return SubstitutionSolution(
        found=True,
        original_ingredients=sorted(ingredients),
        safe_ingredients=sorted(list(final_state)),
        swaps_required=swaps,
        nodes_expanded=res.nodes_expanded,
        runtime_ms=res.runtime_ms,
    )
