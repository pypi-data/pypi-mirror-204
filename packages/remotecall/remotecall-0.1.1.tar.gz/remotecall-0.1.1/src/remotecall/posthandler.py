from __future__ import annotations

import cgi
from dataclasses import dataclass
import re
import logging
import typing
from typing import BinaryIO
from typing import Optional

from .response import Response
from .errors import ClientError
from .constants import headers
from .constants.headers import CONTENT_TYPE
from .constants.headers import CONTENT_DISPOSITION
from .constants.statuscodes import TYPE_ERROR
from .constants.statuscodes import BAD_REQUEST
from .constants.statuscodes import SERVICE_UNAVAILABLE

if typing.TYPE_CHECKING:
    from .endpoint import Endpoint
    from .requesthandler import HTTPRequestHandler


logger = logging.getLogger(__name__)


@dataclass
class MultiPartFormDataField:
    name: str
    content_type: str
    data: bytes


class PostHandler:

    def __init__(self, request: HTTPRequestHandler):
        self.request = request
        self._server = self.request.get_server()
        self._codecs = self._server.codecs

    def handle(self) -> Response:  # pylint: disable=broad-exception-caught
        endpoint_name = self.request.path_component

        try:
            endpoint = self._server.endpoints[endpoint_name]
        except KeyError as err:
            raise ClientError(f"Unknown endpoint: '{endpoint_name}'", BAD_REQUEST) from err

        if not endpoint.enabled:
            raise ClientError("Endpoint disabled.", SERVICE_UNAVAILABLE)

        try:
            arguments = self.get_arguments(endpoint)
        except ValueError as err:
            raise ClientError(
                f"Failed to parse request arguments: {err}", BAD_REQUEST
            ) from err

        try:
            return_value = endpoint(**arguments)
        except TypeError as err:
            raise ClientError(str(err), TYPE_ERROR) from err

        try:
            codec = self._codecs.get_codec_by_value(return_value)
            logger.debug("Using %s to decode return value.", codec)
            response = Response(codec.encode(return_value), codec.get_content_type())
        except Exception as err:
            raise ClientError(
                f"Failed to encode return value: {err}", TYPE_ERROR
            ) from err

        return response

    def get_arguments(self, endpoint: Endpoint) -> dict:
        logger.debug("Get arguments.")

        arguments = {}

        request = self.request
        content_length = request.content_length
        content_type_header = request.headers.get(CONTENT_TYPE)

        if not content_type_header:
            logger.debug("No arguments ('content-type' not set).")
            return arguments

        request_content_type, options = cgi.parse_header(content_type_header)
        if request_content_type != headers.MULTIPART_FORM_DATA:
            raise ClientError(
                f"Invalid content-type: '{request_content_type}'.", BAD_REQUEST,
            )

        boundary = options.get(headers.BOUNDARY)

        if not boundary:
            raise ClientError("Boundary not defined.", BAD_REQUEST)

        fields = self.read_multipart_form_data(request.rfile, content_length, boundary)

        for field in fields:
            arguments[field.name] = self.decode_multipart_form_data(field, endpoint)

        return arguments

    def decode_multipart_form_data(self, field: MultiPartFormDataField, endpoint: Endpoint):
        try:
            parameter = endpoint.get_parameter(field.name)
        except KeyError as err:
            raise ClientError(
                f"{endpoint.name}() got unexpected parameter: {field.name}", BAD_REQUEST
            ) from err

        if field.content_type:
            codec = self._codecs.get_codec_by_content_type(field.content_type)
        else:
            codec = self._codecs.get_codec_by_type(parameter.annotation or str)

        logger.debug("Using %s to decode '%s'.", codec, field.name)

        return codec.decode(field.data)

    @classmethod
    def read_multipart_form_data(
        cls, rfile: BinaryIO, length: int, boundary: str
    ) -> list[MultiPartFormDataField]:
        """
        Example:
            b'--40c00dbb9994e1de1cf94bce01c4e734'
            b'Content-Disposition: form-data; name="text"'
            b'Content-Type: application/str'
            b''
            b'Hello world'
            b'--40c00dbb9994e1de1cf94bce01c4e734--'
            b''
        """

        def read_lines(rfile: BinaryIO, length: int) -> list[bytes]:
            bytes_count = 0

            for line in rfile:
                yield line

                bytes_count += len(line)
                if bytes_count >= length:
                    break

        def get_name(text: str) -> Optional[str]:
            # Example:
            #   Content-Disposition: form-data; name="a"; filename="a"
            try:
                return re.search('name="(.+?)"', text).group(1)
            except AttributeError:
                logger.warning("Expecting name field in '%s'.", text)
                return None

        def get_content_type(text: str) -> str:
            return text.split(":")[1].strip()

        fields = []
        name = None
        content_type = None
        delimiter = b"--" + boundary.encode()
        expect_data = False
        data = []

        for line in read_lines(rfile, length):
            # logger.debug(line)

            # Note: this will also catch the end delimiter with trailing dashes ('--').
            if line.startswith(delimiter):
                if expect_data:
                    fields.append(
                        MultiPartFormDataField(name, content_type, b"\r\n".join(data).rstrip())
                    )
                    data.clear()

                expect_data = False
                continue

            if expect_data:
                data.append(line)
                continue

            if not line or line == b"\r\n":
                expect_data = True
                continue

            text = line.decode().lower()

            if text.startswith(CONTENT_DISPOSITION):
                name = get_name(text)
            elif text.startswith(CONTENT_TYPE):
                content_type = get_content_type(text)

        return fields
