# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable,OrderedDict, Union


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
from volent.Field import Field as _field
# from volent.Relationship import Relationship as _relationship
# from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
from volent.query.Query import Query


@dataclass
class WhereMixin:


    def equals(self,column_name:str,value)->_t.query_type:
        value = format_null(value)
        self.add_where(column_name=column_name,value=value,comparison="=")
        return self
    is_ = equals

    def is_not(self,column_name:str,value)->_t.query_type:
        value = format_null(value)
        self.add_where(column_name=column_name,value=value,comparison="!=")
        return self
    not_ = is_not

    def null(self,column_name:str)->_t.query_type:
        self.add_where(column_name=column_name,value="NULL",comparison="IS")
        return self

    def not_null(self,column_name:str)->_t.query_type:
        self.add_where(column_name=column_name,value="NULL",comparison="IS NOT")
        return self

    def in_(self,column_name:str,options:Iterable[str])->_t.query_type:
        self.add_where(column_name,options,"in")
        return self

    def not_in(self,column_name:str,options:list)->_t.query_type:
        # options = f"({','.join(c.arr.values_to_strings(options))})"
        self.add_where(column_name,options,"not in")
        return self

    def between(self,column_name:str,minimum:Union[int,float],maximum:Union[int,float])->_t.query_type:
        self.add_where(column_name,(minimum,maximum),"between")
        return self

    def greater_than(self,column_name:str,value:Union[int,float])->_t.query_type:
        self.add_where(column_name,value,">")
        return self
    def greater_than_equal(self,column_name:str,value:Union[int,float])->_t.query_type:
        self.add_where(column_name,value,">=")
        return self

    def less_than(self,column_name:str,value:Union[int,float])->_t.query_type:
        self.add_where(column_name,value,">")
        return self

    def less_than_equal(self,column_name:str,value:Union[int,float])->_t.query_type:
        self.add_where(column_name,value,">=")
        return self


def format_null(value):
    if value is None:
        return "NULL"
    return value


