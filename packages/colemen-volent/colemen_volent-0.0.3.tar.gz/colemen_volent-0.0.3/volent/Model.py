# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable, Union
import operator


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
from volent.Column import Column as _column
from volent.Relationship import Relationship as _relationship
from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
from volent.mixins import OrderedClass,MySQLGeneratorMixin
from volent.query.Insert import Insert as _insert
from volent.query.Select import Select as _select
from volent.query.Update import Update as _update

@dataclass
# class Model(MySQLGeneratorMixin):
class Model(MySQLGeneratorMixin,metaclass=OrderedClass):
    _is_root= False
    _name:str = None
    '''The name of this models table'''
    _database_name:str = None
    '''The name of the database that this model belongs to.'''
    _database:_t.database_type = None
    '''A reference to the database instance.'''
    _description:str = None
    '''A description of this model that is applied to the database table.'''
    _columns:Iterable[_t.column_type] = None
    _relationships:Iterable[_t.relationship_type] = None
    '''A list of relationship instances'''
    _unique_constraints:Iterable[_t.unique_constraint_type] = None
    primary_column:_t.column_type = None

    __unique_prop_keys = None
    _saved:bool = False
    
    _parent_models:Iterable[_t.model_type] = None
    '''A list of models that are a parent to this model.'''
    _child_models:Iterable[_t.model_type] = None
    '''A list of models that children of this model.'''

    # _should_create:bool = False
    # _existing_table_data:dict = None

    def __init__(self,_is_root=False,**kwargs) -> None:
        if _is_root is True:
            # _new_get_cls_vars(self)
            _settings.globe.Volent.register(self)
        else:
            self._is_root = False
            # _settings.globe.Volent.register(self)
            # print(f"self.name:{self.name}")
            # mdl = _settings.globe.Volent.get_model(self.name)
            # self.database = mdl.database



        for k,v in kwargs.items():
            col = self.get_column(k)
            if col is not None:
                if col.is_primary is True and v is None:
                    continue
                col.value = v
        self._parent_models = []
        self._child_models = []



    def _get_attrs_from_parent(self):
        '''Used internally to apply the root model attributes to this instance.
        
        Essentially this just copies the database reference to all child instances of a model.
        '''
        if self._is_root is False:
            # print(f"self.name:{self.name}")
            mdl = _settings.globe.Volent.get_model(self.name)
            self._database = mdl.database


    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if not name in self._order:
            self._order.append(name)

        return value

    def ordered_attrs(self, with_order=False):
        return [(k,getattr(self, k)) for k in self._order if k != '_order' or with_order]

    @property
    def summary(self):
        '''
            Get this Model's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 08:25:40
            `@memberOf`: Model
            `@property`: summary
        '''
        value = {
            "name":self.name,
            "description":self._description,
            "columns":[x.summary for x in self.columns],
            "relationships":[x.summary for x in self.relationships],
        }


        return value


    @property
    def name(self):
        '''
            Get this Model's name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 14:15:56
            `@memberOf`: Model
            `@property`: name
        '''
        value = self._name
        if value is None:
            keys = ["__table_name__","__tablename__"]
            for key in keys:
                if hasattr(self,key):
                    value = getattr(self,key)
                    break
            # if hasattr(self,"__table_name__"):
                # value = getattr(self,"__table_name__")
            self._name = value
        return value

    @property
    def database_name(self):
        '''
            Get this Model's database_name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 15:06:52
            `@memberOf`: Model
            `@property`: database_name
        '''
        value = self._database_name
        if value is None:
            keys = ["__database_name__","__databasename__"]
            for key in keys:
                if hasattr(self,key):
                    value = getattr(self,key)
                    break
            # if hasattr(self,"__database_name__"):
                # value = getattr(self,"__database_name__")
            self._database_name = value
        return value

    @property
    def database(self)->_t.database_type:
        '''
            Get this Model's database if it has been associated to one.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 09:48:39
            `@memberOf`: Model
            `@property`: database
        '''
        
        value = self._database
        if value is None:
            self._get_attrs_from_parent()
            value = self._database
        return value

    @property
    def model_description(self)->str:
        '''
            Get this Model's description

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 15:06:52
            `@memberOf`: Model
            `@property`: description
        '''
        value = self._description
        if value is None:
            if hasattr(self,"__description__"):
                value = getattr(self,"__description__")
            else:
                value = self.__class__.__doc__
            self._description = value
        return value

    @property
    def data(self):
        '''
            Get this Model's data

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 14:48:54
            `@memberOf`: Model
            `@property`: data
        '''
        value = {}
        for col in self.columns:
            value[col.name] = col.value
        return value

    def get_column(self,name:str)->_t.column_type:
        for col in self.columns:
            if col.name == name:
                return col

        return None

    @property
    def columns(self):
        '''
            Get this Model's columns

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 14:07:35
            `@memberOf`: Model
            `@property`: columns
        '''
        value = self._columns

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
                if isinstance(val,(_column)):
                    # c.con.log(f"located Column: {name}","green")
                    val.name = name
                    val.model = self
                    if val.is_primary is True:
                        self.primary_column = val
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
        self._columns = value
        return value

    @property
    def primary_columns(self)->Iterable[_t.column_type]:
        '''
            Get this Model's primary_columns

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-24-2023 09:17:42
            `@memberOf`: Model
            `@property`: primary_columns
        '''
        value = []
        # print(f"self.columns: {self.columns}")
        for col in self.columns:
            # c.con.log(f"col.name:{col.name}")
            if col.is_primary is True:
                # print(f"{col.name}.is_primary: {col.is_primary} {type(col.is_primary)}")
                value.append(col)
        return value

    @property
    def unique_constraints(self)->Iterable[_t.unique_constraint_type]:
        '''
            Get a list of unique constraint instances from this model.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-25-2023 08:24:42
            `@memberOf`: Model
            `@property`: unique_constraints
        '''
        # return None
        value = self._unique_constraints

        if value is None:
            dif = self._unique_prop_keys
            # dif = dir(self)
            value = []
            # color = c.rand.option(["magenta","yellow","green","cyan"])
            for prop in dif:
                name = prop
                val = getattr(self,prop)
                if isinstance(val,(_uniqueConstraint)):
                    c.con.log(f"located unique constraint","magenta")
                    val.name = name
                    val.model = self

                    # parent_str = val.parent
                    # val.parent_model = _settings.globe.Volent.get_model(val.parent)
                    # val.parent_column = _settings.globe.Volent.get_column(val.parent)
                    # val.child_column = self.get_column()
                    value.append(val)

            self._unique_constraints = value
        return value

    @property
    def relationships(self)->Iterable[_t.relationship_type]:
        '''
            Get a list of relationships instances associated to this table.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-11-2023 13:47:00
            `@memberOf`: Model
            `@property`: columns
        '''

        value = self._relationships

        if value is None:
            c.con.log(f"Model.relationships","magenta")
            dif = self._unique_prop_keys

            value = []
            for prop in dif:
                name = prop
                val:_t.relationship_type = getattr(self,prop)
                if isinstance(val,(_relationship)):
                    val.name = name
                    val.child_model = self
                    val.parent_model = _settings.globe.Volent.get_model(val.parent)
                    val.parent_column = _settings.globe.Volent.get_column(val.parent)

                    value.append(val)
                    val.parent_model.add_child_model(self)
                    self.add_parent_model(val.parent_model)

            self._relationships = value
        return value

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
            df_props = dir(Model(_is_root=False))
            # # @Mstep [] gather the props of this instance.
            props = dir(self)
            # # @Mstep [] find the props that exist on this instance and not on the base.
            value = c.arr.find_list_diff(props,df_props)
            self.__unique_prop_keys = value

        return value

    @property
    def longest_column_name(self)->tuple:
        '''
            Get this Model's longest_column_name

            A tuple containing the longest column name for this table and how many characters it has.

            (19,"kitties and titties")

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-24-2023 05:53:18
            `@memberOf`: Model
            `@property`: longest_column_name
        '''
        cnames = []
        for col in self.columns:
            cnames.append(col.name)
        return c.arr.longest_string(cnames)


    # def set_instance_var(self,name,value):
    #     self.__dict__[name] = value

    def volent_register_subs(self):
        '''Have this model register its child entities

        - Columns
        - Unique Constraints
        - Relationships
        '''
        
        for uc in self.unique_constraints:
            _settings.globe.Volent.register(uc)
            
        for rel in self.relationships:
            _settings.globe.Volent.register(rel)
            
        for col in self.columns:
            _settings.globe.Volent.register(col)


    # def from_schema(self,schema:_t.schema_type):
    #     data= schema.dump()

    # def drop(self):
    #     self.database.run(self.drop_statement,foreign_key_checks=False)

    # def save(self):
    #     if self._saved is False:
    #         if self.primary_column.value is None:
    #             print(f"SAVING MODEL: {self.name}")
                
    #             self.insert(self.data)
    #         if self.primary_column.value is not None:
    #             print(f"UPDATING MODEL: {self.name}")
    #             self.update(**self.data).is_(self.primary_column.name,self.primary_column.value)

    def insert(self,data:Union[dict,_t.schema_type]=None)->bool:
        # self.database.run('show variables like "max_connections";')
        # print(self.database.fetchall())
        if isinstance(data,(dict)) is False:
            from volent.Schema import Schema as _schema
            if isinstance(data,_schema):
                data.model = self
                data = data.dump(self)
        ins = _insert(self,data)
        # print(f"{self.__class__.__name__}.insert - self.name: {self.name}")
        # print(f"{self.__class__.__name__}.insert - self.database: {self.database}")
        ins.database = self.database
        result = ins.execute()
        # print(f"result:{result}")

    def select(self,*columns)->_select:
        # print(f"columns: {columns}")
        s = _select(self,columns=columns)
        return s

    def update(self,**columns)->_update:
        # print(f"columns: {columns}")
        s = _update(self,columns=columns)
        return s


    def add_parent_model(self,model:_t.model_type):
        '''
            Add a parent model to this model.
            
            This is for internal use do not arbitrarily add models here, they wont do anything.
            ----------

            Arguments
            -------------------------
            `model` {model}
                The parent model to add.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-21-2023 08:25:10
            `memberOf`: Model
            `version`: 1.0
            `method_name`: add_parent_model
            * @xxx [04-21-2023 08:26:12]: documentation for add_parent_model
        '''
        if isinstance(model,Model) is False:
            raise TypeError(f"Expects Model type, received {type(model)}")
        self._parent_models.append(model)


    def add_child_model(self,model:_t.model_type):
        '''
            Add a child model to this model.
            
            This is for internal use do not arbitrarily add models here, they wont do anything.
            ----------

            Arguments
            -------------------------
            `model` {model}
                The child model to add.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-21-2023 08:25:10
            `memberOf`: Model
            `version`: 1.0
            `method_name`: add_child_model
            * @xxx [04-21-2023 08:26:12]: documentation for add_child_model
        '''
        if isinstance(model,Model) is False:
            raise TypeError(f"Expects Model type, received {type(model)}")
        self._child_models.append(model)



# def get_truth(inp, relate, cut):
#     ops = {'>': operator.gt,
#         '<': operator.lt,
#         '>=': operator.ge,
#         '<=': operator.le,
#         '==': operator.eq}
#     return ops[relate](inp, cut)

#     def insert(self,data)->tuple:
#         if isinstance(data,(dict)) is False:
#             raise ValueError("Data should be a dictionary.")

#         data = self.filter_dict_by_columns(data)
#         column_list = ', '.join(list(data.keys()))
#         # total_keys = len(list(data.keys()))
#         ph = []
#         for k in list(data.keys()):
#             ph.append("%s")
#         placeholders = ', '.join(ph)
#         template = f"""INSERT INTO {self.quoted_name} ({column_list}) VALUES ({placeholders})"""
#         data_tuple = tuple(list(data.values()))
#         # print(f"template: {template}")
#         # print(f"data_tuple: {data_tuple}")
#         return (template,data_tuple)



#     def filter_dict_by_columns(self,data:dict)->dict:
#         output = {}
#         for k,v in data.items():
#             col = self.get_column(k)
#             if col is not None:
#                 if v is None and col.nullable is False:
#                     continue
#                 output[k] = v
#         return output

# # def _new_get_cls_vars(instance):


#     # df_props = dir(Model(_is_root=False))
#     # # # @Mstep [] gather the props of this instance.
#     # props = dir(instance)
#     # # # @Mstep [] find the props that exist on this instance and not on the base.
#     # dif = c.arr.find_list_diff(props,df_props)
#     dif = dir(instance)
#     value = []
#     # color = c.rand.option(["magenta","yellow","green","cyan"])
#     # if 'title' in instance.__dict__:
#         # print(f"instance.__dict__['title']: {instance.__dict__['title']}")
#     for prop in dif:
#         name = prop
#         # if isinstance(val,(dict)):
#             # props[name] = val
#         val = getattr(instance,prop)
#         if isinstance(val,(_column,_uniqueConstraint,_relationship)):
#             # print(f"prop: {prop}")
#             # if name in instance.__dict__:
#                 # c.con.log(f"adding {name} to instance dict")
#                 # instance.__dict__[name] = value
#             # print(f"instance.__dict__: {instance.__dict__}")
            
#             setattr(instance,name,val)
#             # instance.set_instance_var(instance,name,val)
#             # val.name = name
#             # val.model = instance
#             # if val.is_primary is True:
#             #     self.primary_column = val
#             # value.append(val)

#     # order_cols = []
#     # for k in list(self.__fields__):
#     #     for col in value:
#     #         if col.name == k:
#     #             order_cols.append(col)
#     #             break
#     # value = order_cols



#         # return props
#         # self._columns = value
#     return instance








