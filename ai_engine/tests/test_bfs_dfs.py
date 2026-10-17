"""Tests for BFS and DFS algorithms."""

import unittest
from ai_engine.search.core import Problem
from ai_engine.search.bfs import breadth_first_search
from ai_engine.search.dfs import depth_first_search


class LinearGraphProblem(Problem[int, int]):
    """1 -> 2 -> 3 -> 4 -> 5."""

    def __init__(self, target: int = 5):
        self.target = target

    def initial_state(self) -> int:
        return 1

    def actions(self, state: int):
        if state < 10:
            return [state + 1]
        return []

    def result(self, state: int, action: int) -> int:
        return action

    def is_goal(self, state: int) -> bool:
        return state == self.target


class CyclicGraphProblem(Problem[str, str]):
    """Graph with cycles: A -> B -> C -> A, and B -> Target."""

    def initial_state(self) -> str:
        return "A"

    def actions(self, state: str):
        graph = {
            "A": ["B"],
            "B": ["C", "Target"],
            "C": ["A"],
            "Target": [],
        }
        return graph.get(state, [])

    def result(self, state: str, action: str) -> str:
        return action

    def is_goal(self, state: str) -> bool:
        return state == "Target"


class TestBfsDfs(unittest.TestCase):
    def test_bfs_linear(self):
        prob = LinearGraphProblem(target=4)
        res = breadth_first_search(prob)
        self.assertTrue(res.found)
        self.assertEqual(res.solution_path, [1, 2, 3, 4])
        self.assertEqual(res.metadata["depth"], 3)

    def test_bfs_cyclic(self):
        prob = CyclicGraphProblem()
        res = breadth_first_search(prob)
        self.assertTrue(res.found)
        self.assertEqual(res.solution_path, ["A", "B", "Target"])

    def test_bfs_initial_is_goal(self):
        prob = LinearGraphProblem(target=1)
        res = breadth_first_search(prob)
        self.assertTrue(res.found)
        self.assertEqual(res.solution_path, [1])
        self.assertEqual(res.nodes_expanded, 0)

    def test_dfs_linear(self):
        prob = LinearGraphProblem(target=5)
        res = depth_first_search(prob)
        self.assertTrue(res.found)
        self.assertEqual(res.solution_path, [1, 2, 3, 4, 5])

    def test_dfs_no_solution(self):
        prob = LinearGraphProblem(target=99)
        res = depth_first_search(prob, max_depth=5)
        self.assertFalse(res.found)
        self.assertIsNone(res.solution_path)


if __name__ == "__main__":
    unittest.main()
