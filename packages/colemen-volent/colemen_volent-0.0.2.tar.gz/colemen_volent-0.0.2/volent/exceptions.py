# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable, OrderedDict, Sized, Union
from collections import OrderedDict

import colemen_utils as c


class VolentError(Exception):
    '''Base Class for Volent exceptions'''



class ValidationError(VolentError):
    _errors = {}
    def __init__(
        self,
        message:Union[str,list,dict],
        field_name:str=None,
        ):
        if field_name is not None:
            self._errors[field_name] = message
        super().__init__(message)

    @property
    def errors(self):
        '''Get a dictionary of errors

        {
            field_name : error_message
        }
        '''
        return self._errors
