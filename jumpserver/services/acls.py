"""ACLs (CommandFilters & LoginACLs) service."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from jumpserver.models.acl import (
    CommandFilter,
    CommandFilterRequest,
    CommandGroup,
    CommandGroupRequest,
    LoginACL,
)
from jumpserver.services import BaseService, from_dict

if TYPE_CHECKING:
    from jumpserver.client import Response



__all__ = ["CommandFiltersService", "LoginACLsService"]

class CommandFiltersService(BaseService):
    """CRUD for /api/v1/acls/command-filter-acls/ and /api/v1/acls/command-groups/."""
    list_url = "/api/v1/acls/command-filter-acls/"
    detail_url = "/api/v1/acls/command-filter-acls/%s/"

    def list(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[CommandFilter], Response]:
        return self._list(CommandFilter, limit=limit, offset=offset, search=search)

    def get(self, id: str) -> tuple[Optional[CommandFilter], Response]:
        return self._get(CommandFilter, id)

    def create(self, req: CommandFilterRequest) -> tuple[Optional[CommandFilter], Response]:
        return self._create(CommandFilter, req)

    def update(self, id: str, req: CommandFilterRequest) -> tuple[Optional[CommandFilter], Response]:
        return self._update(CommandFilter, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)

    # -- Command Groups --------------------------------------------------

    def list_groups(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[CommandGroup], Response]:
        data, resp = self._client.get(
            "/api/v1/acls/command-groups/",
            params=_page_params(limit, offset, search),
        )

        results = (data or {}).get("results", [])
        return [from_dict(CommandGroup, item) for item in results], resp

    def get_group(self, id: str) -> tuple[Optional[CommandGroup], Response]:
        from jumpserver.utils import format_path

        data, resp = self._client.get(format_path("/api/v1/acls/command-groups/%s/", id))
        return from_dict(CommandGroup, data) if data else None, resp

    def create_group(self, req: CommandGroupRequest) -> tuple[Optional[CommandGroup], Response]:

        data, resp = self._client.post("/api/v1/acls/command-groups/", req)
        return from_dict(CommandGroup, data) if data else None, resp

    def update_group(self, id: str, req: CommandGroupRequest) -> tuple[Optional[CommandGroup], Response]:
        from jumpserver.utils import format_path

        data, resp = self._client.patch(format_path("/api/v1/acls/command-groups/%s/", id), req)
        return from_dict(CommandGroup, data) if data else None, resp

    def delete_group(self, id: str) -> Response:
        from jumpserver.utils import format_path

        _, resp = self._client.delete(format_path("/api/v1/acls/command-groups/%s/", id))
        return resp

class LoginACLsService(BaseService):
    """CRUD for /api/v1/acls/login-acls/."""

    list_url = "/api/v1/acls/login-acls/"
    detail_url = "/api/v1/acls/login-acls/%s/"

    def list(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[LoginACL], Response]:
        return self._list(LoginACL, limit=limit, offset=offset, search=search)

    def get(self, id: str) -> tuple[Optional[LoginACL], Response]:
        return self._get(LoginACL, id)

    def delete(self, id: str) -> Response:
        return self._delete(id)

def _page_params(limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> dict[str, Any]:
    params = {}
    params["limit"] = limit if limit is not None else 10
    if offset is not None:
        params["offset"] = offset
    if search:
        params["search"] = search
    return params or None
