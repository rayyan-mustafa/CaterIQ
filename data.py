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
    # --- Starters (Sorted by Tier for Branch & Bound DFS) ---
    {
        "id": "s7",
        "name": "Pan-Seared Hokkaido Scallops",
        "category": "starter",
        "price_per_head": 18.0,
        "is_vegetarian": False,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "s6",
        "name": "Jumbo Lump Crab Cakes",
        "category": "starter",
        "price_per_head": 16.0,
        "is_vegetarian": False,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "s5",
        "name": "Truffled Wild Mushroom Tart",
        "category": "starter",
        "price_per_head": 14.5,
        "is_vegetarian": True,
        "is_gluten_free": False,
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
        "id": "s2",
        "name": "Gluten-Free Caprese Skewers",
        "category": "starter",
        "price_per_head": 11.0,
        "is_vegetarian": True,
        "is_gluten_free": True,
        "is_vegan": False,
    },
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
        "id": "m7",
        "name": "A5 Wagyu Tenderloin Steak",
        "category": "main",
        "price_per_head": 42.0,
        "is_vegetarian": False,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "m6",
        "name": "Butter-Poached Maine Lobster Tail",
        "category": "main",
        "price_per_head": 38.5,
        "is_vegetarian": False,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "m5",
        "name": "Roasted Mediterranean Sea Bass",
        "category": "main",
        "price_per_head": 32.0,
        "is_vegetarian": False,
        "is_gluten_free": True,
        "is_vegan": False,
    },
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
        "id": "d5",
        "name": "24k Gold Dark Chocolate Gianduja",
        "category": "dessert",
        "price_per_head": 13.5,
        "is_vegetarian": True,
        "is_gluten_free": True,
        "is_vegan": False,
    },
    {
        "id": "d4",
        "name": "Tahitian Vanilla Bean Soufflé",
        "category": "dessert",
        "price_per_head": 11.0,
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
        "id": "d1",
        "name": "Dark Chocolate Lava Cake",
        "category": "dessert",
        "price_per_head": 8.5,
        "is_vegetarian": True,
        "is_gluten_free": False,
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

# 6. Client Catering Event Requests (Input Constraints for Real-World AI Delivery)
EVENTS = [
    {
        "id": "ev1",
        "title": "TechCorp Leadership Summit",
        "client": "Sarah Jenkins",
        "date": "2026-10-27",
        "guests": 85,
        "status": "Confirmed",
        "budget_per_head": 48.0,
        "min_vegetarian": 1,
        "min_gluten_free": 0,
        "requested_dish": "Thai Satay Skewers",
        "target_allergens": ["peanut"],
        "allergy_context": "Keynote speaker has severe peanut anaphylaxis",
        "notes": "Severe Peanut Allergy; Needs at least 1 Vegetarian dish in 3-course package; Budget $48/head",
    },
    {
        "id": "ev2",
        "title": "Vance Executive Board Dinner",
        "client": "Marcus Vance",
        "date": "2026-11-04",
        "guests": 30,
        "status": "Confirmed",
        "budget_per_head": 44.0,
        "min_vegetarian": 0,
        "min_gluten_free": 2,
        "requested_dish": "Tuscan Bruschetta",
        "target_allergens": ["gluten"],
        "allergy_context": "Board members require certified Celiac-safe appetizers",
        "notes": "Strict Gluten-Free requirement (min 2 GF dishes); Bruschetta must be adapted; Budget under $44/head",
    },
    {
        "id": "ev3",
        "title": "Greenfield BioTech Annual Gala",
        "client": "Dr. Aris Thorne",
        "date": "2026-11-15",
        "guests": 120,
        "status": "Planning",
        "budget_per_head": 42.0,
        "min_vegetarian": 2,
        "min_gluten_free": 1,
        "requested_dish": "Chocolate Almond Cake",
        "target_allergens": ["dairy"],
        "allergy_context": "Eco-friendly banquet with mandatory non-dairy dessert",
        "notes": "Dairy-Free dessert adaptation; Minimum 2 Vegetarian & 1 Gluten-Free dishes; Budget $42/head",
    },
]

