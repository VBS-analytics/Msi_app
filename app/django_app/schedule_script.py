#!/py/bin/python
import os
import sys
import json
from sqlalchemy import create_engine

# from models import MsiFilters
from global_functions import get_transformations, get_format_mapping,\
    get_table_from_sql_query, get_downloaded_data_to_folder
from pandas import DataFrame, read_sql
from datetime import date, datetime

def get_data_from_database(fil_name):
    print("inside get_data_from_database")
    host=os.environ.get('DB_HOST')
    if host == 'windows':
        host = os.environ['DOCKER_HOST_IP']

    db_address=host #for linux enter host ip
    pwd=os.environ.get('DB_PASS')
    db_user=os.environ.get('DB_USER')
    db_port=os.environ.get('DB_PORT')
    db_name=os.environ.get('DB_NAME')
    print('env variables fetched')
    
    db_connection_str = f"postgresql+psycopg2://{db_user}:{pwd}@{db_address}/{db_name}"
    db_connection = create_engine(db_connection_str)

    df1 = read_sql(f"select * from django_app_msifilters where filter_name='{fil_name}'",con=db_connection)

    print(df1.shape)

    db_connection=db_connection.dispose()
    if df1.empty is False:
        return json.loads(df1['filter_data'].iloc[0])
    else:
        return None

def get_download_data(ret_data,loc,file_name):
    if ret_data is not None:
        print('first condition')
        col={}
        csv_string = None
        print(ret_data['relationship_data']['table_order'])
        print(ret_data['relationship_data']['table'])
        tbl = ret_data['relationship_data']['table']
        tbl_order = ret_data['relationship_data']['table_order']
        # print(tbl,flush=True)
        tbl_order=list(filter(None,tbl_order))

        if tbl is not None and type(tbl) is str:
            df,table_rows_no,csv_string = get_table_from_sql_query(tbl,tbl_order)
            table_names = tbl

        elif tbl is not None and type(tbl) is list:
            df,table_rows_no,csv_string = get_table_from_sql_query(tbl,tbl_order)
            table_names = tbl
        else:
            df=DataFrame()
            table_names = None
            table_rows_no = 0
        if ret_data['format_map_data'] is not None and ret_data['format_map_data'] != {}:
            col={}
            [col.update({j:i}) for i,j in ret_data['format_map_data'].items()]
        
        relationship_data=dict(table=[],columns=None,saved_data=False,table_order=[])
        relationship_data["table"]=table_names
        relationship_data['columns']=df.columns
        relationship_data['saved_data']=True
        relationship_data['table_order']=tbl_order

        if ret_data['filters_data']['index_k'] is not None:
            df,sql_qry,rows,csv_string = get_transformations(relationship_data,ret_data['filters_data'],col)

            if ret_data['format_map_data'] != {}:
                d = {'column_names':[]}
                d["column_names"]=list(ret_data['format_map_data'].values())
                # col={}
                # [col.update({j:i}) for i,j in ret_data['format_map_data'].items()]
                # print(col)

                df, csv_string = get_format_mapping(relationship_data,d,sql_qry,col)
        else:
            print('Second Condition')
            if relationship_data['table']!=[] and relationship_data['table'] is not None:
                
                rel_tbl_drpdwn=list(filter(None,relationship_data['table_order']))

                df,rows,csv_string=get_table_from_sql_query(relationship_data['table'],rel_tbl_drpdwn)

                if ret_data['format_map_data'] != {}:
                    d = {'column_names':[]}
                    d["column_names"]=list(ret_data['format_map_data'].values())
                    # col={}
                    # [col.update({j:i}) for i,j in ret_data['format_map_data'].items()]
                    # print(col)

                    df, csv_string = get_format_mapping(relationship_data,d,None,col)
        
        print(csv_string)
        if csv_string is not None:
            get_downloaded_data_to_folder(csv_string,loc,file_name)


if __name__ == '__main__':
    print(sys.argv[1])
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # loc = os.path.join(os.path.join(dir_path,'media'),'django_app')
    loc = "/app/django_app/media/django_app"
    filter_name = sys.argv[1]
    # print(os.environ.get('DB_HOST'))
    # print(loc)
    ret_data = get_data_from_database(filter_name)
    # print('After get database')
    now = datetime.now().ctime().replace(" ","_")
    file_name=str(filter_name) + '_' + now +".xlsx"
    
    # print(loc)
    get_download_data(ret_data,loc,file_name)
    # print('\n')