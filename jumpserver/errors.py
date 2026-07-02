"""JumpServer SDK - Custom exceptions."""

from typing import Any, Optional


class JumpServerError(Exception):
    """Base exception for all JumpServer SDK errors."""

    status_code: int = 0


class APIError(JumpServerError):
    """Represents a non-2xx response from the JumpServer API."""

    def __init__(
        self,
        status_code: int,
        method: str,
        url: str,
        body: Optional[bytes] = None,
        message: str = "",
    ):
        self.status_code = status_code
        self.method = method
        self.url = url
        self.body = body or b""
        self.message = message
        super().__init__(str(self))

    def __str__(self) -> str:
        if self.message:
            return f"jumpserver: {self.method} {self.url} -> {self.status_code}: {self.message}"
        if self.body and len(self.body) < 256:
            return f"jumpserver: {self.method} {self.url} -> {self.status_code}: {self.body.decode()}"
        return f"jumpserver: {self.method} {self.url} -> {self.status_code}"


class BadRequestError(APIError):
    status_code = 400


class UnauthorizedError(APIError):
    status_code = 401


class ForbiddenError(APIError):
    status_code = 403


class NotFoundError(APIError):
    status_code = 404


class ConflictError(APIError):
    status_code = 409


class RateLimitedError(APIError):
    status_code = 429


class ServerError(APIError):
    status_code = 500


_ERROR_MAP: dict[int, type[APIError]] = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    429: RateLimitedError,
    500: ServerError,
}


def _extract_message(body: Optional[bytes]) -> str:
    """Extract a human-readable message from a Django REST Framework error body."""
    import json

    if not body:
        return ""
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return string_truncate(body)

    for key in ("detail", "message"):
        if key in data:
            return str(data[key])

    # Handle non_field_errors
    if "non_field_errors" in data:
        errors = data["non_field_errors"]
        if isinstance(errors, list) and errors:
            return str(errors[0])

    return string_truncate(body)


def string_truncate(body: bytes) -> str:
    text = body.decode("utf-8", errors="replace")
    if len(text) > 200:
        return text[:200] + "..."
    return text


def map_error(
    status_code: int,
    method: str,
    url: str,
    body: Optional[bytes] = None,
    message: str = "",
) -> APIError:
    """Map an HTTP status code to the appropriate exception class."""
    msg = message or _extract_message(body)
    cls = _ERROR_MAP.get(status_code, APIError)
    return cls(status_code=status_code, method=method, url=url, body=body, message=msg)


def is_not_found(err: Exception) -> bool:
    return isinstance(err, NotFoundError)


def is_unauthorized(err: Exception) -> bool:
    return isinstance(err, UnauthorizedError)


def is_forbidden(err: Exception) -> bool:
    return isinstance(err, ForbiddenError)


def is_rate_limited(err: Exception) -> bool:
    return isinstance(err, RateLimitedError)
