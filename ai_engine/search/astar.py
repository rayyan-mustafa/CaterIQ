"""A* (A-Star) Search.

Expands nodes ordered by evaluation function f(n) = g(n) + h(n),
where g(n) is the exact cost from initial state to n,
and h(n) is the heuristic estimate of cost from n to goal.
Guaranteed to find optimal cost solution if heuristic is admissible (and consistent for graph search).
"""

from __future__ import annotations
import heapq
import time
from typing import Dict, Optional
from ai_engine.search.core import Node, Problem, SearchResult


def astar_search(problem: Problem, max_depth: Optional[int] = None) -> SearchResult:
    """Execute A* Search.

    Args:
        problem: Problem instance with step_cost and heuristic methods.
        max_depth: Optional maximum search depth.

    Returns:
        SearchResult with optimal path, total cost, and efficiency metrics.
    """
    start_time = time.perf_counter()
    initial = problem.initial_state()

    root = Node(
        state=initial,
        path_cost=0.0,
        heuristic_value=problem.heuristic(initial),
    )

    f_init = root.path_cost + root.heuristic_value
    # Priority queue entry: (f_score, node)
    frontier = [(f_init, root)]
    best_g: Dict[object, float] = {initial: 0.0}

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        f_cost, node = heapq.heappop(frontier)

        # Goal test on expansion guarantees optimality
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
                    "f_cost": f_cost,
                },
            )

        # If we have already reached this state with a strictly lower path cost, skip
        if node.path_cost > best_g.get(node.state, float("inf")):
            continue

        nodes_expanded += 1

        if max_depth is not None and node.depth >= max_depth:
            continue

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            step_c = problem.step_cost(node.state, action, child_state)
            new_g = node.path_cost + step_c
            nodes_generated += 1

            if new_g < best_g.get(child_state, float("inf")):
                best_g[child_state] = new_g
                h = problem.heuristic(child_state)
                child_node = Node(
                    state=child_state,
                    parent=node,
                    action=action,
                    path_cost=new_g,
                    heuristic_value=h,
                )
                heapq.heappush(frontier, (new_g + h, child_node))

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
