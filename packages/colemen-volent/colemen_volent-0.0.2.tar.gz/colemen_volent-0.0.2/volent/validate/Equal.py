# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# from dataclasses import dataclass
# from typing import Iterable, OrderedDict, Union
# from collections import OrderedDict
# from abc import ABC, abstractmethod
import re

import colemen_utils as c

import volent.settings as _settings
import volent.settings.types as _t
from volent.exceptions import ValidationError
from volent.validate.Validator import Validator

class Equal(Validator):

    field_name = None
    default_message = "Must be Equal to {comparable}"


    def __init__(
        self,
        comparable
        ):
        self.comparable = comparable
        # if equal is not None and any([min, max]):
        #     raise ValueError(
        #         "The `equal` parameter was provided, maximum or "
        #         "minimum parameter must not be provided."
        #     )

        # self.min = min
        # self.max = max
        # self.equal = equal

    def _format_error(self,value) -> str:
        if self.field_name is not None:
            return  f"{self.field_name} must match {self.comparable}"
        return self.default_message.format(input=value, comparable=self.comparable)

    def _repr_args(self) -> str:
        return f"comparable={self.comparable!r}"

    def __call__(self, value: str,field_name:str=None) -> str:
        self.field_name = field_name
        if value != self.comparable:
            raise ValidationError(self._format_error(value))

        return value