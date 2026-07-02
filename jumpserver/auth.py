"""JumpServer SDK - Authentication methods."""

import datetime
import logging
from abc import ABC, abstractmethod
from typing import Optional

import requests as _requests
from httpsig.requests_auth import HTTPSignatureAuth
from requests import PreparedRequest

__all__ = [
    "Authenticator",
    "SignatureAuth",
    "BearerTokenAuth",
    "PrivateTokenAuth",
    "PasswordAuth",
]

_LOGGER = logging.getLogger("jumpserver")

# Path used by PasswordAuth to exchange credentials for a Bearer token.
_TOKEN_PATH = "/api/v1/authentication/auth/"

# Common date formats returned by JumpServer APIs.
_DT_FORMATS = (
    "%Y/%m/%d %H:%M:%S %z",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M:%S %z",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S+%H:%M",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%Y-%m-%dT%H:%M:%S.%f+%H:%M",
)


def _parse_datetime(value: Optional[str]) -> Optional[datetime.datetime]:
    """Best-effort parse of a date-time string into a naive UTC datetime.

    If the source string carries a timezone offset (e.g. ``+0800``), the
    result is converted to UTC and then made naive so it can be compared
    with ``datetime.utcnow()`` without errors.
    """
    if not value:
        return None
    for fmt in _DT_FORMATS:
        try:
            dt = datetime.datetime.strptime(value, fmt)
            if dt.tzinfo is not None:
                dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
            return dt
        except ValueError:
            continue
    _LOGGER.warning("PasswordAuth: cannot parse date_expired=%r", value)
    return None


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


class PasswordAuth(Authenticator):
    """Authenticate by exchanging username + password for a Bearer token.

    On the first request, a POST to ``/api/v1/authentication/auth/`` is
    made with ``{"username": ..., "password": ...}``.  The returned token
    and its ``date_expired`` are cached.  Subsequent requests reuse the
    cached token as long as it has more than 5 minutes of validity left.
    When the token is missing, expired, or about to expire, a fresh token
    is fetched automatically.  If the server responds with 401 the cached
    token is invalidated and the next request triggers a refresh.
    """

    # Refresh the token this many seconds before it actually expires.
    _REFRESH_MARGIN = datetime.timedelta(minutes=5)

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        verify_ssl: bool = True,
    ) -> None:
        if not username:
            raise ValueError("PasswordAuth: username is required")
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self._token: Optional[str] = None
        self._expires_at: Optional[datetime.datetime] = None
        self._session = _requests.Session()
        self._session.verify = verify_ssl

    def _fetch_token(self) -> tuple[str, Optional[datetime.datetime]]:
        """POST to the auth endpoint and return ``(token, expires_at)``."""
        url = f"{self.base_url}{_TOKEN_PATH}"
        body = {"username": self.username, "password": self.password}
        _LOGGER.debug("PasswordAuth: fetching token from %s", url)
        resp = self._session.post(
            url,
            json=body,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        token = data.get("token", "")
        if not token:
            raise RuntimeError(f"PasswordAuth: auth endpoint returned no token: {data}")
        expires_at = _parse_datetime(data.get("date_expired"))
        _LOGGER.debug("PasswordAuth: got token (expires_at=%s)", expires_at or "unknown")
        return token, expires_at

    def _is_token_valid(self) -> bool:
        """Return True if the cached token is present and not about to expire."""
        if self._token is None:
            return False
        if self._expires_at is None:
            # No expiry info — assume valid; 401 handler will catch it.
            return True
        return datetime.datetime.utcnow() + self._REFRESH_MARGIN < self._expires_at

    def _ensure_token(self) -> None:
        """Fetch a new token if the current one is missing or nearly expired."""
        if not self._is_token_valid():
            self._token, self._expires_at = self._fetch_token()

    def invalidate(self) -> None:
        """Discard the cached token so the next request fetches a new one."""
        self._token = None
        self._expires_at = None

    def __call__(self, request: PreparedRequest) -> None:
        self._ensure_token()
        request.headers["Authorization"] = f"Bearer {self._token}"

    def on_response(self, status_code: int) -> None:
        """Call after a 401 to trigger automatic token refresh.

        Example usage by the Client::

            if resp.status_code == 401 and isinstance(self._auth, PasswordAuth):
                self._auth.on_response(401)
                # retry ...
        """
        if status_code == 401:
            self.invalidate()
