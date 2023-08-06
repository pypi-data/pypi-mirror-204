from __future__ import annotations

import logging
import typing
from http.server import BaseHTTPRequestHandler

from .response import Response
from .authentication import authenticate
from .posthandler import PostHandler
from .gethandler import GetHandler
from .errors import ClientError
from .constants.headers import CONTENT_LENGTH
from .constants.headers import CONTENT_TYPE
from .constants.statuscodes import LENGTH_REQUIRED
from .constants.statuscodes import SERVER_ERROR

if typing.TYPE_CHECKING:
    from .server import Server


logger = logging.getLogger(__name__)


class HTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler."""

    protocol_version = "HTTP/1.1"

    @property
    def path_component(self) -> str:
        path, _, _ = self.path.partition("?")
        return path.lstrip("/")

    @property
    def content_type(self) -> str:
        return self.headers[str(CONTENT_TYPE)]

    @property
    def content_length(self) -> int:
        """Return content length."""
        if CONTENT_LENGTH not in self.headers:
            raise ClientError("Content-length required", LENGTH_REQUIRED)
        return int(self.headers[CONTENT_LENGTH])

    # https://stackoverflow.com/questions/2617615/slow-python-http-server-on-localhost
    def address_string(self):
        host, _ = self.client_address[:2]
        # return socket.getfqdn(host)
        return host

    def get_server(self) -> Server:
        return self.server  # self.server is referring to http.server.BaseServer.

    def do_HEAD(self):  # pylint: disable=invalid-name
        logger.debug("Received HEAD request '%s'", self.path_component)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        logger.debug("Finished HEAD request '%s'", self.path_component)

    def do_GET(self):  # pylint: disable=invalid-name
        logger.debug("Received GET request '%s'", self.path_component)
        self._handle_get()
        logger.debug("Finished GET request '%s'", self.path_component)

    def do_POST(self):  # pylint: disable=invalid-name
        logger.debug("Received POST request '%s'", self.path_component)
        self._handle_post()
        logger.debug("Finished POST request '%s'", self.path_component)

    @authenticate
    def _handle_post(self):
        try:
            handler = PostHandler(self)
            response = handler.handle()
        except ClientError as err:
            logger.exception(err)
            response = self._create_error_response(message=err.message, status_code=err.status_code)
        except Exception as err:  # pylint: disable=broad-exception-caught
            logger.exception(err)

            # Handler is expected to identify expectable errors. This try-catch block catches
            # unexpected server errors that could not be identified.
            response = self._create_error_response(message=str(err), status_code=SERVER_ERROR)

        self._send_response(response)

    @authenticate
    def _handle_get(self):
        try:
            handler = GetHandler(self)
            response = handler.handle()
        except Exception as err:  # pylint: disable=broad-exception-caught
            logger.exception(err)
            response = self._create_error_response(message=str(err), status_code=SERVER_ERROR)

        self._send_response(response)

    def _send_response(self, response: Response):
        """Send response.
        """
        logger.debug("Sending response..")
        bytes_to_send = b"" if response.value is None else response.value

        try:
            self.send_response(response.status_code)

            if response.content_type:
                self.send_header(CONTENT_TYPE, response.content_type)

            self.send_header(CONTENT_LENGTH, str(len(bytes_to_send)))
            self.end_headers()
            self.wfile.write(bytes_to_send)
        except TypeError as err:
            logger.exception(err)
        except Exception as err:  # pylint: disable=broad-exception-caught
            logger.exception(err)

    def _create_error_response(self, message: str, status_code: int) -> Response:
        logger.error(message)
        logger.debug(str(self))

        server = self.get_server()
        codec = server.codecs.get_codec_by_value(message)
        return Response(codec.encode(message), codec.get_content_type(), status_code=status_code)

    def __str__(self):
        info = []
        info.append(f"{self.path}")
        info.append(f"{str(self.headers).strip()}")
        return "\n".join(info)
