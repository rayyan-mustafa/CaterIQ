"""Breadth-First Search (BFS).

Explores shallowest unexpanded nodes first using a FIFO queue.
Guarantees finding the solution with the minimum number of steps (unit costs).
"""

from __future__ import annotations
import collections
import time
from typing import Optional, Set
from ai_engine.search.core import Node, Problem, SearchResult


def breadth_first_search(problem: Problem, max_depth: Optional[int] = None) -> SearchResult:
    """Execute Breadth-First Search on the given problem.

    Args:
        problem: Problem instance defining initial_state, actions, result, is_goal.
        max_depth: Optional cutoff depth to prevent runaway exploration.

    Returns:
        SearchResult containing solution path, total cost, and exploration metrics.
    """
    start_time = time.perf_counter()
    initial = problem.initial_state()

    # Early check for initial state
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

    root = Node(state=initial)
    frontier = collections.deque([root])
    explored: Set[object] = {initial}

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        node = frontier.popleft()
        nodes_expanded += 1

        if max_depth is not None and node.depth >= max_depth:
            continue

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            nodes_generated += 1

            if child_state not in explored:
                cost = node.path_cost + problem.step_cost(node.state, action, child_state)
                child_node = Node(
                    state=child_state,
                    parent=node,
                    action=action,
                    path_cost=cost,
                )

                if problem.is_goal(child_state):
                    elapsed = (time.perf_counter() - start_time) * 1000.0
                    return SearchResult(
                        solution_path=child_node.state_path(),
                        total_cost=child_node.path_cost,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier_size,
                        runtime_ms=elapsed,
                        found=True,
                        metadata={
                            "depth": child_node.depth,
                            "actions": child_node.solution(),
                        },
                    )

                explored.add(child_state)
                frontier.append(child_node)

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
