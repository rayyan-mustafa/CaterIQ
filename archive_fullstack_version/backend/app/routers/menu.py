"""Menu items, ingredients, substitutions, and packages router."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.dependencies import AuthenticatedContext, get_current_context, require_role
from backend.app.models.menu import (
    Allergen,
    Ingredient,
    IngredientAllergen,
    IngredientSubstitution,
    MenuItem,
    MenuItemIngredient,
    Package,
    PackageItem,
)
from backend.app.schemas.menu import (
    IngredientCreate,
    IngredientResponse,
    MenuItemCreate,
    MenuItemResponse,
    PackageCreate,
    PackageResponse,
    SubstitutionCreate,
    SubstitutionResponse,
)

router = APIRouter(tags=["Menu Management"])


# --- INGREDIENTS ---
@router.get("/ingredients", response_model=List[IngredientResponse])
def list_ingredients(
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """List ingredients with associated allergens."""
    return db.query(Ingredient).filter(Ingredient.organization_id == ctx.organization_id).all()


@router.post("/ingredients", response_model=IngredientResponse)
def create_ingredient(
    req: IngredientCreate,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Create a new ingredient and link allergens."""
    ing = Ingredient(
        organization_id=ctx.organization_id,
        name=req.name.strip(),
        unit=req.unit,
        cost_per_unit=req.cost_per_unit,
    )
    db.add(ing)
    db.flush()

    for a_name in req.allergen_names:
        clean_name = a_name.strip().lower()
        allergen = db.query(Allergen).filter(Allergen.name == clean_name).first()
        if not allergen:
            allergen = Allergen(name=clean_name)
            db.add(allergen)
            db.flush()
        link = IngredientAllergen(ingredient_id=ing.id, allergen_id=allergen.id)
        db.add(link)

    db.commit()
    db.refresh(ing)
    return ing


# --- SUBSTITUTIONS ---
@router.get("/ingredient-substitutions", response_model=List[SubstitutionResponse])
def list_substitutions(
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """List allowed ingredient substitutions for BFS module."""
    return db.query(IngredientSubstitution).filter(IngredientSubstitution.organization_id == ctx.organization_id).all()


@router.post("/ingredient-substitutions", response_model=SubstitutionResponse)
def create_substitution(
    req: SubstitutionCreate,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Register an allowed ingredient substitution."""
    sub = IngredientSubstitution(
        organization_id=ctx.organization_id,
        from_ingredient_id=req.from_ingredient_id,
        to_ingredient_id=req.to_ingredient_id,
        swap_cost=req.swap_cost,
        notes=req.notes,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


# --- MENU ITEMS ---
@router.get("/menu-items", response_model=List[MenuItemResponse])
def list_menu_items(
    category: Optional[str] = Query(None),
    is_active: bool = Query(True),
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """List dishes with optional category filter."""
    query = db.query(MenuItem).filter(
        MenuItem.organization_id == ctx.organization_id,
        MenuItem.is_active == is_active,
    )
    if category:
        query = query.filter(MenuItem.category == category.lower())
    return query.all()


@router.post("/menu-items", response_model=MenuItemResponse)
def create_menu_item(
    req: MenuItemCreate,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Add a new dish to the menu catalog."""
    item = MenuItem(
        organization_id=ctx.organization_id,
        name=req.name,
        category=req.category.lower(),
        description=req.description,
        price_per_head=req.price_per_head,
        cost_per_head=req.cost_per_head,
        is_vegetarian=req.is_vegetarian,
        is_vegan=req.is_vegan,
        is_gluten_free=req.is_gluten_free,
        is_halal=req.is_halal,
        popularity_score=req.popularity_score,
        is_active=True,
    )
    db.add(item)
    db.flush()

    for ing_id in req.ingredient_ids:
        link = MenuItemIngredient(menu_item_id=item.id, ingredient_id=ing_id, quantity=1.0)
        db.add(link)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/menu-items/{item_id}", status_code=204)
def delete_menu_item(
    item_id: str,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Soft-delete menu item by marking inactive."""
    item = db.query(MenuItem).filter(MenuItem.id == item_id, MenuItem.organization_id == ctx.organization_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    item.is_active = False
    db.commit()
    return None


# --- PACKAGES ---
@router.get("/packages", response_model=List[PackageResponse])
def list_packages(
    ctx: AuthenticatedContext = Depends(get_current_context),
    db: Session = Depends(get_db),
):
    """List saved menu packages."""
    packages = db.query(Package).filter(Package.organization_id == ctx.organization_id).all()
    results = []
    for pkg in packages:
        items = [pi.menu_item for pi in pkg.items]
        results.append(PackageResponse(
            id=pkg.id,
            name=pkg.name,
            price_per_head=pkg.price_per_head,
            items=[MenuItemResponse.model_validate(it) for it in items],
        ))
    return results


@router.post("/packages", response_model=PackageResponse)
def create_package(
    req: PackageCreate,
    ctx: AuthenticatedContext = Depends(require_role(["owner", "manager"])),
    db: Session = Depends(get_db),
):
    """Save a curated multi-course package."""
    pkg = Package(
        organization_id=ctx.organization_id,
        name=req.name,
        price_per_head=req.price_per_head,
    )
    db.add(pkg)
    db.flush()

    for m_id in req.menu_item_ids:
        p_item = PackageItem(package_id=pkg.id, menu_item_id=m_id)
        db.add(p_item)

    db.commit()
    db.refresh(pkg)
    items = [pi.menu_item for pi in pkg.items]
    return PackageResponse(
        id=pkg.id,
        name=pkg.name,
        price_per_head=pkg.price_per_head,
        items=[MenuItemResponse.model_validate(it) for it in items],
    )
