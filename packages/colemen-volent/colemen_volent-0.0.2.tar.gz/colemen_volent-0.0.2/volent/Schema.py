# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable,OrderedDict


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
from volent.Field import Field as _field
from volent.NestedField import NestedField as _nested_field
from volent.mixins import OrderedClass



@dataclass
class Schema(metaclass=OrderedClass):
    main = None
    # database:_t.database_type = None
    model:_t.model_type = None
    _name:str = None
    _fields:Iterable[_t.field_type] = None
    _schema_description:str = None
    _schema_crud_type:str = None

    __unique_prop_keys = None


    def __init__(self,model:_t.model_type=None) -> None:
        from volent.Model import Model as _model
        if isinstance(model,_model):
            self.model = model
        else:
            if model is not None:
                md = model()

    #     self.from_dict(kwargs)


    @property
    def summary(self):
        '''
            Get this Schema's summary

            {
                name:str,
                fields:[]
            }

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-23-2023 14:39:08
            `@memberOf`: Schema
            `@property`: summary
        '''
        value = {
            "name":self.name.snake_,
            "fields": [x.summary for x in self.fields],
        }
        return value

    @property
    def name(self)->str:
        '''
            Get this Schema's name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-23-2023 14:02:44
            `@memberOf`: Schema
            `@property`: name
        '''
        # print(self.__dict__[])
        # print(f"======================================== SCHEMA")

        # print(self.__class__.__name__)
        value = self._name
        if value is None:
            self.custom_name_key = "__schema_name__"
            if hasattr(self,self.custom_name_key):
                value = getattr(self,self.custom_name_key)
            else:
                value = c.string.to_snake_case(self.__class__.__name__)

            # value = validate_table_name(value)
            # value = c.string.Name(value)
            self._name = value
            # if hasattr(self,"__model_name__"):
            #     value = self.__model_name__
            #     value = _settings.control.mysql.validate_table_name(value)
            #     value = c.string.Name(value)
            #     self._name = value
        return value

    @property
    def schema_description(self):
        '''
            Get this Schema's schema_description

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-24-2023 07:27:06
            `@memberOf`: Schema
            `@property`: schema_description
        '''
        # print(self.__class__.__doc__)
        value = self._schema_description
        if value is None:
            if hasattr(self,"__description__"):
                value = self.__description__
                # value = validate_table_comment(self.name.snake_,value)
                self._schema_description = value
            else:
                value = self.__class__.__doc__
        return value

    @property
    def schema_crud_type(self):
        '''
            Get this Schema's schema_crud_type

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-24-2023 07:27:06
            `@memberOf`: Schema
            `@property`: schema_crud_type
        '''
        value = self._schema_crud_type
        if value is None:
            if hasattr(self,"__schema_crud_type__"):
                value = self.__schema_crud_type__
                self._schema_crud_type = value
        return value

    @property
    def fields(self)->Iterable[_t.field_type]:
        '''
            Get this Model's fields

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 14:07:35
            `@memberOf`: Model
            `@property`: fields
        '''
        value = self._fields

        if value is None:
            dif = self._unique_prop_keys
            # df_props = dir(Model(_is_root=False))
            # # # @Mstep [] gather the props of this instance.
            # props = dir(self)
            # # # @Mstep [] find the props that exist on this instance and not on the base.
            # dif = c.arr.find_list_diff(props,df_props)
            # dif = dir(self)
            value = []
            # color = c.rand.option(["magenta","yellow","green","cyan"])
            for prop in dif:
                name = prop
                # if isinstance(val,(dict)):
                    # props[name] = val
                val = getattr(self,prop)
                if isinstance(val,(_field,_nested_field)):
                    # c.con.log(f"located Field: {name}","green")
                    val.name = c.string.to_snake_case(name)
                    val.schema = self
                    value.append(val)



        order_cols = []
        for k in list(self.ordered_attrs(True)):
            for col in value:
                if col.name == k[0]:
                    order_cols.append(col)
                    break
        value = order_cols
            # order_cols = []
            # for k in list(self.__fields__):
            #     for col in value:
            #         if col.name == k:
            #             order_cols.append(col)
            #             break
            # value = order_cols



            # return props
        self._fields = value
        return value





    def __validate(self):
        '''
            Execute the validation process on all fields associated to this schema
            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-21-2023 07:43:15
            `memberOf`: Schema
            `version`: 1.0
            `method_name`: __validate
            * @xxx [04-21-2023 07:44:01]: documentation for __validate
        '''
        for f in self.fields:
            f.validate()

    def get_field(self,name:str)->_t.field_type:
        '''
            Retrieve a field from this schema
            ----------

            Arguments
            -------------------------
            `name` {string}
                The name of the field to search for.

            Return {field}
            ----------------------
            The field instance if successful, None otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-21-2023 07:44:07
            `memberOf`: Schema
            `version`: 1.0
            `method_name`: get_field
            * @xxx [04-21-2023 07:44:52]: documentation for get_field
        '''
        for field in self.fields:
            if field.name == name:
                return field
        return None

    def from_dict(self,data:dict):
        '''
            Populate a model's column values from a dictionary.

            The keys must match the column names exactly.
            ----------

            Arguments
            -------------------------
            `data` {dict}
                A dictionary to populate the columns with.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-21-2023 07:45:36
            `memberOf`: Schema
            `version`: 1.0
            `method_name`: from_dict
            * @xxx [04-21-2023 07:48:45]: documentation for from_dict
        '''

        if isinstance(data,(dict)) is False:
            raise TypeError(f"Data expects a dictionary, {type(data)} received.")

        for col in self.model.columns:
            if col not in data:
                continue
            field = self.get_field(col.name)
            if field is None:
                continue

            col.column_value = data[col]


    def dump(self,model:_t.model_type=None,many=False)->dict:
        '''Dump the contents of the model(s) using the fields to filter.'''


        if isinstance(model,(list)):
            result = []
            from volent.Model import Model as _model
            for mdl in model:
                if isinstance(mdl,_model) is False:
                    c.con.log(f"The mdl is not an instance of model:{mdl}","magenta")

                # mdl = model
                self.model = mdl
                self._correlate_to_columns()
                self.__validate()
                data = {}
                for f in self.fields:
                    data[f.name] = f.value
                result.append(data)
            return result
        if model is not None:
            self.model = model
        # self.model = model
        self._correlate_to_columns()
        self.__validate()
        data = {}
        for f in self.fields:
            data[f.name] = f.value
        if many:
            data = c.arr.force_list(data)
        return data


    def new(self)->_t.schema_type:
        '''
            Validate this schema's data and submit it to the model's table in the databse.
            ----------

            Return {schema}
            ----------------------
            This schema instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-21-2023 07:50:29
            `memberOf`: Schema
            `version`: 1.0
            `method_name`: new
            * @xxx [04-21-2023 07:51:43]: documentation for new
        '''
        # @Mstep [] correlate the fields to their columns in the model.
        self._correlate_to_columns()
        # @Mstep [] validate the schema fields.
        self.__validate()

        data = {}
        # @Mstep [LOOP] iterate this schema's fields
        for f in self.fields:
            # @Mstep [IF] if the field is NOT dump_only
            if f.dump_only is False:
                # @Mstep [] add the field to the data dictionary.
                data[f.name] = f.value
        # @Mstep [] execute the insert on the model.
        self.model.insert(self)
        # @Mstep [RETURN] return this schema instance.
        return self

    def update(self)->_t.schema_type:
        self._correlate_to_columns()
        self.__validate()
        data = {}
        for f in self.fields:
            if f.dump_only is False:
                data[f.name] = f.value
        self.model.update(**data).is_(self.model.primary_column.name,self.model.primary_column.value).execute()
        return self

    # def to_dict(self):
    #     data = {}
    #     for f in self.fields:
    #         data[f.name] = f.value

    #     # for col in self.model.columns:
    #     #     data[col.name] = col.column_value
    #     return data


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.name.s}>"


    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if not name in self._order:
            self._order.append(name)

        return value

    def ordered_attrs(self, with_order=False):
        '''Get a list of attributes for this schema in the order in which they were declared.'''
        return [(k,getattr(self, k)) for k in self._order if k != '_order' or with_order]



    @property
    def _unique_prop_keys(self):
        '''
            Get this Model's _unique_prop_keys

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 15:45:07
            `@memberOf`: Model
            `@property`: _unique_prop_keys
        '''
        value = self.__unique_prop_keys
        if value is None:
            df_props = dir(Schema())
            # # @Mstep [] gather the props of this instance.
            props = dir(self)
            # # @Mstep [] find the props that exist on this instance and not on the base.
            value = c.arr.find_list_diff(props,df_props)
            self.__unique_prop_keys = value

        return value

    def _correlate_to_columns(self):
        '''
            Iterate all fields to find their corresponding columns in the current model.
            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-21-2023 07:40:42
            `memberOf`: Schema
            `version`: 1.0
            `method_name`: _correlate_to_columns
            * @xxx [04-21-2023 07:41:38]: documentation for _correlate_to_columns
        '''
        if self.model is None:
            raise ValueError(f"No Model Provided to {self.name}")
        for f in self.fields:
            if isinstance(f,_nested_field):
                pri_col = self.model.primary_column
                child_model = _settings.globe.Volent.get_model(f.child_table)
                if child_model is not None:
                    child_model.select().is_(column_name=pri_col.name,value=pri_col.value)
                
            # print(f"{self.__class__.__name__} - self.model:{self.model}")
            col = self.model.get_column(f.name)
            if col is not None:
                f.column = col

