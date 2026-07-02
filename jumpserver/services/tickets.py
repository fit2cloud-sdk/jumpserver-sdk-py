"""Tickets service."""

from jumpserver.models.ticket import Ticket, TicketFlow, TicketFlowRequest, TicketRequest
from jumpserver.services import BaseService

__all__ = ["TicketsService"]


class TicketsService(BaseService):
    """CRUD for /api/v1/tickets/."""

    list_url = "/api/v1/tickets/tickets/"
    detail_url = "/api/v1/tickets/tickets/%s/"

    def list(self, limit=None, offset=None, search=None):
        return self._list(Ticket, limit=limit, offset=offset, search=search)

    def get(self, id: str):
        return self._get(Ticket, id)

    def create(self, req: TicketRequest):
        return self._create(Ticket, req)

    def approve(self, id: str, action: str = "approve"):
        _, resp = self._client.post(f"/api/v1/tickets/tickets/{id}/approve/", {"action": action})
        return resp

    def reject(self, id: str):
        return self.approve(id, action="reject")

    def list_flows(self, limit=None, offset=None):
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        data, resp = self._client.get("/api/v1/tickets/flows/", params=params or None)
        from jumpserver.services import _from_dict

        results = (data or {}).get("results", [])
        return [_from_dict(TicketFlow, item) for item in results], resp

    def update_flow(self, id: str, req: TicketFlowRequest):
        from jumpserver.services import _from_dict
        from jumpserver.utils import format_path

        data, resp = self._client.patch(format_path("/api/v1/tickets/flows/%s/", id), req)
        return _from_dict(TicketFlow, data) if data else None, resp
