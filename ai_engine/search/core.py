"""Core abstractions for classical state-space search.

Follows standard AI formulation (Russell & Norvig, AI: A Modern Approach).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, TypeVar

StateT = TypeVar("StateT")
ActionT = TypeVar("ActionT")


@dataclass
class SearchResult:
    """Unified container for search metrics and results."""

    solution_path: Optional[List[Any]] = None
    total_cost: Optional[float] = None
    nodes_expanded: int = 0
    nodes_generated: int = 0
    max_frontier_size: int = 0
    runtime_ms: float = 0.0
    found: bool = False
    metadata: dict = field(default_factory=dict)


class Node(Generic[StateT, ActionT]):
    """Search tree node representing a path from initial state to state."""

    __slots__ = ("state", "parent", "action", "path_cost", "depth", "heuristic_value", "_entry_id")
    _counter = 0

    def __init__(
        self,
        state: StateT,
        parent: Optional[Node[StateT, ActionT]] = None,
        action: Optional[ActionT] = None,
        path_cost: float = 0.0,
        heuristic_value: float = 0.0,
    ) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1
        self.heuristic_value = heuristic_value
        Node._counter += 1
        self._entry_id = Node._counter

    def solution(self) -> List[ActionT]:
        """Return the sequence of actions from root to this node."""
        actions: List[ActionT] = []
        curr = self
        while curr.parent is not None:
            if curr.action is not None:
                actions.append(curr.action)
            curr = curr.parent
        actions.reverse()
        return actions

    def state_path(self) -> List[StateT]:
        """Return the sequence of states from root to this node."""
        states: List[StateT] = []
        curr: Optional[Node[StateT, ActionT]] = self
        while curr is not None:
            states.append(curr.state)
            curr = curr.parent
        states.reverse()
        return states

    def __repr__(self) -> str:
        return f"<Node state={self.state!r} cost={self.path_cost}>"

    def __lt__(self, other: Node) -> bool:
        """Tie-breaker for priority queues if evaluation function ties."""
        return self._entry_id < other._entry_id


class Problem(Generic[StateT, ActionT]):
    """Abstract formal problem definition."""

    def initial_state(self) -> StateT:
        """Return the initial state."""
        raise NotImplementedError

    def actions(self, state: StateT) -> List[ActionT]:
        """Return valid actions available in the given state."""
        raise NotImplementedError

    def result(self, state: StateT, action: ActionT) -> StateT:
        """Return the new state resulting from applying action to state."""
        raise NotImplementedError

    def is_goal(self, state: StateT) -> bool:
        """Return True if state satisfies goal conditions."""
        raise NotImplementedError

    def step_cost(self, state: StateT, action: ActionT, next_state: StateT) -> float:
        """Cost of taking action from state to next_state."""
        return 1.0

    def heuristic(self, state: StateT) -> float:
        """Estimated cost from state to goal (must be admissible for A* optimality)."""
        return 0.0

    def prune(self, state: StateT) -> bool:
        """Optional hook: return True if this partial state should be pruned early."""
        return False
