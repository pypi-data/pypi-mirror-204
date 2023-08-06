# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

# from dataclasses import dataclass
from typing import Iterable, OrderedDict, Sized, Union
# from collections import OrderedDict
# from abc import ABC, abstractmethod

from datetime import datetime
from datetime import timezone



import colemen_utils as c

import volent.settings as _settings
import volent.settings.types as _t
from volent.exceptions import ValidationError
from volent.validate.Validator import Validator

class PastUnixDate(Validator):

    field_name = None
    message_max = "Date is in the future."
    message_min = "Date is too far in the past."


    def __init__(
        self,
        max_days=None,
        ):

        self.max_days = max_days

    # def _format_error(self, value: Sized, message: str) -> str:
    #     if self.field_name is not None:
    #         message = message[0].lower() + message[1:]
    #         message = f"{self.field_name} {message}"
    #     return message.format(
    #         input=value, min=self.min, max=self.max, equal=self.equal
    #     )


    def _repr_args(self) -> str:
        return f"max_days={self.max_days!r}"


    def __call__(self,value:int,field_name:str=None)->Sized:
        cur = round(datetime.now(tz=timezone.utc).timestamp())
        if value > cur:
            raise ValidationError(self.message_max,field_name)
        if isinstance(self.max_days,(int)):
            max = cur - (self.max_days * 86400)
            if value < max:
                raise ValidationError(self.message_min,field_name)

        return value