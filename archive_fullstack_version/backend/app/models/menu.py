"""Menu, Ingredients, Allergens, Substitutions, and Packages models."""

import uuid
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Allergen(Base):
    __tablename__ = "allergens"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)  # peanut, gluten, dairy, etc.


class IngredientAllergen(Base):
    __tablename__ = "ingredient_allergens"

    ingredient_id = Column(String(36), ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True)
    allergen_id = Column(String(36), ForeignKey("allergens.id", ondelete="CASCADE"), primary_key=True)


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(50), default="kg")
    cost_per_unit = Column(Float, default=0.0, nullable=False)

    allergens = relationship("Allergen", secondary="ingredient_allergens", backref="ingredients")


class IngredientSubstitution(Base):
    __tablename__ = "ingredient_substitutions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    from_ingredient_id = Column(String(36), ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False, index=True)
    to_ingredient_id = Column(String(36), ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False, index=True)
    swap_cost = Column(Float, default=1.0)
    notes = Column(String(255), nullable=True)

    from_ingredient = relationship("Ingredient", foreign_keys=[from_ingredient_id])
    to_ingredient = relationship("Ingredient", foreign_keys=[to_ingredient_id])


class MenuItemIngredient(Base):
    __tablename__ = "menu_item_ingredients"

    menu_item_id = Column(String(36), ForeignKey("menu_items.id", ondelete="CASCADE"), primary_key=True)
    ingredient_id = Column(String(36), ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Float, default=1.0)

    ingredient = relationship("Ingredient")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # starter, main, dessert, drink, side
    description = Column(Text, nullable=True)
    price_per_head = Column(Float, nullable=False, default=0.0)
    cost_per_head = Column(Float, nullable=False, default=0.0)
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=False)
    is_halal = Column(Boolean, default=True)
    popularity_score = Column(Float, default=0.5)  # 0.0 to 1.0
    is_active = Column(Boolean, default=True)

    ingredients = relationship("MenuItemIngredient", cascade="all, delete-orphan")


class PackageItem(Base):
    __tablename__ = "package_items"

    package_id = Column(String(36), ForeignKey("packages.id", ondelete="CASCADE"), primary_key=True)
    menu_item_id = Column(String(36), ForeignKey("menu_items.id", ondelete="CASCADE"), primary_key=True)

    menu_item = relationship("MenuItem")


class Package(Base):
    __tablename__ = "packages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    price_per_head = Column(Float, nullable=False, default=0.0)

    items = relationship("PackageItem", cascade="all, delete-orphan")
