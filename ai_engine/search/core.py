"""Core abstractions for classical state-space search.

Contains the fundamental classes:
1. SearchResult: Container for search results and metrics (nodes expanded, runtime).
2. Node: A search tree node (state, parent, action, path_cost, depth).
3. Problem: Abstract base class defining formal search problem methods.
"""

from dataclasses import dataclass, field


@dataclass
class SearchResult:
    """Stores the output and performance metrics of a search run."""
    solution_path: list = None
    total_cost: float = None
    nodes_expanded: int = 0
    nodes_generated: int = 0
    max_frontier_size: int = 0
    runtime_ms: float = 0.0
    found: bool = False
    metadata: dict = field(default_factory=dict)


class Node:
    """A node in the search tree.

    Attributes:
        state: The problem state at this node.
        parent: The previous Node in the path.
        action: The action taken to reach this node.
        path_cost: Total path cost from start to here.
        depth: Number of steps from the root.
    """

    def __class_getitem__(cls, item):
        """Allows writing Node[State, Action] for backwards compatibility."""
        return cls

    def __init__(self, state, parent=None, action=None, path_cost=0.0, heuristic_value=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = float(path_cost)
        self.depth = 0 if parent is None else parent.depth + 1
        self.heuristic_value = float(heuristic_value)

    def solution(self):
        """Returns the list of actions from the start node to this node."""
        actions = []
        curr = self
        while curr.parent is not None:
            if curr.action is not None:
                actions.append(curr.action)
            curr = curr.parent
        actions.reverse()
        return actions

    def state_path(self):
        """Returns the list of states from the start node to this node."""
        states = []
        curr = self
        while curr is not None:
            states.append(curr.state)
            curr = curr.parent
        states.reverse()
        return states

    def __repr__(self):
        return f"<Node state={self.state!r} cost={self.path_cost}>"


class Problem:
    """Base template for all search problems.

    Any specific search problem overrides:
    - initial_state()
    - actions(state)
    - result(state, action)
    - is_goal(state)
    """

    def __class_getitem__(cls, item):
        """Allows writing Problem[State, Action] for backwards compatibility."""
        return cls

    def initial_state(self):
        """Returns the starting state."""
        raise NotImplementedError

    def actions(self, state):
        """Returns a list of valid actions from the given state."""
        raise NotImplementedError

    def result(self, state, action):
        """Returns the new state after applying the action."""
        raise NotImplementedError

    def is_goal(self, state):
        """Returns True if the state satisfies the goal condition."""
        raise NotImplementedError

    def step_cost(self, state, action, next_state):
        """Cost of taking action from state to next_state. Default is 1.0."""
        return 1.0

    def heuristic(self, state):
        """Estimated cost from state to goal. Default is 0.0."""
        return 0.0

    def prune(self, state):
        """Returns True if this partial state violates constraints and should be pruned."""
        return False
