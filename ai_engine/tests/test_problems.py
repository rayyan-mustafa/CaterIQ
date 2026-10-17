"""Integration tests for all 4 AI problem modules and benchmark runner."""

import unittest
from ai_engine.problems.allergen_substitution import find_allergen_substitutions
from ai_engine.problems.menu_constraints import solve_menu_constraints
from ai_engine.problems.menu_optimizer import optimize_menu_package
from ai_engine.problems.delivery_routing import compare_route_algorithms
from ai_engine.problems.bid_pricing import advise_bid_pricing
from ai_engine.benchmarks.runner import run_all_benchmarks


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

    def test_menu_optimizer_module(self):
        slots = ["starter", "main"]
        dishes = [
            {"id": "1", "name": "Soup", "category": "starter", "price_per_head": 7.0, "popularity_score": 0.8},
            {"id": "2", "name": "Salad", "category": "starter", "price_per_head": 12.0, "popularity_score": 0.5},
            {"id": "3", "name": "Pasta", "category": "main", "price_per_head": 15.0, "popularity_score": 0.9},
            {"id": "4", "name": "Chicken", "category": "main", "price_per_head": 20.0, "popularity_score": 0.7},
        ]

        res = optimize_menu_package(
            slots=slots,
            dishes=dishes,
            max_budget=30.0,
            appeal_weight=5.0,
        )
        self.assertTrue(res["found"])
        self.assertEqual(len(res["dishes"]), 2)
        names = [d["name"] for d in res["dishes"]]
        self.assertIn("Soup", names)
        self.assertIn("Pasta", names)

    def test_delivery_routing_module(self):
        coords = {
            "A": (40.71, -74.00),
            "B": (40.73, -73.99),
            "C": (40.75, -73.98),
        }
        edges = {
            "A": [("B", 10.0)],
            "B": [("C", 15.0)],
            "C": [],
        }
        res = compare_route_algorithms(start="A", goal="C", coordinates=coords, edges=edges)
        self.assertTrue(res["astar"]["found"])
        self.assertEqual(res["astar"]["total_minutes"], 25.0)
        self.assertTrue(res["greedy"]["found"])
        self.assertLessEqual(res["astar"]["total_minutes"], res["greedy"]["total_minutes"])

    def test_bid_pricing_module(self):
        res = advise_bid_pricing(
            base_price=50.0,
            our_cost=30.0,
            headcount=100,
            competitor_est_price=48.0,
            competitor_est_cost=32.0,
            our_rating=4.9,
            competitor_rating=4.3,
            max_rounds=2,
        )
        self.assertGreaterEqual(res["recommended_price_per_head"], 30.0)
        self.assertGreaterEqual(res["expected_total_profit"], 0.0)
        self.assertTrue(res["verification"]["values_match"])
        self.assertLessEqual(res["alpha_beta"]["nodes_evaluated"], res["minimax"]["nodes_evaluated"])

    def test_benchmarks_runner(self):
        bench_data = run_all_benchmarks()
        self.assertIn("bfs_vs_dfs", bench_data)
        self.assertIn("dfs_plain_vs_pruned", bench_data)
        self.assertIn("greedy_vs_astar", bench_data)
        self.assertIn("minimax_vs_alphabeta", bench_data)


if __name__ == "__main__":
    unittest.main()
