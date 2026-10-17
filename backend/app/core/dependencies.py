"""FastAPI dependencies for authentication, multi-tenancy, and authorization."""

from typing import Callable, List, Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.security import decode_access_token

security_scheme = HTTPBearer(auto_error=False)


class AuthenticatedContext:
    """Holds active user ID, active organization ID, and role."""

    def __init__(self, user_id: str, organization_id: str, role: str):
        self.user_id = user_id
        self.organization_id = organization_id
        self.role = role


def get_current_context(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_scheme),
    db: Session = Depends(get_db),
) -> AuthenticatedContext:
    """Extract and validate the caller's JWT token, returning user & tenant context."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        org_id: str = payload.get("org")
        role: str = payload.get("role")

        if not user_id or not org_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing identity or tenant context.",
            )
        return AuthenticatedContext(user_id=user_id, organization_id=org_id, role=role)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(exc)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_role(allowed_roles: List[str]) -> Callable[[AuthenticatedContext], AuthenticatedContext]:
    """Dependency factory enforcing role-based permissions (e.g. owner, manager)."""

    def role_checker(
        context: AuthenticatedContext = Depends(get_current_context),
    ) -> AuthenticatedContext:
        if context.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: role '{context.role}' does not have sufficient access.",
            )
        return context

    return role_checker
