"""AI Suite request and response schemas (Weeks 1-5: BFS & DFS)."""

from typing import List, Optional
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

