# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


# from typing import Iterable, OrderedDict, Union
# from collections import OrderedDict
import re
import sys
from typing import Iterable
import mysql.connector as _mysqlConnnector
from mysql.connector.errors import ProgrammingError
import traceback as _traceback
import colemen_utils as c
import volent.settings as _settings
import volent.settings.types as _t
from volent.mixins.MySQLGeneratorMixin import MySQLGeneratorMixin as _MySQLGeneratorMixin

_log = c.con.log


class DatabaseConnection(_MySQLGeneratorMixin):
    '''Class used as a mixin to allow database connections and the general CRUD procedures.'''
    creds = None
    connection = None
    cursor = None


    def __init__(self):
        self.creds = {}


    def get_databases_with_creds(self)->Iterable[str]:
        '''Retrieve a list of database names that have credentials in the environment.'''
        dbs = []
        for db in self.database_names:
            db_creds = c.build.get_environ(db,None)
            if db_creds is None:
                c.con.log(f"Failed to locate credentials for database: {db}","error")
                c.con.log(f"Add credentials to the environment in order for a connection to be established.","error")
                c.con.log('Example: tmp_creds = {    "database": "database_name",    "user": "username",    "password": "ps",    "host": "162.850.216.128"}',"error")
                continue
            else:
                dbs.append(db)
        return dbs



    def connect(self, db_creds:dict=None):
        '''
            Sets up the database connection with the initial settings.

            If the DB_CREDENTIALS are provided, it attempts to connect to a mysql database.

            ----------

            Keyword Arguments
            -----------------
            `DB_PATH` {string}
                The filepath to the sqlite database

            [`create`=True] {bool}
                If True and SQLite database does not exist yet, create the file.

            `DB_CREDENTIALS` {dict}
                The credentials to connect to the mysql database
                {
                    "user":"string",
                    "password":"string",
                    "host":"string",
                    "database":"string"
                }

            Return {bool}
            ----------
                True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 08:04:18
            `version`: 1.0
        '''
        connect_success = False
        from volent.Database import Database as _Database
        if isinstance(self,_Database):
            db_creds = c.build.get_environ(self.name,None)
            if db_creds is None:
                c.con.log(f"Failed to locate credentials for database: {db}","error")
            else:
                connect_success = self.__connect_to_my_sqldb(db_creds)
                if connect_success:
                    # _traceback.print_stack()
                    c.con.log(f"Successfully connected to {db_creds['database']}","green")

        else:

            from volent.Volent import Volent as _bv
            if isinstance(self,_bv):
                for db in self.databases:
                    result = db.connect()
                    if result is False:
                        c.con.log(f"Failed to connect to {db.name}","warning")
                        connect_success = False



        # if _settings.globe.flavor == "mysql":
        #     if db_creds is None:
        #         db_creds = self.credentials()
        #     if isinstance(db_creds,(dict)):
        #         connect_success = self.__connect_to_my_sqldb(db_creds)
        #         if connect_success:
        #             c.con.log(f"Successfully connected to {db_creds['database']}","green")

        return connect_success

    def __validate_db_credentials(self,creds:dict):
        '''
                Validates that all of the db_credentials are provided.

                ----------

                Return {bool}
                ----------------------
                True upon success, false otherwise.

                Meta
                ----------
                `author`: Colemen Atwood
                `created`: 04-19-2021 08:23:40
                `memberOf`: colemen_database
                `version`: 1.0
                `method_name`: __validate_db_credentials
        '''
        # if 'db_credentials' in self.data:
        error_array = []
        # creds = self.data['db_credentials']
        if 'user' not in creds:
            error_array.append('user is not provided in db_credentials')
        if 'password' not in creds:
            error_array.append('password is not provided in db_credentials')
        if 'host' not in creds:
            error_array.append('host is not provided in db_credentials')
        if 'database' not in creds:
            error_array.append('database is not provided in db_credentials')
        if len(error_array) == 0:
            # print("Successfully validated db_credentials")
            return True
        return False

        print("Credentials are needed to connect to the Mysql Database.")
        return False

    def __connect_to_my_sqldb(self,creds:dict):
        '''
            Attempts to connect to a mysql database.

            ----------

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 08:23:40
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __connect_to_my_sqldb
        '''

        connect_success = False
        if self.connection is not None:
            return True

        if self.__validate_db_credentials(creds) is True:
            _settings.globe.flavor = "mysql"
            self.connection = None
            try:

                self.connection = _mysqlConnnector.connect(
                    user=creds['user'],
                    password=creds['password'],
                    host=creds['host'],
                    database=creds['database']
                )
                self.cursor = self.connection.cursor(
                    buffered=True,
                    dictionary=True
                )

                if self.connection.is_connected():
                    # print("Successfully connected to mysql database")
                    connect_success = True

            except ProgrammingError as error:
                c.con.log(error.msg,"red")

        return connect_success



    @property
    def is_connected(self):
        if self.connection is not None:
            return True
        return False

    def run(self, sql:str, args=False,foreign_key_checks=True):
        '''
            Executes a query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {string}
                The sql query to execute.

            `args` {list}
                A list of arguments to apply to the sql query

            [`foreign_key_checks`=True] {bool}
                If False, the database will be instructed to skip foreign_key_checks.

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            if multiple statements are provided it will return True if ALL statements execute successfully.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:07:54
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: run
        '''

        # if foreign_key_checks is False:
            # self.execute_single_statement("SET FOREIGN_KEY_CHECKS = 0;")
            # sql = f"SET FOREIGN_KEY_CHECKS = 0;\n{sql}\nSET FOREIGN_KEY_CHECKS = 0;"
        statements = sql
        success = False
        # if the sql is a string, split it into a list of statements
        if isinstance(sql, (str)):
            statements = _to_statement_list(sql)

        if len(statements) > 1:
            # print(f"Multiple statements [{len(statements)}] found in sql.")
            success = True
            for statement in statements:
                res = self.execute_single_statement(statement, args,foreign_key_checks=foreign_key_checks)
                if res is False:
                    success = False


        if len(statements) == 1:
            return self.execute_single_statement(sql, args,foreign_key_checks=foreign_key_checks)
        return success


    def run_select(self,sql:str,args=False,default=None,limit=None,offset=None):
        '''
            Execute a select query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {str}
                The Select query to execute.

            `args` {list,dict}
                The arguments to use in parameterized placeholders

            Keyword Arguments
            -------------------------
            [`default`=None] {any}
                The default value to return in the event of an error.

            [`limit`=None] {int}
                The maximum number of results to return

            [`offset`=None] {int}
                The index offset to apply to the query.

            Return {any}
            ----------------------
            The results of the query if successful, the default value otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 11:12:16
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: run_select
            * @xxx [12-09-2022 11:15:35]: documentation for run_select
        '''
        # default = _obj.get_kwarg(['default'],None,None,**kwargs)
        # limit = _obj.get_kwarg(['limit'],None,(int),**kwargs)
        # offset = _obj.get_kwarg(['offset'],None,(int),**kwargs)

        sql = _paginate_select_query(sql,limit,offset)
        if isinstance(args,(dict)):
            sql = _format_query_params(sql,args)
        # print(f"sql:{sql}")
        if self.is_connected is False:
            c.con.log("Not Connected to a database dork.","warning")
        # if self.connect() is False:
            return default

        # _log(f"sql:{sql}","cyan")
        # _log(f"args:{args}","cyan")

        if self.run(sql,args):
            return self.fetchall()
        return default



    def close(self):
        '''
            Close the connection to the mySQL database.

            ----------

            Return {None}
            ----------------------
            None

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 19:19:32
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: close
            * @xxx [06-05-2022 19:20:10]: documentation for close
        '''

        self.connection.close()
        self.connection = None
        self.cursor = None

    def execute_single_statement(self, sql:str, args=False,isTimeoutRetry=False,foreign_key_checks=True):
        '''
            Executes a single SQL query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {string}
                The SQL to be executed.

            `args` {list}
                A list of arguments for parameter substitution.

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2021 09:19:40
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: execute_single_statement
        '''
        success = False
        if self.cursor is None or self.connection is None:
            print("Not connected to a database, aborting query.")
            if self.data['credentials'] is not None:
                self.connect()
        try:
            if foreign_key_checks is False:
                self.execute_single_statement("SET FOREIGN_KEY_CHECKS = 0;")
            
            if args is False:
                # print(f"executing sql: ",sql)
                self.cursor.execute(sql)
            else:

                args = _sanitize_args(args)
                self.cursor.execute(sql, args)

                # print(f"result: ",result)

            self.connection.commit()
            success = True
            if foreign_key_checks is False:
                self.execute_single_statement("SET FOREIGN_KEY_CHECKS = 1;")


        except _mysqlConnnector.errors.IntegrityError:
            _log(f"{_traceback.format_exc()}","error")
            _log(f"SQL: {sql}","error")

        except _mysqlConnnector.errors.InterfaceError:
            if isTimeoutRetry is True:
                _log(f"{_traceback.format_exc()}","error")
                _log(f"SQL: {sql}","error")
            if isTimeoutRetry is False:
                # _log(f"CONNECTION TIMED OUT")
                self.cursor = None
                self.connection = None
                self.connect()
                return self.execute_single_statement(sql,args,True)

        except _mysqlConnnector.errors.DatabaseError:
            # print(f"ERROR: {err}", PRESET="FATAL_ERROR_INVERT")
            _log(f"{_traceback.format_exc()}","error")
            _log(f"SQL: {sql}","error")

        
        # except sqlite3.Warning as error:
        #     _log(f"Warning: {error}","error")
        #     _log(_traceback.format_exc(),"error")

        # except sqlite3.OperationalError as error:
        #     _log(f"Fatal Error: {error}","error")
        #     _log(_traceback.format_exc(),"error")

        except AttributeError:
            _log(f"{_traceback.format_exc()}\n","error")
            _log(f"{print(sys.exc_info()[2])}\n\n","error")
            _log(f"SQL: \033[38;2;(235);(64);(52)m{sql}")
        return success

    def run_from_list(self, query_list,**kwargs):
        '''
            Execute SQL statements from a list.

            ----------

            Arguments
            -------------------------
            `query_list` {list}
                A list of query statements to execute.

            Keyword Arguments
            -------------------------
            [`disable_restraints`=True] {bool}
                If True, temporarily disable foreign_key_checks while executing the queries

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-05-2022 16:32:58
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: run_from_list
            * @xxx [06-05-2022 16:36:56]: documentation for run_from_list
        '''

        disable_foreign_key_restraints = c.obj.get_kwarg(['disable key restraints','disable restraints'],True,(bool),**kwargs)
        # disable_foreign_key_restraints = True
        # if 'DISABLE_KEY_RESTRAINTS' in kwargs:
        #     if kwargs['DISABLE_KEY_RESTRAINTS'] is False:
        #         disable_foreign_key_restraints = False
        if disable_foreign_key_restraints is True:
            self.run("SET foreign_key_checks = 0;")

        success = True
        for idx,que in enumerate(query_list):
            print(f"{idx}/{len(query_list)}",end="\r",flush=True)
            success = self.run(que)
            if success is False:
                break

        if disable_foreign_key_restraints is True:
            self.run("SET foreign_key_checks = 1;")
        return success

    def run_multi(self, sql:str, args):
        sql = sql.replace(";", ";STATEMENT_END")
        statements = sql.split('STATEMENT_END')
        for s in statements:
            if len(s) > 0:
                # print(f"query: {s}")
                self.run(s, args)

    def fetchall(self):
        '''
            Executes the fetchall method on the database and converts the result to a dictionary.

            ----------


            Return {dict|list}
            ----------------------
            If there is more than one result, it returns a list of dicts.
            If there is only one result, it returns a single dictionary.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 13:58:55
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: fetchall
            * @xxx [06-02-2022 13:59:37]: documentation for fetchall
        '''
        return self._to_dict(self.cursor.fetchall())

    def fetchone(self):
        """ DOCBLOCK {
                "class_name":"Database",
                "method_name":"fetchone",
                "author":"Colemen Atwood",
                "created": "04-19-2021 08:04:18",
                "version": "1.0",
                "description":"Executes the fetchone method on the database.",
                "returns":{
                    "type":"dict",
                    "description":"The result of the fetchone command"
                }
            }"""
        r = self.cursor.fetchone()
        return r

    def _to_dict(self, result):
        # print(f"_to_dict: resultType: {type(result)}")
        if isinstance(result, list):
            new_data = []
            for row in result:
                tmp = {}
                for col in row.keys():
                    tmp[col] = row[col]
                new_data.append(tmp)
            return new_data
        # if isinstance(result, sqlite3.Row):
        #     new_data = {}
        #     for col in result.keys():
        #         new_data[col] = result[col]
        #     return new_data





def _to_statement_list(sql):
    sql = sql.replace(";", ";STATEMENT_END")
    statements = sql.split('STATEMENT_END')
    output = [x.strip() for x in statements if len(x.strip()) > 0]
    return output


def _sanitize_args(args):
    if isinstance(args,(dict)):
        output = {}
        for k,v in args.items():
            output[k] = c.string.sanitize_quotes(v)
        return output
    if isinstance(args,(list)):
        output = []
        for v in args:
            output.append(c.string.sanitize_quotes(v))
        return output



def _paginate_select_query(sql:str,limit:int=None,offset:int=None)->str:
    '''
        Apply a limit and offset value to a select query statement.
        ----------

        Arguments
        -------------------------
        `sql` {str}
            The sql statement to modify

        [`limit`=None] {int}
            The limit to apply to the results.

        [`offset`=None] {int}
            The offset to apply to the results.


        Return {str}
        ----------------------
        The sql statement with a limit and offset value applied.

        If the limit/offset if invalid no pagination is added.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2022 11:09:53
        `memberOf`: MySQLDatabase
        `version`: 1.0
        `method_name`: _paginate_select_query
        * @xxx [12-09-2022 11:11:52]: documentation for _paginate_select_query
    '''
    if limit is None and offset is None:
        return sql
    if isinstance(limit,(str)):
        limit = re.sub(r'[^0-9]',"",limit)
        if len(limit) == 0:
            return sql
        limit = int(limit)

    
    if isinstance(offset,(str)):
        offset = re.sub(r'[^0-9]',"",offset)
        if len(offset) == 0:
            offset = None
        else:
            offset = int(offset)

    if limit == 0:
        limit = 1

    if offset is not None:
        if offset < 1:
            offset = None

    sql = c.string.strip(sql,[";"],"right")
    sql = re.sub(r'limit\s*[0-9]*\s*(,|offset)\s*(:?[0-9\s]*)?',"",sql,re.MULTILINE | re.IGNORECASE)

    limit_string = f"LIMIT {limit}"
    offset_string = ""
    if offset is not None:
        offset_string = f"OFFSET {offset}"
    paginate = f"{limit_string} {offset_string}"
    sql = f"{sql} {paginate}"
    return sql


def _format_query_params(sql:str,args:dict)->str:
    '''
        Format an SQL query's parameters to use the python named template format.

        This will only replace matches that have a corresponding key in the args dictionary.

        Parameters can begin with a dollar sign or colon.


        SELECT * from blackholes WHERE hash_id=$hash_id

        SELECT * from blackholes WHERE hash_id=%(hash_id)s

        ----------

        Arguments
        -------------------------
        `sql` {str}
            The sql string to format.

        `args` {dict}
            The dictionary of parameter values.


        Return {str}
        ----------------------
        The sql statement with parameters replaced.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2022 10:39:24
        `memberOf`: MySQLDatabase
        `version`: 1.0
        `method_name`: _format_query_params
        * @xxx [12-09-2022 10:43:23]: documentation for _format_query_params
    '''
    if isinstance(args,(dict)) is False:
        return sql
    # args = sorted(args.items(), key=lambda x: x[1], reverse=True)
    arg_keys = list(args.keys())
    arg_keys.sort(key=len, reverse=True)
    for k in arg_keys:
    # for k,v in args.items():
        sql = re.sub(fr'[$:]{k}',f"%({k})s",sql)

    # matches = re.findall(r'[$:]([a-z_0-9]*)',sql,re.IGNORECASE)
    # if isinstance(matches,(list)):
    #     for match in matches:
    #         if match in args:
    #             sql = sql.replace(f"${match}",f"%({match})s")

    return sql



