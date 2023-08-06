# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from typing import Iterable, Union
import colemen_utils as c
import volent.settings as _settings
import volent.settings.types as _t
from volent.mixins.MySQLGeneratorMixin import MySQLGeneratorMixin

@dataclass
class UniqueConstraint(MySQLGeneratorMixin):
    main:_t._main_type = None
    # database:_t.database_type = None
    model:_t.model_type = None
    name:str = None
    comment:str = None
    columns:Iterable[_t.column_type] = None
    comment:str = None




    def __init__(
        self,
        columns:Iterable[_t.column_type],
        name:str=None,
        comment:str=None,
        ):
        self.name = name
        self.comment = comment
        self.columns = columns



        # _parse_parent(self,parent)


    @property
    def summary(self):
        '''
            Get this Relationship's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-23-2023 14:53:39
            `@memberOf`: Relationship
            `@property`: summary
        '''
        value = {
            "name":self.name,
            "comment":self.comment,
            "columns":[x.name for x in self.columns],
        }
        return value

