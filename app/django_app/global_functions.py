from numpy import round
from pandas import DataFrame, Series

from pandas import read_sql, ExcelWriter, to_datetime

from sqlalchemy import create_engine
from datetime import timedelta, date

import operator as op
import io

import base64
import os

import sys

import re
from dash_extensions.snippets import send_bytes

# get table names
def get_table_names():
    host=os.environ.get('CDB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('CDB_PASS')
    db_user=os.environ.get('CDB_USER')
    db_port=os.environ.get('CDB_PORT')
    db_name=os.environ.get('CDB_NAME')
    db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
    db_connection = create_engine(db_connection_str)
    DB_TABLE_NAMES = db_connection.table_names()
    db_connection=db_connection.dispose()
    # print(DB_TABLE_NAMES)
    return DB_TABLE_NAMES

# creates a sql query of the relationship. 
def get_main_sql_query(sql_qry,rel_tables):
    result = check_if_all_none(sql_qry)
    if result is False:
        temp_str=""
        main_table_names = []
        for i in sql_qry:
            if type(i) is dict:
                if i['table_names'][0].find('/') > -1 and temp_str!="":                   
                    left_tables = i['table_names'][0].split('/')
                    left_table = ""
                    for t in left_tables:
                        stats = check_column_available(i['join_on'][0],t.strip())
                        if stats:
                            left_table = t.strip()
                            break
                
                    right_table = i['table_names'][1]

                    value_left=i['join_on'][0]# check this value in both tables
                    value_right=i['join_on'][1]

                    join_on = i['join']
                    
                    two_join_qry = f" {join_on} JOIN {right_table} ON {right_table}.{value_right} = {left_table}.{value_left}"
                    temp_str = temp_str + two_join_qry
                    main_table_names.append(right_table)
                    main_table_names.append(left_table)
                    
                else:
                    left_table = i['table_names'][0]
                    right_table = i['table_names'][1]

                    value_left=i['join_on'][0]
                    value_right=i['join_on'][1]

                    join_on = i['join']

                    two_join_qry = f"SELECT * FROM {left_table} {join_on} JOIN {right_table} ON {right_table}.{value_right} = {left_table}.{value_left}"
                    temp_str=temp_str+two_join_qry

                    main_table_names.append(right_table)
                    main_table_names.append(left_table) 
        
        temp_copy = temp_str + ';'
        temp_str=temp_str + ' LIMIT 2;'
        main_table_names=list(set(main_table_names))
        host=os.environ.get('CDB_HOST')
        if host == 'windows':
            host = os.environ['DOCKER_HOST_IP']

        db_address=host #for linux enter host ip
        pwd=os.environ.get('CDB_PASS')
        db_user=os.environ.get('CDB_USER')
        db_port=os.environ.get('CDB_PORT')
        db_name=os.environ.get('CDB_NAME')
        db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
        db_connection = create_engine(db_connection_str)
        
        try:
            df1 = read_sql(temp_str, con=db_connection)
        except:
            df1=DataFrame()
        db_connection = db_connection.dispose()

        # rename duplicate columns.
        l=list(df1.columns)
        l1=[item.lower() for item in l]
        dupli=[loc for loc,i in enumerate(l1) if l1.count(i) > 1]
        dupli=list(set([l[i] for i in dupli]))
        z=dict()
        for d in dupli:
            z[d]=[]
            for t in rel_tables:

                stats = check_column_available(d,t.strip())
                if stats:
                    z[d].append(d+'___'+t.strip())  
               
        query = ""
        for i in dupli:
            for j in z[i]:
                query=query + j.split("___")[1] + '.' + j.split("___")[0] + ' AS ' + j + ','

        if query != "" and query[-1] == ',':
            query=query[:-1]
        
        col_list = list(set(l))
        for i in dupli:
            col_list.remove(i)
        
        col_list = str(col_list).replace('[','').replace('\'','').replace(']','').replace('"','')
            
        temp_copy=temp_copy.replace('*',f'{col_list}, {query}')

        # print(f"MIAN QUYER {temp_copy}")


        if df1.shape[0] > 0:
            return True, [temp_copy,main_table_names]
        else:
            return False, []

def check_if_all_none(list_of_elem):
    """ Check if all elements in list are None """
    result = True
    for elem in list_of_elem:
        if elem is not None:
            return False
    return result


#check if the column is available in the table
def check_column_available(colname,tabname):
    host=os.environ.get('CDB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('CDB_PASS')
    db_user=os.environ.get('CDB_USER')
    db_port=os.environ.get('CDB_PORT')
    db_name=os.environ.get('CDB_NAME')

    db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
    db_connection = create_engine(db_connection_str)

    df1 = read_sql(f"select COLUMN_NAME,DATA_TYPE from information_schema.COLUMNS where TABLE_SCHEMA = '{db_name}' \
    AND TABLE_NAME = '{tabname}' AND COLUMN_NAME='{colname}'",con=db_connection)
    db_connection=db_connection.dispose()
    if df1.empty:
        return False
    else:
        return True


#check if the column is available in the table
def get_column_datatype(colname,tabname):
    host=os.environ.get('CDB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('CDB_PASS')
    db_user=os.environ.get('CDB_USER')
    db_port=os.environ.get('CDB_PORT')
    db_name=os.environ.get('CDB_NAME')

    db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
    db_connection = create_engine(db_connection_str)

    df1 = read_sql(f"select COLUMN_NAME,DATA_TYPE from information_schema.COLUMNS where TABLE_SCHEMA = '{db_name}' \
    AND TABLE_NAME = '{tabname}' AND COLUMN_NAME='{colname}'",con=db_connection)
    db_connection=db_connection.dispose()
    if df1.empty:
        return False
    else:
        return df1['DATA_TYPE'].values
#
def get_join_main(d,sql_qry):
    '''Function check wheather a given join is success or error.'''

    result = check_if_all_none(sql_qry)

    if result:
        left_table = d['table_names'][0]
        right_table = d['table_names'][1]

        value_left=d['join_on'][0]
        value_right=d['join_on'][1]

        join_on = d['join']

        two_join_qry = f"SELECT * FROM {left_table} {join_on} JOIN {right_table} \
            ON {right_table}.{value_right} = {left_table}.{value_left} LIMIT 2;"
        
        host=os.environ.get('CDB_HOST')
        if host == 'windows':
            host = os.environ['DOCKER_HOST_IP']

        db_address=host #for linux enter host ip
        pwd=os.environ.get('CDB_PASS')
        db_user=os.environ.get('CDB_USER')
        db_port=os.environ.get('CDB_PORT')
        db_name=os.environ.get('CDB_NAME')
        db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
        db_connection = create_engine(db_connection_str)
        try:
            df1 = read_sql(two_join_qry, con=db_connection)
        except:
            df1=DataFrame()
        db_connection=db_connection.dispose()
        if df1.shape[0] > 0:
            return 'Success', list(df1.columns)
        else:
            return 'Error', []
    else:
        temp_str=""
        d_stat = False
        for i in sql_qry:
            
            if type(i) is dict:
                # print(sql_qry)
                # print(f"{i['table_names']}")
                if i['table_names'][0].find('/') > -1 and temp_str!="":                   
                    left_tables = i['table_names'][0].split('/')
                    left_table = ""
                    for t in left_tables:
                        stats = check_column_available(i['join_on'][0],t.strip())
                        if stats:
                            left_table = t.strip()
                            break
                
                    right_table = i['table_names'][1]

                    value_left=i['join_on'][0]# check this value in both tables
                    value_right=i['join_on'][1]

                    join_on = i['join']
                    
                    two_join_qry = f" {join_on} JOIN {right_table} ON {right_table}.{value_right} = {left_table}.{value_left}"
                    temp_str = temp_str + two_join_qry
                    
                else:
                    left_table = i['table_names'][0]
                    right_table = i['table_names'][1]

                    value_left=i['join_on'][0]
                    value_right=i['join_on'][1]

                    join_on = i['join']

                    two_join_qry = f"SELECT * FROM {left_table} {join_on} JOIN {right_table} ON {right_table}.{value_right} = {left_table}.{value_left}"
                    temp_str=temp_str+two_join_qry
                
                if type(i) is dict:
                    if d['table_names'] == i['table_names']:
                        d_stat = True
        
        
        if d_stat is False:
            # temp_dfs.append(get_joined_table(d,temp_dfs[-1]))
            left_tables = d['table_names'][0].split('/')
            left_table = ""
            for t in left_tables:
                stats = check_column_available(d['join_on'][0],t.strip())
                if stats:
                    left_table = t.strip()
                    break
            # left_table = d['table_names'][0]
            right_table = d['table_names'][1]

            value_left=d['join_on'][0]
            value_right=d['join_on'][1]

            join_on = d['join']
            two_join_qry = f" {join_on} JOIN {right_table} ON {right_table}.{value_right} = {left_table}.{value_left}"
            temp_str = temp_str + two_join_qry

        temp_str=temp_str + ' LIMIT 2;'
        
        host=os.environ.get('CDB_HOST')
        if host == 'windows':
            host = os.environ['DOCKER_HOST_IP']

        db_address=host #for linux enter host ip
        pwd=os.environ.get('CDB_PASS')
        db_user=os.environ.get('CDB_USER')
        db_port=os.environ.get('CDB_PORT')
        db_name=os.environ.get('CDB_NAME')
        db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
        db_connection = create_engine(db_connection_str)
        try:
            df1 = read_sql(temp_str, con=db_connection)
        except:
            df1=DataFrame()
        db_connection = db_connection.dispose()
        # print(f"TEMP STR {temp_str}")
        if df1.shape[0] > 0:
            return 'Success', list(df1.columns)
        else:
            return 'Error', []


def get_table_from_sql_query(sql_qry,rel_tables):
    # for single table.
    if type(sql_qry) is str:
        df,rows,download_data = get_table_from_db(sql_qry)
        return df.head(),rows,download_data

    #for multiple tables.
    elif type(sql_qry) is list:

        host=os.environ.get('CDB_HOST')
        if host == 'windows':
            host = os.environ['DOCKER_HOST_IP']

        db_address=host #for linux enter host ip
        pwd=os.environ.get('CDB_PASS')
        db_user=os.environ.get('CDB_USER')
        db_port=os.environ.get('CDB_PORT')
        db_name=os.environ.get('CDB_NAME')
        db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
        db_connection = create_engine(db_connection_str)
        main_query = sql_qry[0]

        
        main_query=main_query.replace(';',' LIMIT 5;')
        try:
            df1 = read_sql(main_query, con=db_connection)
            rows = read_sql(main_query.replace(re.findall('SELECT.*FROM',main_query)[0],"SELECT COUNT(*) FROM"),con=db_connection)['COUNT(*)'][0]
        except:
            df1=DataFrame()
            rows=0
        db_connection = db_connection.dispose()

        # print(f"MAIN QUERY{df1.columns}")

        # changing the datatypes to show in Dash Datatable.
        if df1.empty is False:
            for col in df1.columns:
                stat=False
                for i in rel_tables:
                    c = col.split('___')[0] # changing the column name to original.
                    stat = get_column_datatype(c,i)
                    # if stat is not False:
                    #     break
                    if stat is not False:
                        if ('datetime','datetime2','smalldatetime','date','time','datetimeoffset','timestamp') in stat:
                            df1[col] = to_datetime(df1[col], infer_datetime_format=True)
                            break

                        if ('money','smallmoney','float','decimal','numeric') in stat:
                            df1[col] = df1[col].fillna(0)
                            df1[col] = df1[col].astype(float)
                            break

                        if ('tinyint','smallint','int','bigint') in stat:
                            df1[col] = df1[col].fillna(0)
                            df1[col] = df1[col].astype(int)
                            break

                        if 'bit' in stat:
                            df1[col]=df1[col].apply(lambda k: int.from_bytes(k,byteorder='big',signed=False))
                            break
                    
    
        download_data = {
            "sql_qry":sql_qry,
            'filter_condi':None,
            "col_replace":None,
            "col_select":None,
            'filter_index':None,

        }

        if df1.shape[0] > 0:
            return df1.head(),rows,download_data
        else:
            return DataFrame(), None, {}


# returns columnms dtypes
def get_columns_dtypes(itms):
    x=[]
    for i,j in itms:
        if str(j) == 'float64':
            j = 'f'
        elif str(j) == 'object':
            j = 'o'
        elif str(j) == 'int64':
            j='i'
        elif str(j) == 'bool':
            j='b'
        elif str(j) == 'datetime64[ns]' or str(j) == 'datetime64':
            j='dt'
        elif str(j) == 'timedelta64[ns]':
            j='td'
        elif str(j) == 'category':
            j='c'
        x.append(str(j)+'    '+str(i))
    return x

def check_new_col_present(fil_dict,add_new_col):
    for i in range(len(fil_dict['index'])):
        col = fil_dict['columns'][i]
        if col.find('___') > -1:#check for repeated columns
            col = fil_dict['columns'][i].split('___')[0] # changing the column name to original.
        
        if list(add_new_col.keys()) != []:
            key=list(add_new_col.keys())[0]
            try:
                if add_new_col[str(key)]['col_names'] !=[]:
                    if all(add_new_col[str(key)]['col_names']) and add_new_col[str(key)]['col_names'] != []:
                        return True
            except:
                if add_new_col[int(key)]['col_names'] !=[]:
                    if all(add_new_col[int(key)]['col_names']) and add_new_col[int(key)]['col_names'] != []:
                        return True
        else:
            return False
def get_filtered_data(fil_dict,table_order,add_new_col):
    # print(f"GET_FILTERED_DATA {fil_dict}")
    pds_list = []
       
    add_new_column_present = check_new_col_present(fil_dict,add_new_col)
    for i in range(len(fil_dict['index'])):
        left_table=""
        col = fil_dict['columns'][i]
        tab = None
     
        if col.find('___') > -1:#check for repeated columns
            col = fil_dict['columns'][i].split('___')[0] # changing the column name to original.
            tab = fil_dict['columns'][i].split('___')[1] # table name.
        
        add_col_qry=None
        if list(add_new_col.keys()) != []:
            key=list(add_new_col.keys())[0]
            try:
                if add_new_col[str(key)]['col_names'] !=[]:
                    if col in add_new_col[str(key)]['col_names']:
                        add_col_qry = f"new_table.{col}"
                        # add_new_column_present = True
            except:
                if add_new_col[int(key)]['col_names'] !=[]:
                    if col in add_new_col[int(key)]['col_names']:
                        add_col_qry = f"new_table.{col}"
                        # add_new_column_present = True

        if add_col_qry is not None:
            left_table = add_col_qry

        elif tab is not None:
            stats = check_column_available(col,tab)
            if stats:
                if add_new_column_present:
                    left_table = "new_table"+'.'+col
                else:
                    left_table = tab+'.'+col
        else:
            for t in table_order:
                stats = check_column_available(col,t.strip())
                if stats:
                    if add_new_column_present:
                        left_table = "new_table"+'.'+col
                    else:
                        left_table = t.strip()+'.'+col
                    break


        
        if fil_dict['condition'][i] == 'is missing':# IS NULL
            # pds_list.append(df1[fil_dict['columns'][i]].isna())
            
            pds_list.append(left_table+' IS NULL')
        
        elif fil_dict['condition'][i] == 'is not missing':# IS NOT NULL
            # pds_list.append(~df1[fil_dict['columns'][i]].isna())
            pds_list.append(left_table+' IS NOT NULL')
            
        elif fil_dict['condition'][i] == 'has value(s)':# col IN (val1,val2)
            # pds_list.append(df1[fil_dict['columns'][i]].isin(fil_dict['values'][i]))#str inputs
            str_input = str(tuple(fil_dict['values'][i]))
            str_input = str_input.replace(",)",')')
            # if re.findall('\'',str_input) != []:
            #     str_input = str_input.replace('\'','')
            # else:
            #     str_input = str_input.replace('\"','')

            pds_list.append(left_table+' IN '+str_input)
            
        elif fil_dict['condition'][i] == 'starts with':# LIKE 'value%';
            # pds_list.append(df1[fil_dict['columns'][i]].str.startswith(fil_dict['values'][i]))#str input

            pds_list.append(left_table+' LIKE '+"'"+fil_dict['values'][i]+"%'")
        
        elif fil_dict['condition'][i] == 'ends with':# LIKE '%value';
            # pds_list.append(df1[fil_dict['columns'][i]].str.endswith(fil_dict['values'][i])) #str input
            pds_list.append(left_table+' LIKE '+"'%"+fil_dict['values'][i]+"'")
        
        elif fil_dict['condition'][i] == 'contains':# LIKE '%value%';
            # pds_list.append(df1[fil_dict['columns'][i]].str.contains(fil_dict['values'][i])) #str input
            pds_list.append(left_table+' LIKE '+"'%"+fil_dict['values'][i]+"%'")
        
        elif fil_dict['condition'][i] == '<':# col < value
            # pds_list.append(df1[fil_dict['columns'][i]] < int(fil_dict['values'][i])) #int input
            pds_list.append(left_table+' < '+str(int(fil_dict['values'][i])))
        
        elif fil_dict['condition'][i] == '<=':# col <= value
            # pds_list.append(df1[fil_dict['columns'][i]] <= int(fil_dict['values'][i])) #int input
            pds_list.append(left_table+' <= '+str(int(fil_dict['values'][i])))
        
        elif fil_dict['condition'][i] == '==':# col = value
            # pds_list.append(df1[fil_dict['columns'][i]] == int(fil_dict['values'][i])) #int input
            pds_list.append(left_table+' = '+str(int(fil_dict['values'][i])))

        
        elif fil_dict['condition'][i] == '>':# col > val
            # pds_list.append(df1[fil_dict['columns'][i]] > int(fil_dict['values'][i])) #int input
            pds_list.append(left_table+' > '+str(int(fil_dict['values'][i])))
        
        elif fil_dict['condition'][i] == '>=':# col >= val
            # pds_list.append(df1[fil_dict['columns'][i]] >= int(fil_dict['values'][i])) #int input
            pds_list.append(left_table+' >= '+str(int(fil_dict['values'][i])))
            
        elif fil_dict['condition'][i] == '!=':# col != val
            # pds_list.append(df1[fil_dict['columns'][i]] != int(fil_dict['values'][i])) #int input
            pds_list.append(left_table+' != '+str(int(fil_dict['values'][i])))
        
        elif fil_dict['condition'][i] == 'days':
            x = fil_dict['values'][i][1]
            y = fil_dict['values'][i][0]
            if type(x) is list:
                x = to_datetime(date.today())
                y = x + timedelta(int(y))
            else:
                x = to_datetime(x)
                y = x + timedelta(int(y))

            max_dt = max(x,y)
            min_dt = min(x,y)
            
            if x == y:
                # pds_list.append((df1[fil_dict['columns'][i]] == y))
                pds_list.append(left_table+' = '+"'"+str(y)+"'")
            elif y == min_dt:
                # pds_list.append((df1[fil_dict['columns'][i]] >= min_dt) &  (df1[fil_dict['columns'][i]] < max_dt))
                pds_list.append(f"({left_table} >= '{min_dt}' AND {left_table} < '{max_dt}')")
            else:
                # pds_list.append((df1[fil_dict['columns'][i]] > min_dt) &  (df1[fil_dict['columns'][i]] <= max_dt))
                pds_list.append(f"({left_table} > '{min_dt}' AND {left_table} <= '{max_dt}')")
        
        elif fil_dict['condition'][i] == 'before':
            x = to_datetime(fil_dict['values'][i])
            # pds_list.append(df1[fil_dict['columns'][i]] < x)
            pds_list.append(left_table+' < '+"'"+str(x)+"'")
        
        elif fil_dict['condition'][i] == 'after':
            x = to_datetime(fil_dict['values'][i])
            # pds_list.append(df1[fil_dict['columns'][i]] > x)
            pds_list.append(left_table+' > '+"'"+str(x)+"'")
        
        elif fil_dict['condition'][i] == 'equals':
            x = to_datetime(fil_dict['values'][i])
            # pds_list.append(df1[fil_dict['columns'][i]] == x)
            pds_list.append(left_table+' = '+"'"+str(x)+"'")
        
        elif fil_dict['condition'][i] == 'not':
            x = to_datetime(fil_dict['values'][i])
            # pds_list.append(df1[fil_dict['columns'][i]] != x)
            pds_list.append(left_table+' != '+"'"+str(x)+"'")

        elif fil_dict['condition'][i] == 'range':
            x = to_datetime(fil_dict['values'][i][0])
            y = to_datetime(fil_dict['values'][i][1])
            max_dt = max(x,y)
            min_dt = min(x,y)
            # pds_list.append((df1[fil_dict['columns'][i]] >= min_dt) & (df1[fil_dict['columns'][i]] <= max_dt))
            pds_list.append(f"({left_table} >= '{str(min_dt)}' AND {left_table} <= '{str(max_dt)}')")
        
    condi=None
    for ele in range(0, len(pds_list)):
        if condi is None:
            condi = pds_list[ele]
        else:
            if ele != 0:
                if fil_dict['logic'][ele] == 'And':
                    # condi = op.and_(condi,pds_list[ele])
                    condi = condi + ' AND '+pds_list[ele]
                elif fil_dict['logic'][ele] == 'Or':
                    # condi = op.or_(condi,pds_list[ele])
                    condi = condi + ' OR '+pds_list[ele]

    if fil_dict['select_drop'] == 'Drop' and condi is not None:
        condi = ' WHERE NOT '+condi
        return condi
    elif condi is not None:
        condi = ' WHERE '+condi
        return condi
    else:
        return None


# Returns given column values to filters modal dropdown.
def get_column_values(relationship,add_new_col,column_name):

    add_col_qry=None
    if add_new_col['add_col_names'] !=[]:
        if column_name in add_new_col['add_col_names']:
            try:
                add_col = add_new_col['add_col_qry']
                col_query= ", "+ str(add_col) + " FROM"
                if type(relationship) is str:
                    add_col_qry = f"SELECT *{col_query} {relationship}"
                elif type(relationship) is list:
                    add_col_qry = relationship[0].replace("FROM",col_query)
                    add_col_qry = add_col_qry.replace(';',"")
            except Exception as e:
                print(e)
            

    if type(relationship) is str:
        c = column_name.split('___')[0] # changing the column name to original.
 
        #f'SELECT DISTINCT(new_column) AS new_col FROM (SELECT * , "primary" AS new_column FROM tblcalldatamaster) AS new_table;'
        stat=False
        if add_col_qry is not None:
            single_qry = f"SELECT DISTINCT({c}) AS {column_name} FROM ({add_col_qry}) AS new_table;"
        else:
            single_qry = f"SELECT DISTINCT({c}) AS {column_name} FROM {relationship};"
            stat = get_column_datatype(c,relationship)
                
        host=os.environ.get('CDB_HOST')
        if host == 'windows':
            host = os.environ['DOCKER_HOST_IP']

        db_address=host #for linux enter host ip
        pwd=os.environ.get('CDB_PASS')
        db_user=os.environ.get('CDB_USER')
        db_port=os.environ.get('CDB_PORT')
        db_name=os.environ.get('CDB_NAME')
        db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
        db_connection = create_engine(db_connection_str)
        try:
            df1 = read_sql(single_qry, con=db_connection)
        except:
            df1=DataFrame()
        db_connection=db_connection.dispose()
        
        if df1.empty is False:
            if stat is not False:
                if ('datetime','datetime2','smalldatetime','date','time','datetimeoffset','timestamp') in stat:
                    df1[column_name] = to_datetime(df1[column_name], infer_datetime_format=True)

                if ('money','smallmoney','float','decimal','numeric') in stat:
                    df1[column_name] = df1[column_name].fillna(0)
                    df1[column_name] = df1[column_name].astype(float)

                if ('tinyint','smallint','int','bigint') in stat:
                    df1[column_name] = df1[column_name].fillna(0)
                    df1[column_name] = df1[column_name].astype(int)

                if 'bit' in stat:
                    df1[column_name]=df1[column_name].apply(lambda k: int.from_bytes(k,byteorder='big'))
            return df1[column_name]
        else:
            return DataFrame()
    elif type(relationship) is list:
        left_table=""
        col = column_name
        tab = None
        if col.find('___') > -1:#check for repeated columns
            col = column_name.split('___')[0] # changing the column name to original.
            tab = column_name.split('___')[1] # table name.
        
        stat=False
        if add_col_qry is not None:
            left_table = f"new_table.{col}"
        else:
            if tab is not None:
                stats = check_column_available(col,tab)
                if stats:
                    left_table = tab+'.'+col
            else:
                for t in relationship[1]:
                    stats = check_column_available(col,t.strip())
                    if stats:
                        left_table = t.strip()+'.'+col
                        tab=t.strip()
                        break
            stat = get_column_datatype(col,tab)


        main_query = relationship[0]
        
        if add_col_qry is not None:
            main_query = f"SELECT DISTINCT({left_table}) AS {column_name} FROM ({add_col_qry}) AS new_table;"
        else:
            main_query = main_query.replace(re.findall("SELECT.*FROM",main_query)[0],f"SELECT DISTINCT({left_table}) AS {column_name} FROM")
        # c = column_name.split('___')[0] # changing the column name to original.
        # for i in relationship[1]:
        
        # if stat is not False:
        #     break

        host=os.environ.get('CDB_HOST')
        if host == 'windows':
            host = os.environ['DOCKER_HOST_IP']

        db_address=host #for linux enter host ip
        pwd=os.environ.get('CDB_PASS')
        db_user=os.environ.get('CDB_USER')
        db_port=os.environ.get('CDB_PORT')
        db_name=os.environ.get('CDB_NAME')
        db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
        db_connection = create_engine(db_connection_str)
        
        # main_query=main_query.replace('SELECT *',f'SELECT DISTINCT({column_name})')
        try:
            df1 = read_sql(main_query, con=db_connection)
        except:
            df1=DataFrame()
        db_connection = db_connection.dispose()
    
        if df1.empty is False:
            if stat is not False:
                if ('datetime','datetime2','smalldatetime','date','time','datetimeoffset','timestamp') in stat:
                    df1[column_name] = to_datetime(df1[column_name], infer_datetime_format=True)

                if ('money','smallmoney','float','decimal','numeric') in stat:
                    df1[column_name] = df1[column_name].fillna(0)
                    df1[column_name] = df1[column_name].astype(float)

                if ('tinyint','smallint','int','bigint') in stat:
                    df1[column_name] = df1[column_name].fillna(0)
                    df1[column_name] = df1[column_name].astype(int)

                if 'bit' in stat:
                    df1[column_name]=df1[column_name].apply(lambda k: int.from_bytes(k,byteorder='big'))
            return df1[column_name]
        else:
            return DataFrame()


def get_transformations(relationship_data,filters_data,col):
    
    
    # print(f"relationship {relationship_data}")

    
    # print(filters_data['filters'].keys())
    # if filters_data['select_or_drop_columns'] != {}:
    if type(relationship_data['table']) is list:
        table_name = relationship_data['table'][0]
    else:
        table_name = f"SELECT * FROM {relationship_data['table']};"

    # print(f"{table_name}",flush=True)
    table_order = relationship_data['table_order']
    columns_to_select=[]
    SQL_QRY = []
    # df1 = get_full_table_from_sql_query(table_name,None)
    sel_drp_sele = False
    fil_sele = False
    sel_col_list = []
    add_new_col_key = None
    for i in range(1,int(filters_data['index_k'])+1):
        sel_keys = filters_data['add_new_col'].keys()
        fil_keys = filters_data['filters'].keys()
        if str(i) in sel_keys or int(i) in sel_keys:
            
            try:
                sel_qry = filters_data['add_new_col'][str(i)]['query']
                sel_col = filters_data['add_new_col'][str(i)]['col_names']
            except:
                sel_qry = filters_data['add_new_col'][i]['query']
                sel_col = filters_data['add_new_col'][i]['col_names']

            if sel_qry is not None and sel_qry != "":
                sel_qry = [sel_qry]
                sel_col_list=sel_col
            sel_drp_sele = True
            SQL_QRY.append(sel_qry)

        elif str(i) in fil_keys or int(i) in fil_keys:
            try:
                condi = get_filtered_data(filters_data['filters'][int(i)],table_order,filters_data['add_new_col'])
            except:
                condi = get_filtered_data(filters_data['filters'][str(i)],table_order,filters_data['add_new_col'])

            fil_sele = True
            SQL_QRY.append(condi)

    # print(SQL_QRY,flush=True)
        
    condi=None
    columns_select = []
    for ele in SQL_QRY:
        if type(ele) is str:
            if condi is None:
                condi = ele
            else:
                condi = condi + ' AND '+ele
        elif type(ele) is list:
            columns_select.append(ele)

    
    add_col_query=None
    if columns_select != []:
        ''''
        SELECT head_code FROM (SELECT main_join_code) as new_table where new_table.colname ...
        '''
        #head_code
        table_name_copy = re.sub('(\w+\.\w+)(?= AS)\ AS\ ','',table_name)
        if table_name_copy.find('*') < 0:
            table_name_copy = re.sub('FROM.*',","+",".join(["new_table."+str(x) for x in sel_col_list])+" FROM",table_name_copy)
        else:
            table_name_copy = re.sub('FROM.*',"FROM",table_name_copy)
        # table_name_copy = table_name_copy.replace("FROM",)

        #(SELECT main_join_code)
        columns_select_1 = [j for sub in columns_select for j in sub]
        col_query = ", "+ str(columns_select_1[0]) + " FROM"
        table_name_copy_main = table_name.replace('FROM',col_query)
        table_name_copy_main = table_name_copy_main.replace(';','')
        
        #as new_table
        table_name_copy_main = '('+table_name_copy_main+') AS new_table;'

        add_col_query = table_name_copy.replace('FROM','FROM '+table_name_copy_main)

        # add_col_query = table_name.replace(re.findall("SELECT.*FROM",table_name)[0],f"SELECT *{col_query}")
        # print(add_col_query)


    if add_col_query is not None:
        table_name = add_col_query

    # condi contains the where clause or the filter condition
    if condi is not None:
        filter_query = table_name.replace(';',condi+';')
    else:
        filter_query = table_name
    # print(f"MAIN ma {filter_query}",flush=True)
    
    # creating conditional columns.
    # if columns_select != []:
    #     columns_select_1= [j for sub in columns_select for j in sub]
    #     col_query = ", "+ str(columns_select_1[0]) + " FROM"
    #     filter_query=filter_query.replace("FROM",col_query)
    #     print(filter_query)   

    host=os.environ.get('CDB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('CDB_PASS')
    db_user=os.environ.get('CDB_USER')
    db_port=os.environ.get('CDB_PORT')
    db_name=os.environ.get('CDB_NAME')
    db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
    db_connection = create_engine(db_connection_str)
    main_query = filter_query
    
    main_query=main_query.replace(';',' LIMIT 5;')
    try:
        df1 = read_sql(main_query, con=db_connection)
        if add_col_query is not None:
            rows = read_sql(re.sub('SELECT.*FROM\ \(',"SELECT COUNT(*) FROM (",main_query),con=db_connection)['COUNT(*)'][0]
            # rows = read_sql(main_query.replace(re.findall('SELECT.*FROM',main_query)[0],),con=db_connection)['COUNT(*)'][0]
        else:
            rows = read_sql(main_query.replace(re.findall('SELECT.*FROM',main_query)[0],"SELECT COUNT(*) FROM"),con=db_connection)['COUNT(*)'][0]
    except:
        df1=DataFrame()
        rows=0
    db_connection = db_connection.dispose()

    # changing the mysql datatype to pandas datatype for easy plotting in the table.
    if df1.empty is False:
        for colm in df1.columns:
            stat=False
            for i in table_order:
                if i is not None:
                    c = colm.split('___')[0] # changing the column name to original.
                    stat = get_column_datatype(c,i)
                    # if stat is not False:
                    #     break
                    if stat is not False:
                        if ('datetime','datetime2','smalldatetime','date','time','datetimeoffset','timestamp') in stat:
                            df1[colm] = to_datetime(df1[colm], infer_datetime_format=True)
                            break

                        if ('money','smallmoney','float','decimal','numeric') in stat:
                            df1[colm] = df1[colm].fillna(0)
                            df1[colm] = df1[colm].astype(float)
                            break

                        if ('tinyint','smallint','int','bigint') in stat:
                            df1[colm] = df1[colm].fillna(0)
                            df1[colm] = df1[colm].astype(int)
                            break

                        if 'bit' in stat:
                            df1[colm]=df1[colm].apply(lambda k: int.from_bytes(k,byteorder='big',signed=False))
                            break

    # columns_select_1= [j for sub in columns_select for j in sub]
    # columns_select = set(columns_select_1)
    # print(main_query,flush=True)
    # print(rows,flush=True)
    filters_condition = {
        "SQL_QRY":filter_query,
        "filter_index":None,
        # "selected_columns":list(columns_select)
    }

    download_data = {
        "sql_qry":table_name,
        'filter_condi':filters_condition,
        "col_replace":col,
        "col_select":None,
    }
    return df1.head(),filters_condition,rows, download_data


def get_format_mapping(relation_data,format_data,fil_condi,col):
    # print(fil_condi)
    if type(relation_data['table']) is list:
        table_name = relation_data['table'][0]
    else:
        table_name = f"SELECT * FROM {relation_data['table']};"

    # table_name = relation_data['table']

    if format_data['column_names'] != []:
        colm_nms = format_data['column_names']

        # df1 = get_full_table_from_sql_query(table_name, None)
        download_data = {
            "sql_qry":table_name,
            'filter_condi':fil_condi,
            "col_replace":col,
            "col_select":colm_nms,
        }

        # print(fil_condi)
        host=os.environ.get('CDB_HOST')
        if host == 'windows':
            host = os.environ['DOCKER_HOST_IP']

        db_address=host #for linux enter host ip
        pwd=os.environ.get('CDB_PASS')
        db_user=os.environ.get('CDB_USER')
        db_port=os.environ.get('CDB_PORT')
        db_name=os.environ.get('CDB_NAME')
        db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
        db_connection = create_engine(db_connection_str)
        if fil_condi is not None:
            main_query = fil_condi['SQL_QRY']
            # columns_select=fil_condi['selected_columns']
        else:
            main_query = table_name
            # columns_select=[]
        # print(f"GLOBAL FUNC {main_query}")
        main_query=main_query.replace(';',' LIMIT 5;')
        try:
            df1 = read_sql(main_query, con=db_connection)
            # rows = read_sql(main_query.replace(re.findall('SELECT.*FROM',main_query)[0],"SELECT COUNT(*) FROM"),con=db_connection)['COUNT(*)'][0]
        except:
            df1=DataFrame()
            # rows=0
        db_connection = db_connection.dispose()

        if df1.empty is False:
            for col in df1.columns:
                stat=False
                for i in relation_data['table_order']:
                    c = col.split('___')[0] # changing the column name to original.
                    stat = get_column_datatype(c,i)
                    # if stat is not False:
                    #     break
                    if stat is not False:
                        if ('datetime','datetime2','smalldatetime','date','time','datetimeoffset','timestamp') in stat:
                            df1[col] = to_datetime(df1[col], infer_datetime_format=True)
                            break

                        if ('money','smallmoney','float','decimal','numeric') in stat:
                            df1[col] = df1[col].fillna(0)
                            df1[col] = df1[col].astype(float)
                            break

                        if ('tinyint','smallint','int','bigint') in stat:
                            df1[col] = df1[col].fillna(0)
                            df1[col] = df1[col].astype(int)
                            break

                        if 'bit' in stat:
                            df1[col]=df1[col].apply(lambda k: int.from_bytes(k,byteorder='big',signed=False))
                            break

        
        # if fil_condi is not None:
        #     condi=None
        #     columns_select = []
        #     for ele in fil_condi['SQL_QRY']:
        #         if type(ele) is Series or type(ele[0]) is bool:
        #             if condi is None:
        #                 condi = Series(ele,index=fil_condi['filter_index'])
        #             else:
        #                 condi = op.and_(condi,Series(ele,index=fil_condi['filter_index']))
        #         elif type(ele) is list and type(ele[0]) is str:
        #             columns_select.append(ele)
            
        #     columns_select_1= [j for sub in columns_select for j in sub]
        #     columns_select = set(columns_select_1)

            # if condi is not None:
            #     df1=df1[condi]
        # if list(columns_select) != []:
            # df1=df1[list(columns_select)] #select or drop filter applied
        
        
        # sys.stderr.write(str(df1.columns))
        # sys.stderr.write(str(colm_nms))
        # print(df1.columns,flush=True)
        # print(colm_nms,flush=True)
        formt_colms = list(set(colm_nms))

        df1=df1[formt_colms].head()
        return df1, download_data
    else:
        return None, None
        
# returns column names
def get_columns(table_name):
    # db_addre`s`s=os.environ['DOCKER_HOST_IP'] #for windows machine
    host=os.environ.get('CDB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('CDB_PASS')
    db_user=os.environ.get('CDB_USER')
    db_port=os.environ.get('CDB_PORT')
    db_name=os.environ.get('CDB_NAME')
    db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
    db_connection = create_engine(db_connection_str)
    df1 = read_sql(f'SELECT * FROM {table_name} LIMIT 1', con=db_connection)
    db_connection=db_connection.dispose()
    return df1.columns

# for single table selection without joins.
def get_table_from_db(table_name):
    '''
    Returns a single table dataframe, which accepts a table name as argument.
    '''
    # db_addre`s`s=os.environ['DOCKER_HOST_IP'] #for windows machine
    # print(os.environ.get('CDB_HOST'))
    host=os.environ.get('CDB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('CDB_PASS')
    db_user=os.environ.get('CDB_USER')
    db_port=os.environ.get('CDB_PORT')
    db_name=os.environ.get('CDB_NAME')
    db_connection_str = f"mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}"
    # print(db_connection_str)
    # print(pwd)
    # print(type(pwd))
    db_connection = create_engine(db_connection_str)
    sql_qry = f'SELECT * FROM {table_name}'
    df1 = read_sql(f'SELECT * FROM {table_name} LIMIT 5;', con=db_connection)
    rows = read_sql(f"SELECT COUNT(*) FROM {table_name}",con=db_connection)['COUNT(*)'][0]

    df3 = read_sql(f'DESC {table_name};',con=db_connection)

    # print(f"db {df1.shape}")
    # print(list(df3['Type']))

    bit_types = df3[df3['Type'].str.startswith('bit')]['Field']

    numeric_types = df3[df3['Type'].str.startswith(('tinyint','smallint','int',\
        'bigint'))]['Field']
    
    float_types = df3[df3['Type'].str.startswith(('money','smallmoney','float',\
        'decimal','numeric'))]['Field']

    datetime_types = df3[df3['Type'].str.startswith(('datetime','datetime2',\
        'smalldatetime','date','time','datetimeoffset','timestamp'))]['Field']

    # print("dataframe initalization")

    if datetime_types.empty is False:
        for i in datetime_types:
            df1[i] = to_datetime(df1[i], infer_datetime_format=True)

    if float_types.empty is False:
        for i in float_types:
            df1[i] = df1[i].fillna(0)
            df1[i] = df1[i].astype(float)

    if numeric_types.empty is False:
        for i in numeric_types:
            df1[i] = df1[i].fillna(0)
            df1[i] = df1[i].astype(int)
    
    if bit_types.empty is False:
        for i in bit_types:
            df1[i]=df1[i].apply(lambda k: int.from_bytes(k,byteorder='big'))

    # print("value conversion done")

    download_data = {
        "sql_qry":[table_name],
        'filter_condi':None,
        "col_replace":None,
        "col_select":None,
    }
    # print("inside get_table_from_db")

    return df1, rows, download_data

#check column in query
def get_bool_on_col(download_data,columns_list):
    '''
    This function returns the table which appears on format mapping tab as excel.
    this function accepts **download_data** a dict variable which as all the data about
    the table relation, applied filters and format mapped.
    '''
    if type(download_data['sql_qry']) is list:
        table_name = download_data['sql_qry'][0]
    else:
        table_name = f"SELECT * FROM {download_data['sql_qry']};"

    host=os.environ.get('CDB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('CDB_PASS')
    db_user=os.environ.get('CDB_USER')
    db_port=os.environ.get('CDB_PORT')
    db_name=os.environ.get('CDB_NAME')
    db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
    db_connection = create_engine(db_connection_str)
    
    if download_data['filter_condi'] is not None:   
        main_query = download_data['filter_condi']['SQL_QRY']
        # columns_select=download_data['filter_condi']['selected_columns']
    else:
        main_query = table_name
        # columns_select=[]
    main_query=main_query.replace(';',' LIMIT 5;')
    try:
        df1 = read_sql(main_query, con=db_connection)
        # rows = read_sql(main_query.replace(re.findall('SELECT.*FROM',main_query)[0],"SELECT COUNT(*) FROM"),con=db_connection)['COUNT(*)'][0]
    except:
        df1=DataFrame()
        # rows=0
    db_connection = db_connection.dispose()

    val = 0
    err_list=[]
    err_loc=[]
    if df1.empty is False:
        for loc,i in enumerate(columns_list):
            if i in df1.columns:
                val+=1
            else:
                err_list.append(i)
                err_loc.append(loc)

    
    if len(columns_list) == val:
        return True,[],[]
    else:
        return False,err_list,err_loc

    
    # if download_data['col_select'] is not None:
    #     df1=df1[download_data['col_select']]
    
    # if download_data['col_replace'] != {} and download_data['col_replace'] is not None:
    #     def to_xlsx(bytes_io):
    #         xlsx_io = io.BytesIO()
    #         writer = ExcelWriter(bytes_io, engine='xlsxwriter')
            
    #         df1.rename(columns=download_data['col_replace']).to_excel(writer,index=False)
    #         writer.save()

    #     return send_bytes(to_xlsx, "some_name.xlsx")
    # else:
    #     def to_xlsx(bytes_io):
    #         xlsx_io = io.BytesIO()
    #         writer = ExcelWriter(bytes_io, engine='xlsxwriter')
            
    #         df1.to_excel(writer,index=False)
    #         writer.save()
            
    #     return send_bytes(to_xlsx, "some_name.xlsx")


# function to export the table as excel file.
def get_downloaded_data(download_data):
    '''
    This function returns the table which appears on format mapping tab as excel.
    this function accepts **download_data** a dict variable which as all the data about
    the table relation, applied filters and format mapped.
    '''
    if type(download_data['sql_qry']) is list:
        table_name = download_data['sql_qry'][0]
    else:
        table_name = f"SELECT * FROM {download_data['sql_qry']};"

    host=os.environ.get('CDB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('CDB_PASS')
    db_user=os.environ.get('CDB_USER')
    db_port=os.environ.get('CDB_PORT')
    db_name=os.environ.get('CDB_NAME')
    db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
    db_connection = create_engine(db_connection_str)
    
    if download_data['filter_condi'] is not None:   
        main_query = download_data['filter_condi']['SQL_QRY']
        # columns_select=download_data['filter_condi']['selected_columns']
    else:
        main_query = table_name
        # columns_select=[]
    
    try:
        df1 = read_sql(main_query, con=db_connection)
        # rows = read_sql(main_query.replace(re.findall('SELECT.*FROM',main_query)[0],"SELECT COUNT(*) FROM"),con=db_connection)['COUNT(*)'][0]
    except:
        df1=DataFrame()
        # rows=0
    db_connection = db_connection.dispose()

    # df1 = get_full_table_from_sql_query(download_data['sql_qry'], None)

    # if download_data['filter_condi'] is not None:
    #     condi = None
    #     columns_select = []

    #     for ele in download_data['filter_condi']['SQL_QRY']:
    #         if type(ele) is Series or type(ele[0]) is bool:
    #             if condi is None:
    #                 condi=Series(ele,index=download_data['filter_condi']['filter_index'])
    #             else:
    #                 condi=op.and_(condi,Series(ele,index=download_data['filter_condi']['filter_index']))
    #         elif type(ele) is list and type(ele[0]) is str:
    #             columns_select.append(ele)
        
    #     columns_select_1= [j for sub in columns_select for j in sub]
    #     columns_select = set(columns_select_1)
    #     # df1=df1[condi]
    #     # df1=df1[list(columns_select)]
    #     if condi is not None:
    #         df1=df1[condi]
    # if list(columns_select) != []:
    #     df1=df1[list(columns_select)]
        
    
    if download_data['col_select'] is not None:
        df1=df1[download_data['col_select']]
    
    if download_data['col_replace'] != {} and download_data['col_replace'] is not None:
        def to_xlsx(bytes_io):
            xlsx_io = io.BytesIO()
            writer = ExcelWriter(bytes_io, engine='xlsxwriter')
            
            df1.rename(columns=download_data['col_replace']).to_excel(writer,index=False)
            writer.save()

        return send_bytes(to_xlsx, "some_name.xlsx")
        # xlsx_io.seek(0)
        # # https://en.wikipedia.org/wiki/Data_URI_scheme
        # media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # data = base64.b64encode(xlsx_io.read()).decode("utf-8")
        # csv_string = f'data:{media_type};base64,{data}'
        # return csv_string
    else:
        def to_xlsx(bytes_io):
            xlsx_io = io.BytesIO()
            writer = ExcelWriter(bytes_io, engine='xlsxwriter')
            
            df1.to_excel(writer,index=False)
            writer.save()
            
        return send_bytes(to_xlsx, "some_name.xlsx")
        # xlsx_io.seek(0)
        # # https://en.wikipedia.org/wiki/Data_URI_scheme
        # media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # data = base64.b64encode(xlsx_io.read()).decode("utf-8")
        # csv_string = f'data:{media_type};base64,{data}'
        
        # return csv_string



# function to export the table as excel file.
def get_downloaded_data_to_folder(download_data,loc,file_name,sch_email):
    '''
    This function returns the table which appears on format mapping tab as excel.
    this function accepts **download_data** a dict variable which as all the data about
    the table relation, applied filters and format mapped.
    '''
    if type(download_data['sql_qry']) is list:
        table_name = download_data['sql_qry'][0]
    else:
        table_name = f"SELECT * FROM {download_data['sql_qry']};"

    host=os.environ.get('CDB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('CDB_PASS')
    db_user=os.environ.get('CDB_USER')
    db_port=os.environ.get('CDB_PORT')
    db_name=os.environ.get('CDB_NAME')
    db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
    db_connection = create_engine(db_connection_str)
    
    if download_data['filter_condi'] is not None:   
        main_query = download_data['filter_condi']['SQL_QRY']
        # columns_select=download_data['filter_condi']['selected_columns']
    else:
        main_query = table_name
        # columns_select=[]
    print(f"Main Query used to download data.\n{main_query}",flush=True)
    # print(,flush=True)
    try:
        df1 = read_sql(main_query, con=db_connection)
        # rows = read_sql(main_query.replace(re.findall('SELECT.*FROM',main_query)[0],"SELECT COUNT(*) FROM"),con=db_connection)['COUNT(*)'][0]
    except:
        df1=DataFrame()
        # rows=0
    db_connection = db_connection.dispose()

    # if list(columns_select) != []:
    #     df1=df1[list(columns_select)]
        
    # print(df1.shape)
    # print(type(download_data['col_replace']))
    # print(download_data['col_replace'])
    # print(os.path.join(loc,file_name))

    if download_data['col_select'] is not None:
        df1=df1[download_data['col_select']]
    
    if download_data['col_replace'] != {} and download_data['col_replace'] is not None:
        # xlsx_io = io.BytesIO()
        # writer = ExcelWriter(xlsx_io, engine='xlsxwriter')
        
        df1.rename(columns=download_data['col_replace']).to_excel(os.path.join(loc,file_name),index=False)
        send_email_with_attach(os.path.join(loc,file_name),sch_email)
        # writer.save()
        # xlsx_io.seek(0)
        # https://en.wikipedia.org/wiki/Data_URI_scheme
        # media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # data = base64.b64encode(xlsx_io.read()).decode("utf-8")
        # csv_string = f'data:{media_type};base64,{data}'
        # return csv_string
    else:
        # xlsx_io = io.BytesIO()
        # writer = ExcelWriter(xlsx_io, engine='xlsxwriter')
        
        df1.to_excel(os.path.join(loc,file_name),index=False)
        send_email_with_attach(os.path.join(loc,file_name),sch_email)
        # writer.save()
        # xlsx_io.seek(0)
        # # https://en.wikipedia.org/wiki/Data_URI_scheme
        # media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # data = base64.b64encode(xlsx_io.read()).decode("utf-8")
        # csv_string = f'data:{media_type};base64,{data}'
        
        # return csv_string


# send mail
def send_email_with_attach(filename,sch_email):
    import smtplib, ssl
    from email.mime.multipart import MIMEMultipart # for attachment
    from email.mime.text import MIMEText # html format
    from email.mime.application import MIMEApplication # for attachment

    
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587 
    #Replace with your own gmail account
    print(sch_email,flush=True)
    gmail = sch_email['from']
    password = sch_email['pass']

    message = MIMEMultipart('mixed')
    message['From'] = 'Contact <{sender}>'.format(sender = gmail)
    message['To'] = sch_email['to']
    message['CC'] = sch_email['cc']
    message['Subject'] = sch_email['sub']
    to=sch_email['to']
    cc=sch_email['cc']

    msg_content = sch_email['msg']
    msg_html_body = f'<!doctype html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head> <title></title> <meta http-equiv="X-UA-Compatible" content="IE=edge"> \
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> \
        <style type="text/css"> #outlook a{{padding: 0;}}.ReadMsgBody{{width: 100%;}}.ExternalClass{{width: 100%;}}.ExternalClass *{{line-height: 100%;}}body{{margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;}}table, td{{border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt;}}img{{border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}} \
        p{{display: block; margin: 13px 0;}}</style> <style type="text/css"> @media only screen and (max-width:480px){{@-ms-viewport{{width: 320px;}}@viewport{{width: 320px;}}}}</style> \
        <style type="text/css"> @media only screen and (min-width:480px){{.mj-column-per-100{{width: 100% !important;}}}}</style> <style type="text/css"> </style></head> \
        <body style="background-color:#f9f9f9;"> <div style="background-color:#f9f9f9;"> <div style="background:#f9f9f9;background-color:#f9f9f9;Margin:0px auto;max-width:600px;"> <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#f9f9f9;background-color:#f9f9f9;width:100%;"> \
        <tbody> <tr> <td style="border-bottom:#d81b1b solid 10px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;"> </td></tr></tbody> </table> </div><div style="background:#fff;background-color:#fff;Margin:0px auto;max-width:600px;"> <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#fff;background-color:#fff;width:100%;"> <tbody> <tr> <td style="border:#dddddd solid 1px;border-top:0px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;"> <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;"> <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:bottom;" width="100%"> <tr> <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;"> <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;"> <tbody> <tr> <td style="width:64px;"> <img height="auto" \
        src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAMAAACahl6sAAAA/1BMVEX///////3//v/4+fr9//0CGDje4eX9/v8fMkzEy9MAEjL+/fzy9Pfn6u4AFDUAEjSxucN9iJcMHjkADy65wMoOHjxpdYrt7/Wosr4wP1NOXHIrOlT98/Fnc4RcanuJkqLcNiYRJD0dMEfy2NOut75CUWXT2OAAEy9vfYwcKkP76+jturO6v8wOHTrjnpURJTvHzdLkqaKVnaXvycXQNijbhn7UbWPIOCoDGz/PRjpWXXY+S2HTX1JWZHfRKBoTJELKbmbNfnLDSz3IOCfdrqOdpK1GS1sXHTPSRDrXioXCUUAoLT58hY4uO0wAByT00c43SGbOYVjTlIrvuLXDRzUnbbqsAAAPIklEQVR4nO1bCZviRpJNHSmBUgcgUVwltHWAoGqwadp208OweMrG3e3pbttr///fMi9SBwK6yvbOfm7Vfvm+Kg6hFPkUkREvMhPGFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFP6fQhO6LjRrG/IMPpA/+dmR1N8lLtM0/XN39Wmgg7qmefG88Si6RMTUPndPfw/ooGYa0+ajiCadZ0GEERHTNgyb/o0q5EG7N342ROBfQpim0LSit1r+qGNkPCciYEJchImRLyEEHcUjnutPxC5f2KUpJA3bZoIO4Cj+MiIHa9UPggjIW3/gVMA0YQIbrlVYpL5Mcvd5AjjhQERndSXCdC8i/C1DdIalq1WI2PUlwqLNfDRqjE5BORAP87HFngmR2+tCl5zD98Ph8yHScLqLTFWV4NxxfMfhfJ3Wn0jRoVYj4J35tUQprLI3u/XaqT0RrULEbyTRLdCqgN5t+doHEXlmbYmUICKjiNkHgSVf0kO7y0+J6LXL7XZRWLQavjOIZG/LTpqaiQzD2gvu1J+ImSfpgoiWJXYbtsFnpgmN0u48AyKl2mg1nHTQhBoRFYUCFoLZ7+tPxBSGa5iyU5JIRG4l7m4KXOrkXu8X9R4j6LJm3M5aBp41IkKuZTJ2ef/tNxn+eSNgMCISnBKpUdRCDwXrxW/abk4kICLM1i6/ePVVhoeXKEs0u12xiFuo38/d/QOkaO/FnQMRGiO6JPJfGX57ieoKRLqHMVJDIrIz7gURYVUi7EDk4RkRySwiDkTMYyIayvf6E9Fzi1BV9QeJeCBi1I7IwbWOiXxXda1zIjWziEyEPUlEL6JWE6mlQuQ1iJglEckkL3VrxKNKRMssQuEX0uoo/NoHi1AbWOSNVL/1gV4lIkoiTDOPEqJuVl1LY24y7Bso3+sziX1K5DYXjZCJFYkiNEiUikVMw5t6Qug1yuznRDKtBSKHkyhmMbtCRCOnAhFWGx6PEkFKBBnqqCCJb9qSSJgTgWQRpIk/d+8r+CSRppyqrsCkUw9E6jjFeESEZURQ6qK4NY+WEgCIRppFkS4nW9WKzSkRyHjeSFq3GYqZB4ltNkaysaNprF758Dz8OpxfHePLDJ31Oihcq374xBjha56mKefpYRkUL/Cfz2vVE2dErkMQeQTpx1oTgdIoiGgsmpzPYJcYXMfPgwgSn7esrN0uJaqruVPjc3f4MZBrVYjIxaoie+Sn5C+yp99dCfp8QBIviaDGEjpKdzODkKA5Lht5XqN10PryYCYkUzb5gPutfwqCJuvqJEc+DUlEWsS0dfnuBHI9VwOfz9G7PwGaLMwsYpqyEtRK16o4WI1y+GMwy1mUx0CbhcDyL+zT/wo5kZnlPQrXRi1Vd5todKt78aIxeRSbxKiV0H0MyB3u7KpTxdVVJxeM9PJN7NbfIJQSBTOW/aewNJ6DQWjjxvGWrDPIqFWfCZMn8OQNpwqd9jj+Zb35T6Bl+ePsiR5yqVXz8FtsiyurcHmgfKLHSm1bY2RdfaSXhQimh796UlH7kxGfFG9l21VuIP3waWmtU0g9+Z909Pd79ueud356pX//tw71x4nbf0xsV8omeka1URRTuq6VM4hUnTxxW44+oMiG87VsQ+cf1vzVaxxXc7R8dvblnzpQHsL5dsFfo7VD4mXnZwntUVc9PirnUD/1wdOoxnQq3Kplqahu1X2ECDvo8uwOVgo/VIQFMbzKV32LUysXkiOkdBVUkHbx6nFzVDxLnnXUL/Okvtay/azSunZ58OSKRw1YtdqQpYhsJ4qwaz5Z34r8XFPLbKEVx/4sskai+mWSbeX9SUeqrLKdM9W0LU2kySYQLow2yZ4RqR6QM/MnXyCOjJJ/mI30cryL0z25RpQkSWQwWlMSrNfHu6VB3tdr3dLiGPWKudFqtfeyBqZGTVaejLIezr/12N3LFwe8vKSlD9vat+MZfaiZbj9ZVTA1jGX+ch9RYWmLm+8P7b+/yZlh7Fv7qSFoDxUNv+V+SpGESmdJwW3tK9Nkxn6+60wsKrfxrrXZvRlEctN084cflnIDOJzPit/M8c7MDGLMdovB1KZvm06uFmOL3Xz7+u3b1/L/9cO7O7iK0dpek57/ML7tCWuymx9wvTeM9/Pdjv7mo9kUHiDuf3z1OsPbtz/e50RsjSX/eu9lm8Hgwqt/DWkrQuYwuLv7D4NlxXDTQeB09i4Dcd2ddYNwPKXO99ppp03y28Yba/wxHDVZPiCNOAznOZFN+nE4ZT/98t8lvvr6ToPRNmnghKHj8NHKsAZ4EQS+HwSOE6Yr14jlSweHO1swEd+/OlzguxciBy7/cdC0pXJGT5JuMITvUJjEiOoljY8fKkQ0I+nIBRgdxJsbHsz7sp6Lfg6cyRLuY0PuWeOQg0g+RIx44TdAxCQiPPz7FBZ59ertqwy/fX3HwDz1eWc+53STDOsH2KbT7XbX3c7V4goWmXXXa6rAOHcWM4+J+we0fAtz4OnhXsZRSidJ10/bXr4GYSe7IJ30XalJmdduOLxqEQ0m4fwKvYdft78MAtwhXKjXXvj+HDWqsM2MyKERiDiSiE4WISJ391+UoDFiRiNn0Wj3+7NBurVsd49BlWwWfHeB52RKRPzGBYbjeM7DQcTEzYvKBW40M0tAuE1rZ9OknwvALGw193k62LtUXVvtL0Ne3lzpWhr8iYdjD2N6OuHBbu/SFBRcg3YlTWEASSRNB4cxEi/S0iJpOpxq2mUVOjP6V85ijFjhRe8jE3WXCxD9iF4YmjFbhIMWjk7HC+d6j15U2wuZ2pCF4CucdxJX3k1NEuHOYNVj9jS+olWLKhFUqlGD+/OWYbNk54cTRAYit0g762C+wt2wS4toBZGOc3CtdDs9yjO0Mm3c7gL+dxnmPENKDwzduBtcL7OFKuOCh6OIjNte4EuqwZbJvKPRTAAuDoQb3E25sVYS4U4j8abjjsPXaz6quBaYumPOg9hj1oT7cmeFyaKBwzvZzukKkTyFlGNEIxuG8MXLm5cF7miuly0HwXoX95c96hiImLZmxzxoNG2Z6o0ZD0DEs1pDDMo90+/K9j9dmlJNCyIpl4gWq3yH8GrudLvE5GLboX3daz6oWITcpT/nPqy0n/vhpknRzpst/N1mhDZ7KWhyIjIqaqdE4H837/6R45cXlEVwASfgnevJrEVj06ZflZBFGk2dputApAuLuKvhz911sMGFX35TXODbn4QsLKVBnN1wvg7gJPKGr+bhbrhZZHvU58Ofg5PBDvMPwbxtbbmMEbgZtwjJg3274/OtVSWSVUlGzIkISSUaI9tq+H317hLRVBPNIQ/TNFyMEisjwjIidklkEHnbMPCDOXygEn4Rsyg1I+22OzwdRuQlGN9CDvZwl0TDhc99fzeLtqE/OHItDO3+jjubdoM7owjZSYNBAh57zY3jj/pk1IyIJhd1SiKktimPEJFvvss30LwGEZppMJrxoOM79I0eLgnDg4ifuVaFCOeNtkV55Le8/Xc/0lYiajHd+D6CaXJFNsdIla61W9lN+JU/n1nWKRGEOuFNOO/u1jy98Ei9tAZBAAYuQnAn7hVEmhUiAYjQCg/lEbjW3Yuvc7y7v0Q/aI3EayXbBpzgagX9I86IBCCCWHiFLALiN++KC/zPjYAJdR0jRC4C41YhkhpkktU82CW2vRwv5nAcEEmrY0QWDTZ482CdNlpowbxYGoRhyIfOqMUqFqFoouVjRMsTIoiIy7sCl3JhJxON1n7Y5enEoziIkXVExBlEFLJ2bYMUa6X9pS4LgenID3Z9A7ntijtQQYLlRBhbzhJ0ztrKlHAgQmNAp0i3Xjtb2eB24Dsfbil0zhZON3ZZGX7zqIVQ0O0bFH6jQUpEKmqVyiqasfMojWnwTn7dlPt7MyJ6xbVYNAqQ76TEZNUrYEi5bU56A7d1iTHf6JOOJtdK4GK2i1FFFjka7HLW36afEnCOZEgRJ+74aQxKJmuNMEpa7Ciz21LUONupTUzhwSQxjmFDRb9f0jpDb5wTEeRazvEYQXMk4IQ8T0LP/4VuwiABjRBkRkhUntJPmnIiVIVSwDgnIrGETknJSXR2O0qD0S0VeMy64E7nwpVEGkkUtVqtqGeK5ghZJm4tmxQfGrcGu3x5/+t9gZtL21uNOsN9czrtjzgfTGnfGYgsMiKwH7kWJcTWKMgy8B21//VX+ru/vxM0PDn5h44kFo14Kk2y2mWulaUBIjI6JwKd4ksNLA3C6S5TqSpNEoFIwLvZAvoEg8NFZOSL0WbU9Z30Ajfr5p8Prwv8+MWlHY1CP51vhkOM9jSmzYtmptCaJMmJyEJmdi/mzhx9Ey9/yVs/PLz+B0Tj8gN3voRBqLhwY3wbolBGRK5v0+2gqFWVKBkgrkakBdCufx2Gcps+DW0rdoLFzCD2pLsD5+OcNJwFiQAhHvhOZ9I0BPLIVwcV/vUdpBDcIYWK930f5Q0cRBIJr1Hq6HKUdT7SPjsbX+bAJEcy/tW9cGcppA+5LEWU6IOMOWx1FXaScp7D2n50PkWkR9slEVC98YJ3Zp6cM4BM6NP216U3DkmFA4tRkwTcdDaiDLuYj5sGqpSbb4qNmMgkkPHMSzY7Dq0Ku+0NMyfyJqXhQjoHREL5cxmoUed6BRn/W9n+q4d7o/mB87kcIaRVpEkQcFfz9KogYhORxfkYgde12qgqkYfacTxb2lmkRWxIxnjr7sfxRSzx3pJK1G3NhpNJjPqXNv0d8ojMJIJWTJLtZjDYxJEtMxUy9V42lqHP6MfjNrSgMFrxdowQc8gjlEmMaBbHiWcKckkwac7icWKxaDaeRXYxfeOhT23rE/M7VArDCeRGMVI7ch5B/ijdMIT8Ebot39DOV5o3MSzLQmCys0hTVeFSYyBiTZvNqSu1g0YPdCGkGPTNpm+Ry72mLXW90I9kvOyECRlMQQKqM1t+kRfA15lZh7XseudE5OyFLmeiWEkknykSR6fKLuQmFvRrHWEf54Est2fvEHegym0aJyTOSWrkczaaKH7aK0XJ4QL5r4HoB+S2KbtFOUnIhfqiiV3+qPwpiEden6IyP3n6UTbX+ERr+3gm7rCidTbbxE5mqxQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFP4K/BviPMZK1iH0CAAAAABJRU5ErkJggg==" style="border:0;display:block;outline:none;text-decoration:none;width:100%;" width="64"/> </td></tr></tbody> </table> </td></tr><tr> <td align="center" style="font-size:0px;padding:10px 25px;padding-bottom:40px;word-break:break-word;"> \
        <div style="font-family:\'Helvetica Neue\',Arial,sans-serif;font-size:28px;font-weight:bold;line-height:1;text-align:center;color:#555;"> MIS report generator <sup><i>beta*</i></sup> </div> \
        </td></tr><hr><tr> <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;"> <div style="font-family:\'Helvetica Neue\',Arial,sans-serif;font-size:16px;line-height:22px; \
        text-align:left;color:#555;"> {msg_content} </div></td></tr></table> </div><div style="Margin:0px auto;max-width:600px;"> <table align="center" border="0" cellpadding="0" cellspacing="0" \
        role="presentation" style="width:100%;"> <tbody> <tr> <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;"> <div class="mj-column-per-100 outlook-group-fix" \
        style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;"> <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%"> <tbody> <tr> \
        <td style="vertical-align:bottom;padding:0;"> <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%"><hr><tr><td align="center" style="font-size:0px;padding:0;word-break:break-word;"> \
        <div style="font-family:\'Helvetica Neue\',Arial,sans-serif;font-size:12px;font-weight:300;line-height:1;text-align:center;color:#575757;"> Valuestream Business Solutions Pvt Ltd, Zenith house. 1st floor b wing, \
        </div><div style="font-family:\'Helvetica Neue\',Arial,sans-serif;font-size:12px;font-weight:300;line-height:1;text-align:center;color:#575757;"> # 4 Industrial Layout, Koramangala, 7th block Bangalore - 560095 \
        </div></td></tr></table> </td></tr></tbody> </table> </div></td></tr></tbody> </table> </div></div></body></html>'
    body = MIMEText(msg_html_body, 'html')
    message.attach(body)

    attachmentPath = filename
    try:
        with open(attachmentPath, "rb") as attachment:
            p = MIMEApplication(attachment.read(),_subtype="pdf")	
            p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.split("/")[-1]) 
            message.attach(p)
    except Exception as e:
        print(str(e),flush=True)
    msg_full = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()  
        server.starttls(context=context)
        server.ehlo()
        server.login(gmail, password)
        server.sendmail(gmail,to.split(";") + (cc.split(";") if cc else []),msg_full)
        server.quit()

    print(f"email sent out successfully to {to} and cc {cc} from {gmail}",flush=True)



# return table for the frontend.
# def get_full_table_from_sql_query(sql_qry,col_names):
#     # print(f"{sql_qry}",flush=True)
#     # for single table.
#     if type(sql_qry) is str:
#         df,_,_ = get_table_from_db(sql_qry)
#         if col_names is not None:
#             return df[col_names]
#         else:
#             return df

#     #for multiple tables.
#     elif type(sql_qry) is list:

#         temp_dfs = []
#         result  = check_if_all_none(sql_qry)
                
#         if result:
#             return DataFrame()
#         else:
#             for i in sql_qry:
#                 if type(i) is dict:
#                     if i['table_names'][0].find('/') > -1 and temp_dfs!=[]:
#                         temp_dfs.append(get_joined_table(i, temp_dfs[-1]))
#                     else:
#                         temp_dfs.append(get_joined_table(i,None))
     
            
#         if temp_dfs[-1].shape[0] > 0:
#             if col_names is not None:
#                 return temp_dfs[-1][col_names]
#             else:
#                 return temp_dfs[-1]
#         else:
            # return DataFrame()


# def get_join_dataframe(table_name): # Step 4
#     '''
#     Function returns a full table and also changes the datatype of columns.
#     accepts a single table input and gives single dataframe output.
#     '''
#     # db_address=os.environ['DOCKER_HOST_IP'] #for windows machine
#     host=os.environ.get('CDB_HOST')
#     if host == 'windows':
#         host = os.environ['DOCKER_HOST_IP']

#     db_address=host #for linux enter host ip
#     pwd=os.environ.get('CDB_PASS')
#     db_user=os.environ.get('CDB_USER')
#     db_port=os.environ.get('CDB_PORT')
#     db_name=os.environ.get('CDB_NAME')

#     sql_qry = f'SELECT *from {table_name}'
#     db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
#     db_connection = create_engine(db_connection_str)
#     df1 = read_sql(sql_qry, con=db_connection)
#     df3 = read_sql(f'DESC {table_name};',con=db_connection)
#     bit_types = df3[df3['Type'].str.startswith('bit')]['Field']

#     numeric_types = df3[df3['Type'].str.startswith(('tinyint','smallint','int',\
#         'bigint'))]['Field']
    
#     float_types = df3[df3['Type'].str.startswith(('money','smallmoney','float',\
#         'decimal','numeric'))]['Field']

#     datetime_types = df3[df3['Type'].str.startswith(('datetime','datetime2',\
#         'smalldatetime','date','time','datetimeoffset','timestamp'))]['Field']

#     if datetime_types.empty is False:
#         for i in datetime_types:
            
#             df1[i] = to_datetime(df1[i], infer_datetime_format=True)

#     if float_types.empty is False:
#         for i in float_types:
#             df1[i] = df1[i].fillna(0)
#             df1[i] = df1[i].astype(float)

#     if numeric_types.empty is False:
#         for i in numeric_types:
#             df1[i] = df1[i].fillna(0)
#             df1[i] = df1[i].astype(int)

#     if bit_types.empty is False:
#         for i in bit_types:
#             df1[i]=df1[i].apply(lambda k: int.from_bytes(k,byteorder='big'))

#     db_connection=db_connection.dispose()
#     return df1


# def get_joined_table(d,dd): # Step 2
#     '''
#     Function joins two or more tables.

#     returns full table as dataframe.
#     '''

#     if type(dd) is DataFrame:
#         df_left = dd
#         df_right = get_join_dataframe(d['table_names'][1])

#         l_sufx = d['table_names'][0].replace(' / ','_').strip()
#         r_sufx = d['table_names'][1]

#         value_left = d['join_on'][0]
#         value_right = d['join_on'][1]
#         try:
#             ddf=df_left.set_index(value_left).join(df_right.set_index(value_right),\
#                 how=d['join'],lsuffix=f'_{l_sufx}',rsuffix=f'_{r_sufx}')
#         except:
#             ddf=DataFrame()

#         df_left=0
#         df_right=0
#         return ddf
#     else:
#         df_left=get_join_dataframe(d['table_names'][0])
#         df_right=get_join_dataframe(d['table_names'][1])

#         value_left=d['join_on'][0]
#         value_right=d['join_on'][1]

#         l_sufx = d['table_names'][0].replace(' / ','_').strip()
#         r_sufx = d['table_names'][1]

#         try:
#             ddf=df_left.set_index(value_left).join(df_right.set_index(value_right),\
#                 how=d['join'],lsuffix=f'_{l_sufx}',rsuffix=f'_{r_sufx}')
#         except:
#             ddf=DataFrame()

#         df_left=0
#         df_right=0
#         return ddf


# Returns wheather a join is success or failure. # Step 1
# def get_join_main(d,sql_qry):
#     temp_dfs = []
#     result = check_if_all_none(sql_qry)
            
#     if result:
#         temp_dfs.append(get_joined_table(d,None))
#     else:
#         stats = False
#         for i in sql_qry:
#             if type(i) is dict:
#                 if i['table_names'][0].find('/') > -1 and temp_dfs!=[]:
#                     temp_dfs.append(get_joined_table(i, temp_dfs[-1]))
#                 else:
#                     temp_dfs.append(get_joined_table(i,None))
                
#                 if type(i) is dict:
#                     if d['table_names'] == i['table_names']:
#                         stats = True
        

#         if stats is False:
#             temp_dfs.append(get_joined_table(d,temp_dfs[-1]))
        
#     # sys.stderr.write(str(y))
   

#     if temp_dfs[-1].shape[0] > 0:
#         return 'Success', list(temp_dfs[-1].columns)
#     else:
#         return 'Error', []
# def  get_table_from_sql_query(sql_qry):
#     if type(sql_qry) is str:



# return table for the frontend.
# def get_table_from_sql_query(sql_qry):
#     # for single table.
#     if type(sql_qry) is str:
#         df,rows,download_data = get_table_from_db(sql_qry)
#         return df.head(),rows,download_data

#     #for multiple tables.
#     elif type(sql_qry) is list:

#         temp_dfs = [] # storing dataframes
#         result  = check_if_all_none(sql_qry)
                
#         if result:
#             return DataFrame()
#         else:
#             for i in sql_qry:
#                 if type(i) is dict:
#                     if i['table_names'][0].find('/') > -1 and temp_dfs!=[]:
#                         temp_dfs.append(get_joined_table(i, temp_dfs[-1]))
#                     else:
#                         temp_dfs.append(get_joined_table(i,None))
     
#             download_data = {
#                 "sql_qry":sql_qry,
#                 'filter_condi':None,
#                 "col_replace":None,
#                 "col_select":None,
#                 'filter_index':None,

#             }
#         if temp_dfs[-1].shape[0] > 0:
#             return temp_dfs[-1].head(),temp_dfs[-1].shape[0],download_data
#         else:
#             return DataFrame(), None, {}

# def get_filtered_data(fil_dict,df1):
#     pds_list = []
    
#     # df1=1
#     for i in range(len(fil_dict['index'])):
#         if fil_dict['condition'][i] == 'is missing':# IS NULL
#             pds_list.append(df1[fil_dict['columns'][i]].isna())
        
#         elif fil_dict['condition'][i] == 'is not missing':# IS NOT NULL
#             pds_list.append(~df1[fil_dict['columns'][i]].isna())
            
#         elif fil_dict['condition'][i] == 'has value(s)':# col IN (val1,val2)
#             pds_list.append(df1[fil_dict['columns'][i]].isin(fil_dict['values'][i]))#str inputs
            
#         elif fil_dict['condition'][i] == 'starts with':# LIKE 'value%';
#             pds_list.append(df1[fil_dict['columns'][i]].str.startswith(fil_dict['values'][i]))#str input
        
#         elif fil_dict['condition'][i] == 'ends with':# LIKE '%value';
#             pds_list.append(df1[fil_dict['columns'][i]].str.endswith(fil_dict['values'][i])) #str input
        
#         elif fil_dict['condition'][i] == 'contains':# LIKE '%value%';
#             pds_list.append(df1[fil_dict['columns'][i]].str.contains(fil_dict['values'][i])) #str input
        
#         elif fil_dict['condition'][i] == '<':# col < value
#             pds_list.append(df1[fil_dict['columns'][i]] < int(fil_dict['values'][i])) #int input
        
#         elif fil_dict['condition'][i] == '<=':# col <= value
#             pds_list.append(df1[fil_dict['columns'][i]] <= int(fil_dict['values'][i])) #int input
        
#         elif fil_dict['condition'][i] == '==':# col = value
#             pds_list.append(df1[fil_dict['columns'][i]] == int(fil_dict['values'][i])) #int input
        
#         elif fil_dict['condition'][i] == '>':# col > val
#             pds_list.append(df1[fil_dict['columns'][i]] > int(fil_dict['values'][i])) #int input
        
#         elif fil_dict['condition'][i] == '>=':# col >= val
#             pds_list.append(df1[fil_dict['columns'][i]] >= int(fil_dict['values'][i])) #int input
            
#         elif fil_dict['condition'][i] == '!=':# col != val
#             pds_list.append(df1[fil_dict['columns'][i]] != int(fil_dict['values'][i])) #int input
        
#         elif fil_dict['condition'][i] == 'days':
#             x = fil_dict['values'][i][1]
#             y = fil_dict['values'][i][0]
#             if type(x) is list:
#                 x = to_datetime(date.today())
#                 y = x + timedelta(int(y))
#             else:
#                 x = to_datetime(x)
#                 y = x + timedelta(int(y))

#             max_dt = max(x,y)
#             min_dt = min(x,y)
            
#             if x == y:
#                 pds_list.append((df1[fil_dict['columns'][i]] == y))
#             elif y == min_dt:
#                 pds_list.append((df1[fil_dict['columns'][i]] >= min_dt) &  (df1[fil_dict['columns'][i]] < max_dt))
#             else:
#                 pds_list.append((df1[fil_dict['columns'][i]] > min_dt) &  (df1[fil_dict['columns'][i]] <= max_dt))
        
#         elif fil_dict['condition'][i] == 'before':
#             x = to_datetime(fil_dict['values'][i])
#             pds_list.append(df1[fil_dict['columns'][i]] < x)
        
#         elif fil_dict['condition'][i] == 'after':
#             x = to_datetime(fil_dict['values'][i])
#             pds_list.append(df1[fil_dict['columns'][i]] > x)
        
#         elif fil_dict['condition'][i] == 'equals':
#             x = to_datetime(fil_dict['values'][i])
#             pds_list.append(df1[fil_dict['columns'][i]] == x)
        
#         elif fil_dict['condition'][i] == 'not':
#             x = to_datetime(fil_dict['values'][i])
#             pds_list.append(df1[fil_dict['columns'][i]] != x)

#         elif fil_dict['condition'][i] == 'range':
#             x = to_datetime(fil_dict['values'][i][0])
#             y = to_datetime(fil_dict['values'][i][1])
#             max_dt = max(x,y)
#             min_dt = min(x,y)
#             pds_list.append((df1[fil_dict['columns'][i]] >= min_dt) & (df1[fil_dict['columns'][i]] <= max_dt))
        
#     condi=None
#     for ele in range(0, len(pds_list)):
#         if condi is None:
#             condi = pds_list[ele]
#         else:
#             if fil_dict['logic'][ele] == 'And':
#                 condi = op.and_(condi,pds_list[ele])
#             elif fil_dict['logic'][ele] == 'Or':
#                 condi = op.or_(condi,pds_list[ele])

#     if fil_dict['select_drop'] == 'Drop':
#         condi = op.inv(condi)
#         return condi
#     else:
#         return condi

# def get_column_values(table_name,column_name):
#     # db_addre`s`s=os.environ['DOCKER_HOST_IP'] #for windows machine
#     host=os.environ.get('CDB_HOST')
#     if host == 'windows':
#         host = os.environ['DOCKER_HOST_IP']

#     db_address=host #for linux enter host ip
#     pwd=os.environ.get('CDB_PASS')
#     db_user=os.environ.get('CDB_USER')
#     db_port=os.environ.get('CDB_PORT')
#     db_name=os.environ.get('CDB_NAME')
#     db_connection_str = f'mysql+pymysql://{db_user}:{pwd}@{db_address}:{db_port}/{db_name}'
#     db_connection = create_engine(db_connection_str)
#     table_name = table_name['table'][0]
#     df1 = read_sql(f'SELECT {column_name} FROM {table_name}', con=db_connection)

#     df3 = read_sql(f'DESC {table_name};',con=db_connection)
#     bit_types = df3[df3['Type'].str.startswith('bit')]['Field']
    
#     numeric_types = df3[df3['Type'].str.startswith(('tinyint','smallint','int',\
#         'bigint'))]['Field']
    
#     float_types = df3[df3['Type'].str.startswith(('money','smallmoney','float',\
#         'decimal','numeric'))]['Field']

#     datetime_types = df3[df3['Type'].str.startswith(('datetime','datetime2',\
#         'smalldatetime','date','time','datetimeoffset','timestamp'))]['Field']

#     if datetime_types.empty is False:
#         for i in datetime_types:
            
#             df1[i] = to_datetime(df1[i], infer_datetime_format=True)

#     if float_types.empty is False:
#         for i in float_types:
#             df1[i] = df1[i].fillna(0)
#             df1[i] = df1[i].astype(float)

#     if numeric_types.empty is False:
#         for i in numeric_types:
#             df1[i] = df1[i].fillna(0)
#             df1[i] = df1[i].astype(int)

#     if bit_types.empty is False:
#         for i in bit_types:
#             df1[i]=df1[i].apply(lambda k: int.from_bytes(k,byteorder='big'))

#     db_connection=db_connection.dispose()
#     return df1