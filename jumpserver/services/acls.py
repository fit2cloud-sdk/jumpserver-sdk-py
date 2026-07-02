"""ACLs (CommandFilters & LoginACLs) service."""

from jumpserver.models.acl import (
    CommandFilter,
    CommandFilterRequest,
    CommandGroup,
    CommandGroupRequest,
    LoginACL,
)
from jumpserver.services import BaseService

__all__ = ["CommandFiltersService", "LoginACLsService"]


class CommandFiltersService(BaseService):
    """CRUD for /api/v1/acls/command-filter-acls/ and /api/v1/acls/command-groups/."""

    list_url = "/api/v1/acls/command-filter-acls/"
    detail_url = "/api/v1/acls/command-filter-acls/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(CommandFilter, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(CommandFilter, id)

    def create(self, req: CommandFilterRequest):
        return self._create(CommandFilter, req)

    def update(self, id: str, req: CommandFilterRequest):
        return self._update(CommandFilter, id, req)

    def delete(self, id: str):
        return self._delete(id)

    # -- Command Groups --------------------------------------------------

    def list_groups(self, limit=None, offset=None, search=None):
        data, resp = self._client.get(
            "/api/v1/acls/command-groups/",
            params=_page_params(limit, offset, search),
        )
        from jumpserver.services import _from_dict

        results = (data or {}).get("results", [])
        return [_from_dict(CommandGroup, item) for item in results], resp

    def get_group(self, id: str):
        from jumpserver.services import _from_dict
        from jumpserver.utils import format_path

        data, resp = self._client.get(format_path("/api/v1/acls/command-groups/%s/", id))
        return _from_dict(CommandGroup, data) if data else None, resp

    def create_group(self, req: CommandGroupRequest):
        from jumpserver.services import _from_dict

        data, resp = self._client.post("/api/v1/acls/command-groups/", req)
        return _from_dict(CommandGroup, data) if data else None, resp

    def update_group(self, id: str, req: CommandGroupRequest):
        from jumpserver.services import _from_dict
        from jumpserver.utils import format_path

        data, resp = self._client.patch(format_path("/api/v1/acls/command-groups/%s/", id), req)
        return _from_dict(CommandGroup, data) if data else None, resp

    def delete_group(self, id: str):
        from jumpserver.utils import format_path

        _, resp = self._client.delete(format_path("/api/v1/acls/command-groups/%s/", id))
        return resp


class LoginACLsService(BaseService):
    """CRUD for /api/v1/acls/login-acls/."""

    list_url = "/api/v1/acls/login-acls/"
    detail_url = "/api/v1/acls/login-acls/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(LoginACL, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(LoginACL, id)

    def delete(self, id: str):
        return self._delete(id)


def _page_params(limit=None, offset=None, search=None):
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if search:
        params["search"] = search
    return params or None
