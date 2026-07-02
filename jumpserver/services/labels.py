"""Labels service."""

from jumpserver.models.acl import Label, LabelRequest
from jumpserver.services import BaseService

__all__ = ["LabelsService"]


class LabelsService(BaseService):
    """CRUD for /api/v1/labels/labels/."""

    list_url = "/api/v1/labels/labels/"
    detail_url = "/api/v1/labels/labels/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(Label, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(Label, id)

    def create(self, req: LabelRequest):
        return self._create(Label, req)

    def update(self, id: str, req: LabelRequest):
        return self._update(Label, id, req)

    def delete(self, id: str):
        return self._delete(id)
