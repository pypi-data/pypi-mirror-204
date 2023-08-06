# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable, OrderedDict, Sequence, Sized, Any, TypeVar
from collections import OrderedDict
from abc import ABC, abstractmethod


import colemen_utils as c

import volent.settings as _settings
import volent.settings.types as _t
from volent.exceptions import ValidationError
from volent.validate.Validator import Validator


_T = TypeVar("_T")

class OneOf(Validator):

    field_name = None
    default_message = "One or more of the choices you made was not in: {choices}."


    def __init__(
        self,
        choices=Iterable,
        ):

        self.choices = choices
        self.choices_str = ', '.join(str(choice) for choice in self.choices)

    def _format_error(self, value: Any, message: str) -> str:
        if self.field_name is not None:
            message = f"{self.field_name} was not in {self.choices}"
        return message.format(
            input=value, choices=self.choices_str
        )


    def _repr_args(self) -> str:
        return f"min={self.min!r}, max={self.max!r}, equal={self.equal!r}"


    def __call__(self,value:Any,field_name:str=None)->Any:
        self.field_name = field_name
        test_value = c.arr.force_list(value)
        match_found = False
        for val in test_value:
            if val in self.choices:
                match_found = True
        if match_found is False:
            raise ValidationError(self._format_error(value,self.default_message))
        return value


class ContainsOnly(OneOf):

    field_name = None
    default_message = "One or more of the choices you made was not in: {choices}."


    def __init__(
        self,
        choices=Iterable,
        ):

        self.choices = choices
        self.choices_str = ', '.join(str(choice) for choice in self.choices)

    def _format_error(self, value: str, message: str) -> str:
        if self.field_name is not None:
            message = f"{self.field_name} was not in {self.choices}"
        return message.format(
            input=value, choices=self.choices_str
        )


    def _repr_args(self) -> str:
        return f"min={self.min!r}, max={self.max!r}, equal={self.equal!r}"


    def __call__(self,value:Sequence[_T],field_name:str=None)->Sequence[_T]:
        self.field_name = field_name
        test_value = c.arr.force_list(value)

        for val in test_value:
            if val not in self.choices:
                raise ValidationError(self._format_error(value,self.default_message))

        return value
