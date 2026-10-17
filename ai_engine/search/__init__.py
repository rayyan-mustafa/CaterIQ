"""Search algorithms package."""

from ai_engine.search.core import Node, Problem, SearchResult
from ai_engine.search.bfs import breadth_first_search
from ai_engine.search.dfs import depth_first_search
from ai_engine.search.greedy import greedy_best_first_search
from ai_engine.search.astar import astar_search
from ai_engine.search.adversarial import minimax, alpha_beta_search

__all__ = [
    "Node",
    "Problem",
    "SearchResult",
    "breadth_first_search",
    "depth_first_search",
    "greedy_best_first_search",
    "astar_search",
    "minimax",
    "alpha_beta_search",
]
