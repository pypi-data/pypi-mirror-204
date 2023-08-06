from __future__ import annotations

import abc
import json
from typing import Type


class NotFoundError(Exception):
    pass


class Codecs:
    def __init__(self, codecs: list[Type[Codec]]):
        self._codecs = codecs

    def register(self, codec: Type[Codec]):
        """Register codec type."""
        if not issubclass(codec, Codec):
            raise ValueError(f"Expecting type subclassed from Codec. Got {type(codec)}.")

        if codec in self._codecs:
            return

        self._codecs.append(codec)

    def unregister(self, codec: Type[Codec]):
        """Unregister codec type."""
        self._codecs.pop(codec, None)

    def clear(self):
        """Clear all registered codec types."""
        self._codecs.clear()

    def get_codec_by_value(self, obj) -> Codec:
        """Get codec by Python object."""
        for codec in self._codecs:
            if codec.is_matching_type(type(obj)):
                return codec.create_by_value(obj)

        raise NotFoundError(f"No matching codec found for object: {obj}")

    def get_codec_by_type(self, type_: Type) -> Codec:
        """Create codec by Python type."""
        for codec in self._codecs:
            if codec.is_matching_type(type_):
                return codec()

        raise NotFoundError(f"No matching codec found for type: {type_}")

    def get_codec_by_content_type(self, content_type: str) -> Codec:
        """Create codec by content-type."""
        for codec in self._codecs:
            if codec.is_matching_content_type(content_type):
                return codec.create_by_content_type(content_type)

        raise NotFoundError(f"No matching codec found for content-type: {content_type}")


class Codec(abc.ABC):
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        Codec.subclasses.append(cls)

    @classmethod
    def create_by_value(cls, obj) -> Codec:
        """Create codec by Python object."""
        return cls()

    @classmethod
    def create_by_content_type(cls, content_type: str) -> Codec:
        """Create codec by content type."""
        return cls()

    @classmethod
    def is_matching_type(cls, type_: Type) -> bool:
        """Is codec matching with the given Python type."""
        return type_ == cls.get_type()

    @classmethod
    def is_matching_content_type(cls, content_type: str) -> bool:
        """Is codec matching with content-type."""
        type_name = cls.get_type().__name__
        return content_type == f"application/{type_name}"

    def get_content_type(self) -> str:
        """Get content-type associated with codec."""
        return f"application/{self.get_type().__name__}"

    @classmethod
    @abc.abstractmethod
    def get_type(cls) -> Type:
        """Get Python type associated with codec."""

    @abc.abstractmethod
    def encode(self, obj) -> bytes:
        """Encode object as bytes."""

    @abc.abstractmethod
    def decode(self, data: bytes) -> object:
        """Decode bytes as object."""


class NoneCodec(Codec):
    CONTENT_TYPE = "application/none"

    @classmethod
    def get_type(cls) -> Type:
        return type(None)

    @classmethod
    def is_matching_content_type(cls, content_type: str) -> bool:
        return content_type == cls.CONTENT_TYPE

    def get_content_type(self) -> str:
        return self.CONTENT_TYPE

    def encode(self, obj: None) -> bytes:
        return "None".encode()

    def decode(self, data: bytes) -> None:
        return None


class BytesCodec(Codec):

    @classmethod
    def get_type(cls) -> Type:
        return bytes

    def encode(self, obj: bytes) -> bytes:
        return obj

    def decode(self, data: bytes) -> bytes:
        return data


class IntCodec(Codec):

    @classmethod
    def get_type(cls) -> Type:
        return int

    def encode(self, obj: int) -> bytes:
        return str(obj).encode()

    def decode(self, data: bytes) -> int:
        return int(data)


class FloatCodec(Codec):

    @classmethod
    def get_type(cls) -> Type:
        return float

    def encode(self, obj: float) -> bytes:
        return str(obj).encode()

    def decode(self, data: bytes) -> float:
        return float(data)


class BoolCodec(Codec):

    @classmethod
    def get_type(cls) -> Type:
        return bool

    def encode(self, obj: bool) -> bytes:
        return str(obj).encode()

    def decode(self, data: bytes) -> bool:
        str_value = data.decode()
        return str_value.lower() == "true"


class StrCodec(Codec):

    @classmethod
    def get_type(cls) -> Type:
        return str

    def encode(self, obj: str) -> bytes:
        return obj.encode()

    def decode(self, data: bytes) -> str:
        return data.decode()


class DictCodec(Codec):

    @classmethod
    def get_type(cls) -> Type:
        return dict

    def encode(self, obj: dict) -> bytes:
        return json.dumps(obj).encode()

    def decode(self, data: bytes) -> dict:
        return json.loads(data.decode())


class ListCodec(Codec):

    @classmethod
    def get_type(cls) -> Type:
        return list

    def encode(self, obj: list) -> bytes:
        return json.dumps(obj).encode()

    def decode(self, data: bytes) -> list:
        return json.loads(data.decode())


class TupleCodec(Codec):

    @classmethod
    def get_type(cls) -> Type:
        return tuple

    def encode(self, obj: tuple) -> bytes:
        return json.dumps(obj).encode()

    def decode(self, data: bytes) -> tuple:
        return tuple(json.loads(data.decode()))
