# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable
import colemen_utils as c
import volent.settings as _settings
import volent.settings.types as _t




@dataclass
class TypeBase:
    data_length:int = None
    '''The column specific length for this data type'''
    
    sql_type_name:str = None
    '''The SQL name for the data type'''

    python_data_type:tuple = None
    '''The python equivalent data type'''
    
    max_data_length:int = None
    '''The maximum length of this data type'''
    min_data_length:int = None
    '''The minimum length of this data type'''

    def __init__(self,data_length:int=None) -> None:
        self.data_length = data_length

    @property
    def summary(self):
        '''
            Get this TypeBase's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 08:34:13
            `@memberOf`: TypeBase
            `@property`: summary
        '''
        value = {
            "sql_type_name":self.sql_type_name,
            "data_length":self.data_length,
            "python_type_name":self.python_type_name,
            # "max_data_length":self.max_data_length,
            # "min_data_length":self.min_data_length,
        }
        return value

    def _validate_data_length(self,data_length:int=None,default_value:int=None):
        if data_length is None:
            if default_value is None:
                self.data_length = data_length
                return
            data_length = default_value
        if isinstance(data_length,(float)):
            data_length = int(data_length)
        if isinstance(data_length,(int)) is False:
            raise TypeError(f"The data_length must be an integer")


        if self.max_data_length is not None and self.min_data_length is not None:
            if data_length > self.max_data_length or data_length < self.min_data_length:
                raise ValueError(f"The data_length for a {self.sql_type_name} must range from {self.min_data_length} to {self.max_data_length}")
        self.data_length = data_length

    @property
    def sql(self):
        '''
            Get this Type's sql data type

            BOOLEAN,VARCHAR(255)

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-24-2023 04:23:20
            `@memberOf`: Bool
            `@property`: mysql
        '''
        # if self.flavored_name in ["BIGINT","INTEGER"]:
        if self.data_length is None:
            return self.flavored_name
        return f"{self.flavored_name}({self.data_length})"

    @property
    def flavored_name(self):
        '''
            Get this TypeBase's flavored_name

            This is the sql_type_name converted to the sql flavor.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-24-2023 06:18:40
            `@memberOf`: TypeBase
            `@property`: flavored_name
        '''
        value = self.sql_type_name
        if _settings.globe.flavor == "sqlite":
            value = c.types.mysql_to_sqlite(self.sql_type_name)
        return value

    @property
    def python_type_name(self):
        '''
            Get this TypeBase's python_type_name

            This is the python type that is equivalent to this data type.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-24-2023 05:01:21
            `@memberOf`: TypeBase
            `@property`: python_type_name
        '''
        # value = self.python_data_type[0].__repr__
        # value = value.replace("<slot wrapper '__repr__' of '","")
        # value = value.replace("' objects>","")
        value = self.python_data_type.__name__
        # value = self.python_data_type[0]
        return value



    # def coerce(value):
    #     type_name = 





    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.python_type_name}>"