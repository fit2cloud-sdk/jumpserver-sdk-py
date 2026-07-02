"""ACLs (CommandFilters & LoginACLs) service."""

from typing import Optional

from jumpserver.client import Client, Response
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
    """CRUD for /api/v1/acls/command-filters/."""

    list_url = "/api/v1/acls/command-filters/"
    detail_url = "/api/v1/acls/command-filters/%s/"

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
