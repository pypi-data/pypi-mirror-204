from __future__ import annotations

import typing

from .response import JsonResponse

if typing.TYPE_CHECKING:
    from .requesthandler import HTTPRequestHandler


class GetHandler:
    def __init__(self, request: HTTPRequestHandler):
        self.request = request
        self._server = request.get_server()

    def handle(self) -> JsonResponse:  # pylint: disable=broad-exception-caught
        endpoints = [e.to_dict() for e in self._server.endpoints.values()]
        definition = {
            "endpoints": endpoints,
            "ssl_enabled": self._server.ssl_enabled
        }

        return JsonResponse(definition)
