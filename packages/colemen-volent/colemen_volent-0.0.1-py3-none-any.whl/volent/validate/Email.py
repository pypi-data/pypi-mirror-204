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

class Email(Validator):

    field_name = None
    default_message = "Invalid email address."

    USER_REGEX = re.compile(
        r"(^[-!#$%&'*+/=?^`{}|~\w]+(\.[-!#$%&'*+/=?^`{}|~\w]+)*\Z"  # dot-atom
        # quoted-string
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]'
        r'|\\[\001-\011\013\014\016-\177])*"\Z)',
        re.IGNORECASE | re.UNICODE,
    )
    
    DOMAIN_REGEX = re.compile(
        # domain
        r"(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+" r"(?:[A-Z]{2,6}|[A-Z0-9-]{2,})\Z"
        # literal form, ipv4 address (SMTP 4.1.3)
        r"|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)"
        r"(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]\Z",
        re.IGNORECASE | re.UNICODE,
    )

    DOMAIN_WHITELIST = ("localhost",)

    def __init__(
        self,
        ):
        pass
        # if equal is not None and any([min, max]):
        #     raise ValueError(
        #         "The `equal` parameter was provided, maximum or "
        #         "minimum parameter must not be provided."
        #     )

        # self.min = min
        # self.max = max
        # self.equal = equal

    def _format_error(self, message: str) -> str:
        if self.field_name is not None:
            return  f"{self.field_name} is not a valid email address"
        return self.default_message

    # def _repr_args(self) -> str:
    #     return f"min={self.min!r}, max={self.max!r}, equal={self.equal!r}"

    def __call__(self, value: str,field_name:str=None) -> str:
        self.field_name = field_name
        message = self._format_error(value)

        if not value or "@" not in value:
            raise ValidationError(message)

        user_part, domain_part = value.rsplit("@", 1)

        if not self.USER_REGEX.match(user_part):
            raise ValidationError(message)

        if domain_part not in self.DOMAIN_WHITELIST:
            if not self.DOMAIN_REGEX.match(domain_part):
                try:
                    domain_part = domain_part.encode("idna").decode("ascii")
                except UnicodeError:
                    pass
                else:
                    if self.DOMAIN_REGEX.match(domain_part):
                        return value
                raise ValidationError(message)

        return value