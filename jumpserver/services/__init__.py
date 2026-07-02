"""Base service with CRUD helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Optional, TypeVar

from jumpserver.utils import build_url, format_path

if TYPE_CHECKING:
    from jumpserver.client import Client, Response

T = TypeVar("T")
R = TypeVar("R")

__all__ = ["BaseService"]


class BaseService:
    """Generic CRUD service used by domain-specific services.

    Subclasses set ``list_url`` and ``detail_url`` template strings
    and can call inherited list / get / create / update / delete methods.
    """

    list_url: str = ""
    detail_url: str = ""

    def __init__(self, client: Client) -> None:
        self._client = client

    def _list(
        self,
        cls: type[T],
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
        order: Optional[str] = None,
    ) -> tuple[list[T], Response]:
        """Fetch a paginated list and return ``(items, response)``."""
        params: dict[str, Any] = {}
        if filters:
            params.update(filters)
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if search:
            params["search"] = search
        if order:
            params["order"] = order

        data, resp = self._client.get(self.list_url, params=params)
        if data is None:
            return [], resp
        results = data.get("results", [])
        items = [_from_dict(cls, item) for item in results]
        return items, resp

    def _get(self, cls: type[T], id: str) -> tuple[Optional[T], Response]:
        """Fetch a single resource by ID."""
        data, resp = self._client.get(format_path(self.detail_url, id))
        if data is None:
            return None, resp
        return _from_dict(cls, data), resp

    def _create(self, cls: type[T], body: Any) -> tuple[Optional[T], Response]:
        """Create a new resource and return it."""
        data, resp = self._client.post(self.list_url, body)
        if data is None:
            return None, resp
        return _from_dict(cls, data), resp

    def _update(self, cls: type[T], id: str, body: Any) -> tuple[Optional[T], Response]:
        """Patch-update a resource by ID."""
        data, resp = self._client.patch(format_path(self.detail_url, id), body)
        if data is None:
            return None, resp
        return _from_dict(cls, data), resp

    def _replace(self, cls: type[T], id: str, body: Any) -> tuple[Optional[T], Response]:
        """Full replace (PUT) a resource by ID."""
        data, resp = self._client.put(format_path(self.detail_url, id), body)
        if data is None:
            return None, resp
        return _from_dict(cls, data), resp

    def _delete(self, id: str) -> Response:
        """Delete a resource by ID."""
        _, resp = self._client.delete(format_path(self.detail_url, id))
        return resp

    def _action(
        self, cls: type[T], url: str, body: Any = None
    ) -> tuple[Optional[T], Response]:
        data, resp = self._client.post(url, body)
        if data is None:
            return None, resp
        return _from_dict(cls, data), resp


def _camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    result = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0 and name[i - 1].islower():
            result.append("_")
        result.append(ch.lower())
    return "".join(result)


def _from_dict(cls: type[T], data: dict) -> T:
    """Convert a dict to a dataclass instance, mapping camelCase keys to snake_case fields."""

    import dataclasses

    if not dataclasses.is_dataclass(cls):
        return data  # type: ignore

    field_names = {f.name for f in dataclasses.fields(cls)}
    kwargs: dict[str, Any] = {}

    for key, value in data.items():
        snake = _camel_to_snake(key)
        # Try direct match
        if snake in field_names:
            kwargs[snake] = value
        elif key in field_names:
            kwargs[key] = value
        # Handle common mismatches
        elif key == "MFA":
            continue
        else:
            # If value is a dict and field expects a dataclass, recurse
            if isinstance(value, dict):
                # Try to find a matching field
                for fname in field_names:
                    if fname == snake:
                        kwargs[snake] = value
                        break
                else:
                    kwargs[snake] = value
            else:
                kwargs[snake] = value

    return cls(**kwargs)
