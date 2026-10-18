"""Module C2 — Delivery Routing (Greedy Best-First vs A* Search).

Solves shortest delivery route from kitchen/depot to event venues.
Compares Greedy Best-First (heuristic-only) with A* (cost + admissible heuristic).
"""

from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Any, Dict, List, Optional, Tuple
from ai_engine.search.core import Problem, SearchResult
from ai_engine.search.greedy import greedy_best_first_search
from ai_engine.search.astar import astar_search


@dataclass(frozen=True)
class LocationPoint:
    """Geographic point in the delivery graph."""

    name: str
    latitude: float
    longitude: float


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate Great Circle distance between two points in kilometers."""
    r = 6371.0  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


class RoutePlanningProblem(Problem[str, str]):
    """Routing problem on an explicit road graph.

    State: current location name (str).
    Action: neighbor location name to drive to (str).
    Cost: actual travel time in minutes.
    Heuristic: straight-line distance / max_speed (minutes).
    """

    def __init__(
        self,
        start_location: str,
        goal_location: str,
        coordinates: Dict[str, Tuple[float, float]],
        edges: Dict[str, List[Tuple[str, float]]],
        max_speed_kmh: float = 60.0,
    ) -> None:
        """Initialize routing problem.

        Args:
            start_location: Origin depot/kitchen.
            goal_location: Destination event venue.
            coordinates: Map of location_name -> (lat, lon).
            edges: Adjacency list: location -> [(neighbor, travel_minutes)].
            max_speed_kmh: Maximum vehicle speed for admissible heuristic.
        """
        self.start = start_location
        self.goal = goal_location
        self.coordinates = coordinates
        self.edges = edges
        # speed in km per minute = max_speed_kmh / 60
        self.speed_km_per_min = max_speed_kmh / 60.0

    def initial_state(self) -> str:
        return self.start

    def is_goal(self, state: str) -> bool:
        return state == self.goal

    def actions(self, state: str) -> List[str]:
        return [dest for dest, _ in self.edges.get(state, [])]

    def result(self, state: str, action: str) -> str:
        return action

    def step_cost(self, state: str, action: str, next_state: str) -> float:
        for dest, minutes in self.edges.get(state, []):
            if dest == next_state:
                return minutes
        return 10.0  # default fallback

    def heuristic(self, state: str) -> float:
        """Admissible heuristic: straight-line distance / maximum speed.

        Vehicles cannot travel faster than max_speed or travel less than the straight-line
        distance. Therefore, h(n) <= true travel minutes.
        """
        if state not in self.coordinates or self.goal not in self.coordinates:
            return 0.0

        lat1, lon1 = self.coordinates[state]
        lat2, lon2 = self.coordinates[self.goal]
        dist_km = haversine_distance_km(lat1, lon1, lat2, lon2)
        return dist_km / self.speed_km_per_min


def compare_route_algorithms(
    start: str,
    goal: str,
    coordinates: Dict[str, Tuple[float, float]],
    edges: Dict[str, List[Tuple[str, float]]],
    max_speed_kmh: float = 60.0,
) -> Dict[str, Any]:
    """Execute both Greedy Best-First and A* to compare path cost and exploration."""
    problem = RoutePlanningProblem(
        start_location=start,
        goal_location=goal,
        coordinates=coordinates,
        edges=edges,
        max_speed_kmh=max_speed_kmh,
    )

    greedy_res: SearchResult = greedy_best_first_search(problem)
    astar_res: SearchResult = astar_search(problem)

    return {
        "start": start,
        "goal": goal,
        "astar": {
            "found": astar_res.found,
            "path": astar_res.solution_path,
            "total_minutes": round(astar_res.total_cost or 0.0, 1),
            "nodes_expanded": astar_res.nodes_expanded,
            "nodes_generated": astar_res.nodes_generated,
            "runtime_ms": astar_res.runtime_ms,
            "is_optimal": True,
        },
        "greedy": {
            "found": greedy_res.found,
            "path": greedy_res.solution_path,
            "total_minutes": round(greedy_res.total_cost or 0.0, 1),
            "nodes_expanded": greedy_res.nodes_expanded,
            "nodes_generated": greedy_res.nodes_generated,
            "runtime_ms": greedy_res.runtime_ms,
            "is_optimal": (greedy_res.total_cost == astar_res.total_cost) if greedy_res.found and astar_res.found else False,
        },
    }
