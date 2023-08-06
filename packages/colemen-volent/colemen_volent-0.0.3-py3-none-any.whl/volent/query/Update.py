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
from volent.query.WhereMixin import WhereMixin


@dataclass
class Update(Query,WhereMixin):
    def __init__(self,model:_t.model_type,columns=None) -> None:
        self._params = {}
        self._updates = []
        self.limit = 100
        self.offset = 0

        self.query_crud_type = "update"
        super().__init__(model,update_columns=columns)

    @property
    def select_string(self)->str:
        '''
            Get the compiled select string for this query.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:56:15
            `@memberOf`: SelectQuery
            `@property`: select_string
        '''
        if len(self._selects) == 0:
            value = "*"
        else:
            selects = []
            for sel in self._selects:
                value = None
                if sel['alias'] is not None:
                    value = f"{sel['column_name']} as {sel['alias']}"
                else:
                    value = f"{sel['column_name']}"
                if value is not None:
                    selects.append(value)
            value = ', '.join(selects)

        if self._count is True:
            value = f"COUNT({value})"
        if self._average is True:
            value = f"AVG({value})"
        if self.sum_ is True:
            value = f"SUM({value})"
        return value


    @property
    def query(self):


        value = f"UPDATE {self.model.quoted_name} SET {self.update_string}{self.where_string}"

        value = self._paginate_select_query(value)
        value = self._format_query_params(value,self._params)
        return value,self._params
        # return value,self._params

    def execute(self)->Union[bool,dict,int]:

        sql,args= self.query

        if sql is False:
            return False

        # print(f"sql:{sql}")
        # print(f"args:{args}")

        # @Mstep [] execute the insert query.
        result = self.database.run(sql,args)
        data = self.model.select().add_where_from_wheres(self._wheres).execute(return_models=False)
        data = data[0]
        for k,v in data.items():
            col = self.model.get_column(k)
            col._column_value = v
            self.model._saved = True
        return data
        models = []
        for r in result:
            mdl = self.model.__class__(**r)
            mdl.__doc__ = self.model.__doc__
            mdl._name = self.model.name
            mdl._database_name = self.model._database_name
            mdl._database = self.model._database
            models.append(mdl)
        return models
        return result



    @property
    def update_string(self):
        '''
            Get this UpdateQuery's update_string

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:56:15
            `@memberOf`: UpdateQuery
            `@property`: update_string
        '''
        if len(self._updates) == 0:
            return None
        else:
            selects = []
            for k,v in self._updates.items():
                value = None
                value = f"{k}=:{k}"
                self._params[k] = v
                selects.append(value)
            value = ', '.join(selects)

        return value

    def add_update(self,column_name:str,value):
        self._updates[column_name] = value


def format_null(value):
    if value is None:
        return "NULL"
    return value

