"""Module D — Bid Pricing Advisor (Minimax + Alpha-Beta Pruning).

Simulates competitive 2-player bidding against a rival caterer.
MAX = Our caterer (wants to maximize expected profit margin).
MIN = Rival caterer (wants to minimize our advantage/win the bid).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
from ai_engine.search.adversarial import (
    GameState,
    minimax,
    alpha_beta_search,
)


@dataclass(frozen=True)
class BidState(GameState):
    """Immutable state in the bidding game."""

    round_num: int
    max_rounds: int
    turn: str  # 'MAX' or 'MIN'
    our_price: float
    competitor_price: float
    our_cost: float
    competitor_est_cost: float
    headcount: int
    our_quality_rating: float
    competitor_quality_rating: float
    allowed_multipliers: Tuple[float, ...]

    def is_terminal(self) -> bool:
        """Game ends when max rounds are reached."""
        return self.round_num >= self.max_rounds

    def to_move(self) -> str:
        return self.turn

    def legal_moves(self) -> List[float]:
        """Available percentage price adjustments."""
        return list(self.allowed_multipliers)

    def make_move(self, multiplier: float) -> BidState:
        """Produce the next game state after a price choice."""
        if self.turn == "MAX":
            new_our_price = max(self.our_cost * 1.05, self.our_price * (1.0 + multiplier))
            return BidState(
                round_num=self.round_num,
                max_rounds=self.max_rounds,
                turn="MIN",
                our_price=new_our_price,
                competitor_price=self.competitor_price,
                our_cost=self.our_cost,
                competitor_est_cost=self.competitor_est_cost,
                headcount=self.headcount,
                our_quality_rating=self.our_quality_rating,
                competitor_quality_rating=self.competitor_quality_rating,
                allowed_multipliers=self.allowed_multipliers,
            )
        else:
            new_comp_price = max(
                self.competitor_est_cost * 1.02,
                self.competitor_price * (1.0 + multiplier),
            )
            return BidState(
                round_num=self.round_num + 1,
                max_rounds=self.max_rounds,
                turn="MAX",
                our_price=self.our_price,
                competitor_price=new_comp_price,
                our_cost=self.our_cost,
                competitor_est_cost=self.competitor_est_cost,
                headcount=self.headcount,
                our_quality_rating=self.our_quality_rating,
                competitor_quality_rating=self.competitor_quality_rating,
                allowed_multipliers=self.allowed_multipliers,
            )

    def utility(self, player: str = "MAX") -> float:
        """Compute the payoff at a terminal state.

        Client decision rule:
        The client evaluates price adjusted by perceived quality reputation.
        Quality advantage allows a higher price threshold.
        """
        # Quality bonus (e.g., $2.00 per rating point difference)
        quality_offset = (self.our_quality_rating - self.competitor_quality_rating) * 2.5
        effective_our_price = self.our_price - quality_offset

        # If we win the client bid
        if effective_our_price <= self.competitor_price:
            profit_per_head = self.our_price - self.our_cost
            total_profit = max(0.0, profit_per_head * self.headcount)
            return total_profit
        else:
            # We lost the contract
            return 0.0


def advise_bid_pricing(
    base_price: float,
    our_cost: float,
    headcount: int,
    competitor_est_price: float,
    competitor_est_cost: float,
    our_rating: float = 4.8,
    competitor_rating: float = 4.5,
    max_rounds: int = 3,
) -> Dict[str, Any]:
    """Execute Minimax and Alpha-Beta advisor on competitive pricing."""
    # Action set: [-8%, -4%, 0%, +4%, +8%]
    multipliers = (-0.08, -0.04, 0.0, 0.04, 0.08)

    initial_state = BidState(
        round_num=0,
        max_rounds=max_rounds,
        turn="MAX",
        our_price=base_price,
        competitor_price=competitor_est_price,
        our_cost=our_cost,
        competitor_est_cost=competitor_est_cost,
        headcount=headcount,
        our_quality_rating=our_rating,
        competitor_quality_rating=competitor_rating,
        allowed_multipliers=multipliers,
    )

    # Run Alpha-Beta search (production algorithm)
    ab_result = alpha_beta_search(initial_state, max_depth=max_rounds * 2)

    # Run plain Minimax for comparison verification
    mm_result = minimax(initial_state, max_depth=max_rounds * 2)

    best_mult = ab_result.best_move if ab_result.best_move is not None else 0.0
    recommended_price = round(max(our_cost * 1.05, base_price * (1.0 + best_mult)), 2)
    expected_profit = round(ab_result.expected_payoff, 2)
    margin_pct = (
        round(((recommended_price - our_cost) / recommended_price) * 100, 1)
        if recommended_price > 0
        else 0.0
    )

    # Verification: Minimax and Alpha-Beta must match in expected value
    values_match = abs(ab_result.expected_payoff - mm_result.expected_payoff) < 1e-4

    return {
        "recommended_price_per_head": recommended_price,
        "recommended_adjustment_pct": round(best_mult * 100, 1),
        "expected_total_profit": expected_profit,
        "projected_margin_pct": margin_pct,
        "alpha_beta": {
            "nodes_evaluated": ab_result.nodes_evaluated,
            "pruned_branches": ab_result.pruned_branches,
            "runtime_ms": ab_result.runtime_ms,
        },
        "minimax": {
            "nodes_evaluated": mm_result.nodes_evaluated,
            "runtime_ms": mm_result.runtime_ms,
        },
        "verification": {
            "values_match": values_match,
            "pruning_efficiency_pct": round(
                (1.0 - (ab_result.nodes_evaluated / max(1, mm_result.nodes_evaluated))) * 100,
                1,
            ),
        },
    }
