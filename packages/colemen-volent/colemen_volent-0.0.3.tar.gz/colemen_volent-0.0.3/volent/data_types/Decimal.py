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
class Decimal(_type_base):


    def __init__(self,data_length:int=10,decimal:int=0) -> None:
        super().__init__(data_length)
        self.min_data_length = 0
        self.max_data_length = 65
        self.sql_type_name = "Decimal"
        self.python_data_type = (float)

        self._validate_data_length(data_length,_settings.control.varchar_default_length)
        if decimal > 30 or decimal < 0:
            raise ValueError("The decimal for a Decimal must range from 0 to 10")

        self.decimal = decimal


    @property
    def sql(self):
        '''
            Get this Decimals SQL data type

            Decimal(10,8)

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-24-2023 04:23:20
            `@memberOf`: String
            `@property`: mysql
        '''
        if _settings.globe.flavor == "mysql":
            value = f"{self.flavored_name}({self.data_length},{self.decimal})"
        if _settings.globe.flavor == "sqlite":
            value = f"{self.flavored_name}({self.data_length},{self.decimal})"
        return value



    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.data_length} {self.decimal}>"