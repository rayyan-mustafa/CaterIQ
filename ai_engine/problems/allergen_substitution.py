"""Module A — Allergen Substitution Finder (Breadth-First Search).

Finds the minimum number of ingredient swaps required to make a dish
safe from specified guest allergens.
"""

from dataclasses import dataclass
from ai_engine.search.core import Problem, SearchResult
from ai_engine.search.bfs import breadth_first_search


class SwapAction:
    """Represents swapping one ingredient for an alternative."""

    def __init__(self, replace_ingredient: str, with_ingredient: str, cost: float = 1.0):
        self.replace_ingredient = replace_ingredient
        self.with_ingredient = with_ingredient
        self.cost = cost

    def __repr__(self):
        return f"Swap({self.replace_ingredient} -> {self.with_ingredient})"


class AllergenSubstitutionProblem(Problem):
    """Formal BFS problem for ingredient allergen substitution.

    State: frozenset of ingredients currently in the recipe.
    Action: SwapAction(from, to) replacing an unsafe ingredient.
    Goal: No ingredient in the state contains any target allergens.
    """

    def __init__(self, initial_ingredients, ingredient_allergens, allowed_substitutions, target_allergens):
        self._initial = frozenset(initial_ingredients) #use frozenset because it is immutable and hashable
        self.ingredient_allergens = {k: set(v) for k, v in ingredient_allergens.items()}
        self.allowed_substitutions = allowed_substitutions
        self.target_allergens = set(target_allergens)

    def initial_state(self):
        """Returns the initial recipe ingredients as a frozenset."""
        return self._initial

    def is_goal(self, state):
        """Returns True if none of the ingredients contain any target allergens."""
        for ing in state:
            allergens_in_ing = self.ingredient_allergens.get(ing, set())
            # If the ingredient contains any target allergen, it's not safe
            #  (isdisjoint): Goal test! Checks if the allergens in any ingredient overlap with the guest's allergens
            #   (target_allergens). If there is zero overlap across all ingredients, goal is reached!
            if not allergens_in_ing.isdisjoint(self.target_allergens):
                return False
        return True

    def actions(self, state):
        """Returns valid substitution moves for unsafe ingredients."""
        available_actions = []
        for ing in state:
            allergens_in_ing = self.ingredient_allergens.get(ing, set())
            # Only swap ingredients that actually have a target allergen
            if not allergens_in_ing.isdisjoint(self.target_allergens):
                subs = self.allowed_substitutions.get(ing, [])
                for sub, cost in subs:
                    available_actions.append(
                        SwapAction(replace_ingredient=ing, with_ingredient=sub, cost=cost)
                    )
        return available_actions

# result() implements the formal transition model by replacing an unsafe ingredient and returning a new frozenset. 
    def result(self, state, action):
        """Applies the swap to produce a new recipe ingredient set."""
        new_set = set(state)
        new_set.discard(action.replace_ingredient)
        new_set.add(action.with_ingredient)
        return frozenset(new_set)

    def step_cost(self, state, action, next_state):
        """Unit cost: BFS finds the minimal number of substitutions."""
        return 1.0


@dataclass
class SubstitutionSolution:
    """Clean response container for API and UI display."""
    found: bool
    original_ingredients: list
    safe_ingredients: list = None
    swaps_required: list = None
    nodes_expanded: int = 0
    runtime_ms: float = 0.0
    safety_disclaimer: str = (
        "Note: Allergen finder is an AI decision aid. Kitchen staff must verify all physical ingredient packaging."
    )
# Since all swaps have a unit cost of 1.0, Breadth-First Search guarantees the minimal number of substitutions. 
# The helper function find_allergen_substitutions() ties everything together: it initializes the problem, executes BFS,
#  extracts the final safe recipe from res.solution_path[-1], and packages the required swaps and search metrics into a
#   clean SubstitutionSolution object for the Streamlit dashboard.

def find_allergen_substitutions(
    ingredients,
    ingredient_allergens,
    allowed_substitutions,
    target_allergens,
    max_depth=5,
):
    """Main helper called by the FastAPI router to solve allergen substitution via BFS."""
    problem = AllergenSubstitutionProblem(
        initial_ingredients=set(ingredients),
        ingredient_allergens=ingredient_allergens,
        allowed_substitutions=allowed_substitutions,
        target_allergens=set(target_allergens),
    )

    res = breadth_first_search(problem, max_depth=max_depth)

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
    actions = res.metadata.get("actions", [])
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
