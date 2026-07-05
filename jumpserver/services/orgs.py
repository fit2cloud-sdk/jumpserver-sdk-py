"""Organizations service."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from jumpserver.models.org import Organization, OrganizationRequest
from jumpserver.services import BaseService

if TYPE_CHECKING:
    from jumpserver.client import Response



__all__ = ["OrgsService"]

class OrgsService(BaseService):
    """CRUD for /api/v1/orgs/orgs/."""
    list_url = "/api/v1/orgs/orgs/"
    detail_url = "/api/v1/orgs/orgs/%s/"

    def list(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[Organization], Response]:
        return self._list(Organization, limit=limit, offset=offset, search=search)

    def get(self, id: str) -> tuple[Optional[Organization], Response]:
        return self._get(Organization, id)

    def create(self, req: OrganizationRequest) -> tuple[Optional[Organization], Response]:
        return self._create(Organization, req)

    def update(self, id: str, req: OrganizationRequest) -> tuple[Optional[Organization], Response]:
        return self._update(Organization, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)
