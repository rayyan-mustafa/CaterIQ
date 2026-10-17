"""Menu, ingredient, allergen, and package schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class AllergenSchema(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class IngredientCreate(BaseModel):
    name: str
    unit: str = "kg"
    cost_per_unit: float = 0.0
    allergen_names: List[str] = Field(default_factory=list)


class IngredientResponse(BaseModel):
    id: str
    name: str
    unit: str
    cost_per_unit: float
    allergens: List[AllergenSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True


class SubstitutionCreate(BaseModel):
    from_ingredient_id: str
    to_ingredient_id: str
    swap_cost: float = 1.0
    notes: Optional[str] = None


class SubstitutionResponse(BaseModel):
    id: str
    from_ingredient_id: str
    to_ingredient_id: str
    swap_cost: float
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    name: str
    category: str  # starter, main, dessert, drink, side
    description: Optional[str] = None
    price_per_head: float
    cost_per_head: float = 0.0
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_halal: bool = True
    popularity_score: float = 0.5
    ingredient_ids: List[str] = Field(default_factory=list)


class MenuItemResponse(BaseModel):
    id: str
    name: str
    category: str
    description: Optional[str] = None
    price_per_head: float
    cost_per_head: float
    is_vegetarian: bool
    is_vegan: bool
    is_gluten_free: bool
    is_halal: bool
    popularity_score: float
    is_active: bool

    class Config:
        from_attributes = True


class PackageCreate(BaseModel):
    name: str
    price_per_head: float
    menu_item_ids: List[str] = Field(default_factory=list)


class PackageResponse(BaseModel):
    id: str
    name: str
    price_per_head: float
    items: List[MenuItemResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
