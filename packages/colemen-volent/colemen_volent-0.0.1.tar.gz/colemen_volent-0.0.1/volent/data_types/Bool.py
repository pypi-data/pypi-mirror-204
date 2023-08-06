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
class Bool(_type_base):


    def __init__(self) -> None:
        super().__init__()
        self.sql_type_name = "BOOLEAN"
        self.python_data_type = (bool)


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} >"