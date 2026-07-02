"""Users & User Groups service."""

from __future__ import annotations

from typing import Any, Optional

from jumpserver.client import Response
from jumpserver.models.user import Group, GroupRequest, User, UserRequest
from jumpserver.services import BaseService, _from_dict
from jumpserver.utils import format_path

__all__ = ["UsersService", "GroupsService"]


class UsersService(BaseService):
    """CRUD service for /api/v1/users/users/."""

    list_url = "/api/v1/users/users/"
    detail_url = "/api/v1/users/users/%s/"

    def list(
        self,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
        order: Optional[str] = None,
    ) -> tuple[list[User], Response]:
        return self._list(User, filters, limit, offset, search, order)

    def get(self, id: str) -> tuple[Optional[User], Response]:
        return self._get(User, id)

    def profile(self) -> tuple[Optional[User], Response]:
        data, resp = self._client.get("/api/v1/users/profile/")
        return _from_dict(User, data) if data else None, resp

    def create(self, req: UserRequest) -> tuple[Optional[User], Response]:
        return self._create(User, req)

    def update(self, id: str, req: UserRequest) -> tuple[Optional[User], Response]:
        return self._update(User, id, req)

    def replace(self, id: str, req: UserRequest) -> tuple[Optional[User], Response]:
        return self._replace(User, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)

    def invite(self, user_ids: list[str], org_roles: list[str]) -> Response:
        body = {"users": user_ids, "org_roles": org_roles}
        _, resp = self._client.post("/api/v1/users/users/invite/", body)
        return resp

    def list_groups(
        self, user_id: str, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> tuple[list[Group], Response]:
        path = format_path("/api/v1/users/users/%s/groups/", user_id)
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get(path, params=params)
        items = [_from_dict(Group, item) for item in (data or [])]
        return items, resp


class GroupsService(BaseService):
    """CRUD service for /api/v1/users/groups/."""

    list_url = "/api/v1/users/groups/"
    detail_url = "/api/v1/users/groups/%s/"

    def list(
        self,
        filters: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[list[Group], Response]:
        return self._list(Group, filters, limit, offset, search)

    def get(self, id: str) -> tuple[Optional[Group], Response]:
        return self._get(Group, id)

    def create(self, req: GroupRequest) -> tuple[Optional[Group], Response]:
        return self._create(Group, req)

    def update(self, id: str, req: GroupRequest) -> tuple[Optional[Group], Response]:
        return self._update(Group, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)
