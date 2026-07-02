"""Organizations service."""

from typing import Optional

from jumpserver.client import Client, Response
from jumpserver.models.org import Organization, OrganizationRequest
from jumpserver.services import BaseService

__all__ = ["OrgsService"]


class OrgsService(BaseService):
    """CRUD for /api/v1/orgs/orgs/."""

    list_url = "/api/v1/orgs/orgs/"
    detail_url = "/api/v1/orgs/orgs/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(Organization, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(Organization, id)

    def create(self, req: OrganizationRequest):
        return self._create(Organization, req)

    def update(self, id: str, req: OrganizationRequest):
        return self._update(Organization, id, req)

    def delete(self, id: str):
        return self._delete(id)
