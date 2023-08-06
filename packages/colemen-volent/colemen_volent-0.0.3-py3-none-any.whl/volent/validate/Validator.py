# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Any
from collections import OrderedDict
from abc import ABC, abstractmethod

import colemen_utils as c

import volent.settings as _settings
import volent.settings.types as _t
from volent.Column import Column as _column
from volent.Relationship import Relationship as _relationship
# from volent.mixins.EntityNameMixin import EntityNameMixin
# from volent.meta_validators import validate_table_comment,validate_table_name

class Validator(ABC):
    """Abstract base class for validators.

    .. note::
        This class does not provide any validation behavior. It is only used to
        add a useful `__repr__` implementation for validators.
    """

    error = None  # type: str | None

    def __repr__(self) -> str:
        args = self._repr_args()
        args = f"{args}, " if args else ""

        return "<{self.__class__.__name__}({args}error={self.error!r})>".format(
            self=self, args=args
        )

    def _repr_args(self) -> str:
        """A string representation of the args passed to this validator. Used by
        `__repr__`.
        """
        return ""

    @abstractmethod
    def __call__(self, value: Any) -> Any:
        ...