# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
from string import Template
from typing import Iterable
# from typing import Iterable

import colemen_utils as c
import sqlite3
import mysql.connector as _mysqlConnnector


import volent.settings as _settings
import volent.settings.types as _t

qc:str = _settings.control.sql_quote_char
'''The quote character to use.'''
indent:str = " " * _settings.control.mysql.create_table_indent
'''The indentation string used for the table contents'''


@dataclass
class MySQLGeneratorMixin:


    def master_sql(self,file_path:str=None,drops=True):
        '''Generate the Master SQL for all databases and tables.

        This can only be called on the Volent instance.,
        '''
        database_drops = []
        database_creates = []
        table_drops = []
        table_creates = []
        master_string = ""

        from volent.Volent import Volent as _bv
        from volent.Database import Database as _database
        if isinstance(self,_bv):

            # print(f"generating MYSQL SQL content")
            for mdl in self.models:
                table_drops.append(mdl.drop_statement)
                table_creates.append(mdl.create_statement)
            for db in self.databases:
                database_drops.append(db.drop_statement)
                database_creates.append(db.create_statement)
            if drops:
                master_list = table_drops + database_drops + database_creates + table_creates
            else:
                master_list = database_creates + table_creates
            master_string = '\n'.join(master_list)


        if isinstance(self,_database):

            for mdl in self.models:
                table_drops.append(mdl.drop_statement)
                table_creates.append(mdl.create_statement)
            database_drops.append(self.drop_statement)
            database_creates.append(self.create_statement)
            if drops:
                master_list = table_drops + database_drops + database_creates + table_creates
            else:
                master_list = database_creates + table_creates
            master_string = '\n'.join(master_list)

        c.file.write(file_path,master_string)
        return master_string

    @property
    def quoted_name(self):
        '''
            Get this MySQLGeneratorMixin's quoted_name

            If this is a database:
                \`database_name\`
            If this is a model:
                \`database_name\`.\`table_name\`

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-25-2023 09:35:15
            `@memberOf`: MySQLGeneratorMixin
            `@property`: quoted_name
        '''
        from volent.Database import Database as _database
        from volent.Model import Model as _model
        from volent.Column import Column as _column
        from volent.UniqueConstraint import UniqueConstraint as _unique_constraint
        from volent.Relationship import Relationship as _relationship

        if isinstance(self,_database):
            return f"{qc}{self.name}{qc}"

        if isinstance(self,_model):
            if self.database_name is not None:
                # print(self.database.name)
                # print(self.database.name.name)
                return f"{qc}{self.database_name}{qc}.{qc}{self.name}{qc}"
            else:
                return f"{qc}{self.name}{qc}"

        if isinstance(self,_column):
            return f"{qc}{self.name}{qc}"

        if isinstance(self,_unique_constraint):
            return f"{qc}{self.name}{qc}"

        if isinstance(self,_relationship):
            return f"{qc}{self.name}{qc}"

    def gen_quoted_name(self,table_name:str,database_name:str=None):
        if isinstance(database_name,(str)):
            database_name = f"{qc}{database_name}{qc}."
        else:
            database_name = ""
        value = f"{database_name}{qc}{table_name}{qc}"
        return value
        



    @property
    def drop_statement(self):
        from volent.Database import Database as _database
        from volent.Model import Model as _model

        if isinstance(self,_database):
            exists = _gen_safe_script_exists()
            return f"DROP SCHEMA {exists}{self.quoted_name};"
        if isinstance(self,_model):
            exists = _gen_safe_script_exists()
            return f"DROP TABLE {exists}{self.quoted_name};"

    def gen_drop_table_statement(self,table_name,database_name:str=None):
        qn = self.gen_quoted_name(table_name,database_name)
        value = f"DROP TABLE IF EXISTS {qn}"
        return value
        

    @property
    def create_statement(self):
        from volent.Database import Database as _database
        from volent.Model import Model as _model
        from volent.Column import Column as _column
        from volent.UniqueConstraint import UniqueConstraint as _unique_constraint
        from volent.Relationship import Relationship as _relationship


        if isinstance(self,_database):
            exists = _gen_safe_script_not_exists()
            return f"CREATE SCHEMA {exists}{self.quoted_name};"

        if isinstance(self,_column):
            return _gen_column_declaration(self)

        if isinstance(self,_unique_constraint):
            return _gen_unique_constraint_create(self)

        if isinstance(self,_relationship):
            return _gen_relationship_create(self)

        if isinstance(self,_model):
            return _gen_table_create_statement(self)





    @property
    def show_columns(self):
        '''
            Get this MySQLGeneratorMixin's show_columns

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 09:36:19
            `@memberOf`: MySQLGeneratorMixin
            `@property`: show_columns
        '''
        
        from volent.Model import Model as _model
        if isinstance(self,_model):
            sql = f"SHOW FULL COLUMNS FROM {self.quoted_name}"
            return sql


    @property
    def describe(self):
        '''
            Get the 

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-18-2023 09:33:48
            `@memberOf`: MySQLGeneratorMixin
            `@property`: describe
        '''
        from volent.Model import Model as _model
        if isinstance(self,_model):
            sql = f"DESC {self.quoted_name}"
            return sql







# ---------------------------------------------------------------------------- #
#                               COLUMN GENERATORS                              #
# ---------------------------------------------------------------------------- #


def _gen_column_declaration(column:_t.column_type)->str:
    '''Generate a mysql column declaration

    `device_id`      bigint NOT NULL COMMENT 'description: The id of the device to associate'
    '''
    value = []
    lcn,_ = column.model.longest_column_name
    q = _settings.control.sql_quote_char
    sql_name = f"{q}{column.name}{q}"
    sql_name = c.string.rightPad(sql_name,lcn + 5," ")
    data_type = column.data_type
    if isinstance(column.data_type,(str)) is False:
        data_type = column.data_type.sql

    auto_increment = _gen_auto_increment(column.auto_increment)
    nullable = _gen_sql_nullable(column.nullable)
    comment = _gen_column_comment(column.comment)
    default = _gen_column_default(column)
    value.append(sql_name)
    value.append(data_type)
    value.append(nullable)
    value.append(auto_increment)
    value.append(default)
    value.append(comment)
    value = c.arr.strip_list_nulls(value)
    string_value = ' '.join(value)
    indent = " " * _settings.control.mysql.create_table_indent
    return f"{indent}{string_value}"

def _gen_sql_nullable(nullable:bool)->str:
    '''
        Generates the MySQL null value

        "NULL" or "NOT NULL"
        ----------

        Arguments
        -------------------------
        `nullable` {bool}
            The nullable value of the column

        Return {str}
        ----------------------
        "NULL" if the column is nullable, "NOT NULL" if it is not nullable

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-24-2023 06:33:06
        `version`: 1.0
        `method_name`: _gen_sql_nullable
        * @xxx [03-24-2023 06:34:55]: documentation for _gen_sql_nullable
    '''
    value = "NOT NULL"
    if nullable:
        value = "NULL"

    return value

def _gen_auto_increment(auto_increment:bool)->str:

    value = None
    if auto_increment:
        value = "AUTO_INCREMENT"

    return value

def _gen_column_comment(comment:str=None)->str:
    '''
        Generate a MySQL column comment
        ----------

        Arguments
        -------------------------
        `comment` {str,None}
            The comment value


        Return {str,None}
        ----------------------
        The comment string if the value is not None and has a length greater than zero

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-24-2023 06:39:39
        `version`: 1.0
        `method_name`: _gen_column_comment
        * @TODO []: documentation for _gen_column_comment
    '''
    value = None
    if comment is None:
        return comment
    comment = c.string.strip(comment,[" "])
    if len(comment) == 0:
        return value


    return f"COMMENT '{comment}'"

def _gen_column_default(column:_t.column_type)->str:
    '''
        Generate a MySQL column default
        ----------

        Arguments
        -------------------------
        `comment` {str,None}
            The comment value


        Return {str,None}
        ----------------------
        The comment string if the value is not None and has a length greater than zero

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-24-2023 06:39:39
        `version`: 1.0
        `method_name`: _gen_column_comment
        * @TODO []: documentation for _gen_column_comment
    '''
    value = column.default
    # dt = column.data_type.python_data_type
    dt = column.data_type.python_type_name
    # print(f"dt:{dt}")
    if value is None:
        return "DEFAULT NULL"

    if isinstance(value,_settings.types.NoDefault):
        return None


    if dt in ["str","string"]:
        return f"DEFAULT '{value}'"
    if dt in ["bool"]:
        return f"DEFAULT {c.types.bool_to_int(value)}"
    if dt in ["int"]:
        return f"DEFAULT {int(value)}"
    if dt in ["float"]:
        return f"DEFAULT {float(value)}"


    return None




# ---------------------------------------------------------------------------- #
#                               UNIQUE CONSTRAINT                              #
# ---------------------------------------------------------------------------- #


_UNIQUE_CONSTRAINT_TEMPLATE = '''${indent}UNIQUE KEY $name ($columns)$comment'''
def _gen_unique_constraint_create(u:_t.unique_constraint_type)->str:
    s = Template(_UNIQUE_CONSTRAINT_TEMPLATE)
    col_list = []
    for col in u.columns:
        col_list.append(col.quoted_name)
    columns = ','.join(col_list)

    val = s.substitute(
        indent=indent,
        name=u.quoted_name,
        columns=columns,
        comment=_gen_column_comment(u.comment) or ""
    )
    return val




# ---------------------------------------------------------------------------- #
#                            FOREIGN KEY GENERATORS                            #
# ---------------------------------------------------------------------------- #


_RELATIONSHIP_TEMPLATE = '''${indent}KEY ${qc}$fk_name${qc} ($child_column_name),
${indent}CONSTRAINT $relationship_name FOREIGN KEY ${qc}$fk_name${qc} ($child_column_name) REFERENCES $parent_table ($parent_column)$on_update$on_delete'''

def _gen_relationship_create(r:_t.relationship_type)->str:
    on_update = ""
    on_delete = ""
    if r.on_update is not None:
        on_update = f" ON UPDATE {r.on_update}"
    if r.on_delete is not None:
        on_delete = f" ON DELETE {r.on_delete}"
    s = Template(_RELATIONSHIP_TEMPLATE)
    december= s.substitute(
        indent=indent,
        qc=qc,
        fk_name=f"FK_{c.rand.rand()}",
        child_column_name=r.child_column.quoted_name,
        relationship_name=r.quoted_name,
        parent_table=r.parent_model.quoted_name,
        parent_column=r.parent_column.quoted_name,
        on_delete=on_delete,
        on_update=on_update,
    )
    return december




# ---------------------------------------------------------------------------- #
#                               TABLE GENERATORS                               #
# ---------------------------------------------------------------------------- #


def _gen_table_comment(comment:str=None):
    '''
        Generate a MySQL table comment
        ----------

        Arguments
        -------------------------
        `comment` {str,None}
            The comment value


        Return {str,None}
        ----------------------
        The comment string if the value is not None and has a length greater than zero

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-24-2023 06:39:39
        `version`: 1.0
        `method_name`: _gen_table_comment
        * @TODO []: documentation for _gen_table_comment
    '''
    value = None
    if comment is None:
        return ""
    comment = c.string.strip(comment,[" "])
    if len(comment) == 0:
        return value


    return f" COMMENT='{comment}'"

def _gen_table_create_columns(model:_t.model_type)->Iterable[str]:
    '''Generates a list of column create statements for a table'''
    columns = []
    for col in model.columns:
        columns.append(col.create_statement)
    return columns

def _gen_primary_columns(model:_t.model_type)->Iterable[str]:
    '''Generates a list of primary key statements for a table'''
    primary_cols = model.primary_columns
    if len(primary_cols) == 1:
        col:_t.column_type = primary_cols[0]
        return [f"{indent}PRIMARY KEY({col.quoted_name})"]

def _gen_unique_constraints(model:_t.model_type)->Iterable[str]:
    '''Generates a list of unique constraint statements for a table'''
    uqs = []
    uc = model.unique_constraints
    if isinstance(uc,(list)):
        for u in uc:
            uqs.append(u.create_statement)
    return uqs

def _gen_relationship_decs(model:_t.model_type)->Iterable[str]:
    '''Generates a list of foreign key statements for a table'''
    value = []
    rels = model.relationships
    if isinstance(rels,(list)):
        for r in rels:
            value.append(r.create_statement)
    return value

def _gen_table_create_contents(model:_t.model_type):
    '''
        Generates the contents of an SQL create table statement

        Columns,primary keys,foreign keys,unique constraints.

        ----------

        Arguments
        -------------------------
        `model` {model}
            The model instance to generate the contents for.


        Return {str}
        ----------------------
        The string SQL contents for the table.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-25-2023 08:26:41
        `memberOf`: MySQLGenerator
        `version`: 1.0
        `method_name`: _gen_table_create_contents
        * @xxx [03-25-2023 08:28:07]: documentation for _gen_table_create_contents
    '''
    value = []
    value = c.arr.append(value,_gen_table_create_columns(model),skip_nulls=True)
    value = c.arr.append(value,_gen_primary_columns(model),skip_nulls=True)
    value = c.arr.append(value,_gen_unique_constraints(model),skip_nulls=True)
    value = c.arr.append(value,_gen_relationship_decs(model),skip_nulls=True)

    value = c.arr.strip_list_nulls(value)

    return ',\n'.join(value)


_TABLE_CREATE_TEMPLATE = """
CREATE TABLE $not_exists$table_name
(
$contents
)$table_comment;"""

def _gen_table_create_statement(model:_t.model_type):
    exists = _gen_safe_script_not_exists()

    s = Template(_TABLE_CREATE_TEMPLATE)
    value = s.substitute(
        not_exists=exists,
        table_name=model.quoted_name,
        contents=_gen_table_create_contents(model),
        table_comment=_gen_table_comment(model.model_description),
    )
    return value




# ---------------------------------------------------------------------------- #
#                              GENERAL GENERATORS                              #
# ---------------------------------------------------------------------------- #


def _gen_safe_script_exists():
    '''Generates "IF EXISTS" if _settings.control.mysql.safe_scripts is True'''
    exists = ""
    if _settings.control.mysql.safe_scripts:
        exists = "IF EXISTS "
    return exists

def _gen_safe_script_not_exists():
    '''Generates "IF NOT EXISTS" if _settings.control.mysql.safe_scripts is True'''
    exists = ""
    if _settings.control.mysql.safe_scripts:
        exists = "IF NOT EXISTS "
    return exists






