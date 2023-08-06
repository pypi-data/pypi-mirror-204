# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable, OrderedDict, Sequence, Sized, Any, TypeVar, Union
from collections import OrderedDict
from abc import ABC, abstractmethod


import colemen_utils as c

import volent.settings as _settings
import volent.settings.types as _t
from volent.exceptions import ValidationError
from volent.validate.Validator import Validator


_T = TypeVar("_T")

class Range(Validator):

    field_name = None
    

    message_min = "Must be {min_op} {{min}}."
    message_max = "Must be {max_op} {{max}}."
    message_all = "Must be {min_op} {{min}} and {max_op} {{max}}."

    message_gte = "greater than or equal to"
    message_gt = "greater than"
    message_lte = "less than or equal to"
    message_lt = "less than"
    
    
    # default_message = "Must be within range {min}-{max}"
    # below_min_message = "Must be greater than {min}"
    # above_max_message = "Must be less than {max}"


    def __init__(
        self,
        min:Union[int,float]=None,
        max:Union[int,float]=None,
        min_inclusive:bool=True,
        max_inclusive:bool=True,
        error:str=None,
        ):
        '''
            A validator that passes if the value is within the range.
            ----------

            Arguments
            -------------------------
            `min` {int,float}
                The minimum value

            `max` {int,float}
                The maximum value

            `min_inclusive` {bool}
                If False, the min value is not considered a valid value

            `max_inclusive` {bool}
                If False, the max value is not considered a valid value

            `error` {str}
                The custom error to use if this validator fails.
                Accepts `input`, `min`, `max`, `field_name`

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
        self.min = min
        self.max = max
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.error = error
        # self.use_custom_error = False
        # if error is not None:
            # self.use_custom_error = True
        self.message_min = self.message_min.format(
            min_op=self.message_gte if self.min_inclusive else self.message_gt
        )
        self.message_max = self.message_max.format(
            max_op=self.message_lte if self.max_inclusive else self.message_lt
        )
        self.message_all = self.message_all.format(
            min_op=self.message_gte if self.min_inclusive else self.message_gt,
            max_op=self.message_lte if self.max_inclusive else self.message_lt,
        )
        # self.error = error or self.default_message  # type: str

        if min is None and max is None:
            raise ValueError("min or max must be provided.")


    def _format_error(self, value: _T,message:str) -> str:
        args = {
            "input":value,
            "min":self.min,
            "max":self.max,
        }
        if self.field_name is not None:
            args["field_name"] = self.field_name

        return (self.error or message).format(**args)


    def _repr_args(self) -> str:
        return f"min={self.min!r},max={self.max!r},min_inclusive={self.min_inclusive!r},max_inclusive={self.max_inclusive!r}"


    def __call__(self,value:_T,field_name:str=None)->_T:
        self.field_name = field_name

        if self.min is not None and (
            value < self.min if self.min_inclusive else value <= self.min
        ):
            message = self.message_min if self.max is None else self.message_all
            raise ValidationError(self._format_error(value, message))

        if self.max is not None and (
            value > self.max if self.max_inclusive else value >= self.max
        ):
            message = self.message_max if self.min is None else self.message_all
            raise ValidationError(self._format_error(value, message))

        return value

        return value


# class ContainsOnly(OneOf):

#     field_name = None
#     default_message = "One or more of the choices you made was not in: {choices}."


#     def __init__(
#         self,
#         choices=Iterable,
#         ):

#         self.choices = choices
#         self.choices_str = ', '.join(str(choice) for choice in self.choices)

#     def _format_error(self, value: str, message: str) -> str:
#         if self.field_name is not None:
#             message = f"{self.field_name} was not in {self.choices}"
#         return message.format(
#             input=value, choices=self.choices_str
#         )


#     def _repr_args(self) -> str:
#         return f"min={self.min!r}, max={self.max!r}, equal={self.equal!r}"


#     def __call__(self,value:Sequence[_T],field_name:str=None)->Sequence[_T]:
#         self.field_name = field_name
#         test_value = c.arr.force_list(value)

#         for val in test_value:
#             if val not in self.choices:
#                 raise ValidationError(self._format_error(value,self.default_message))

#         return value
