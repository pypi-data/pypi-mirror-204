# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable
import colemen_utils as c
import volent.settings as _settings
import volent.settings.types as _t
from volent.data_types.TypeBase import TypeBase as _type_base


@dataclass
class String(_type_base):


    def __init__(self,data_length:int=None) -> None:
        super().__init__(data_length)
        self.min_data_length = 0
        self.max_data_length = 65535
        self.sql_type_name = "VARCHAR"
        self.python_data_type = (str)

        self._validate_data_length(data_length,_settings.control.varchar_default_length)

    @property
    def mysql(self):
        '''
            Get this String's mysql

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-24-2023 04:23:20
            `@memberOf`: String
            `@property`: mysql
        '''
        value = f"varchar({self.data_length})"
        return value

    def _serialize(self,value):
        if isinstance(value,(str)):
            return value

        if isinstance(value,(int,float)):
            return str(value)

        if isinstance(value,(bool)):
            return c.types.bool_to_string(value)

    def _deserialize(self,value):
        return value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.data_length}>"