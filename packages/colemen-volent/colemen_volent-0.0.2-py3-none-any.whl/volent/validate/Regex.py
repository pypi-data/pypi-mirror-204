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

class Regex(Validator):

    field_name = None
    default_message = "String does not match expected pattern."


    def __init__(
        self,
        regex:Union[str,bytes,Pattern],
        flags:int=0,
        error:str=None,
        ):
        '''
            A validator that passes if the value is within the range.
            ----------

            Arguments
            -------------------------
            `regex` {str,bytes}
                The regular expression string to use. Can also be a compiled regular expression pattern.

            `flags` {int,float}
                The regexp flags to use, for example re.IGNORECASE. Ignored
                if ``regex`` is not a string.

            `error` {str}
                The custom error to use if this validator fails.
                Accepts `input`, `regex`, `field_name`

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
        self.regex = (
            re.compile(regex, flags) if isinstance(regex, (str, bytes)) else regex
        )
        self.flags = flags

        self.error = error or self.default_message  # type: str


    def _format_error(self, value: Union[str,bytes]) -> str:
        args = {
            "input":value,
            "regex":self.regex,
        }
        if self.field_name is not None:
            args["field_name"] = self.field_name

        return self.error.format(**args)


    def _repr_args(self) -> str:
        return f"regex={self.regex!r}"

    def __call__(self,value:_T,field_name:str=None)->_T:
        self.field_name = field_name
        if self.regex.match(value) is None:
            raise ValidationError(self._format_error(value))
        return value

