"""Pure Python In-Memory Data Store for CaterIQ.

Following Weeks 2 & 3 of the AI Lab syllabus:
Uses standard Python lists, dictionaries, and sets to represent the catering domain
and knowledge graph for state-space search algorithms (BFS & DFS).
No external SQL or databases required.
"""

# 1. Allergen Reference List
ALLERGENS = ["peanut", "tree_nut", "gluten", "dairy", "soy", "egg"]

# 2. Ingredients and the Allergens they contain 
INGREDIENT_ALLERGENS = {
    "Peanut Butter": {"peanut"},
    "Sunflower Seed Butter": set(),
    "Almond Butter": {"tree_nut"},
    "Wheat Flour": {"gluten"},
    "Rice Flour": set(),
    "Heavy Cream": {"dairy"},
    "Coconut Cream": set(),
    "Chicken Breast": set(),
    "Ribeye Beef": set(),
    "Wild Salmon": set(),
    "Arborio Rice": set(),
    "Parmesan Cheese": {"dairy"},
    "Nutritional Yeast Seasoning": set(),
    "Extra Virgin Olive Oil": set(),
    "Fresh Farm Eggs": {"egg"},
    "Honeycrisp Apples": set(),
    "Soy Sauce": {"soy"},
    "Coconut Aminos": set(),
}

# 3. Allowed Ingredient Substitutions (Graph Edges for BFS)
# Format: ingredient_name: [(substitute_name, swap_cost)]
ALLOWED_SUBSTITUTIONS = {
    "Peanut Butter": [("Sunflower Seed Butter", 1.0), ("Almond Butter", 1.0)],
    "Almond Butter": [("Sunflower Seed Butter", 1.0)],
    "Wheat Flour": [("Rice Flour", 1.0)],
    "Heavy Cream": [("Coconut Cream", 1.0)],
    "Parmesan Cheese": [("Nutritional Yeast Seasoning", 1.0)],
    "Soy Sauce": [("Coconut Aminos", 1.0)],
}

# 4. Predefined Dish Recipes (For BFS Allergen Substitution Demo)
RECIPES = {
    "Thai Satay Skewers": [
        "Peanut Butter",
        "Chicken Breast",
        "Soy Sauce",
        "Heavy Cream",
    ],
    "Tuscan Bruschetta": [
        "Wheat Flour",
        "Extra Virgin Olive Oil",
        "Parmesan Cheese",
    ],
    "Chocolate Almond Cake": [
        "Wheat Flour",
        "Almond Butter",
        "Heavy Cream",
        "Fresh Farm Eggs",
    ],
    "Creamy Mushroom Risotto": [
        "Arborio Rice",
        "Heavy Cream",
        "Parmesan Cheese",
        "Extra Virgin Olive Oil",
    ],
}

# 5. Dish Catalog (Candidates for DFS Menu Constraint Satisfaction)
# Format: List of Dictionaries 
DISH_CATALOG = [
    # --- Starters ---
    {
        "id": "s1",
        "name": "Tuscan Bruschetta",
        "category": "starter",
        "price_per_head": 9.0,
        "is_vegetarian": True,
        "is_gluten_free": False,
        "is_vegan": True,
    },
    {
        "id": "s2",
        "name": "Gluten-Free Caprese Skewers",
        "category": "starter",
        "price_per_head": 11.0,
        "is_vegetarian": True,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "s3",
        "name": "Thai Satay Skewers",
        "category": "starter",
        "price_per_head": 12.5,
        "is_vegetarian": False,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "s4",
        "name": "Garden Herb Salad",
        "category": "starter",
        "price_per_head": 8.0,
        "is_vegetarian": True,
        "is_gluten_free": True,
        "is_vegan": True,
    },

    # --- Mains ---
    {
        "id": "m1",
        "name": "Prime Ribeye Steak",
        "category": "main",
        "price_per_head": 28.0,
        "is_vegetarian": False,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "m2",
        "name": "Pan-Seared Wild Salmon",
        "category": "main",
        "price_per_head": 24.0,
        "is_vegetarian": False,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "m3",
        "name": "Wild Mushroom Risotto",
        "category": "main",
        "price_per_head": 18.0,
        "is_vegetarian": True,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "m4",
        "name": "Artisan Spinach Ravioli",
        "category": "main",
        "price_per_head": 16.5,
        "is_vegetarian": True,
        "is_gluten_free": False,
        "is_vegan": False,
    },

    # --- Desserts ---
    {
        "id": "d1",
        "name": "Dark Chocolate Lava Cake",
        "category": "dessert",
        "price_per_head": 8.5,
        "is_vegetarian": True,
        "is_gluten_free": False,
        "is_vegan": False,
    },
    {
        "id": "d2",
        "name": "Gluten-Free Berry Pavlova",
        "category": "dessert",
        "price_per_head": 9.0,
        "is_vegetarian": True,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "d3",
        "name": "Organic Fruit Sorbet Trio",
        "category": "dessert",
        "price_per_head": 6.5,
        "is_vegetarian": True,
        "is_gluten_free": True,
        "is_vegan": True,
    },
]

# 6. Client Catering Event Requests (Input Constraints for AI)
EVENTS = [
    {
        "id": "ev1",
        "title": "TechCorp Leadership Summit",
        "client": "Sarah Jenkins",
        "date": "2026-10-27",
        "guests": 85,
        "notes": "Severe Peanut Allergy; Needs at least 1 Vegetarian dish",
        "status": "Confirmed",
    },
    {
        "id": "ev2",
        "title": "Vance Executive Board Dinner",
        "client": "Marcus Vance",
        "date": "2026-11-04",
        "guests": 30,
        "notes": "Strict Gluten-Free requirement; Budget under $45 per head",
        "status": "Confirmed",
    },
    {
        "id": "ev3",
        "title": "Greenfield BioTech Annual Gala",
        "client": "Dr. Aris Thorne",
        "date": "2026-11-15",
        "guests": 120,
        "notes": "Dairy-Free and Vegetarian options mandatory",
        "status": "Planning",
    },
]
