"""Search algorithms package (Weeks 1-5: Foundations, BFS, DFS)."""

from ai_engine.search.core import Node, Problem, SearchResult
from ai_engine.search.bfs import breadth_first_search
from ai_engine.search.dfs import depth_first_search

__all__ = [
    "Node",
    "Problem",
    "SearchResult",
    "breadth_first_search",
    "depth_first_search",
]
