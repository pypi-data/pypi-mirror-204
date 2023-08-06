# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable,OrderedDict


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
from volent.Column import Column as _column
from volent.Relationship import Relationship as _relationship
from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
from volent.mixins import MySQLGeneratorMixin
from collections import OrderedDict
from volent.exceptions import ValidationError


@dataclass
class NestedField:
    '''A schema field used for retrieving related schemas as a list. '''
    
    
    main:_t._main_type = None
    model:_t.model_type = None
    schema:_t.schema_type = None
    child_schema:_t.schema_type = None
    child_table:str = None
    '''The name of the model that this field references.'''


    name:str = None
    '''The name of this nested field.'''

    _description:str = None
    column:_t.column_type = None


    required:bool = False
    nullable:bool = True
    default = None
    validators = None


    def __init__(
        self,
        child_table:str=None,
        child_schema:_t.schema_type=None,
        default=_settings.types.no_default,
        ):
        # '''
        #     Create a schema Field
        #     ----------

        #     Arguments
        #     -------------------------
        #     [`column`=None] {str}
        #         The name of the column that this field represents.
        #         The dot delimited path to the column

        #         If None, it will attempt to find a matching column in the model.

        #     [`required`=False] {bool}
        #         arg_description

        #     [`empty_string_is_null`=True] {bool}
        #         Treat empty strings as None

        #     [`default`] {any}
        #         The default value to assign to this field

        #     [`validate`=None] {any}
        #         A list of validators to apply to this field

        #     Meta
        #     ----------
        #     `author`: Colemen Atwood
        #     `created`: 03-26-2023 09:34:14
        #     `memberOf`: Field
        #     `version`: 1.0
        #     `method_name`: Field
        #     * @xxx [04-14-2023 08:24:58]: documentation for Field
        # '''
        self.child_table = child_table
        self.child_schema = child_schema
        self.default = default
        # self.required = required
        # self.nullable = nullable
        # self.empty_string_is_null = empty_string_is_null

        # self.validators = c.arr.force_list(validate,allow_nulls=False)


    @property
    def summary(self):
        '''
            Get this Model's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-23-2023 14:39:08
            `@memberOf`: Model
            `@property`: summary
        '''
        value = {
            "name":self.name,
        }
        return value

    @property
    def dump_only(self):
        '''
            Get this Field's dump_only

            If True, this field can only be retrieved from the database and not inserted or updated.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 15:42:42
            `@memberOf`: Field
            `@property`: dump_only
        '''
        value = self.column.dump_only
        return value

    @property
    def value(self):
        '''
            Get this Field's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-25-2023 12:02:50
            `@memberOf`: Field
            `@property`: value
        '''
        value = self.column.value
        return value

    def validate(self):
        # val = self.value
        val = self.column.deserialized_value
        # val = self.column.data_type.

        if isinstance(val,self.column.data_type.python_data_type) is False:
            if self.column.is_primary is True:
                pass
            elif self.column.nullable is True:
                pass
            else:
                raise ValidationError(f"{self.column.name} expects {self.column.data_type.python_data_type} types.",self.name)

        if self._less_than_data_len(val) is False:
            raise ValidationError(f"{self.column.name} is too long.",self.name)



        if self._is_null(val):
            raise ValidationError(f"{self.name} cannot be null.",self.name)


        for valid in self.validators:
            val = valid(val,self.name)

    def _is_null(self,val):
        if isinstance(val,(str)):
            if len(val) == 0:
                val = None

        if self.nullable is False and self.value is None:
            return True
        return False

    def _less_than_data_len(self,val):
        if isinstance(self.column.data_type.data_length,(int)):
            val = str(val)
            length = len(val)
            if length > self.column.data_type.data_length:
                return False
        return True




    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.name}>"



# def _gather_subs(model:_t.model_type):
#     columns = []
#     relationships:Iterable[_t.relationship_type] = []


#     # @Mstep [] create an base instance to compare to.
#     # print(f"model.__dataclass_fields__:{model.__fields__}")
#     # print(list(model.__dict__.keys()))
#     # print("\n\n\n")
#     # print(dir(Model()))
#     df_props = dir(Model())
#     # @Mstep [] gather the props of this instance.
#     props = dir(model)
#     # @Mstep [] find the props that exist on this instance and not on the base.
#     dif = c.arr.find_list_diff(props,df_props)

#     for prop in dif:
#         # print(f"prop: {prop} - {type(prop)}")
#         if isinstance(getattr(model,prop),_column):
#             prop:_t.model_type = getattr(model,prop)
#             prop.database = model.database
#             prop.main = model.main
#             prop.model = model
#             columns.append(prop)
#             continue

#         if isinstance(getattr(model,prop),_relationship):
#             prop:_t.model_type = getattr(model,prop)
#             prop.database = model.database
#             prop.main = model.main
#             prop.child_model = model
#             if isinstance(prop.child,_column):
#                 prop.child_column = prop.child
#             if isinstance(prop,(str)):
#                 prop.child_column = model.get_column(prop)
#             relationships.append(prop)

#     order_cols = []
#     for k in list(model.__fields__):
#         for col in columns:
#             if col.name == k:
#                 order_cols.append(col)
#         # if k in columns:
#         #     order_cols.append(columns[])



#     model._columns = order_cols
#     model._relationships = relationships





