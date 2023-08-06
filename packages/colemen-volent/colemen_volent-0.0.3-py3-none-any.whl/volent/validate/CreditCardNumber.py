# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
import re
from typing import Iterable, OrderedDict, Pattern, Sequence, Sized, Any, TypeVar, Union
from collections import OrderedDict
from abc import ABC, abstractmethod


import colemen_utils as c

import volent.settings as _settings
import volent.settings.types as _t
from volent.exceptions import ValidationError
from volent.validate.Validator import Validator


_T = TypeVar("_T")

class CreditCardNumber(Validator):

    field_name = None

    default_message = "Invalid credit card number"


    def __init__(
        self,
        error:str=None,
        ):
        '''
            A validator that passes if the value is a credit card number
            ----------

            Arguments
            -------------------------

            `error` {str}
                The custom error to use if this validator fails.
                Accepts `input`,`field_name`

            Return {any}
            ----------------------
            The test value is successful, raises ValidationError if it fails.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 03-27-2023 09:10:41
            `memberOf`: NoneOf
            `version`: 1.0
            `method_name`: NoneOf
            * @xxx [03-27-2023 09:13:12]: documentation for NoneOf
        '''
        self.regex = re.compile(r"(4[0-9]{12}(?:[0-9]{3})?$)|(^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$)|(3[47][0-9]{13})|(^3(?:0[0-5]|[68][0-9])[0-9]{11}$)|(^6(?:011|5[0-9]{2})[0-9]{12}$)|(^(?:2131|1800|35\d{3})\d{11})")
        self.error = error or self.default_message  # type: str


    def _format_error(self, value: Union[str,bytes]) -> str:
        args = {
            "input":value,
        }
        if self.field_name is not None:
            args["field_name"] = self.field_name

        return self.error.format(**args)


    def _repr_args(self) -> str:
        return f""

    def __call__(self,value:_T,field_name:str=None)->_T:
        self.field_name = field_name
        if self.regex.match(value) is None:
            raise ValidationError(self._format_error(value))


        return value


