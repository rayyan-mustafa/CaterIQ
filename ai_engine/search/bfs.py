"""Breadth-First Search (BFS).

Explores shallowest nodes first using a FIFO (First-In, First-Out) queue.
Guarantees finding the shortest path when all step costs are equal.
"""

from collections import deque
import time
from ai_engine.search.core import Node, SearchResult


def breadth_first_search(problem, max_depth=None):
    """Execute Breadth-First Search on a problem.

    Args:
        problem: An instance of Problem defining initial_state, actions, result, is_goal.
        max_depth: Optional depth limit.

    Returns:
        SearchResult containing the solution path and performance metrics.
    """
    start_time = time.perf_counter()
    initial_state = problem.initial_state()

    # Step 1: Check if the starting state is already the goal
    #Early goal check on the root. If the recipe is already allergen-free, return immediately without building queues.
    if problem.is_goal(initial_state):
        elapsed = (time.perf_counter() - start_time) * 1000.0
        return SearchResult(
            solution_path=[initial_state],
            total_cost=0.0,
            nodes_expanded=0,
            nodes_generated=1,
            max_frontier_size=1,
            runtime_ms=elapsed,
            found=True,
            metadata={"depth": 0, "actions": []},
        )

    # Step 2: Initialize FIFO Queue with root node, and track explored states
    root = Node(state=initial_state)
    frontier = deque([root])
    explored = {initial_state}

    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1

    # Step 3: Loop while queue has nodes
    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        current_node = frontier.popleft()  # FIFO: remove from front
        nodes_expanded += 1

        # Check depth limit
        if max_depth is not None and current_node.depth >= max_depth:
            continue

        # Step 4: Expand valid moves
        for action in problem.actions(current_node.state):
            child_state = problem.result(current_node.state, action)
            nodes_generated += 1

            # Only visit unexplored states
            if child_state not in explored:
                cost = current_node.path_cost + problem.step_cost(current_node.state, action, child_state)
                child_node = Node(
                    state=child_state,
                    parent=current_node,
                    action=action,
                    path_cost=cost,
                )

                # Early Goal Testing
                #before expanding more nodes check the generated node for the goal
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
                frontier.append(child_node)  # FIFO: add to back of queue

    # Step 5: Queue exhausted, no solution exists
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
