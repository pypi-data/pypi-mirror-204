# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    The master control settings for volent

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 03-24-2023 07:16:43
    `name`: control
    * @xxx [03-24-2023 07:16:59]: documentation for control
'''




from typing import Union


sql_quote_char:str = "`"
'''The character to use for quoting strings in the sql output'''
varchar_default_length:int = 50
'''The default character length for varchar columns'''


# mysql_maximum_column_name_length:int = 64
class mysql:
    '''MySQL specific settings'''
    create_table_indent:int = 4
    '''How many spaces to indent the contents of a create table statement'''
    safe_scripts:bool = True
    '''If True the statements include "IF [NOT] EXISTS" to avoid errors'''
    
    # _max_col_name_len:int = 64
    # '''The maximum length of a column name (don't fuckin change this, this is the MySQL limitation)'''
    _max_table_name_len:int = 64
    '''The maximum length of a table name (don't fuckin change this, this is the MySQL limitation)'''
    _max_database_name_len:int = 64
    '''The maximum length of a database name (don't fuckin change this, this is the MySQL limitation)'''
    _max_index_name_len:int = 64
    '''The maximum length of a index name (don't fuckin change this, this is the MySQL limitation)'''
    _max_constraint_name_len:int = 64
    '''The maximum length of a constraint name (don't fuckin change this, this is the MySQL limitation)'''

    _max_table_column_count:int = 4096
    '''The maximum number of columns a table can have (don't fuckin change this, this is the MySQL limitation)'''
    _max_table_comment_len:int = 2048
    '''The maximum length of a table comment (don't fuckin change this, this is the MySQL limitation)'''
    # _max_column_comment_len:int = 1024
    # '''The maximum length of a column comment (don't fuckin change this, this is the MySQL limitation)'''

    _reserved_terms = ["accessible","add","all","alter","analyze","and","as","asc","asensitive","before","between","bigint","binary","blob","both","by","call","cascade","case","change","char","character","check","collate","column","condition","constraint","continue","convert","create","cross","cube","cume_dist","current_date","current_time","current_timestamp","current_user","cursor","database","databases","day_hour","day_microsecond","day_minute","day_second","dec","decimal","declare","default","delayed","delete","dense_rank","desc","describe","deterministic","distinct","distinctrow","div","double","drop","dual","each","else","elseif","empty","enclosed","escaped","except","exists","exit","explain","false","fetch","first_value","float","float4","float8","for","force","foreign","from","fulltext","function","generated","get","grant","group","grouping","groups","having","high_priority","hour_microsecond","hour_minute","hour_second","if","ignore","in","index","infile","inner","inout","insensitive","insert","int","int1","int2","int3","int4","int8","integer","intersect","interval","into","io_after_gtids","io_before_gtids","is","iterate","join","json_table","key","keys","kill","lag","last_value","lateral","lead","leading","leave","left","like","limit","linear","lines","load","localtime","localtimestamp","lock","long","longblob","longtext","loop","low_priority","master_bind","master_ssl_verify_server_cert","match","maxvalue","mediumblob","mediumint","mediumtext","middleint","minute_microsecond","minute_second","mod","modifies","natural","not","no_write_to_binlog","nth_value","ntile","null","numeric","of","on","optimize","optimizer_costs","option","optionally","or","order","out","outer","outfile","over","partition","percent_rank","precision","primary","procedure","purge","range","rank","read","reads","read_write","real","recursive","references","regexp","release","rename","repeat","replace","require","resignal","restrict","return","revoke","right","rlike","row","rows","row_number","schema","schemas","second_microsecond","select","sensitive","separator","set","show","signal","smallint","spatial","specific","sql","sqlexception","sqlstate","sqlwarning","sql_big_result","sql_calc_found_rows","sql_small_result","ssl","starting","stored","straight_join","system","table","terminated","then","tinyblob","tinyint","tinytext","to","trailing","trigger","true","undo","union","unique","unlock","unsigned","update","usage","use","using","utc_date","utc_time","utc_timestamp","values","varbinary","varchar","varcharacter","varying","virtual","when","where","while","window","with","write","xor","year_month","zerofill"]
    '''A list of terms that are reserved by MySQL (don't fuckin change this, this is the MySQL limitation)'''
    _invalid_name_first_chars = [*"@#$0123456789"]
    '''A list of characters that a column name cannot start with. (don't fuckin change this, this is the MySQL limitation)'''

    ignore_reserved_terms:bool = False
    '''If True, the name validation will not raise an error if there is a collision.'''




    class database:
        max_name_length:int = 64
        '''The maximum length of a database name (don't fuckin change this, this is the MySQL limitation)'''


    class table:

        max_comment_length:int = 2048
        '''The maximum length of a table comment (don't fuckin change this, this is the MySQL limitation)'''
        max_name_length:int = 64
        '''The maximum length of a table name (don't fuckin change this, this is the MySQL limitation)'''
        _max_column_count:int = 4096
        '''The maximum number of columns a table can have (don't fuckin change this, this is the MySQL limitation)'''


    class column:

        max_comment_length:int = 1024
        '''The maximum length of a column comment (don't fuckin change this, this is the MySQL limitation)'''
        max_name_length:int = 64
        '''The maximum length of a column name (don't fuckin change this, this is the MySQL limitation)'''






