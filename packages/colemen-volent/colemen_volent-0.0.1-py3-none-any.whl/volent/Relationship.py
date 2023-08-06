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
class Relationship(MySQLGeneratorMixin):
    main:_t._main_type = None
    # database:_t.database_type = None
    model:_t.model_type = None
    name:str = None
    on_delete:str = None
    on_update:str = None
    
    # _parent_database_name:str = None
    # _parent_model_name:str = None
    # _parent_column_name:str = None

    parent_model:_t.model_type = None
    parent_column:_t.column_type = None

    child_model:_t.model_type = None
    child_column:_t.model_type = None
    # schemas:Iterable[_t.schema_type] = None



    def __init__(
        self,
        child:Union[str,_t.column_type],
        parent:str,
        name:str=None,
        on_delete:str = None,
        on_update:str = None,
        ):
        self.name = name
        self.on_delete = on_delete
        self.on_update = on_update
        self.parent = parent
        self.child_column = child


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
            "on_delete":self.on_delete,
            "on_update":self.on_update,
            "parent_model":self.parent_model.name,
            "parent_column":self.parent_column.name,
            "child_model":self.child_model.name,
            "child_column":self.child_column.name,
        }
        return value


    # def locate_parent(self):
    #     database = self._parent_database_name
    #     model = self._parent_model_name
    #     column = self._parent_column_name
    #     if database is not None:
    #         self.main






# def _parse_parent(relationship:Relationship,value):
#     value = c.string.strip_excessive_chars(value,["."])
#     pl = value.split(".")
#     if len(pl) == 3:
#         relationship._parent_database_name = pl[0]
#         relationship._parent_model_name = pl[1]
#         relationship._parent_column_name = pl[2]
#     if len(pl) == 2:
#         relationship._parent_model_name = pl[0]
#         relationship._parent_column_name = pl[1]
#     if len(pl) == 1:
#         relationship._parent_column_name = pl[0]