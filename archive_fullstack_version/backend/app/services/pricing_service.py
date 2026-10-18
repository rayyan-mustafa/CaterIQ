"""Pricing and financial calculation services."""

from typing import List, Tuple
from backend.app.models.event import Event, EventItem


def calculate_event_totals(event: Event) -> Tuple[float, float, float, float]:
    """Calculate (total_revenue, total_cost, profit, margin_pct) for an event.

    Total revenue is based on items × unit_price × headcount.
    Total cost is based on items × unit_cost × headcount.
    """
    total_revenue = 0.0
    total_cost = 0.0

    for item in event.items:
        # Items are multiplied by item quantity and headcount if per-head
        qty = item.quantity
        total_revenue += item.unit_price * qty * event.headcount
        total_cost += item.unit_cost * qty * event.headcount

    profit = total_revenue - total_cost
    margin_pct = (profit / total_revenue * 100.0) if total_revenue > 0 else 0.0

    return (
        round(total_revenue, 2),
        round(total_cost, 2),
        round(profit, 2),
        round(margin_pct, 1),
    )
