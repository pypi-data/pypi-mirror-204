# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable, OrderedDict, Sized, Union
from collections import OrderedDict
from abc import ABC, abstractmethod


import colemen_utils as c

import volent.settings as _settings
import volent.settings.types as _t
from volent.exceptions import ValidationError
from volent.validate.Validator import Validator

class Length(Validator):

    field_name = None
    message_min = "Shorter than minimum length {min}."
    message_max = "Longer than maximum length {max}."
    message_all = "Length must be between {min} and {max}."
    message_equal = "Length must be {equal}."


    def __init__(
        self,
        min=None,
        max=None,
        equal=None
        ):
        if equal is not None and any([min, max]):
            raise ValueError(
                "The `equal` parameter was provided, maximum or "
                "minimum parameter must not be provided."
            )

        self.min = min
        self.max = max
        self.equal = equal

    def _format_error(self, value: Sized, message: str) -> str:
        if self.field_name is not None:
            message = message[0].lower() + message[1:]
            message = f"{self.field_name} {message}"
        return message.format(
            input=value, min=self.min, max=self.max, equal=self.equal
        )


    def _repr_args(self) -> str:
        return f"min={self.min!r}, max={self.max!r}, equal={self.equal!r}"


    def __call__(self,value:Sized,field_name:str=None)->Sized:
        length = len(value)
        self.field_name = field_name

        if self.equal is not None:
            if length != self.equal:
                raise ValidationError(self._format_error(value,self.message_equal),field_name)
            return value

        if self.min is not None and length < self.min:
            message = self.message_min if self.max is None else self.message_all
            raise ValidationError(self._format_error(value, message),field_name)

        if self.max is not None and length > self.max:
            message = self.message_max if self.min is None else self.message_all
            raise ValidationError(self._format_error(value, message),field_name)
        return value