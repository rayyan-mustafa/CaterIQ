"""Tests for Greedy Best-First and A* algorithms."""

import unittest
from ai_engine.search.core import Problem
from ai_engine.search.greedy import greedy_best_first_search
from ai_engine.search.astar import astar_search


class DeceptiveRouteProblem(Problem[str, str]):
    """A deceptive graph where greedy chooses a path that looks closer, but A* finds the true optimal route."""

    def __init__(self):
        self.heuristics = {
            "Start": 100.0,
            "DirectMid": 10.0,
            "DetourMid": 80.0,
            "Goal": 0.0,
        }
        self.adj = {
            "Start": [("DirectMid", 50.0), ("DetourMid", 10.0)],
            "DirectMid": [("Goal", 50.0)],
            "DetourMid": [("Goal", 20.0)],
            "Goal": [],
        }

    def initial_state(self) -> str:
        return "Start"

    def actions(self, state: str):
        return [dest for dest, _ in self.adj.get(state, [])]

    def result(self, state: str, action: str) -> str:
        return action

    def is_goal(self, state: str) -> bool:
        return state == "Goal"

    def step_cost(self, state: str, action: str, next_state: str) -> float:
        for dest, cost in self.adj.get(state, []):
            if dest == next_state:
                return cost
        return 1.0

    def heuristic(self, state: str) -> float:
        return self.heuristics.get(state, 0.0)


class TestGreedyAstar(unittest.TestCase):
    def test_greedy_vs_astar_optimality(self):
        prob = DeceptiveRouteProblem()

        greedy_res = greedy_best_first_search(prob)
        astar_res = astar_search(prob)

        self.assertTrue(greedy_res.found)
        self.assertTrue(astar_res.found)

        self.assertEqual(greedy_res.solution_path, ["Start", "DirectMid", "Goal"])
        self.assertEqual(greedy_res.total_cost, 100.0)

        self.assertEqual(astar_res.solution_path, ["Start", "DetourMid", "Goal"])
        self.assertEqual(astar_res.total_cost, 30.0)

        # Course verification: A* cost <= Greedy cost
        self.assertLessEqual(astar_res.total_cost, greedy_res.total_cost)


if __name__ == "__main__":
    unittest.main()
