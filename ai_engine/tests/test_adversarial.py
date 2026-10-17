"""Tests for Minimax and Alpha-Beta Pruning."""

from dataclasses import dataclass
from typing import Any, List
import unittest
from ai_engine.search.adversarial import (
    GameState,
    minimax,
    alpha_beta_search,
)


@dataclass(frozen=True)
class SimpleTreeState(GameState):
    """Explicit game tree for testing pruning exactness."""

    name: str
    turn: str
    children: tuple
    terminal_val: float = 0.0

    def is_terminal(self) -> bool:
        return len(self.children) == 0

    def to_move(self) -> str:
        return self.turn

    def utility(self, player: str = "MAX") -> float:
        return self.terminal_val

    def legal_moves(self) -> List[Any]:
        return list(range(len(self.children)))

    def make_move(self, move: int) -> GameState:
        return self.children[move]


def build_classic_textbook_tree() -> GameState:
    """Classic 2-level tree from Russell & Norvig Figure 5.2.

    MAX root:
      Child 1 (MIN): leaves 3, 12, 8 -> min is 3
      Child 2 (MIN): leaves 2, 4, 6 -> min is 2
      Child 3 (MIN): leaves 14, 5, 2 -> min is 2
    Root value = max(3, 2, 2) = 3.
    """
    c1 = SimpleTreeState(
        name="C1",
        turn="MIN",
        children=(
            SimpleTreeState("L1", "MAX", (), terminal_val=3.0),
            SimpleTreeState("L2", "MAX", (), terminal_val=12.0),
            SimpleTreeState("L3", "MAX", (), terminal_val=8.0),
        ),
    )
    c2 = SimpleTreeState(
        name="C2",
        turn="MIN",
        children=(
            SimpleTreeState("L4", "MAX", (), terminal_val=2.0),
            SimpleTreeState("L5", "MAX", (), terminal_val=4.0),
            SimpleTreeState("L6", "MAX", (), terminal_val=6.0),
        ),
    )
    c3 = SimpleTreeState(
        name="C3",
        turn="MIN",
        children=(
            SimpleTreeState("L7", "MAX", (), terminal_val=14.0),
            SimpleTreeState("L8", "MAX", (), terminal_val=5.0),
            SimpleTreeState("L9", "MAX", (), terminal_val=2.0),
        ),
    )
    root = SimpleTreeState(name="Root", turn="MAX", children=(c1, c2, c3))
    return root


class TestAdversarial(unittest.TestCase):
    def test_minimax_and_alphabeta_equivalence(self):
        root = build_classic_textbook_tree()

        mm_res = minimax(root, max_depth=3)
        ab_res = alpha_beta_search(root, max_depth=3)

        # 1. Optimal payoff must be exactly 3.0
        self.assertEqual(mm_res.expected_payoff, 3.0)
        self.assertEqual(ab_res.expected_payoff, 3.0)

        # 2. Both must pick the first branch (Child 1)
        self.assertEqual(mm_res.best_move, 0)
        self.assertEqual(ab_res.best_move, 0)

        # 3. Alpha-Beta must evaluate strictly fewer nodes than full Minimax
        self.assertLess(ab_res.nodes_evaluated, mm_res.nodes_evaluated)
        self.assertGreater(ab_res.pruned_branches, 0)


if __name__ == "__main__":
    unittest.main()
