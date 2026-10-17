"""AI Suite router exposing search algorithms and benchmark runner."""

import json
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_engine.benchmarks.runner import run_all_benchmarks
from ai_engine.problems.allergen_substitution import find_allergen_substitutions
from ai_engine.problems.bid_pricing import advise_bid_pricing
from ai_engine.problems.delivery_routing import compare_route_algorithms
from ai_engine.problems.menu_constraints import solve_menu_constraints
from ai_engine.problems.menu_optimizer import optimize_menu_package
from backend.app.core.database import get_db
from backend.app.core.dependencies import AuthenticatedContext, get_current_context
from backend.app.models.menu import (
    Ingredient,
    IngredientSubstitution,
    MenuItem,
)
from backend.app.models.support import AIRun
from backend.app.schemas.ai import (
    AllergenSubstitutionRequest,
    BidAdviceRequest,
    MenuOptimizeRequest,
    MenuSolveRequest,
    RoutePlanRequest,
)

router = APIRouter(prefix="/ai", tags=["AI Search & Optimization Suite"])


def record_ai_run(
    db: Session,
    org_id: str,
    module_name: str,
    params: Dict[str, Any],
    nodes_expanded: int,
    runtime_ms: float,
    result: Dict[str, Any],
):
    """Persist search run into ai_runs table to feed analytics and benchmark history."""
    try:
        run = AIRun(
            organization_id=org_id,
            module=module_name,
            params_json=json.dumps(params),
            nodes_expanded=nodes_expanded,
            runtime_ms=runtime_ms,
            result_json=json.dumps(result, default=str),
        )
        db.add(run)
        db.commit()
    except Exception:
        db.rollback()


@router.post("/allergen-substitution")
def allergen_substitution_api(
    req: AllergenSubstitutionRequest,
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Module A: Breadth-First Search (BFS) for minimal ingredient substitutions."""
    # Load ingredients from DB if dish_id is given
    target_ingredients = list(req.ingredients)
    if req.dish_id:
        dish = (
            db.query(MenuItem)
            .filter(MenuItem.id == req.dish_id, MenuItem.organization_id == ctx.organization_id)
            .first()
        )
        if dish:
            for mi_ing in dish.ingredients:
                target_ingredients.append(mi_ing.ingredient.name)

    # Load all tenant ingredients & their allergens
    db_ingredients = (
        db.query(Ingredient)
        .filter(Ingredient.organization_id == ctx.organization_id)
        .all()
    )
    allergen_map: Dict[str, List[str]] = {}
    for ing in db_ingredients:
        allergen_map[ing.name] = [a.name.lower() for a in ing.allergens]

    # Load allowed substitutions from DB
    db_subs = (
        db.query(IngredientSubstitution)
        .filter(IngredientSubstitution.organization_id == ctx.organization_id)
        .all()
    )
    subs_map: Dict[str, List] = {}
    for sub in db_subs:
        from_name = sub.from_ingredient.name
        to_name = sub.to_ingredient.name
        subs_map.setdefault(from_name, []).append((to_name, sub.swap_cost))

    solution = find_allergen_substitutions(
        ingredients=target_ingredients,
        ingredient_allergens=allergen_map,
        allowed_substitutions=subs_map,
        target_allergens=[a.lower() for a in req.target_allergens],
    )

    out = {
        "found": solution.found,
        "original_ingredients": solution.original_ingredients,
        "safe_ingredients": solution.safe_ingredients,
        "swaps_required": solution.swaps_required,
        "nodes_expanded": solution.nodes_expanded,
        "runtime_ms": solution.runtime_ms,
        "safety_disclaimer": solution.safety_disclaimer,
    }

    record_ai_run(
        db,
        ctx.organization_id,
        "bfs_allergen_substitution",
        req.model_dump(),
        solution.nodes_expanded,
        solution.runtime_ms,
        out,
    )
    return out


@router.post("/menu-solve")
def menu_constraint_api(
    req: MenuSolveRequest,
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Module B: Depth-First Search (DFS) with backtracking for constrained menu packages."""
    dishes = (
        db.query(MenuItem)
        .filter(MenuItem.organization_id == ctx.organization_id, MenuItem.is_active == True)
        .all()
    )
    dish_list = [
        {
            "id": d.id,
            "name": d.name,
            "category": d.category,
            "price_per_head": d.price_per_head,
            "cost_per_head": d.cost_per_head,
            "is_vegetarian": d.is_vegetarian,
            "is_vegan": d.is_vegan,
            "is_gluten_free": d.is_gluten_free,
            "is_halal": d.is_halal,
            "popularity_score": d.popularity_score,
        }
        for d in dishes
    ]

    result = solve_menu_constraints(
        slots=req.slots,
        dishes=dish_list,
        max_budget=req.max_budget,
        min_vegetarian=req.min_vegetarian,
        min_gluten_free=req.min_gluten_free,
        min_vegan=req.min_vegan,
        use_pruning=req.use_pruning,
        find_all=req.find_all,
        max_solutions=req.max_solutions,
    )

    record_ai_run(
        db,
        ctx.organization_id,
        "dfs_menu_constraints",
        req.model_dump(),
        result["nodes_expanded"],
        result["runtime_ms"],
        result,
    )
    return result


@router.post("/menu-optimize")
def menu_optimizer_api(
    req: MenuOptimizeRequest,
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Module C1: A* Search with admissible heuristic for value-optimal menu combinations."""
    dishes = (
        db.query(MenuItem)
        .filter(MenuItem.organization_id == ctx.organization_id, MenuItem.is_active == True)
        .all()
    )
    dish_list = [
        {
            "id": d.id,
            "name": d.name,
            "category": d.category,
            "price_per_head": d.price_per_head,
            "cost_per_head": d.cost_per_head,
            "is_vegetarian": d.is_vegetarian,
            "is_vegan": d.is_vegan,
            "is_gluten_free": d.is_gluten_free,
            "is_halal": d.is_halal,
            "popularity_score": d.popularity_score,
        }
        for d in dishes
    ]

    result = optimize_menu_package(
        slots=req.slots,
        dishes=dish_list,
        max_budget=req.max_budget,
        appeal_weight=req.appeal_weight,
        min_vegetarian=req.min_vegetarian,
        min_gluten_free=req.min_gluten_free,
    )

    record_ai_run(
        db,
        ctx.organization_id,
        "astar_menu_optimizer",
        req.model_dump(),
        result.get("nodes_expanded", 0),
        result.get("runtime_ms", 0.0),
        result,
    )
    return result


@router.post("/route-plan")
def route_planner_api(
    req: RoutePlanRequest,
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Module C2: Delivery routing comparing Greedy Best-First vs A* search."""
    # Stored network of locations and waypoints
    coordinates = {
        "Central Kitchen": (40.7128, -74.0060),
        "North Kitchen Hub": (40.7589, -73.9851),
        "Midtown Express Hub": (40.7484, -73.9857),
        "Downtown Waypoint": (40.7282, -73.9942),
        "Waterfront Grand Ballroom": (40.7614, -73.9776),
        "Highline Loft": (40.7450, -74.0080),
        "City Convention Center": (40.7560, -74.0020),
    }

    edges = {
        "Central Kitchen": [
            ("Downtown Waypoint", 12.0),
            ("North Kitchen Hub", 28.0),
            ("Highline Loft", 16.0),
        ],
        "Downtown Waypoint": [
            ("Midtown Express Hub", 10.0),
            ("Waterfront Grand Ballroom", 35.0),
        ],
        "Midtown Express Hub": [
            ("Waterfront Grand Ballroom", 8.0),
            ("City Convention Center", 6.0),
        ],
        "North Kitchen Hub": [
            ("Waterfront Grand Ballroom", 14.0),
        ],
        "Highline Loft": [
            ("City Convention Center", 11.0),
        ],
        "City Convention Center": [
            ("Waterfront Grand Ballroom", 10.0),
        ],
    }

    # Ensure start and goal are valid
    start = req.start_location if req.start_location in coordinates else "Central Kitchen"
    goal = req.goal_location if req.goal_location in coordinates else "Waterfront Grand Ballroom"

    comparison = compare_route_algorithms(
        start=start,
        goal=goal,
        coordinates=coordinates,
        edges=edges,
        max_speed_kmh=req.max_speed_kmh,
    )

    record_ai_run(
        db,
        ctx.organization_id,
        "route_greedy_vs_astar",
        req.model_dump(),
        comparison["astar"]["nodes_expanded"],
        comparison["astar"]["runtime_ms"],
        comparison,
    )
    return comparison


@router.post("/bid-advice")
def bid_advisor_api(
    req: BidAdviceRequest,
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Module D: Minimax and Alpha-Beta Pruning game tree advisor for competitive bidding."""
    advice = advise_bid_pricing(
        base_price=req.base_price,
        our_cost=req.our_cost,
        headcount=req.headcount,
        competitor_est_price=req.competitor_est_price,
        competitor_est_cost=req.competitor_est_cost,
        our_rating=req.our_rating,
        competitor_rating=req.competitor_rating,
        max_rounds=req.max_rounds,
    )

    record_ai_run(
        db,
        ctx.organization_id,
        "minimax_bid_advisor",
        req.model_dump(),
        advice["alpha_beta"]["nodes_evaluated"],
        advice["alpha_beta"]["runtime_ms"],
        advice,
    )
    return advice


@router.get("/benchmarks")
def get_benchmarks(
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """Execute live benchmark suite across all 4 search algorithms."""
    results = run_all_benchmarks()

    # Query recent AI runs history for this organization
    recent_runs = (
        db.query(AIRun)
        .filter(AIRun.organization_id == ctx.organization_id)
        .order_by(AIRun.created_at.desc())
        .limit(20)
        .all()
    )
    history = [
        {
            "id": r.id,
            "module": r.module,
            "nodes_expanded": r.nodes_expanded,
            "runtime_ms": r.runtime_ms,
            "created_at": str(r.created_at),
        }
        for r in recent_runs
    ]

    return {
        "benchmarks": results,
        "recent_runs": history,
    }
