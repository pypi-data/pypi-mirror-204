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
class TinyInt(_type_base):

    def __init__(self,data_length:int=None) -> None:
        super().__init__(data_length)
        self.min_data_length = 0
        self.max_data_length = 255
        self.sql_type_name = "TINYINT"
        self.python_data_type = (int)

        self._validate_data_length(data_length,_settings.control.varchar_default_length)


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.data_length}>"