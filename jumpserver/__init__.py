"""JumpServer Python SDK.

A Python client library for the JumpServer API.

Usage::

    from jumpserver import Client

    client = Client(
        base_url="https://jumpserver.example.com",
        access_key="<key>",
        access_secret="<secret>",
    )
    user, _ = client.users.profile()
    print(user.name)
"""

from jumpserver.client import Client, Response
from jumpserver.errors import (
    APIError,
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    UnauthorizedError,
    is_forbidden,
    is_not_found,
    is_rate_limited,
    is_unauthorized,
)

__all__ = [
    "Client",
    "Response",
    "APIError",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitedError",
    "ServerError",
    "is_not_found",
    "is_unauthorized",
    "is_forbidden",
    "is_rate_limited",
]

__version__ = "0.1.0"
