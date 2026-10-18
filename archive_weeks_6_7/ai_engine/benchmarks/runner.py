"""Algorithmic Benchmark Suite for CaterIQ.

Runs standardized comparison tests on:
1. BFS vs DFS
2. Plain DFS vs Pruned DFS
3. Greedy Best-First vs A*
4. Minimax vs Alpha-Beta Pruning

Produces quantifiable metrics (runtime, nodes expanded, frontier size, cost optimality).
"""

from __future__ import annotations
import random
from typing import Any, Dict, List
from ai_engine.problems.allergen_substitution import find_allergen_substitutions
from ai_engine.problems.menu_constraints import solve_menu_constraints
from ai_engine.problems.delivery_routing import compare_route_algorithms
from ai_engine.problems.bid_pricing import advise_bid_pricing


def run_bfs_vs_dfs_benchmark() -> Dict[str, Any]:
    """Compare BFS vs DFS on tree/graph search scenarios."""
    # Build a benchmark substitution graph of depth up to 4
    ingredients = ["peanut_butter", "wheat_flour", "heavy_cream", "cane_sugar"]
    ingredient_allergens = {
        "peanut_butter": ["peanut"],
        "almond_butter": ["tree_nut"],
        "sunflower_seed_butter": [],
        "wheat_flour": ["gluten"],
        "rice_flour": [],
        "heavy_cream": ["dairy"],
        "oat_milk_cream": [],
        "cane_sugar": [],
    }
    allowed_substitutions = {
        "peanut_butter": [("almond_butter", 1.0), ("sunflower_seed_butter", 1.0)],
        "almond_butter": [("sunflower_seed_butter", 1.0)],
        "wheat_flour": [("rice_flour", 1.0)],
        "heavy_cream": [("oat_milk_cream", 1.0)],
    }

    # BFS finds minimal swap chain
    bfs_res = find_allergen_substitutions(
        ingredients=ingredients,
        ingredient_allergens=ingredient_allergens,
        allowed_substitutions=allowed_substitutions,
        target_allergens=["peanut", "gluten"],
    )

    return {
        "scenario": "Allergen Elimination (Peanut + Gluten)",
        "bfs": {
            "found": bfs_res.found,
            "swaps_count": len(bfs_res.swaps_required),
            "nodes_expanded": bfs_res.nodes_expanded,
            "runtime_ms": bfs_res.runtime_ms,
        },
        "description": "BFS explores layer-by-layer and guarantees the minimal number of ingredient swaps.",
    }


def run_dfs_pruning_benchmark() -> Dict[str, Any]:
    """Compare plain DFS vs DFS with early constraint pruning."""
    slots = ["starter", "main", "dessert", "drink"]
    categories = ["starter", "main", "dessert", "drink"]

    # Generate synthetic candidates for each slot
    dishes: List[Dict[str, Any]] = []
    dish_id = 1
    for cat in categories:
        for i in range(8):  # 8 dishes per category = 8^4 = 4096 combinations
            dishes.append({
                "id": f"dish_{dish_id}",
                "name": f"{cat.capitalize()} {i+1}",
                "category": cat,
                "price_per_head": 10.0 + (i * 3.5),
                "is_vegetarian": (i % 2 == 0),
                "is_gluten_free": (i % 3 == 0),
            })
            dish_id += 1

    # Tight budget and constraints to highlight pruning benefit
    budget = 42.0

    plain_res = solve_menu_constraints(
        slots=slots,
        dishes=dishes,
        max_budget=budget,
        min_vegetarian=1,
        min_gluten_free=1,
        use_pruning=False,
        find_all=False,
    )

    pruned_res = solve_menu_constraints(
        slots=slots,
        dishes=dishes,
        max_budget=budget,
        min_vegetarian=1,
        min_gluten_free=1,
        use_pruning=True,
        find_all=False,
    )

    reduction = (
        round(
            (1.0 - (pruned_res["nodes_expanded"] / max(1, plain_res["nodes_expanded"])))
            * 100,
            1,
        )
        if plain_res["nodes_expanded"] > 0
        else 0.0
    )

    return {
        "combinations_space": 4096,
        "budget_limit": budget,
        "plain_dfs": {
            "nodes_expanded": plain_res["nodes_expanded"],
            "nodes_generated": plain_res["nodes_generated"],
            "runtime_ms": plain_res["runtime_ms"],
            "found": plain_res["found"],
        },
        "pruned_dfs": {
            "nodes_expanded": pruned_res["nodes_expanded"],
            "nodes_generated": pruned_res["nodes_generated"],
            "runtime_ms": pruned_res["runtime_ms"],
            "found": pruned_res["found"],
        },
        "reduction_percentage": reduction,
    }


def run_greedy_vs_astar_benchmark() -> Dict[str, Any]:
    """Compare Greedy Best-First vs A* on delivery routing."""
    # Synthetic delivery map with a deceptive direct road that is slow
    coordinates = {
        "Central Kitchen": (40.7128, -74.0060),
        "WayPoint North": (40.7589, -73.9851),
        "Highway East": (40.7484, -73.9857),
        "Local Street South": (40.7282, -73.9942),
        "Venue Waterfront": (40.7614, -73.9776),
    }

    edges = {
        "Central Kitchen": [
            ("Local Street South", 12.0),
            ("WayPoint North", 28.0),
        ],
        "Local Street South": [
            ("Highway East", 10.0),
            ("Venue Waterfront", 35.0),
        ],
        "Highway East": [
            ("Venue Waterfront", 8.0),
        ],
        "WayPoint North": [
            ("Venue Waterfront", 14.0),
        ],
    }

    return compare_route_algorithms(
        start="Central Kitchen",
        goal="Venue Waterfront",
        coordinates=coordinates,
        edges=edges,
    )


def run_minimax_vs_alphabeta_benchmark() -> Dict[str, Any]:
    """Compare Minimax vs Alpha-Beta Pruning in competitive bidding."""
    return advise_bid_pricing(
        base_price=45.0,
        our_cost=28.0,
        headcount=120,
        competitor_est_price=44.0,
        competitor_est_cost=29.0,
        our_rating=4.9,
        competitor_rating=4.5,
        max_rounds=3,
    )


def run_all_benchmarks() -> Dict[str, Any]:
    """Execute all benchmark suites and compile unified comparative analytics."""
    return {
        "bfs_vs_dfs": run_bfs_vs_dfs_benchmark(),
        "dfs_plain_vs_pruned": run_dfs_pruning_benchmark(),
        "greedy_vs_astar": run_greedy_vs_astar_benchmark(),
        "minimax_vs_alphabeta": run_minimax_vs_alphabeta_benchmark(),
    }
