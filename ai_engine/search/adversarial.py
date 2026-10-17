"""Adversarial Search: Minimax and Alpha-Beta Pruning.

Used for 2-player zero-sum (or competitive) decision problems.
Provides both full minimax and alpha-beta pruning to benchmark branch cutoffs.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import time
from typing import Any, List, Optional, Tuple


@dataclass
class AdversarialResult:
    """Results from minimax and alpha-beta search."""

    best_move: Any
    expected_payoff: float
    nodes_evaluated: int
    pruned_branches: int
    runtime_ms: float
    tree_depth: int
    principal_variation: List[Any] = field(default_factory=list)


class GameState:
    """Abstract interface for a 2-player game state."""

    def is_terminal(self) -> bool:
        raise NotImplementedError

    def utility(self, player: str) -> float:
        """Payoff from perspective of 'MAX'."""
        raise NotImplementedError

    def to_move(self) -> str:
        """Returns 'MAX' or 'MIN'."""
        raise NotImplementedError

    def legal_moves(self) -> List[Any]:
        raise NotImplementedError

    def make_move(self, move: Any) -> GameState:
        raise NotImplementedError


def minimax(
    state: GameState,
    max_depth: int = 4,
    maximizing_player: bool = True,
) -> AdversarialResult:
    """Full Minimax search without pruning.

    Exhaustively searches tree to max_depth.
    """
    start_time = time.perf_counter()
    nodes_evaluated = 0

    def _minimax_rec(curr_state: GameState, depth: int, is_max: bool) -> Tuple[float, Optional[Any]]:
        nonlocal nodes_evaluated
        nodes_evaluated += 1

        if depth == 0 or curr_state.is_terminal():
            return curr_state.utility("MAX"), None

        moves = curr_state.legal_moves()
        if not moves:
            return curr_state.utility("MAX"), None

        if is_max:
            best_val = float("-inf")
            best_move = moves[0]
            for m in moves:
                next_st = curr_state.make_move(m)
                val, _ = _minimax_rec(next_st, depth - 1, False)
                if val > best_val:
                    best_val = val
                    best_move = m
            return best_val, best_move
        else:
            best_val = float("inf")
            best_move = moves[0]
            for m in moves:
                next_st = curr_state.make_move(m)
                val, _ = _minimax_rec(next_st, depth - 1, True)
                if val < best_val:
                    best_val = val
                    best_move = m
            return best_val, best_move

    val, move = _minimax_rec(state, max_depth, maximizing_player)
    elapsed = (time.perf_counter() - start_time) * 1000.0

    return AdversarialResult(
        best_move=move,
        expected_payoff=val,
        nodes_evaluated=nodes_evaluated,
        pruned_branches=0,
        runtime_ms=elapsed,
        tree_depth=max_depth,
    )


def alpha_beta_search(
    state: GameState,
    max_depth: int = 4,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    maximizing_player: bool = True,
) -> AdversarialResult:
    """Minimax search enhanced with Alpha-Beta Pruning.

    Prunes branches that cannot influence the final decision.
    Guaranteed to return the identical optimal value as minimax,
    with significantly fewer evaluated nodes.
    """
    start_time = time.perf_counter()
    nodes_evaluated = 0
    pruned_branches = 0

    def _alphabeta_rec(
        curr_state: GameState,
        depth: int,
        a: float,
        b: float,
        is_max: bool,
    ) -> Tuple[float, Optional[Any]]:
        nonlocal nodes_evaluated, pruned_branches
        nodes_evaluated += 1

        if depth == 0 or curr_state.is_terminal():
            return curr_state.utility("MAX"), None

        moves = curr_state.legal_moves()
        if not moves:
            return curr_state.utility("MAX"), None

        if is_max:
            value = float("-inf")
            best_m = moves[0]
            for m in moves:
                next_st = curr_state.make_move(m)
                child_val, _ = _alphabeta_rec(next_st, depth - 1, a, b, False)
                if child_val > value:
                    value = child_val
                    best_m = m
                a = max(a, value)
                if a >= b:
                    pruned_branches += 1
                    break  # Beta cutoff
            return value, best_m
        else:
            value = float("inf")
            best_m = moves[0]
            for m in moves:
                next_st = curr_state.make_move(m)
                child_val, _ = _alphabeta_rec(next_st, depth - 1, a, b, True)
                if child_val < value:
                    value = child_val
                    best_m = m
                b = min(b, value)
                if a >= b:
                    pruned_branches += 1
                    break  # Alpha cutoff
            return value, best_m

    val, move = _alphabeta_rec(state, max_depth, alpha, beta, maximizing_player)
    elapsed = (time.perf_counter() - start_time) * 1000.0

    return AdversarialResult(
        best_move=move,
        expected_payoff=val,
        nodes_evaluated=nodes_evaluated,
        pruned_branches=pruned_branches,
        runtime_ms=elapsed,
        tree_depth=max_depth,
    )
