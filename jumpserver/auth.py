"""JumpServer SDK - Authentication methods."""

import datetime
from abc import ABC, abstractmethod
from typing import Optional

from requests import PreparedRequest
from httpsig.requests_auth import HTTPSignatureAuth

__all__ = [
    "Authenticator",
    "SignatureAuth",
    "BearerTokenAuth",
    "PrivateTokenAuth",
    "BasicAuth",
]


class Authenticator(ABC):
    """Abstract base for request authentication strategies."""

    @abstractmethod
    def __call__(self, request: PreparedRequest) -> None:
        """Mutate the request in-place (typically by setting headers)."""


class SignatureAuth(Authenticator):
    """HMAC-SHA256 HTTP Signature auth (JumpServer Access Key scheme).

    Signs requests using the '(request-target)' and 'date' headers.
    """

    def __init__(self, key_id: str, secret_id: str) -> None:
        if not key_id or not secret_id:
            raise ValueError("SignatureAuth: key_id and secret_id are required")
        self.key_id = key_id
        self.secret_id = secret_id
        self._httpsig = HTTPSignatureAuth(
            key_id=key_id,
            secret=secret_id,
            algorithm="hmac-sha256",
            headers=["(request-target)", "date"],
        )

    def __call__(self, request: PreparedRequest) -> None:
        # Ensure Date header is set before signing
        if "Date" not in request.headers:
            gmt_form = "%a, %d %b %Y %H:%M:%S GMT"
            request.headers["Date"] = datetime.datetime.utcnow().strftime(gmt_form)
        self._httpsig(request)


class BearerTokenAuth(Authenticator):
    """Sets ``Authorization: Bearer <token>``."""

    def __init__(self, token: str) -> None:
        if not token:
            raise ValueError("BearerTokenAuth: token is required")
        self.token = token

    def __call__(self, request: PreparedRequest) -> None:
        request.headers["Authorization"] = f"Bearer {self.token}"


class PrivateTokenAuth(Authenticator):
    """Sets ``Authorization: Token <token>`` (legacy scheme)."""

    def __init__(self, token: str) -> None:
        if not token:
            raise ValueError("PrivateTokenAuth: token is required")
        self.token = token

    def __call__(self, request: PreparedRequest) -> None:
        request.headers["Authorization"] = f"Token {self.token}"


class BasicAuth(Authenticator):
    """HTTP Basic auth. Useful for obtaining a Bearer token."""

    def __init__(self, username: str, password: str) -> None:
        if not username:
            raise ValueError("BasicAuth: username is required")
        self.username = username
        self.password = password

    def __call__(self, request: PreparedRequest) -> None:
        from requests.auth import HTTPBasicAuth

        HTTPBasicAuth(self.username, self.password)(request)
