"""Support tables: CalendarTokens, TravelTimes, AuditLog, and AIRun."""

from datetime import datetime, timezone
import secrets
import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from backend.app.core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_token() -> str:
    return secrets.token_hex(20)


class CalendarToken(Base):
    __tablename__ = "calendar_tokens"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(64), unique=True, index=True, default=generate_token, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class TravelTime(Base):
    __tablename__ = "travel_times"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    from_place = Column(String(255), nullable=False)
    to_place = Column(String(255), nullable=False)
    minutes = Column(Float, nullable=False, default=15.0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), nullable=True)
    action = Column(String(50), nullable=False)  # create, update, delete, approve
    entity = Column(String(50), nullable=False)  # event, proposal, invoice
    entity_id = Column(String(36), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    details_json = Column(Text, nullable=True)


class AIRun(Base):
    __tablename__ = "ai_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    module = Column(String(50), nullable=False)  # bfs_substitution, dfs_menu, astar_optimize, routing, minimax_pricing
    params_json = Column(Text, nullable=True)
    nodes_expanded = Column(Integer, default=0)
    runtime_ms = Column(Float, default=0.0)
    result_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
