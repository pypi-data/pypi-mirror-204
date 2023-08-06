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

class SocialSecurityNumber(Validator):

    field_name = None
    default_message = "Invalid Social Security number"



    def __init__(
        self,
        error:str=None,
        ):
        '''
            A validator that passes if the value is a Social security number
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
        self.regex = re.compile(r"^(?!0{3})(?!6{3})[0-8]\d{2}-(?!0{2})\d{2}-(?!0{4})\d{4}$")
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


