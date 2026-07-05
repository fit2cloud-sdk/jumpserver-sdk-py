"""Labels service."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from jumpserver.models.acl import Label, LabelRequest
from jumpserver.services import BaseService

if TYPE_CHECKING:
    from jumpserver.client import Response



__all__ = ["LabelsService"]

class LabelsService(BaseService):
    """CRUD for /api/v1/labels/labels/."""
    list_url = "/api/v1/labels/labels/"
    detail_url = "/api/v1/labels/labels/%s/"

    def list(self, limit: int = 10, offset: Optional[int] = None, search: Optional[str] = None) -> tuple[list[Label], Response]:
        return self._list(Label, limit=limit, offset=offset, search=search)

    def get(self, id: str) -> tuple[Optional[Label], Response]:
        return self._get(Label, id)

    def create(self, req: LabelRequest) -> tuple[Optional[Label], Response]:
        return self._create(Label, req)

    def update(self, id: str, req: LabelRequest) -> tuple[Optional[Label], Response]:
        return self._update(Label, id, req)

    def delete(self, id: str) -> Response:
        return self._delete(id)
