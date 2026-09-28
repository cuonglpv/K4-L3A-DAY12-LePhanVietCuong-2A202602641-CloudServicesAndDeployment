"""API-key authentication helpers."""

import secrets

from fastapi import Header, HTTPException, status

from .config import get_settings

ANONYMOUS_USER = "anonymous"


def verify_api_key(
    x_api_key: str | None = Header(default=None),
    x_user_id: str | None = Header(default=None),
) -> str:
    """Validate ``X-API-Key`` in constant time and return a user id."""
    configured = get_settings().agent_api_key
    if x_api_key is None or not secrets.compare_digest(x_api_key, configured):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or missing API key")
    return x_user_id or ANONYMOUS_USER


authenticate = verify_api_key
