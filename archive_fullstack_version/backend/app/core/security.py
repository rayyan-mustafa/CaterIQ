"""Security utilities: password hashing and JWT token handling."""

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os
from typing import Any, Dict, Optional, Union
import jwt
from backend.app.core.config import settings


def hash_password(password: str) -> str:
    """Hash password using salt + PBKDF2-HMAC-SHA256 (industry standard & dependency-free)."""
    salt = os.urandom(16).hex()
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,
    ).hex()
    return f"{salt}${key}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against stored salt$key hash."""
    try:
        salt, expected_key = hashed_password.split("$", 1)
        computed_key = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt.encode("utf-8"),
            100000,
        ).hex()
        return hmac.compare_digest(computed_key, expected_key)
    except Exception:
        return False


def create_access_token(
    subject: Union[str, Any],
    organization_id: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create signed JWT token containing user identity and tenant context."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "org": str(organization_id),
        "role": str(role),
        "exp": expire,
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT access token."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
