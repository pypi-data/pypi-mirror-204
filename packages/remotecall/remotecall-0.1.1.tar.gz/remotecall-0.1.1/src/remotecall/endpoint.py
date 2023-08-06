from __future__ import annotations

import logging
import typing
from inspect import signature, Signature, getdoc, cleandoc, Parameter
from types import MappingProxyType

logger = logging.getLogger(__name__)


class EndpointNotFound(Exception):
    """Raised if endpoint is not found by name."""


class Endpoint:
    def __init__(self, name: str, handler: typing.Callable):
        self.name = name
        self.handler = handler
        self.signature = signature(self.handler)
        self.enabled = True
        self.check_annotations()

    def __str__(self) -> str:
        return f"Endpoint('{self.name}')"

    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)

    @property
    def doc(self) -> str:
        doc = getdoc(self.handler)
        return cleandoc(doc) if doc else ""

    @property
    def parameters(self) -> MappingProxyType[str, Parameter]:
        return self.signature.parameters

    def get_parameter(self, name: str) -> Parameter:
        return self.parameters[name]

    def check_annotations(self):
        for parameter in self.parameters.values():
            if parameter.annotation is Signature.empty:
                logger.warning(
                    "%s() takes '%s' as an argument but is missing type annotation. "
                    "Server considers the argument as 'str' unless client call provides "
                    "the missing type annotation.",
                    self.name,
                    parameter.name,
                )

    def to_dict(self) -> dict:
        parameters = [self._parameter_to_dict(p) for p in self.parameters.values()]
        definition = {"name": self.name, "documentation": self.doc, "parameters": parameters}

        if self.signature.return_annotation is not Signature.empty:
            definition["return_type"] = self.signature.return_annotation.__name__

        return definition

    @classmethod
    def _parameter_to_dict(cls, parameter):
        definition = {"name": parameter.name, "type": parameter.annotation.__name__}

        if parameter.default is not parameter.empty:
            definition["default"] = parameter.default

        return definition
