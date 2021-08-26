from numpy.lib.npyio import save
from numpy.lib.twodim_base import tri
from pandas.io import sql
from flask_caching import Cache
from ..server import app
from dash.dependencies import Output, Input, State, MATCH, ALL
from dash import callback_context
from dash_core_components import Dropdown, Store
from dash_html_components import Div, H5, Br, I, A
from dash_bootstrap_components import Col, Row, Modal, ModalHeader, ModalFooter,\
    ModalBody, Button, DropdownMenuItem, Tooltip, Toast, Alert
import dash_html_components as dhc

from ..global_functions import get_columns, get_join_main, get_main_sql_query,get_table_names

import json
from .. models import MsiFilters
import sys
import regex
import ast 
import re
import os
from django.http import HttpResponse
from django.conf import settings

from pandas import read_excel, ExcelWriter

from crontab import CronTab

from dash.exceptions import PreventUpdate
from dash_extensions.snippets import send_bytes, send_file



@app.callback(
    [
        Output('sch-hourly-body','style'),
        Output('sch-daily-body','style'),
        Output('sch-weekly-body','style'),
        Output('sch-monthly-body','style'),
    ],
    [
        Input("schedule-radio","value")
    ]
)
def update_view_of_schedules(value):
    if value == "hourly":
        return {},{"display":"none"},{"display":"none"},{"display":"none"}
    elif value == "daily":
        return {"display":"none"},{},{"display":"none"},{"display":"none"}
    elif value == "weekly":
        return {"display":"none"},{"display":"none"},{},{"display":"none"}
    elif value == "monthly":
        return {"display":"none"},{"display":"none"},{"display":"none"},{}
    else:
        return {"display":"none"},{"display":"none"},{"display":"none"},{"display":"none"}

@app.callback(
    Output('schedule-body','style'),
    [
        Input('schedule-cklist','value')
    ],
)
def update_view_of_schedule_body(value):
    if value != []:
        return {}
    else:
        return {"display":"none"}


# Display no.of rows count to front-end from memory.
@app.callback(
    Output('noofpolicies-card','children'),
    [
        Input('total-rows','data')
    ]
)
def update_noofpolicies(data):
    if data is not None:
        return str(data)
    else:
        return None


# stores no.of rows count into memory
@app.callback(
    Output('total-rows','data'),
    [
        Input('relation-rows','data'),
        Input('transformations-rows','data')
    ]
)
def display_rows(data1,data2):
    if data1 is not None and data2 is not None:
        return data2
    elif data1 is not None and data2 is None:
        return data1
    else:
        return None

# download scheduled excel files
@app.callback(
    Output('schedule-fil-download','data'),
    [
        Input('schedule-fil-modal-download','n_clicks'),
    ],
    [
        State('schedule-radio-btn','value')
    ]
)
def download_schedule_excel(n_clicks,value):
    # file_path = os.path.join(settings.MEDIA_ROOT, path)
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]
    # file_name = os.path.basename(value)

    if triggred_compo == 'schedule-fil-modal-download' and n_clicks is not None and value is not None:
        # def to_xlsx(bytes_io):
        #     xslx_writer = ExcelWriter(bytes_io, engine="xlsxwriter")
        #     df=read_excel(value)
        #     df.to_excel(xslx_writer, index=False)
        #     xslx_writer.save()

        # return send_bytes(to_xlsx, file_name)
        return send_file(value)
    return None


# show schedule filters in a pop-up
@app.callback(
    [
        Output('schedule-fil-modal','is_open'),
        Output('schedule-radio-btn','options'),
    ],
    [
        Input('scheduled-outputs','n_clicks'),
        Input('schedule-fil-modal-close','n_clicks'),
        Input('schedule-fil-modal-delete','n_clicks'),
    ],
    [
        State('schedule-fil-modal','is_open'),
        State('schedule-radio-btn','value')
    ]
)
def update_schedule_filters(n_clicks,close_n_clicks,del_n_clicks,is_open,value):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo == 'scheduled-outputs' and n_clicks is not None:
        # value = settings.BASE_DIR
        media_path = os.path.join(os.path.join(os.path.join(settings.BASE_DIR,'django_app'),'media'),'django_app')
        arr_txt = [x for x in os.listdir(media_path) if x.endswith(".xlsx")]
        file_loc = [os.path.join(media_path,i) for i in arr_txt]
        radio_options=[] 
        for i in arr_txt:
            fil_name = i
            # fil_date = i['filter_date']

            option_name = str(fil_name)
            radio_options.append(option_name)
        
        fil_options = [{'label':i,'value':j} for i,j in zip(radio_options,file_loc)]
     
        return not is_open, fil_options
    elif triggred_compo == 'schedule-fil-modal-close' and close_n_clicks is not None:
        return not is_open, []
    elif triggred_compo == 'schedule-fil-modal-delete' and del_n_clicks is not None and value is not None:
        os.remove(value)
        media_path = os.path.join(os.path.join(os.path.join(settings.BASE_DIR,'django_app'),'media'),'django_app')
        arr_txt = [x for x in os.listdir(media_path) if x.endswith(".xlsx")]
        file_loc = [os.path.join(media_path,i) for i in arr_txt]
        radio_options=[] 
        for i in arr_txt:
            fil_name = i
            # fil_date = i['filter_date']

            option_name = str(fil_name)
            radio_options.append(option_name)
        
        fil_options = [{'label':i,'value':j} for i,j in zip(radio_options,file_loc)]
  

        return is_open, fil_options

    else:
        return is_open, []




# show saved changes in a pop-up
@app.callback(
    [
        Output('saved-fil-modal','is_open'),
        Output('filter-radio-btn','options'),
    ],
    [
        Input('saved-filters-btn','n_clicks'),
        Input('saved-fil-modal-close','n_clicks'),
        Input('retrived-data','data'),
    ],
    [
        State('saved-fil-modal','is_open'),
        State('filter-radio-btn','value'),
    ]
)
def update_saved_filters(n_clicks,close_n_clicks,ret_data,is_open,fil_radio_val):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo == 'saved-filters-btn' and n_clicks is not None:
        filters_objects = MsiFilters.objects.all().values()
         
        radio_options=[] 
        for i in filters_objects:
            fil_name = i['filter_name']
            fil_date = i['filter_date']

            option_name = str(fil_name) + ' ▬ ' + str(fil_date)
            radio_options.append(option_name)
        
        fil_options = [{'label':i,'value':i} for i in radio_options]
     
        return not is_open, fil_options
    elif triggred_compo == 'saved-fil-modal-close' and close_n_clicks is not None:
        return not is_open, []
    elif triggred_compo == 'retrived-data' and ret_data is None and fil_radio_val is not None:
        filters_objects = MsiFilters.objects.all().values()
         
        radio_options=[] 
        for i in filters_objects:
            fil_name = i['filter_name']
            fil_date = i['filter_date']

            option_name = str(fil_name) + ' ▬ ' + str(fil_date)
            radio_options.append(option_name)
        
        fil_options = [{'label':i,'value':i} for i in radio_options]
     
        return is_open, fil_options
    elif triggred_compo == 'retrived-data' and ret_data is not None:
        return False, []
    else:
        return is_open, []


# Save applied changes to Database
@app.callback(
    Output('modal-sf-status','is_open'),
    [
        Input('modal-sf-save','n_clicks'),
    ],
    [
        State('save-changes','data'),
        State('modal-sf-filter-name','value'),
        
        State('schedule-cklist','value'),
        State('schedule-radio','value'),
        
        State('sch-hourly-min-input','value'),
        
        State('sch-daily-hour-input','value'),
        State('sch-daily-min-input','value'),

        State('sch-weekly-week-input','value'),
        State('sch-weekly-hour-input','value'),
        State('sch-weekly-min-input','value'),

        State('sch-monthly-month-input','value'),
        State('sch-monthly-date-input','value'),
        State('sch-monthly-hour-input','value'),
        State('sch-monthly-min-input','value'),

        State('sch-email-input','value'),
        State('sch-auto-del-input','value'),
    ]
)
def save_to_db(n_clicks,data,fil_name,cklist_value,sch_radio_value,\
    sch_hly_val,sch_dly_hr_val,sch_dly_min_val,sch_wly_wk_val,\
    sch_wly_hr_val,sch_wly_min_val,sch_mly_mon_val,sch_mly_dt_val,\
    sch_mly_hr_val,sch_mly_min_val,sch_email_val,sch_auto_del_val):
    if n_clicks is not None and fil_name is not None:
        if cklist_value != []:
            sch_str=""
            if 'hourly' in sch_radio_value:
                sch_str=f'{sch_hly_val} * * * *'
            elif 'daily' in sch_radio_value:
                sch_str=f'{sch_dly_min_val} {sch_dly_hr_val} * * *'
            elif 'weekly' in sch_radio_value:
                sch_str=f"{sch_wly_min_val} {sch_wly_hr_val} * * {','.join(sch_wly_wk_val)}"
            elif 'monthly' in sch_radio_value:
                sch_str=f"{sch_mly_min_val} {sch_mly_hr_val} {sch_mly_dt_val} {','.join(sch_mly_mon_val)} *"
            
            cron = CronTab(user='root')

            local = os.path.join(settings.BASE_DIR,'django_app')

            # log_file = os.path.join(local,'test.out')

            schedule_script_loc = os.path.join(os.path.join(settings.BASE_DIR,'django_app'),'schedule_script.py')

            

            # fil_name = fil_name + '_' + now

            job = cron.new(command=f'/app/django_app/schedule_script.py {fil_name} >> /app/django_app/media/django_app/test.log',comment=str(fil_name))
            # job = cron.new(command=f'/py/bin/python {schedule_script_loc} {fil_name}',comment=str(fil_name))
            
            # for j in cron:
            #     print(sch_str,flush=True)
            #     print(j,flush=True)

            if sch_str != "":
                job.setall(sch_str)
                cron.write()
                if sch_auto_del_val is not None:
                    job2 = cron.new(command=f'/usr/bin/find /app/django_app/media/django_app -type f -name "{fil_name}*.xlsx" -mtime +{int(sch_auto_del_val)} -exec rm -f {{}} \;',comment=str(fil_name))
                    job2.setall('0 0 * * *')
                    cron.write()

            data = json.dumps(data)
            filter_data = MsiFilters(filter_name=fil_name,filter_data=data)
            filter_data.save()
            return True
                
        else:
            data = json.dumps(data)
            filter_data = MsiFilters(filter_name=fil_name,filter_data=data)
            filter_data.save()
            return True
    else:
        return False


# Retrive saved changes from database
@app.callback(
    Output('retrived-data','data'),
    [
       Input('saved-fil-modal-apply','n_clicks'),
       Input('saved-fil-modal-delete','n_clicks'),
    ],
    [
        State('filter-radio-btn','value'),
        State('retrived-data','data'),
    ]
)
def update_retrived_data(n_clicks,del_n_clicks,value,data):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo == 'saved-fil-modal-apply' and n_clicks is not None:
        fil_name = value.split('▬')[0].strip()
        fil_date = value.split('▬')[1].strip()

        try:
            dat = MsiFilters.objects.filter(filter_name=fil_name,filter_date=fil_date).values()
        except:
            dat = None
        
        if dat is not None:
            # print(dat[0]['filter_data'],flush=True)
            return json.loads(dat[0]['filter_data'])
        else:
            return None

    elif triggred_compo == 'saved-fil-modal-delete' and del_n_clicks is not None:
        fil_name = value.split('▬')[0].strip()
        fil_date = value.split('▬')[1].strip()

        try:
            dat = MsiFilters.objects.filter(filter_name=fil_name,filter_date=fil_date).delete()
            cron = CronTab(user=True)
            cron.remove_all(comment=str(fil_name))
            cron.write()
        except:
            dat = None

        return None
    else:
        raise PreventUpdate
    
# save modal open or close
@app.callback(
    Output('sf-modal','is_open'),
    [
        Input('run','n_clicks'),
        Input('modal-sf-close','n_clicks'),
    ],
    [
        State('sf-modal','is_open')
    ]
)
def sf_modal_open(n_clicks,close_n_clicks,is_open):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    # sys.stderr.write(str(triggred_compo))
    # print(f"\n{str(is_open)}")
    # print(f"\n{str(close_n_clicks)}")

    if triggred_compo == 'run' and n_clicks is not None:
        return not is_open
    elif triggred_compo == 'modal-sf-close' and close_n_clicks is not None:
        return not is_open
    else:
        return is_open

# save changes to memory
@app.callback(
    Output('save-changes','data'),
    [
        Input('relationship-data','data'),
        
        Input('format-map-data','data'),
        Input('upload-file-columns-data','data'),
    ],
    [
        State('column-names-row','children'),
        State('tables-row', 'children'),
        State('filters-div','children'),
        State('transformations-table-column-data','data'),
        State('transformations-filters-condi','data'),
        State('save-changes','data'),
        State('filters-data','data'), 
        State('select-drop-select-drop','value'),
        State('select-drop-col-names','value')
    ],
)
def update_chngs_db(relationship_data,\
    format_map_data,upload_file_columns_data,format_row,tables_row,filter_rows,\
        transformations_table_column_data,\
        transformations_filters_condi,save_changes_data,filters_data,\
        sel_drp_val,sel_drp_col_val):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    # print(save_changes_data,flush=True)
    # print(relationship_data,flush=True)

    if triggred_compo == 'relationship-data':
        # print(f"\n{type(relationship_data)}",flush=True)
        # print(f"\n{tables_row}",flush=True)
        save_changes_data['relationship_data']=relationship_data
        save_changes_data['filters_data']=filters_data
        save_changes_data['transformations_table_column_data']=transformations_table_column_data
        save_changes_data['transformations_filters_condi']=transformations_filters_condi
        tables_row = str(tables_row)
        tables_row=regex.sub("'n_clicks': [\d|None]*","'n_clicks': None",tables_row)
        tables_row=ast.literal_eval(str(tables_row))

        save_changes_data['tables_rows'] = tables_row
        
        filter_rows = str(filter_rows)
        filter_rows=regex.sub("'n_clicks': [\d|None]*","'n_clicks': None",filter_rows)
        filter_rows=ast.literal_eval(str(filter_rows))

        save_changes_data['filter_rows'] = filter_rows

        save_changes_data['sel_val'] = sel_drp_val
        save_changes_data['sel_col'] = sel_drp_col_val
        
        # print(f"\n\n{save_changes_data}",flush=True)
        return save_changes_data
    
    elif triggred_compo == 'format-map-data':
        save_changes_data['format_map_data']=format_map_data
        save_changes_data['format_rows'] = format_row
        return save_changes_data
    
    elif triggred_compo == 'upload-file-columns-data':
        save_changes_data['upload_file_columns_data']=upload_file_columns_data
        return save_changes_data
    else:
        return save_changes_data

# showing the changes made in a dropdown menu in Top right.
@app.callback(
    Output('applied-changes-dropdown','children'),
    [
        Input('relationship-data','data'),        
    ],
    [
        State('filters-data','data'),
        State('applied-changes-dropdown','children'),
        State({'type':'applied-changes-menu','index':ALL},'id'),
    ]

)
def update_applied_filters_menu(relation_data,filters_data,applied_changes,applied_id):
    print(relation_data,flush=True)
    print(filters_data,flush=True)
    # print(fil_val,flush=True)
    rel_val = relation_data['table']
    add_val = filters_data['add_new_col']
    fil_val = filters_data['filters']

    # print(rel_val,flush=True)
    # print(sel_val,flush=True)
    # print(fil_val,flush=True)

    relationship_menu = [True if type(i['props']['id']) == dict and \
            i['props']['children'] is not None and\
            i['props']['children'].startswith('Table Relation')\
            else False for indx,i in enumerate(applied_changes)]
    
    add_col_menu = [True if type(i['props']['id']) == dict and \
            i['props']['children'] is not None and\
            i['props']['children'].startswith('New column added')\
            else False for indx,i in enumerate(applied_changes)]

    filters_menu = [True if type(i['props']['id']) == dict and \
            i['props']['children'] is not None and\
            i['props']['children'].startswith('Filters')\
            else False for indx,i in enumerate(applied_changes)]

    if rel_val is not None and rel_val != [] and any(relationship_menu) is False:
        rel_id = [i['index'] for i in applied_id]
        rel = DropdownMenuItem(f"Table Relations  X"\
                ,id={'type':'applied-changes-menu','index':max(rel_id)+1})
        applied_changes.append(rel)
    
    if (rel_val is None or rel_val == []) and any(relationship_menu) is True:
        [applied_changes.remove(applied_changes[indx]) for indx,i in enumerate(applied_changes) \
            if type(i['props']['id']) == dict and \
            i['props']['children'] is not None and\
            i['props']['children'].startswith(('Table Relation','New column added','Filters'))]
    
    if add_val is not None and add_val != {} and any(add_col_menu) is False:
        add_id = [i['index'] for i in applied_id]
           
        add_col = DropdownMenuItem(f"New column added  X"\
            ,id={'type':'applied-changes-menu','index':max(add_id)+1})
        
        applied_changes.append(add_col)

    if (add_val is None or add_val == {}) and any(add_col_menu) is True:
        [applied_changes.remove(applied_changes[indx]) for indx,i in enumerate(applied_changes) \
            if type(i['props']['id']) == dict and \
            i['props']['children'] is not None and\
            i['props']['children'].startswith('New column added')]
    
    if fil_val is not None and fil_val != {} and any(filters_menu) is False:
        fil_id = [i['index'] for i in applied_id]
           
        fil = DropdownMenuItem(f"Filters  X"\
            ,id={'type':'applied-changes-menu','index':max(fil_id)+1})
        
        applied_changes.append(fil)
    if (fil_val is None or fil_val == {}) and any(filters_menu) is True:
        [applied_changes.remove(applied_changes[indx]) for indx,i in enumerate(applied_changes) \
            if type(i['props']['id']) == dict and \
            i['props']['children'] is not None and\
            i['props']['children'].startswith('Filters')]
    
    return applied_changes


# load table names to first dropdown options
@app.callback(
    Output({'type':'relationship-table-dropdown','index':0}, 'options'),
    [
        # Input('db-table-names','data'),
        Input('content', 'children')
    ]
)
def update_db_table_names(data):
    if data is not None and data != []:
        print("COntent-children")
        tb = get_table_names()
        x=[{'label':i,'value':i} for i in tb]
        # print(f"Table Names {x}")
        return x
    

# add new table dropdown
@app.callback(
    Output('tables-row', 'children'),
    [
        Input('add-table-button','n_clicks'),
        Input('retrived-data','data'),
        Input({'type':'relationship-table-close','index':ALL},'n_clicks'),
    ],
    [
        State('table-rows-save','data'),
        State({'type':'relationship-table-dropdown','index':ALL},'value'),
        State('db-table-names','data'),
        State('tables-row','children'),
    ]
)
def update_tables_row(clk,ret_data,rel_close_click,table_save,value,data,childs):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    
    
    if triggred_compo == 'add-table-button':
        x=data
        if None not in value:
            [x.remove(i) for i in value]
            component_id = len(value)

            options=[{'label':i,'value':i} for i in x]

            childs = str(childs)
            apply_clicks = re.findall("'apply-join-modal', 'index': [\d|None]*}, 'className': 'ml-auto'. 'n_clicks': [\d|None]*",childs)
            for s in apply_clicks:
                new_s=regex.sub("'n_clicks': [\d|None]*","'n_clicks': None",s)
                childs=childs.replace(s,new_s)


            # childs=regex.sub("'n_clicks': [\d|None]*","'n_clicks': None",childs)
            childs=ast.literal_eval(str(childs))

            mod = Modal([
                    ModalHeader(H5('Join on')),
                    ModalBody([
                        Div([
                            Row(Col(Dropdown(id={'type':'sql-join-modal','index':component_id},\
                                options=[{'label':i,'value':i} for i in ['LEFT', 'RIGHT', 'CROSS', 'INNER']]))),
                            Br(),
                            Row([
                                Col(H5(id={'type':'left-table-name','index':component_id})),
                                Col(H5(id={'type':'right-table-name','index':component_id}))
                            ]),
                            Row([
                                Col(Dropdown(id={'type':'left-table-join-modal','index':component_id})),
                                Col(Dropdown(id={'type':'right-table-join-modal','index':component_id}))
                            ]),
                            # Row(
                            #     Col(
                            #         H5(id={'type':'join-status','index':component_id})
                            #     )
                            # )
                            Div(Alert("Error",color='danger',is_open=False,id={"type":'join-status','index':component_id}))
                        ])
                    ]),
                    ModalFooter([
                        # Toast(id={"type":'join-status','index':component_id}),
                        Button("Apply",id={'type':'apply-join-modal','index':component_id},className='ml-auto'),
                        Button("Close",id={'type':'close-join-modal','index':component_id},className='ml-auto'),
                    ])
                ],id={'type':'join-modal','index':component_id},centered=True,size='lg')
            
            store = Store(id={'type':'sql-joins-query','index':component_id},data=None)

            childs.append(store)

            childs.append(mod)

            childs.append(
                {'props':{'children': {'props':{
                    'children':{'props':{'src':app.get_asset_url('sql-join-icon.png')},
                                'type':'Img',
                                'namespace':'dash_html_components'},

                    'id': {'type': 'relationship-sql-joins',
                                'index': component_id
                            },
                    },
                    'type':'A',
                    "namespace":'dash_html_components'
                },  
                "width":1},
                'type': 'Col',
                'namespace': 'dash_bootstrap_components'}
            )

            childs.append(
                {'props': {'children': {'props': {'id': {'type': 'relationship-table-dropdown',
                    'index': component_id},
                    'value': None,
                    'options':options},
                    'type': 'Dropdown',
                    'namespace': 'dash_core_components'},
                'width': 3},
                'type': 'Col',
                'namespace': 'dash_bootstrap_components'}
            )

            childs.append(
                Col(
                    A(
                        I(className='fa fa-times'),
                        id={'type':'relationship-table-close','index':component_id},
                    ),
                )
            )

            


            return childs
    elif triggred_compo.rfind('relationship-table-close') > -1:
        # indx = triggred_compo['index']
        indx = int(triggred_compo[9])

        childs_copy = childs.copy()

        for itm in childs_copy:
            try:
                if itm['props']['children']['props']['id']['index'] == indx:
                    childs.remove(itm)
            except:
                if itm['props']['id']['index'] == indx:
                    childs.remove(itm)

        return childs
    elif triggred_compo == 'retrived-data' and ret_data is not None:
        return ret_data['tables_rows']
    else:
        return childs

    
# enable or disable the Add table button and Run Button
@app.callback(
    [
        Output('add-table-button','disabled'),
        Output('preview-table-button','disabled'),
    ],

    [
        Input({'type':'relationship-table-dropdown','index':ALL},'value'),
        Input({'type':'relationship-sql-joins','index':ALL},'children'),
    ],
    [
        State({'type':'relationship-table-dropdown','index':ALL},'options')
    ]
)
def update_add_button_status(values,childs,options):
    #print(f'VALUES OPTIONS... {options}')
    y=[i['props']['src'] for i in childs[1:]]
    if None not in values and app.get_asset_url('sql-join-icon.png') not in y:
        return False, False
    else:
        return True, True


@app.callback(
    Output('table-dropdown-alert','is_open'),
    [
        # Input({'type':'relationship-sql-joins','index':ALL},'n_clicks'),
        Input({'type':'relationship-table-dropdown','index':ALL},'value'),
    ],
    [
        State({'type':'relationship-table-dropdown','index':ALL},'options'),
    ]

)
def update_table_dropdown_alert(value,options):
    #print(f"values **** {options}")
    if None not in value:
        return False
    else:
        return True
    

# load sql join table column names and modal open
@app.callback(
    [
        Output({'type':'join-modal','index':MATCH},'is_open'),
        Output({'type':'left-table-join-modal','index':MATCH},'options'),
        Output({'type':'right-table-join-modal','index':MATCH},'options'),
        Output({'type':'left-table-name','index':MATCH},'children'),
        Output({'type':'right-table-name','index':MATCH},'children')
    ],
    [
        Input({'type':'relationship-sql-joins','index':MATCH},'n_clicks'),
        Input({'type':'close-join-modal','index':MATCH},'n_clicks'),
        Input({'type':'join-status','index':MATCH},'is_open'),
    ],
    [
        State({'type':'relationship-table-dropdown','index':ALL},'value'),
        State({'type':'relationship-table-dropdown','index':ALL},'id'),
        State({'type':'relationship-sql-joins','index':MATCH},'id'),
        State({'type':'sql-joins-query','index':ALL},'data'),
    ]
)
def update_join_modal(n_clicks,close_n_clicks,is_open,value,id_1,id_2,sql_qry):
    # print(id_2)
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggred_compo.rfind('relationship-sql-joins') > -1 and n_clicks is not None and None not in value:
        index_no=id_2['index']
        index_no=[i for i,v in enumerate(id_1) if v['index'] == index_no][0]
        right_name = value[index_no]
        
        if sql_qry != [] and sql_qry[index_no-1] is not None:
            left_name = str(sql_qry[index_no-1]['table_names'][0]) + ' / ' + str(sql_qry[index_no-1]['table_names'][1])
            left_opt = [{'label':i,'value':i} for i in sql_qry[index_no-1]['col_list']]
        else:
            left_name = value[index_no-1]
            left_opt = [{'label':i,'value':i} for i in get_columns(left_name)]
            
        right_opt = [{'label':i,'value':i} for i in get_columns(right_name)]

        return True,left_opt,right_opt,left_name,right_name
    elif triggred_compo.rfind('close-join-modal') > -1 and close_n_clicks is not None:
        return False, [], [], 'None', 'None'
    elif triggred_compo.rfind('join-status') > -1 and is_open is False:
        return False, [], [], 'None', 'None'
    else:
        raise PreventUpdate

# update the join and relationship to main-sql-query memory
@app.callback(
    Output('main-sql-query','data'),
    [
        Input({'type':'sql-joins-query','index':ALL},'data'),
    ],
    [
        State({'type':'relationship-table-dropdown','index':ALL},'value'),
        State({'type':'relationship-table-dropdown','index':ALL},'id'),
    ]
)
def update_main_sql_query(data,rel_values,ids):
    sql_qry = [i for i in data if i]
    
    if sql_qry != []:
        rel_values=list(filter(None,rel_values))
        #print(f"RELATION SHIP {rel_values}")


        # print(f"IDS {ids}")
        status,qry_list=get_main_sql_query(sql_qry,rel_values)
        if status:
            return qry_list
        else:
            return None
    else:
        return None




# apply join function
@app.callback(
    [
        Output({'type':'sql-joins-query','index':MATCH},'data'),
        Output({'type':'relationship-sql-joins','index':MATCH},'children'),
        Output({'type':'join-status','index':MATCH},'is_open'),
    ],
    [
        Input({'type':'apply-join-modal','index':MATCH},'n_clicks')
    ],
    [
        State({'type':'left-table-name','index':MATCH},'children'),
        State({'type':'right-table-name','index':MATCH},'children'),

        State({'type':'left-table-join-modal','index':MATCH},'value'),
        State({'type':'right-table-join-modal','index':MATCH},'value'),
        State({'type':'sql-join-modal','index':MATCH},'value'),

        State({'type':'sql-joins-query','index':ALL},'data'),
        State({'type':'relationship-sql-joins','index':MATCH},'children'),
        State({'type':'join-status','index':MATCH},'is_open'),
        State({'type':'relationship-sql-joins','index':MATCH},'id'),

    ]
)
def update_on_apply_joins(n_clicks,tbl_l,tbl_r,value_l,value_r,join_value,\
    sql_qry,sql_join_icon,join_status,id_rel):

    # print(f"corona --- {id_rel}")
    # print(f"Corona -- {n_clicks}")

    if n_clicks is not None and value_l is not None and value_r is not None and\
        join_value is not None:

        compo_id  = id_rel['index']
        for i in sql_qry: # removing if the component if its already exists.
            if i is not None:
                if i['compo_id'] == compo_id:
                    sql_qry.remove(i)
                    

        d = {
            'table_names':[tbl_l,tbl_r],
            'join':join_value,
            'join_on':[value_l,value_r],
            'col_list':[],
            'compo_id':compo_id,
        }
        # print(f"{sql_qry}",flush=True)

        data,col_list = get_join_main(d,sql_qry)
        d['col_list']=col_list

        join_open = None
        # join_icon = None

        y = app.get_asset_url('sql-join-icon.png')
        if data != 'Error':
            if join_value == 'INNER':
                y=app.get_asset_url('sql-join-inner-icon.png')
            elif join_value == 'LEFT':
                y=app.get_asset_url('sql-join-left-icon.png')
            elif join_value == 'RIGHT':
                y=app.get_asset_url('sql-join-right-icon.png')
            elif join_value == 'CROSS':
                y=app.get_asset_url('sql-join-outer-icon.png')
            join_open = False
            # join_icon = "success"
        elif data == 'Error':
            y = app.get_asset_url('sql-join-icon.png')
            join_open = True
            # join_icon = "danger"
        
        rel_icon={'props':{'src':y},
                            'type':'Img',
                            'namespace':'dash_html_components'}
            
    
        return d, rel_icon, join_open
    else:
        sql_q = None
        compo_id  = id_rel['index']
        for i in sql_qry: # removing if the component if its already exists.
            if i is not None:
                if i['compo_id'] == compo_id:
                    sql_q = i

        return sql_q, sql_join_icon, join_status