"""AI Suite router exposing search algorithms (Weeks 1-5: BFS & DFS)."""

import json
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_engine.problems.allergen_substitution import find_allergen_substitutions
from ai_engine.problems.menu_constraints import solve_menu_constraints
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
    MenuSolveRequest,
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

