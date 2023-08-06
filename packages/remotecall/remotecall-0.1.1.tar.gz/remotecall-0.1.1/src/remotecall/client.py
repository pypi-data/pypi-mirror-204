from __future__ import annotations

from typing import Any
import logging
import requests

from .codecs import Codec
from .codecs import Codecs
from .constants import headers
from .errors import ClientError
from .errors import ServerError


logger = logging.getLogger(__name__)


class BaseClient:
    DEFAULT_SERVER_ADDRESS = ("localhost", 8000)

    def __init__(self, server_address: tuple[str, int] = DEFAULT_SERVER_ADDRESS):
        self.server_address = server_address
        self._codecs = Codecs(Codec.subclasses)
        self._ssl_enabled = False
        self._cert_file = None
        self._authentication = None

    @property
    def server_url(self) -> str:
        """Get server URL."""
        host, port = self.server_address
        scheme = "https" if self._ssl_enabled else "http"
        return f"{scheme}://{host}:{port}"

    @property
    def ssl_enabled(self) -> bool:
        """Is SSL enabled."""
        return self._ssl_enabled

    def use_ssl(self, cert_file: str):
        """Enable SSL."""
        self._cert_file = cert_file
        self._ssl_enabled = True

    def set_authentication(self, authentication):
        """Set authentication method."""
        self._authentication = authentication

    def call(self, function_name: str, timeout=None, **kwargs):
        """Call remote function with arguments."""
        logger.debug("Preparing to call %s.", function_name)
        url = self._get_url(function_name)
        multipart_form_data = self._encode_multipart_form_data(fields=kwargs)

        logger.debug("Sending POST request %s.", url)

        response = requests.post(url=url,
                                 files=multipart_form_data,
                                 verify=self._cert_file,
                                 auth=self._authentication,
                                 timeout=timeout)

        logger.debug("Received status code: %s.", response.status_code)

        if response.status_code >= 500:
            self._log_response(response)
            raise ServerError(f"Server error: {response.text}", response.status_code)

        if response.status_code >= 400:
            self._log_response(response)
            raise ClientError(f"Client error: {response.text}", response.status_code)

        return self._get_response_value(response)

    def _get_url(self, command: str) -> str:
        return f"{self.server_url}/{command}"

    def _encode_multipart_form_data(self, fields: dict[str, Any]) -> dict[str, tuple]:
        logger.debug("Encoding multipart/form-data ...")
        form_data = {}

        for name, value in fields.items():
            logger.debug("Get codec for '%s.", type(value))
            codec = self._codecs.get_codec_by_value(value)  # OK

            logger.debug("Encoding '%s' with %s.", name, codec)
            form_data[name] = (None, codec.encode(value), codec.get_content_type())

        return form_data

    @classmethod
    def _log_response(cls, response: requests.Response):
        logger.debug("Response:")
        logger.debug("  status: %s", response.status_code)
        logger.debug("  headers: %s", response.headers)
        logger.debug("  text: %s", response.text)

    def _get_response_value(self, response: requests.Response):
        content_type = response.headers.get(str(headers.CONTENT_TYPE))

        if not content_type:
            return response.content

        codec = self._codecs.get_codec_by_content_type(content_type)

        logger.debug("Using %s to decode '%s' response.", codec, content_type)

        return codec.decode(response.content)
