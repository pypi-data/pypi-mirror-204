# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
import os
from typing import Iterable


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
# from volent.Column import Column as _column
# from volent.Relationship import Relationship as _relationship
# from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
# from volent.mixins import OrderedClass,MySQLGeneratorMixin
# from volent.query.Insert import Insert as _insert
from volent.mixins.DatabaseConnection import DatabaseConnection as _DatabaseConnection


# class Model(MySQLGeneratorMixin):
@dataclass
class Database(_DatabaseConnection):
    main:_t._main_type = None
    '''A reference to volent instance.'''

    _name:str = None
    '''The name of this database.'''

    _models:Iterable[_t.model_type] = None
    '''A list of model instances that belong to this database.'''


    _models_lookup:dict = None
    '''A dictionary of models used for lookups.'''

    def __init__(self,main:_t._main_type,name:str) -> None:
        self.main = main
        self._name = name
        self._models = []
        self._models_lookup = {}

    def generate_sql(self,file_path:str=None,drops:bool=True):
        if file_path is None:
            file_path = f"{os.getcwd()}/{self.name}.sql"
        sql = self.master_sql(file_path,drops)
        return sql

    @property
    def summary(self):
        '''
            Get this Database's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 08:24:31
            `@memberOf`: Database
            `@property`: summary
        '''
        value = {
            "models":[x.summary for x in self.models]
        }

        # for m in self.models:
        #     value["models"][m.name] = m.summary
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
        return self._name

    @property
    def models(self):
        '''
            Get this Database's models

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 08:15:08
            `@memberOf`: Database
            `@property`: models
        '''
        value = self._models
        return value

    def get_model(self,name:str):
        model = None
        for m in self.models:
            if m.name == name:
                return m

        return model


    def register_models(self):
        '''
            Iterate all registered model instances and associate any that have this database's name.

            This should ONLY be called by volent._generate_databases.
            Otherwise, leave this alone.

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-18-2023 08:12:17
            `memberOf`: Database
            `version`: 1.0
            `method_name`: register_models
            * @xxx [04-18-2023 08:13:08]: documentation for register_models
        '''
        for mdl in self.main.models:
            if mdl.database_name == self.name:
                print(f"associating")
                mdl._database = self
                self._models.append(mdl)
                self._models_lookup[mdl.name] = mdl

    def existing_tables(self):
        sql = f"""SELECT * FROM information_schema.tables WHERE table_type = 'base table' AND TABLE_SCHEMA = '{self.name}'"""
        print(f"sql:{sql}")
        self.run(sql)
        result = self.fetchall()
        # print(f"result:{result}")
        c.file.writer.to_json("live_db.json",result)
        for x in result:
            # if x['TABLE_SCHEMA'] == self.name:
            table_name = x['TABLE_NAME']
            if table_name not in self._models_lookup:
                c.con.log(f"No Model exists for table {table_name}","magenta")
            else:
                c.con.log(f"Model located for table {table_name}","blue")



            # table = self.get_model(table_name)
            # if table is None:
            #     c.con.log(f"model {table_name} does not exist in the database","magenta")
            # print(x['table_name'])



    def drop_tables(self):
        '''
            Drop all tables that are associated to this database.

            This will remove tables regardless of if a model exists, ALL TABLES WILL BE DROPPED.

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-18-2023 09:58:49
            `memberOf`: Database
            `version`: 1.0
            `method_name`: drop_tables
            * @xxx [04-18-2023 10:15:24]: documentation for drop_tables
        '''
        sql = f"""SELECT table_name FROM information_schema.tables WHERE table_type = 'base table' AND TABLE_SCHEMA = '{self.name}'"""
        self.run(sql)
        result = self.fetchall()
        for x in result:
            name = x['table_name']
            # drop_statement = f"DROP TABLE `{self.name}`.`{name}`;"
            drop_statement = self.gen_drop_table_statement(name,self.name)
            result = self.run(drop_statement,foreign_key_checks=False)
            if result is True:
                c.con.log(f"Successfully Dropped table: {name}","success")

    def drop_model_tables(self):
        '''
            Drop all tables that have an associated model.

            This means any tables that already exist in the database but do not have a model will be kept.

            ----------


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-18-2023 10:19:45
            `memberOf`: Database
            `version`: 1.0
            `method_name`: drop_model_tables
            * @xxx [04-18-2023 10:20:36]: documentation for drop_model_tables
        '''
        for m in self.models:
            name = m.name
            # drop_statement = f"DROP TABLE `{self.name}`.`{name}`;"
            drop_statement = self.gen_drop_table_statement(name,self.name)
            result = self.run(drop_statement,foreign_key_checks=False)
            if result is True:
                c.con.log(f"Successfully Dropped table: {name}","success")

    def create_model_tables(self,force:bool=False,foreign_key_checks:bool = False):
        '''
            Create tables for all models associated to this database.

            ----------

            Arguments
            -------------------------
            [`force`=bool] {False}
                If True, this will drop the tables then recreate them

            [`foreign_key_checks`=False] {bool}
                If False, the database will be instructed to skip foreign_key_checks.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-18-2023 10:17:07
            `memberOf`: Database
            `version`: 1.0
            `method_name`: create_model_tables
            * @xxx [04-18-2023 10:18:44]: documentation for create_model_tables
        '''
        for m in self.models:
            if force is True:
                self.run(m.drop_statement,foreign_key_checks=foreign_key_checks)
            self.run(m.create_statement,foreign_key_checks=foreign_key_checks)



    def last_id(self)->int:
        '''
            Retrieve the last insert id committed to the database.
            ----------

            Return {int}
            ----------------------
            The primary id of the last inserted row.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-16-2022 08:43:06
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: last_id
            * @xxx [12-16-2022 08:44:37]: documentation for last_id
        '''
        sql = 'SELECT LAST_INSERT_ID();'
        result = self.run_select(sql)
        if isinstance(result,(list)):
            result = result[0]['LAST_INSERT_ID()']
        return result









