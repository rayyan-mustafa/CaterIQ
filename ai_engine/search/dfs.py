"""Depth-First Search (DFS) with Backtracking and Pruning.

Explores deep down a branch first using a LIFO (Last-In, First-Out) stack.
Supports early constraint pruning to reject invalid branches early.
"""

import time
from ai_engine.search.core import Node, SearchResult


def depth_first_search(problem, use_pruning=True, max_depth=None, find_all=False, max_solutions=1):
    """Execute Depth-First Search with optional constraint pruning.

    Args:
        problem: An instance of Problem.
        use_pruning: If True, calls problem.prune() to skip invalid branches.
        max_depth: Optional depth limit.
        find_all: Whether to collect multiple solutions.
        max_solutions: Max number of solutions to return.

    Returns:
        SearchResult containing the solution path and metrics.
    """
    start_time = time.perf_counter()
    initial_state = problem.initial_state()

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    solutions = []

    # Step 1: Initialize stack with root node
    root = Node(state=initial_state)
    stack = [root]

    # Step 2: Loop while stack has nodes
    while stack:
        max_frontier_size = max(max_frontier_size, len(stack))
        current_node = stack.pop()  # LIFO: remove from top of stack
        nodes_expanded += 1

        # Step 3: Check goal condition
        if problem.is_goal(current_node.state):
            solutions.append(current_node)
            if not find_all or len(solutions) >= max_solutions:
                break
            continue

        # Check depth limit
        if max_depth is not None and current_node.depth >= max_depth:
            continue

        # Step 4: Expand valid moves
        actions = problem.actions(current_node.state)

        # Explore in reverse so the first action is popped and tested first
        for action in reversed(actions):
            child_state = problem.result(current_node.state, action)
            nodes_generated += 1

            # EARLY PRUNING: Stop if the constraint is already violated!
            if use_pruning and problem.prune(child_state):
                continue  # Discard branch, do not push to stack

            cost = current_node.path_cost + problem.step_cost(current_node.state, action, child_state)
            child_node = Node(
                state=child_state,
                parent=current_node,
                action=action,
                path_cost=cost,
            )
            stack.append(child_node)

    elapsed = (time.perf_counter() - start_time) * 1000.0

    # Step 5: Format and return result
    if solutions:
        best_node = solutions[0]
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
        metadata={"reason": "exhausted"},
    )
