"""Integration tests for Week 1-5 AI problem modules (BFS & DFS)."""

import unittest
from ai_engine.problems.allergen_substitution import find_allergen_substitutions
from ai_engine.problems.menu_constraints import solve_menu_constraints


class TestProblems(unittest.TestCase):
    def test_allergen_substitution_module(self):
        ingredients = ["peanut_oil", "chicken_breast", "soy_sauce"]
        allergens = {
            "peanut_oil": ["peanut"],
            "sunflower_oil": [],
            "chicken_breast": [],
            "soy_sauce": ["soy"],
            "coconut_aminos": [],
        }
        subs = {
            "peanut_oil": [("sunflower_oil", 1.0)],
            "soy_sauce": [("coconut_aminos", 1.0)],
        }

        # Case 1: Eliminate peanut
        res1 = find_allergen_substitutions(
            ingredients=ingredients,
            ingredient_allergens=allergens,
            allowed_substitutions=subs,
            target_allergens=["peanut"],
        )
        self.assertTrue(res1.found)
        self.assertEqual(len(res1.swaps_required), 1)
        self.assertEqual(res1.swaps_required[0], {"from": "peanut_oil", "to": "sunflower_oil"})
        self.assertIn("sunflower_oil", res1.safe_ingredients)
        self.assertNotIn("peanut_oil", res1.safe_ingredients)

        # Case 2: Impossible substitution (no replacement exists)
        res2 = find_allergen_substitutions(
            ingredients=["chicken_breast"],
            ingredient_allergens={"chicken_breast": ["poultry"]},
            allowed_substitutions={},
            target_allergens=["poultry"],
        )
        self.assertFalse(res2.found)
        self.assertIsNone(res2.safe_ingredients)

    def test_menu_constraint_module(self):
        slots = ["starter", "main", "dessert"]
        dishes = [
            {"id": "1", "name": "Bruschetta", "category": "starter", "price_per_head": 8.0, "is_vegetarian": True, "is_gluten_free": False},
            {"id": "2", "name": "Beef Tartare", "category": "starter", "price_per_head": 12.0, "is_vegetarian": False, "is_gluten_free": True},
            {"id": "3", "name": "Mushroom Risotto", "category": "main", "price_per_head": 20.0, "is_vegetarian": True, "is_gluten_free": True},
            {"id": "4", "name": "Ribeye Steak", "category": "main", "price_per_head": 32.0, "is_vegetarian": False, "is_gluten_free": True},
            {"id": "5", "name": "Fruit Sorbet", "category": "dessert", "price_per_head": 6.0, "is_vegetarian": True, "is_gluten_free": True},
        ]

        # Under budget $38, need at least 1 vegetarian and 1 gluten-free
        res = solve_menu_constraints(
            slots=slots,
            dishes=dishes,
            max_budget=38.0,
            min_vegetarian=1,
            min_gluten_free=1,
            use_pruning=True,
        )
        self.assertTrue(res["found"])
        self.assertGreater(len(res["packages"]), 0)
        package = res["packages"][0]
        self.assertLessEqual(package["total_price_per_head"], 38.0)

        # Pruned DFS should expand <= Plain DFS
        res_plain = solve_menu_constraints(
            slots=slots,
            dishes=dishes,
            max_budget=38.0,
            min_vegetarian=1,
            min_gluten_free=1,
            use_pruning=False,
        )
        self.assertLessEqual(res["nodes_expanded"], res_plain["nodes_expanded"])


if __name__ == "__main__":
    unittest.main()

