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

class IpAddress(Validator):

    field_name = None

    default_message = "Invalid IP Address"


    def __init__(
        self,
        ipv4:bool=True,
        ipv6:bool=True,
        error:str=None,
        ):
        '''
            A validator that passes if the value is an ip address
            ----------

            Arguments
            -------------------------
            [`ipv4`=True] {bool}
                If True ipv4 ip addresses are allowed
            [`ipv6`=True] {bool}
                If True ipv6 ip addresses are allowed

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
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.ipv4_regex = re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
        self.ipv6_regex = re.compile(r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))")

        self.error = error or self.default_message  # type: str


    def _format_error(self, value: Union[str,bytes]) -> str:
        args = {
            "input":value,
        }
        if self.field_name is not None:
            args["field_name"] = self.field_name

        return self.error.format(**args)


    def _repr_args(self) -> str:
        return f"ipv4={self.ipv4!r},ipv6={self.ipv6!r}"

    def __call__(self,value:_T,field_name:str=None)->_T:
        self.field_name = field_name
        if self.ipv4 is True:
            if self.ipv4_regex.match(value) is True:
                return value

        if self.ipv6 is True:
            if self.ipv6_regex.match(value) is True:
                return value

        raise ValidationError(self._format_error(value))


