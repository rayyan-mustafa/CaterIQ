"""Greedy Best-First Search.

Expands node with lowest estimated cost to goal h(n).
Fast heuristic search; not guaranteed to find optimal-cost path.
"""

from __future__ import annotations
import heapq
import time
from typing import Optional, Set
from ai_engine.search.core import Node, Problem, SearchResult


def greedy_best_first_search(problem: Problem, max_depth: Optional[int] = None) -> SearchResult:
    """Execute Greedy Best-First Search.

    Prioritizes frontier nodes strictly by heuristic value h(n).

    Args:
        problem: Problem instance with heuristic(state) implemented.
        max_depth: Optional depth cutoff.

    Returns:
        SearchResult with path and performance metrics.
    """
    start_time = time.perf_counter()
    initial = problem.initial_state()

    if problem.is_goal(initial):
        elapsed = (time.perf_counter() - start_time) * 1000.0
        return SearchResult(
            solution_path=[initial],
            total_cost=0.0,
            nodes_expanded=0,
            nodes_generated=1,
            max_frontier_size=1,
            runtime_ms=elapsed,
            found=True,
            metadata={"depth": 0, "actions": []},
        )

    root = Node(state=initial, heuristic_value=problem.heuristic(initial))

    # Priority queue item: (heuristic, node)
    frontier = [(root.heuristic_value, root)]
    explored: Set[object] = set()

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        _, node = heapq.heappop(frontier)

        if problem.is_goal(node.state):
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return SearchResult(
                solution_path=node.state_path(),
                total_cost=node.path_cost,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                max_frontier_size=max_frontier_size,
                runtime_ms=elapsed,
                found=True,
                metadata={
                    "depth": node.depth,
                    "actions": node.solution(),
                    "final_heuristic": node.heuristic_value,
                },
            )

        if node.state in explored:
            continue
        explored.add(node.state)
        nodes_expanded += 1

        if max_depth is not None and node.depth >= max_depth:
            continue

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            nodes_generated += 1

            if child_state not in explored:
                cost = node.path_cost + problem.step_cost(node.state, action, child_state)
                h = problem.heuristic(child_state)
                child_node = Node(
                    state=child_state,
                    parent=node,
                    action=action,
                    path_cost=cost,
                    heuristic_value=h,
                )
                heapq.heappush(frontier, (h, child_node))

    elapsed = (time.perf_counter() - start_time) * 1000.0
    return SearchResult(
        solution_path=None,
        total_cost=None,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        runtime_ms=elapsed,
        found=False,
        metadata={"reason": "exhausted"},
    )
