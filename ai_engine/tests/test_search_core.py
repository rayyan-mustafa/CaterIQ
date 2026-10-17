"""Unit tests for Node, Problem, and SearchResult."""

import unittest
from ai_engine.search.core import Node, Problem, SearchResult


class ToyGraphProblem(Problem[str, str]):
    def __init__(self):
        self.adj = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }

    def initial_state(self) -> str:
        return "A"

    def actions(self, state: str):
        return self.adj.get(state, [])

    def result(self, state: str, action: str) -> str:
        return action

    def is_goal(self, state: str) -> bool:
        return state == "D"


class TestSearchCore(unittest.TestCase):
    def test_node_path_and_solution(self):
        root = Node("A")
        child1 = Node("B", parent=root, action="A->B", path_cost=1.0)
        child2 = Node("D", parent=child1, action="B->D", path_cost=2.0)

        self.assertEqual(child2.depth, 2)
        self.assertEqual(child2.path_cost, 2.0)
        self.assertEqual(child2.solution(), ["A->B", "B->D"])
        self.assertEqual(child2.state_path(), ["A", "B", "D"])
        self.assertIn("cost=2.0", repr(child2))

    def test_problem_defaults(self):
        prob = ToyGraphProblem()
        self.assertEqual(prob.initial_state(), "A")
        self.assertEqual(prob.step_cost("A", "B", "B"), 1.0)
        self.assertEqual(prob.heuristic("B"), 0.0)
        self.assertFalse(prob.prune("B"))


if __name__ == "__main__":
    unittest.main()
