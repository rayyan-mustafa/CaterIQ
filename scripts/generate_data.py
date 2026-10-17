"""Synthetic Data Generator Interface for CaterIQ (Project 2 Handoff).

Generates hundreds of realistic historical events, menu choices, seasonal demand fluctuations,
and guest rating feedback to train machine learning models in Project 2.
"""

import argparse
from datetime import date
from typing import Any, Dict, List


def generate_synthetic_historical_events(
    num_events: int = 500,
    start_date: date = date(2025, 1, 1),
    end_date: date = date(2026, 10, 1),
    output_path: str = "synthetic_events.json",
) -> List[Dict[str, Any]]:
    """Planned interface for generating historical dataset for Project 2 ML modules.

    Target downstream uses in Project 2:
    - Customer segmentation (clustering)
    - Seasonal demand & headcount forecasting (regression/time series)
    - Ingredient shortage expert system
    - Neural network dish recommendation
    """
    print(f"[Project 2 Data Generator Hook] Generating {num_events} events between {start_date} and {end_date}...")
    # Interface placeholder ready for Project 2 implementation
    return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic catering data for ML training.")
    parser.add_argument("--count", type=int, default=500, help="Number of historical events to generate.")
    args = parser.parse_args()
    generate_synthetic_historical_events(num_events=args.count)
