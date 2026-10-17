"""Depth-First Search (DFS) with Backtracking and Pruning.

Explores the deepest node first.
Provides both plain backtracking and early constraint-pruning modes
to demonstrate search tree reduction on the benchmark page.
"""

from __future__ import annotations
import time
from typing import List, Optional
from ai_engine.search.core import Node, Problem, SearchResult


def depth_first_search(
    problem: Problem,
    use_pruning: bool = True,
    max_depth: Optional[int] = None,
    find_all: bool = False,
    max_solutions: int = 1,
) -> SearchResult:
    """Execute Depth-First Search with optional early constraint pruning.

    Args:
        problem: Problem instance.
        use_pruning: If True, calls problem.prune(state) to cut unpromising branches early.
        max_depth: Depth limit to prevent infinite loops.
        find_all: If True, gathers multiple valid solutions up to max_solutions.
        max_solutions: Maximum solutions to collect when find_all is True.

    Returns:
        SearchResult containing the found path (or paths) and search metrics.
    """
    start_time = time.perf_counter()
    initial = problem.initial_state()

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1

    solutions: List[Node] = []

    # Stack holds Node objects
    root = Node(state=initial)
    stack: List[Node] = [root]

    # For cyclic graph safety, keep track of current branch ancestors
    # or visited states when appropriate
    while stack:
        max_frontier_size = max(max_frontier_size, len(stack))
        node = stack.pop()
        nodes_expanded += 1

        # Check goal condition
        if problem.is_goal(node.state):
            solutions.append(node)
            if not find_all or len(solutions) >= max_solutions:
                break
            continue

        if max_depth is not None and node.depth >= max_depth:
            continue

        # Generate actions and branch
        actions = problem.actions(node.state)

        # Iterate in reverse so the first action is popped and explored first
        for action in reversed(actions):
            child_state = problem.result(node.state, action)
            nodes_generated += 1

            # Early pruning check (course requirement: plain DFS vs DFS with pruning)
            if use_pruning and problem.prune(child_state):
                continue

            cost = node.path_cost + problem.step_cost(node.state, action, child_state)
            child_node = Node(
                state=child_state,
                parent=node,
                action=action,
                path_cost=cost,
            )
            stack.append(child_node)

    elapsed = (time.perf_counter() - start_time) * 1000.0

    if solutions:
        best_node = solutions[0]
        all_paths = [s.state_path() for s in solutions]
        return SearchResult(
            solution_path=best_node.state_path(),
            total_cost=best_node.path_cost,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            runtime_ms=elapsed,
            found=True,
            metadata={
                "depth": best_node.depth,
                "actions": best_node.solution(),
                "solutions_found": len(solutions),
                "all_solutions": all_paths,
                "pruning_enabled": use_pruning,
            },
        )

    return SearchResult(
        solution_path=None,
        total_cost=None,
        nodes_expanded=nodes_expanded,
        nodes_generated=nodes_generated,
        max_frontier_size=max_frontier_size,
        runtime_ms=elapsed,
        found=False,
        metadata={"pruning_enabled": use_pruning, "reason": "exhausted"},
    )
