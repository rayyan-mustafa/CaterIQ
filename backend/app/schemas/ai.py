"""AI Suite request and response schemas."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AllergenSubstitutionRequest(BaseModel):
    dish_id: Optional[str] = None
    ingredients: List[str] = Field(default_factory=list)
    target_allergens: List[str]  # e.g. ["peanut", "gluten"]


class MenuSolveRequest(BaseModel):
    slots: List[str] = Field(default_factory=lambda: ["starter", "main", "dessert"])
    max_budget: float
    min_vegetarian: int = 0
    min_gluten_free: int = 0
    min_vegan: int = 0
    use_pruning: bool = True
    find_all: bool = False
    max_solutions: int = 3


class MenuOptimizeRequest(BaseModel):
    slots: List[str] = Field(default_factory=lambda: ["starter", "main", "dessert"])
    max_budget: float
    appeal_weight: float = 10.0
    min_vegetarian: int = 0
    min_gluten_free: int = 0


class RoutePlanRequest(BaseModel):
    start_location: str
    goal_location: str
    max_speed_kmh: float = 60.0


class BidAdviceRequest(BaseModel):
    base_price: float
    our_cost: float
    headcount: int
    competitor_est_price: float
    competitor_est_cost: float
    our_rating: float = 4.8
    competitor_rating: float = 4.5
    max_rounds: int = 3
