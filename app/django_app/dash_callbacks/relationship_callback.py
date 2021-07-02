from flask_caching import Cache
from ..server import app
from dash.dependencies import Output, Input, State, MATCH, ALL
from dash import callback_context
from dash_core_components import Dropdown, Store
from dash_html_components import Div, H5, Br
from dash_bootstrap_components import Col, Row, Modal, ModalHeader, ModalFooter,\
    ModalBody, Button, DropdownMenuItem

from ..global_functions import get_columns, get_join_main

import json
from .. models import MsiFilters
import sys
import regex
import ast 

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


# show saved changes in a pop-up
@app.callback(
    [
        Output('saved-fil-modal','is_open'),
        Output('filter-radio-btn','options'),
    ],
    [
        Input('saved-filters-btn','n_clicks'),
    ],
    [
        State('saved-fil-modal','is_open')
    ]
)
def update_saved_filters(n_clicks,is_open):
    if n_clicks is not None:
        filters_objects = MsiFilters.objects.all().values()
         
        radio_options=[] 
        for i in filters_objects:
            fil_name = i['filter_name']
            fil_date = i['filter_date']

            option_name = str(fil_name) + ' ▬ ' + str(fil_date)
            radio_options.append(option_name)
        
        fil_options = [{'label':i,'value':i} for i in radio_options]
     
        return not is_open, fil_options
    else:
        return is_open, []


# Save applied changes to Database
@app.callback(
    Output('modal-sf-status','hidden'),
    [
        Input('modal-sf-save','n_clicks'),
    ],
    [
        State('save-changes','data'),
        State('modal-sf-filter-name','value'),
    ]
)
def save_to_db(n_clicks,data,fil_name):
    if n_clicks is not None and fil_name is not None:
        data = json.dumps(data)
        filter_data = MsiFilters(filter_name=fil_name,filter_data=data)
        filter_data.save()
        return False
    else:
        return True


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
            return json.loads(dat[0]['filter_data'])
        else:
            return None

    elif triggred_compo == 'saved-fil-modal-delete' and del_n_clicks is not None:
        fil_name = value.split('▬')[0].strip()
        fil_date = value.split('▬')[1].strip()

        try:
            dat = MsiFilters.objects.filter(filter_name=fil_name,filter_date=fil_date).delete()
        except:
            dat = None

        return None
    else:
        return None
    
# save modal open or close
@app.callback(
    Output('sf-modal','is_open'),
    [
        Input('run','n_clicks')
    ],
    [
        State('sf-modal','is_open')
    ]
)
def sf_modal_open(n_clicks,is_open):
    if n_clicks:
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

    if triggred_compo == 'relationship-data':
        save_changes_data['relationship_data']=relationship_data
        save_changes_data['filters_data']=filters_data
        save_changes_data['transformations_table_column_data']=transformations_table_column_data
        save_changes_data['transformations_filters_condi']=transformations_filters_condi
        tables_row = str(tables_row)
        tables_row=regex.sub("'n_clicks': \d*","'n_clicks': None",tables_row)
        tables_row=ast.literal_eval(str(tables_row))

        save_changes_data['tables_rows'] = tables_row
        
        filter_rows = str(filter_rows)
        filter_rows=regex.sub("'n_clicks': \d*","'n_clicks': None",filter_rows)
        filter_rows=ast.literal_eval(str(filter_rows))

        save_changes_data['filter_rows'] = filter_rows

        save_changes_data['sel_val'] = sel_drp_val
        save_changes_data['sel_col'] = sel_drp_col_val
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
    rel_val = relation_data['table']
    sel_val = filters_data['select_or_drop_columns']
    fil_val = filters_data['filters']

    relationship_menu = [True if type(i['props']['id']) == dict and \
            i['props']['children'] is not None and\
            i['props']['children'].startswith('Table Relation')\
            else False for indx,i in enumerate(applied_changes)]
    
    select_col_menu = [True if type(i['props']['id']) == dict and \
            i['props']['children'] is not None and\
            i['props']['children'].startswith('Select/Drop')\
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
            i['props']['children'].startswith(('Table Relation','Select/Drop','Filters'))]
    
    if sel_val is not None and sel_val != {} and any(select_col_menu) is False:
        sel_id = [i['index'] for i in applied_id]
           
        sel = DropdownMenuItem(f"Select/Drop Columns  X"\
            ,id={'type':'applied-changes-menu','index':max(sel_id)+1})
        
        applied_changes.append(sel)
    if (sel_val is None or sel_val == {}) and any(select_col_menu) is True:
        [applied_changes.remove(applied_changes[indx]) for indx,i in enumerate(applied_changes) \
            if type(i['props']['id']) == dict and \
            i['props']['children'] is not None and\
            i['props']['children'].startswith('Select/Drop')]
    
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
        Input('db-table-names','data'),
    ]
)
def update_db_table_names(data):
    x=[{'label':i,'value':i} for i in data]
    return x
    

# add new table dropdown
@app.callback(
    Output('tables-row', 'children'),
    [
        Input('add-table-button','n_clicks'),
        Input('retrived-data','data'),
    ],
    [
        State('table-rows-save','data'),
        State({'type':'relationship-table-dropdown','index':ALL},'value'),
        State('db-table-names','data'),
        State('tables-row','children'),
    ]
)
def update_tables_row(clk,ret_data,table_save,value,data,childs):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggred_compo == 'add-table-button':
        x=data
        if None not in value:
            [x.remove(i) for i in value]
            component_id = len(value)

            options=[{'label':i,'value':i} for i in x]

            mod = Modal([
                    ModalHeader(H5('Join on')),
                    ModalBody([
                        Div([
                            Row(Col(Dropdown(id={'type':'sql-join-modal','index':component_id},\
                                options=[{'label':i,'value':i} for i in ['left', 'right', 'outer', 'inner']]))),
                            Br(),
                            Row([
                                Col(H5(id={'type':'left-table-name','index':component_id})),
                                Col(H5(id={'type':'right-table-name','index':component_id}))
                            ]),
                            Row([
                                Col(Dropdown(id={'type':'left-table-join-modal','index':component_id})),
                                Col(Dropdown(id={'type':'right-table-join-modal','index':component_id}))
                            ]),
                            Row(
                                Col(
                                    H5(id={'type':'join-status','index':component_id})
                                )
                            )
                        ])
                    ]),
                    ModalFooter([Button("Apply",id={'type':'apply-join-modal','index':component_id},className='ml-auto')])
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
                    
                'width': 1},
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
        Input({'type':'relationship-sql-joins','index':ALL},'children')
    ],
)
def update_add_button_status(values,childs):
    
    y=[i['props']['src'] for i in childs[1:]]
    if None not in values and app.get_asset_url('sql-join-icon.png') not in y:
        return False, False
    else:
        return True, True


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
        
    ],
    [
        State({'type':'relationship-table-dropdown','index':ALL},'value'),
        State({'type':'relationship-table-dropdown','index':ALL},'id'),
        State({'type':'relationship-sql-joins','index':MATCH},'id'),
        State({'type':'sql-joins-query','index':ALL},'data'),
    ]
)
def update_join_modal(n_clicks,value,id_1,id_2,sql_qry):
        
    if n_clicks is not None and None not in value:
        index_no=id_2['index']
        right_name = value[index_no]

        if sql_qry != [] and sql_qry[index_no-1] is not None:
            left_name = str(sql_qry[index_no-1]['table_names'][0]) + ' / ' + str(sql_qry[index_no-1]['table_names'][1])
            left_opt = [{'label':i,'value':i} for i in sql_qry[index_no-1]['col_list']]
        else:
            left_name = value[index_no-1]
            left_opt = [{'label':i,'value':i} for i in get_columns(left_name)]
            
        right_opt = [{'label':i,'value':i} for i in get_columns(right_name)]

        return True,left_opt,right_opt,left_name,right_name
    else:
        return False,[],[],'None','None'


# apply join function
@app.callback(
    [
        Output({'type':'sql-joins-query','index':MATCH},'data'),
        Output({'type':'relationship-sql-joins','index':MATCH},'children'),
        Output({'type':'join-status','index':MATCH},'children'),
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
        State({'type':'join-status','index':MATCH},'children'),
        State({'type':'relationship-sql-joins','index':MATCH},'id'),

    ]
)
def update_on_apply_joins(n_clicks,tbl_l,tbl_r,value_l,value_r,join_value,\
    sql_qry,sql_join_icon,join_status,id_rel):

    if n_clicks is not None and value_l is not None and value_r is not None and\
        join_value is not None:

        compo_id  = id_rel['index']
        for i in sql_qry:
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

        data,col_list = get_join_main(d,sql_qry)
        d['col_list']=col_list

        y = app.get_asset_url('sql-join-icon.png')
        if data != 'Error':
            if join_value == 'inner':
                y=app.get_asset_url('sql-join-inner-icon.png')
            elif join_value == 'left':
                y=app.get_asset_url('sql-join-left-icon.png')
            elif join_value == 'right':
                y=app.get_asset_url('sql-join-right-icon.png')
            elif join_value == 'outer':
                y=app.get_asset_url('sql-join-outer-icon.png')
        elif data == 'Error':
            y = app.get_asset_url('sql-join-icon.png')
        
        rel_icon={'props':{'src':y},
                            'type':'Img',
                            'namespace':'dash_html_components'}
    
        
        
        return d, rel_icon, data
    else:
        return None, sql_join_icon, []