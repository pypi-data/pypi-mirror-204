# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable

import colemen_utils as _c

import volent.settings.types as _t
import volent.settings as _settings
from volent.mixins import MySQLGeneratorMixin

@dataclass
class Column(MySQLGeneratorMixin):
    model:_t.model_type = None

    name:str = None
    data_type:_t.type_base_type = None
    default = None
    nullable:bool = None
    comment:str = None
    is_foreign_key:bool = None
    is_primary:bool = None
    auto_increment = None
    unique:bool = None
    is_private:bool = None
    dump_only:bool = None

    # relationship:Iterable[_t.relationship_type] = None
    # _column_value = "__NO_VALUE__"
    _column_value = _t.undefined

    def __init__(
        self,
        data_type:str,
        name:str=None,
        nullable:bool=False,
        comment:str=None,
        is_foreign_key:bool=False,
        is_primary:bool=False,
        auto_increment:bool=False,
        unique:bool=False,
        default=_settings.types.no_default,
        dump_only=False,
        ):

        self.name = name
        self.data_type = data_type
        self.default = default
        self.unique = unique
        self.nullable = nullable

        self.comment = comment
        self.is_foreign_key = is_foreign_key
        self.is_primary = is_primary
        self.auto_increment = auto_increment
        self.dump_only = dump_only
        self._column_value = None

    @property
    def summary(self):
        '''
            Get this Column's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 08:26:42
            `@memberOf`: Column
            `@property`: summary
        '''
        value = {
            "name":self.name,
            "data_type":self.data_type.summary,
            "default":self.default,
            "unique":self.unique,
            "nullable":self.nullable,
            "comment":self.comment,
            "is_foreign_key":self.is_foreign_key,
            "is_primary":self.is_primary,
            "auto_increment":self.auto_increment,
        }
        if self.default == _t.no_default:
            value['default'] = "no default"
        return value

    def __call__(self, *args, **kwds):
        return self._column_value


    @property
    def dot_path(self):
        '''
            Get this Column's dot_path

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-14-2023 07:22:26
            `@memberOf`: Column
            `@property`: dot_path
        '''
        value = self.name
        if self.model is not None:
            value = f"{self.model.name}.{self.name}"
        return value


    @property
    def value(self):
        '''
            Get this Column's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 14:49:51
            `@memberOf`: Column
            `@property`: value
        '''
        value = self._column_value
        if value == _t.undefined:
            if self.default != _t.no_default:
                value = self.default
            self.value = value
        return value

    @value.setter
    def value(self,value):
        '''
            Set the Column's value property

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 14:54:15
            `@memberOf`: Column
            `@property`: value
        '''
        if value != self._column_value:
            self.model._saved = False
        self._column_value = value

    @property
    def serialized_value(self):
        '''
            Get this Column's serialized_value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-27-2023 11:05:37
            `@memberOf`: Column
            `@property`: serialized_value
        '''
        value = self.value
        if hasattr(self.data_type,"__serialize"):
            return self.data_type.__serialize(value)
        return value

    @property
    def deserialized_value(self):
        '''
            Get this Column's deserialized_value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-27-2023 11:05:37
            `@memberOf`: Column
            `@property`: serialized_value
        '''
        value = self.value
        if hasattr(self.data_type,"__deserialize"):
            return self.data_type.__deserialize(value)
        return value


