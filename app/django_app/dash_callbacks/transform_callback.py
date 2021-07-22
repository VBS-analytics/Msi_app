from numpy.core.multiarray import empty_like
from ..server import app, server
from dash.dependencies import Output, Input, State, ALL, MATCH
from dash import callback_context
from dash_core_components import Dropdown, Textarea, DatePickerRange, DatePickerSingle,\
    Checklist
from dash_core_components import Input as TextInput
from dash_html_components import H6, Br, Div, I
from dash_bootstrap_components import Col, Row, Button

import dash_html_components as dhc


from ..global_functions import get_transformations,\
    get_format_mapping, get_columns_dtypes, get_table_from_sql_query, get_column_values


from pandas import DataFrame, Series

from itertools import chain

import sys

from dash.exceptions import PreventUpdate

# add condition row
def get_condition_rows(columns,indx):
    return Row([
                Col(
                    Dropdown(
                        id={'type':'filters-column-names','index':indx},
                        options=[{'label':i,'value':i} for i in columns.keys()],
                        value=None
                    )
                ,width=4),

                Col(
                    Dropdown(id={'type':'filters-conditions','index':indx})
                ,width=3),

                Col(id={'type':'filters-text-drpdwn','index':indx},width=4),
            ],id={'type':'condition-rows','index':indx})

# generates the body for filter rows
def get_filter_rows(table_names,columns):
    col = columns
    return Div([
        Row(
            Col(
                Dropdown(
                    id='select_or_drop_rows_select_drop',
                    options=[{'label':i,'value':i} for i in ['Select','Drop']],
                    value=None
                )
            ,width=3),
        ),
        Row(Col(H6('where'),width=3)),

        
        Div([
            Row([
                
                Col(
                    Dropdown(
                        id={'type':'trans-column-names','index':0},
                        options=[{'label':i,'value':i} for i in columns.keys()],
                        value=None
                    )
                ,width=4),

                Col(
                    Dropdown(id={'type':'trans-conditions','index':0})
                ,width=3),

                
            ], id={'type':'condition-rows','index':0}),

        ],id='trans-conditional-div'),

        Row(Col(Button("add condition", size="sm",id='trans-add-condition'))),
        
    ])

# display the saved filters changes to front-end
@app.callback(
    Output('filters-div','children'),
    [
        Input('retrived-data','data'),
        Input('preview-table-button','n_clicks'),
        Input({'type':'applied-changes-menu','index':ALL},'n_clicks'),
    ],
    [
        State('filters-div','children'),
        State({'type':'applied-changes-menu','index':ALL},'children'),
    ],
)
def update_filter_div(data,n_clicks,menu_n_clicks,childs,apply_menu_child):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    empty_div = [
                Row(
                    Col(
                        Dropdown(
                            id='filters-select-drop',
                            options=[{'label':i,'value':i} for i in ['Select','Drop']],
                            value=None
                        )
                    ,width=3)
                ),

                Row(Col(H6('where'),width=3)),

                Div([
                    Row([
                        Col(
                            Dropdown(
                                id={'type':'filters-column-names','index':0},
                                value=None
                            )
                        ,width=4),

                        Col(
                            Dropdown(
                                id={'type':'filters-conditions','index':0}
                            )
                        ,width=3),

                        Col([
                            Dropdown(id={"type":'trans-multi-text','index':0},style={'display':'none'}),
                            Textarea(id={"type":'trans-text','index':0},style={'display':'none'}),
                            TextInput(id={'type':'trans-input','index':0},style={'display':'none'}),
                            DatePickerRange(id={'type':'trans-date-range','index':0},style={'display':'none'}),
                            DatePickerSingle(id={'type':'trans-date-single','index':0},style={'display':'none'}),
                            DatePickerSingle(id={'type':'trans-days-single','index':0},style={'display':'none'}),
                            Checklist(id={'type':'trans-use-current-date','index':0},style={'display':'none'}),
                        ],id={'type':'filters-text-drpdwn','index':0},width=4),

                    ],id={'type':'condition-rows','index':0}),

                    Row([
                        dhc.Button(id={'type':'logic-close','index':0},hidden=True)
                    ],
                    id={'type':'filters-logic','index':0}),


                ],id='filters-conditional-div'),

                Row(
                    Col(
                        Button('add condition', size='sm', id='filters-add-condition')
                    )
                ),
                
            ]

    if triggred_compo == 'retrived-data' and data is not None and data['filters_data']['filters'] != {}:
        return data['filter_rows']
    elif triggred_compo == 'preview-table-button':
        if n_clicks is not None:
            return empty_div
        else:
            raise PreventUpdate
    elif triggred_compo.rfind('applied-changes-menu') > -1:
        # print(f"{apply_menu_child}",flush=True)
        # print(f"{menu_n_clicks}",flush=True)

        if any(menu_n_clicks):
            for idx,i in enumerate(menu_n_clicks):
                if i is not None and i > 0:
                    if apply_menu_child[idx].startswith('Filters'):
                        return empty_div
        else:
            raise PreventUpdate
    else:
        return childs

# retrived status
@app.callback(
    Output('filters-retrived-status','data'),
    [
        Input('filters-add-condition','n_clicks'),
        Input('preview-table-button','n_clicks'),
        Input('filters-apply','n_clicks'),
        Input('select-drop-apply','n_clicks'),
    ],
    [
        State('filters-retrived-status','data')
    ]
)
def update_retrived_stat(fil_add_condi_n_clicks,previ_n_clicks,fil_apply_n_clicks,\
    sel_apply_n_clicks,data):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo == "filters-add-condition" and fil_add_condi_n_clicks is not None:
        return True
    elif triggred_compo == "preview-table-button" and previ_n_clicks is not None:
        return True
    elif triggred_compo == "filters-apply" and fil_apply_n_clicks is not None:
        return True
    elif triggred_compo == "select-drop-apply" and sel_apply_n_clicks is not None:
        return True
    else:
        return None


# Adds a new condition row for filter rows.
@app.callback(
    Output('filters-conditional-div','children'),
    [
        Input('filters-add-condition','n_clicks'),
    ],
    [
        State('filters-conditional-div','children'),
        State('transformations-table-column-data','data'),
        State('filters-retrived-status','data')
    ],
)
def update_filters_condition_div(n_clicks,childs,trans_columns,ret_stat):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggred_compo == 'filters-add-condition' and n_clicks is not None:
        indx = n_clicks + 1
        condition_row = get_condition_rows(trans_columns,indx)
        logic_and_or = Row([
            Col(
                Dropdown(id={'type':'logic-dropdown','index':indx},
                    options=[{'label':i,'value':i} for i in ["And","Or"]]
                )
            ,width=3),

            Col(
                dhc.Button(
                    I(className='fa fa-times'),
                    id={'type':'logic-close','index':indx},
                )
            ,width=2),
        ],id={'type':'filters-logic','index':indx})
        childs.append(Br())
        childs.append(logic_and_or)
        childs.append(condition_row)
        return childs
    else:
        raise PreventUpdate

# clear added filter component
@app.callback(
    [
        Output({'type':'condition-rows','index':MATCH},'children'),
        Output({'type':'filters-logic','index':MATCH},'children')
    ],
    [
        Input({'type':'logic-close','index':MATCH},'n_clicks')
    ],
    [
        State({'type':'logic-close','index':MATCH},'id'),
        State({'type':'condition-rows','index':MATCH},'children'),
        State({'type':'filters-logic','index':MATCH},'children')
    ]
)
def close_condition(n_clciks,id,childs,fil_childs):
    if n_clciks is not None:
        return None, None
    else:
        raise PreventUpdate

# Update condition dropdown based on column selected Eg: >, <, ==..etc
@app.callback(
    Output({'type':'filters-conditions','index':MATCH}, 'options'),
    [
        Input({'type':'filters-column-names','index':MATCH}, 'value'),
    ],
    [
        State({'type':'filters-column-names','index':MATCH},'id'),
        State('transformations-table-column-data','data'),
        State('retrived-data','data')
    ]
)
def update_filters_condition_dropdown(value,id,data,ret_data):
    if value is not None and data != {} and (data[value] == 'float64' or data[value] == 'int64'):
        return [{'label':i,'value':i} for i in ['<','<=','==','!=','>','>=', \
            'is missing','is not missing']]
    elif value is not None and data != {} and (data[value] == 'object' or data[value] == 'category'):
        return [{'label':i,'value':i} for i in ['has value(s)', 'starts with', \
            'contains','ends with','is missing','is not missing']]
    elif value is not None and data != {} and (data[value] == 'datetime64[ns]' or data[value] == 'datetime64'):
        return [{'label':i,'value':i} for i in ['days','before','after',\
            'not','equals','range','is missing','is not missing']]

    elif value is not None and data == {} and ret_data is not None and\
        (ret_data['transformations_table_column_data'][value] == 'float64' or\
            ret_data['transformations_table_column_data'][value] == 'int64'):
        return [{'label':i,'value':i} for i in ['<','<=','==','!=','>','>=', \
            'is missing','is not missing']]
    elif value is not None and data == {} and ret_data is not None and\
        (ret_data['transformations_table_column_data'][value] == 'object' or\
            ret_data['transformations_table_column_data'][value] == 'category'):
        return [{'label':i,'value':i} for i in ['has value(s)', 'starts with', \
            'contains','ends with','is missing','is not missing']]
    elif value is not None and data == {} and ret_data is not None and\
        (ret_data['transformations_table_column_data'][value] == 'datetime64[ns]'or\
            ret_data['transformations_table_column_data'][value] == 'datetime64'):
        return [{'label':i,'value':i} for i in ['days','before','after',\
            'not','equals','range','is missing','is not missing']]
    else:       
        return []

# add multi-dropdown or textbox based on condition selected
@app.callback(
    Output({'type':'filters-text-drpdwn',"index":MATCH},'children'),
    [
        Input({'type':'filters-conditions','index':MATCH},'value')
    ],

    [
        State({'type':'filters-conditions','index':MATCH},'id'),
        State({'type':'filters-text-drpdwn',"index":MATCH},'children'),
        State({'type':'filters-column-names','index':MATCH}, 'value'),
        
        State('relationship-data','data'),
        State('retrived-data','data'),
        State('filters-retrived-status','data')
    ]
)
def update_multi_drop_or_text(value,id,childs,column_name,relation_data,ret_data,ret_stat):
    indx = id['index'] 

    # textfile = open("example.txt", "w")
    # a = textfile.write(str(ret_data))
    # textfile.close()
    # print(f"{relation_data['saved_data']}",flush=True)
    # print(f"{ret_stat}",flush=True)


    
    if value is not None and ret_data is not None and ret_data['filters_data']['filters'] != {} and \
        relation_data is not None and relation_data['saved_data'] is True and ret_stat is None:
        dat_rows = ret_data['filter_rows'][2]['props']['children']
        lnth = len(dat_rows)
        
        for i in range(lnth):
            try:
                idx = dat_rows[i]['props']['children'][2]['props']['id']['index']
                # sys.stderr.write(str(dat_rows[i]['props']['children'][2]))
                # print(str(dat_rows[i]['props']['children'][2]),flush=True)

                if idx == indx:
                    return dat_rows[i]['props']['children'][2]
            except:
                pass
        
        if value in ['<','<=','==','>=','>','!=']:
            return Textarea(id={"type":'trans-text','index':indx},\
                persistence=True,value=None)

        elif value in ['starts with','contains','ends with']:
            return Textarea(id={"type":'trans-text','index':indx},\
                persistence=True,value=None)

        elif value in ['has value(s)'] and relation_data['table']!=[]:
            
            df1=get_column_values(relation_data['table'],column_name)
            # print(f"columns .. {df1.columns}")

            if type(df1) is Series:
                col=df1.unique()
            else:
                col=df1[column_name].unique
            return Dropdown(id={"type":'trans-multi-text','index':indx},
                        options=[{'label':i,'value':i} for i in col],
                        multi=True,
                        persistence=True,
                    )
        
        elif value in ['days'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],column_name)

            max_dt = df1.max()
            min_dt = df1.min()

            return Row([
                Col(TextInput(id={'type':'trans-input','index':indx},persistence=True,
                value=None)),

                Col([
                    DatePickerSingle(
                        id={'type':'trans-days-single','index':indx},
                        placeholder='mm/dd/YYYY',
                        min_date_allowed=min_dt,
                        max_date_allowed=max_dt,
                    ),

                    Checklist(
                        id={'type':'trans-use-current-date','index':indx},
                        options=[
                            {'label': 'Use current sys date', 'value': 'Use'},
                        ],
                        value=[]
                    ),
                ])
            ]) 
        
        elif value in ['before','after','equals','not'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],column_name)

            max_dt = df1.max()
            min_dt = df1.min()

            return DatePickerSingle(
                id={'type':'trans-date-single','index':indx},
                placeholder='mm/dd/YYYY',
                min_date_allowed=min_dt,
                max_date_allowed=max_dt,
            )
        
        elif value in ['range'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],column_name)
            max_dt = df1.max()
            min_dt = df1.min()

            return DatePickerRange(
                id={'type':'trans-date-range','index':indx},
                min_date_allowed=min_dt,
                max_date_allowed=max_dt,
            )
        else:
            return None
    elif value is not None and relation_data['table'] != []:
        
        if value in ['<','<=','==','>=','>','!=']:
            return Textarea(id={"type":'trans-text','index':indx},\
                persistence=True,value=None)

        elif value in ['starts with','contains','ends with']:
            return Textarea(id={"type":'trans-text','index':indx},\
                persistence=True,value=None)

        elif value in ['has value(s)'] and relation_data['table']!=[]:
            
            df1=get_column_values(relation_data['table'],column_name)
            # print(f"columns .. {df1.columns}")

            if type(df1) is Series:
                col=df1.unique()
            else:
                col=df1[column_name].unique
            return Dropdown(id={"type":'trans-multi-text','index':indx},
                        options=[{'label':i,'value':i} for i in col],
                        multi=True,
                        persistence=True,
                    )
        
        elif value in ['days'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],column_name)

            max_dt = df1.max()
            min_dt = df1.min()

            return Row([
                Col(TextInput(id={'type':'trans-input','index':indx},persistence=True,
                value=None)),

                Col([
                    DatePickerSingle(
                        id={'type':'trans-days-single','index':indx},
                        placeholder='mm/dd/YYYY',
                        min_date_allowed=min_dt,
                        max_date_allowed=max_dt,
                    ),

                    Checklist(
                        id={'type':'trans-use-current-date','index':indx},
                        options=[
                            {'label': 'Use current sys date', 'value': 'Use'},
                        ],
                        value=[]
                    ),
                ])
            ]) 
        
        elif value in ['before','after','equals','not'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],column_name)

            max_dt = df1.max()
            min_dt = df1.min()

            return DatePickerSingle(
                id={'type':'trans-date-single','index':indx},
                placeholder='mm/dd/YYYY',
                min_date_allowed=min_dt,
                max_date_allowed=max_dt,
            )
        
        elif value in ['range'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],column_name)
            max_dt = df1.max()
            min_dt = df1.min()

            return DatePickerRange(
                id={'type':'trans-date-range','index':indx},
                min_date_allowed=min_dt,
                max_date_allowed=max_dt,
            )
        else:
            return None
    else:
        return childs

# check applied filters for None
@app.callback(
    Output('select-drop-apply','disabled'),
    [
        Input('select-drop-select-drop','value'),
    ],
)
def check_applied_filters(sel_drp_val):
    if sel_drp_val is not None:
        return False
    else:
        return True


# load the save changes to select_drop columns filter
@app.callback(
    [
        Output('select-drop-select-drop','value'),
        Output('select-drop-col-names','value')
    ],
    [
        Input('retrived-data','data'),
        Input('preview-table-button','n_clicks'),
        Input({'type':'applied-changes-menu','index':ALL},'n_clicks'),
    ],
    [
        State('select-drop-select-drop','value'),
        State('select-drop-col-names','value'),
        State({'type':'applied-changes-menu','index':ALL},'children'),
    ]
)
def ret_changes(ret_data,n_clicks,menu_n_clicks,sel_val,sel_col_val,apply_childs):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo == 'retrived-data' and ret_data is not None:
        return ret_data['sel_val'],ret_data['sel_col']
    
    elif triggred_compo == 'preview-table-button':
        if n_clicks is not None:
            return None, []
        else:
            raise PreventUpdate
    elif triggred_compo.rfind('applied-changes-menu') > -1:
        if any(menu_n_clicks):
            for idx,i in enumerate(menu_n_clicks):
                if i is not None and i > 0:
                    if apply_childs[idx].startswith('Select'):
                        return None, []
        else:
            sys.stderr.write(str(menu_n_clicks))
            print(f"PREVENT UPDATE",flush=True)
            raise PreventUpdate
    else:
        return sel_val, sel_col_val


# enable or disable the apply button in filters row
@app.callback(
    Output('filters-apply','disabled'),
    [
        Input('filters-select-drop','value'),#select or drop rows
        Input({'type':'filters-column-names','index':ALL},'value'),
        Input({'type':'filters-conditions','index':ALL},'value'),
        Input({"type":'trans-text','index':ALL},'value'),
        Input({"type":'trans-multi-text','index':ALL},'value'),
        Input({'type':'trans-input','index':ALL},'value'),
        Input({'type':'trans-date-range','index':ALL},'start_date'),
        Input({'type':'trans-date-range','index':ALL},'end_date'),
        Input({'type':'trans-date-single','index':ALL},'date'),
        Input({'type':'trans-days-single','index':ALL},'date'),
        Input({'type':'trans-use-current-date','index':ALL},'value'),
        Input({'type':'logic-dropdown','index':ALL},'value'),
    ]
)
def enab_disa_filters_apply(fil_sel_drop,fil_col_names,fil_condi,trans_txt,\
    trans_multi_txt,trans_input,trans_dt_start,trans_dt_end,trans_dt_single,\
        trans_days_single,trans_current_date,logic_dropdown):
        if fil_sel_drop is not None and None not in fil_col_names and None not in fil_condi:
            text_area=False
            multi_drp=False
            single_dt=False
            txt_box=False
            range_dt=False
            sys_dt_chk=False
            single_days=False

            
            if any([True for i in fil_condi if i in ['starts with','contains','ends with','<','<=','==','>=','>','!=']]):
                text_area=True
            if any([True for i in fil_condi if i in ['has value(s)']]):
                multi_drp=True
            if any([True for i in fil_condi if i in ['days']]):
                single_days=True
                txt_box=True
                sys_dt_chk=True
            if any([True for i in fil_condi if i in ['before','after','equals','not']]):
                single_dt=True
            if any([True for i in fil_condi if i in ['range']]):
                range_dt=True

            chk=[]
            chk2=[]
            
            if single_days is True and txt_box is True and sys_dt_chk is True:
                chk2.append(trans_days_single)
                chk2.append(trans_input)
                chk2.append(trans_current_date)
            
            
            if text_area is True:
                chk.append(trans_txt)
            elif multi_drp is True:
                chk.append(trans_multi_txt)
            elif single_dt is True:
                chk.append(trans_dt_single)
            elif range_dt is True:
                chk.append(trans_dt_start)
                chk.append(trans_dt_end)
            

            rt=False
            rtt=False

            rt2=False
            rtt2=False


            if chk != []:
                for i in chk:
                    if all([True if k is not None and k !=[] and k != '' else False for k in i]) == True:
                        rt=True
                    else:
                        rtt=True

            
            if chk2 != []:
                z1=[True for i,j in zip(chk2[0],chk2[2]) if i != [] and i is not None and i != '' or j != []]

                if all([True if i is not None and i != [] and i != '' else False for i in chk2[1]]) is True and\
                    len(chk2[0]) == z1.count(True):

                    rt2=True
                else:
                    rtt2=True

            
            if rt is True and rtt is False and rt2 is False and rtt2 is False:
                return False
            elif rt is False and rtt is False and rt2 is True and rtt2 is False:
                return False
            elif rt is True and rtt is False and rt2 is True and rtt2 is False:
                return False
            else:
                return True
        else:
            return True


# enable or disable the date picker when current date is used.
@app.callback(
    [
        Output({'type':'trans-days-single','index':MATCH},'disabled'),
        Output({'type':'trans-days-single','index':MATCH},'date'),
    ],
    [
        Input({'type':'trans-use-current-date','index':MATCH},'value'),
    ],
    [
        State({'type':'trans-days-single','index':MATCH},'date'),
    ]
)
def update_state_date_picker(use_curr_date,date_pick):
    
    if use_curr_date == []:
        return False, date_pick
    else:
        return True, None


# transformations filters modal data feeding.
@app.callback(
    [
        Output('select-drop-col-names','options'),
        Output({'type':'filters-column-names','index':0},'options')
    ],
    [
        Input('transformations-dropdown','value'),
    ],
    [
        State('relationship-data','data'),
        State('transformations-table-column-data','data'),
    ]
)
def update_transformation_modal(value,data,trans_column_data):
    if value is not None and data != {}:
        if value == 'Select or drop columns':
            col = data['columns']
            return [{'label':i,'value':i} for i in col],[]

        elif value == 'Filter rows':
            # modal_head = H5(value)
            
            return [], [{'label':i,'value':i} for i in trans_column_data.keys()]
    else:
        return [], []


# transformations filter modal open and close.
@app.callback(
    [
        Output("select-drop-modal", "is_open"),
        Output('filters-modal','is_open'),
        Output('change-col-dtype-modal','is_open'),
    ],
    [
        Input('transformations-dropdown','value'),
        Input('change-col-dtype-modal','n_clicks'),
        Input("select-drop-close", "n_clicks"),
        Input('filters-close','n_clicks'),
    ],
    [
        State("select-drop-modal", "is_open"),
        State('filters-modal','is_open'),
        State('change-col-dtype-modal','is_open')
    ],
)
def transformation_modal_expand(trans_drop_value,change_col_aply, \
    sel_drp_close,fil_close,sel_drp_is_open,fil_is_open,change_col_dtype_is_open):

    if trans_drop_value is not None and trans_drop_value == 'Select or drop columns':
        if sel_drp_close:
            return not sel_drp_is_open, False, False
        return not sel_drp_is_open, False, False

    elif trans_drop_value is not None and trans_drop_value == 'Filter rows':
        if fil_close:
            return False, not fil_is_open, False
        return False, not fil_is_open, False
    
    elif trans_drop_value is not None and trans_drop_value == 'Change columns datatype':
        if change_col_aply:
            return False, False, not change_col_dtype_is_open
        return False, False, not change_col_dtype_is_open
    else:
        return False, False, False


# transformations table data feeding.
@app.callback(
    [
        Output('table','data'), # relationship table rows/data
        Output('table','columns'), # relationship table columns

        Output('format-table','data'), # format table rows/data
        Output('format-table','columns'), # format table columns


        Output('table-filter','data'),# filter table rows/data
        Output('table-filter','columns'),# filter table columns

        Output('relationship-data','data'), # Stores the relationship details
        Output('relation-rows','data'), # no of rows in table
        
        Output('transformations-table-column-data','data'), # stores the column names of filter table
        Output('transformations-filters-condi','data'), # stores the applied filters
        # Output('transformations-rows','data'),
        Output('download_data','data'), # stores all relations, filters and format mapping data

        Output('filters-data','data'), # stores all applied filters
        Output('table-rows-save','data'),
    ],
    [
        Input('preview-table-button','n_clicks'),
        Input('retrived-data','data'),
        Input({'type':'applied-changes-menu','index':ALL},'n_clicks'),

        Input('select-drop-apply','n_clicks'),
        Input('filters-apply','n_clicks'),
        Input('format-map-data','data'),
    ],
    [

        State('tables-row','children'),
        State('table','data'),
        State('table','columns'),
        State({'type':'relationship-table-dropdown','index':ALL},'value'),
        State({'type':'relationship-sql-joins','index':ALL},'children'),
        State('main-sql-query','data'),
        State('relationship-data','data'),
        State({'type':'applied-changes-menu','index':ALL},'children'),
        State('relation-rows','data'),

        State('table-filter','data'),
        State('table-filter','columns'),
        State('transformations-table-column-data','data'),
        State('transformations-filters-condi','data'),
        
        State('select-drop-select-drop','value'),
        State('select-drop-col-names','value'),
        State('transformations-dropdown','value'),
        State('filters-select-drop','value'),#select or drop rows
        State({'type':'filters-column-names','index':ALL},'value'),
        State({'type':'filters-conditions','index':ALL},'value'),#545445654
        State({"type":'trans-text','index':ALL},'value'),
        State({"type":'trans-multi-text','index':ALL},'value'),
        State({'type':'trans-input','index':ALL},'value'),
        State({'type':'trans-date-range','index':ALL},'start_date'),
        State({'type':'trans-date-range','index':ALL},'end_date'),
        State({'type':'trans-date-single','index':ALL},'date'),
        State({'type':'trans-days-single','index':ALL},'date'),
        State({'type':'trans-use-current-date','index':ALL},'value'),

        State({'type':'logic-dropdown','index':ALL},'value'),

        State({'type':'filters-column-names','index':ALL},'id'),
        State({'type':'filters-conditions','index':ALL},'id'),
        State({"type":'trans-text','index':ALL},'id'),
        State({"type":'trans-multi-text','index':ALL},'id'),
        State({'type':'trans-input','index':ALL},'id'),
        State({'type':'trans-date-range','index':ALL},'id'),
        State({'type':'trans-date-single','index':ALL},'id'),
        State({'type':'trans-days-single','index':ALL},'id'),
        State({'type':'trans-use-current-date','index':ALL},'id'),
        State({'type':'logic-dropdown','index':ALL},'id'),
        State('filters-data','data'),

        State('format-table','data'), # format table rows/data
        State('format-table','columns'), # format table column
        State('download_data','data'),
    ],

)

def update_table_all(rel_n_clicks,ret_data,menu_n_clicks,\
    sel_aply_n_clicks,fil_aply_n_clicks,format_data,table_row,rel_tbl_data,rel_tbl_col,\
    rel_tbl_drpdwn,rel_join,join_qry,relationship_data,apply_menu_child,\
    relation_rows,data,columns,trans_column_data,trans_fil_condi,sel_drp_val,\
    sel_drp_col_val,trans_value,fil_sel_val,fil_col,fil_condi,trans_text,trans_multi,\
    trans_input,trans_dt_start,trans_dt_end,trans_dt_single,trans_days_single,\
    trans_use_current_dt,logic_val,fil_col_id,fil_condi_id,trans_text_id,\
    trans_multi_id,trans_input_id,trans_dt_id,trans_dt_single_id,trans_days_id,\
    trans_use_curr_id,logic_val_id,filters_data,formt_tbl_data,formt_tbl_col,\
    download_data):

    ctx = callback_context
    table_data = data
    table_columns = columns
    trans_col = trans_column_data
    rows = relation_rows
    csv_string = download_data

    relationship_table_data = rel_tbl_data
    relationship_table_columns = rel_tbl_col
    relationship_data = relationship_data
    table_rows_no = relation_rows

    

    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]
    # print(f"##### {triggred_compo}",flush=True)


    col={}
    
    if format_data is not None and format_data != {}:
        col={}
        [col.update({j:i}) for i,j in format_data.items()]
    elif ret_data is not None:
        if ret_data['format_map_data'] is not None and ret_data['format_map_data'] != {}:
            col={}
            [col.update({j:i}) for i,j in ret_data['format_map_data'].items()]
    
    index_k = 0 if filters_data['index_k'] is None else filters_data['index_k']

    
    if triggred_compo == 'select-drop-apply':
        if sel_drp_val is not None:
            # keys = list(fil_data['select_or_drop_columns'].keys())
            # if keys != []:
            k = None
            if index_k != 0 and filters_data['select_or_drop_columns'] != {}:
                check_val = True if index_k in filters_data['select_or_drop_columns'].keys() else False

                if check_val is False:
                    idx = list(filters_data['select_or_drop_columns'].keys())[0]
                    filters_data['select_or_drop_columns'].pop(str(idx))
                    k = int(idx)
                else:
                    filters_data['select_or_drop_columns'].pop(str(index_k))
                    k = int(index_k)

            i_k = None
            if k is not None and int(k) < filters_data['index_k']:
                i_k = filters_data['index_k']
            elif k is not None and int(k) >= filters_data['index_k']:
                i_k = k

            k = k if k is not None else index_k + 1

            filters_data['select_or_drop_columns'].update({
                k:{
                    'select_drop':sel_drp_val,
                    'column_names':sel_drp_col_val
                }
            })
            filters_data['index_k']=k if i_k is None else i_k

            relationship_data['saved_data']=False
            
            
            if filters_data['index_k'] is not None:
                df,sql_qry,rows, csv_string = get_transformations(relationship_data,filters_data,col)
                # df = df.fillna('None')
                table_data_format=df.to_dict('records')
                table_columns_format=[{"name": c, "id": c} for c in df.columns]

                column_dtypes =get_columns_dtypes(df.dtypes.to_dict().items())
                table_columns_fil=[{"name": c, "id": c} for c in column_dtypes]

                trans_col = {}
                [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]

                col_rename={}
                [col_rename.update({i:j}) for i,j in zip(df.columns,column_dtypes)]
                df = df.rename(columns=col_rename)
                table_data_fil = df.to_dict('records')

                return rel_tbl_data,rel_tbl_col,table_data_format, table_columns_format,\
                    table_data_fil, table_columns_fil,relationship_data,rows,\
                    trans_col, sql_qry,csv_string,filters_data,table_row
            else:
                return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                    table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                    csv_string,filters_data,table_row
    
    elif triggred_compo == 'filters-apply':
        # keys = list(filters_data['filters'].keys())
        in_k = None

        if index_k != 0 and filters_data['filters'] != {}:
            check_val = True if index_k in filters_data['filters'].keys() else False

            if check_val is False:
                idx = list(filters_data['filters'].keys())[0]
                filters_data['filters'].pop(str(idx))
                in_k = int(idx)
            else:
                filters_data['filters'].pop(str(index_k))
                in_k = int(index_k)
            
        i_k = None
        if in_k is not None and int(in_k) < filters_data['index_k']:
            i_k = filters_data['index_k']
        elif in_k is not None and int(in_k) >= filters_data['index_k']:
            i_k = in_k


        # if fil_col_id filters_data['filters'][index_k]['index']
        in_k = in_k if in_k is not None else index_k+1
        filters_data['filters'].update({
            in_k:{
                'select_drop':None,
                'index':[],
                'columns':[],
                'condition':[],
                'values':[],
                'logic':[]
            }
        })
        

        trans_text_id=[i['index'] for i in trans_text_id]
        trans_multi_id=[i['index'] for i in trans_multi_id]
        fil_col_id=[i['index'] for i in fil_col_id]
        trans_input_id=[i['index'] for i in trans_input_id]
        trans_dt_id=[i['index'] for i in trans_dt_id]
        trans_dt_single_id = [i['index'] for i in trans_dt_single_id]
        trans_days_id = [i['index'] for i in trans_days_id]
        trans_use_curr_id = [i['index'] for i in trans_use_curr_id]

        x={'index':[],'val':[]}
        [(x['index'].append(i),x['val'].append(j)) for i,j in \
            zip(trans_text_id,trans_text)]
        [(x['index'].append(i),x['val'].append(j)) for i,j in \
            zip(trans_multi_id,trans_multi)]
        # [(x['index'].append(i),x['val'].append(j)) for i,j in \
        #     zip(trans_days_id,trans_days_single)]
        # [(x['index'].append(i),x['val'].append(j)) for i,j in \
        #     zip(trans_use_curr_id,trans_use_current_dt)]
        [(x['index'].append(i),x['val'].append(j)) for i,j in \
            zip(trans_dt_single_id,trans_dt_single)]
        # [(x['index'].append(i),x['val'].append(j)) for i,j in \
        #     zip(trans_input_id,trans_input)]
        # [(x['index'].append(i),x['val'].append(j)) for i,j in \
        #     zip(trans_dt_single_id,trans_dt_single)]
        [(x['index'].append(i),x['val'].append(j)) for i,j in \
            zip(trans_dt_id,zip(trans_dt_start,trans_dt_end))]
        
        # x_l=len(trans_dt_single_id)
        # y_l=len(trans_input_id)

        # z=[None for i in range(abs(x_l-y_l))]

        # if x_l < y_l:
        #     trans_dt_single=list(chain(trans_dt_single,z))
        #     trans_dt_single_id=list(chain(trans_dt_single_id,z))
        # elif y_l < x_l:
        #     trans_input=list(chain(trans_input,z))
        #     trans_input_id=list(chain(trans_input_id,z))
        
        for indx, idx_1 in zip(range(len(trans_input_id)),trans_use_curr_id):
            if trans_use_current_dt[indx] != []:
                x['index'].append(idx_1)
                x['val'].append([trans_input[indx],trans_use_current_dt[indx]])
            elif trans_days_single[indx] is not None:
                x['index'].append(idx_1)
                x['val'].append([trans_input[indx],trans_days_single[indx]])

        
        indx_ismis = [i for i,v in zip(fil_col_id,fil_condi) if v == 'is missing']
        indx_isntmis = [i for i,v in zip(fil_col_id,fil_condi) if v == 'is not missing']

        if indx_ismis != []:
            [(x['index'].append(v),x['val'].append('IS-None')) for v in indx_ismis]
        if indx_isntmis != []:
            [(x['index'].append(v),x['val'].append('NOT-None')) for v in indx_isntmis]

        logic_val.insert(0,None)

        logic_val_id = [i['index'] for i in logic_val_id]
        logic_val_id.insert(0,00)

        y={
            'index':fil_col_id,
            'fil_condi':fil_condi,
            'fil_col':fil_col,
            
        }

        z={
            'logi_id':logic_val_id,
            'logic_val':logic_val
        }

        x = DataFrame(x).sort_values(by='index')['val'].to_list()
        y = DataFrame(y).sort_values(by='index').reset_index()
        z = DataFrame(z).sort_values(by='logi_id').reset_index()


        for i,k,j,v,l in zip(y['fil_col'],y['fil_condi'],y['index'],x,z['logic_val']):
            filters_data['filters'][in_k]['index'].append(j)
            filters_data['filters'][in_k]['condition'].append(k)
            filters_data['filters'][in_k]['columns'].append(i)
            filters_data['filters'][in_k]['values'].append(v)
            filters_data['filters'][in_k]['logic'].append(l)
        filters_data['filters'][in_k]['select_drop']=fil_sel_val
        filters_data['index_k']=in_k if i_k is None else i_k

        relationship_data['saved_data']=False
        

        if filters_data['index_k'] is not None:
            df,sql_qry,rows, csv_string = get_transformations(relationship_data,filters_data,col)
            # df = df.fillna('None')
            table_data_format=df.to_dict('records')
            table_columns_format=[{"name": c, "id": c} for c in df.columns]

            column_dtypes =get_columns_dtypes(df.dtypes.to_dict().items())
            table_columns_fil=[{"name": c, "id": c} for c in column_dtypes]

            trans_col = {}
            [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]

            col_rename={}
            [col_rename.update({i:j}) for i,j in zip(df.columns,column_dtypes)]
            df = df.rename(columns=col_rename)
            table_data_fil = df.to_dict('records')

            return rel_tbl_data,rel_tbl_col,table_data_format, table_columns_format,\
                table_data_fil, table_columns_fil,relationship_data,rows,\
                trans_col, sql_qry,csv_string,filters_data,table_row
        else:
            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                csv_string,filters_data,table_row


    elif triggred_compo == 'preview-table-button':

        # result = check_if_all_none(join_qry)
        rel_tbl_drpdwn=list(filter(None,rel_tbl_drpdwn))

        if join_qry is None and rel_tbl_drpdwn != []:
            if rel_tbl_drpdwn[0] is not None:
                df,table_rows_no,csv_string=get_table_from_sql_query(rel_tbl_drpdwn[0],rel_tbl_drpdwn)
                table_names = rel_tbl_drpdwn[0]
        
        elif join_qry is not None:
            df,table_rows_no,csv_string=get_table_from_sql_query(join_qry,rel_tbl_drpdwn)
            table_names = join_qry
            
        else:
            df=DataFrame()
            table_rows_no = 0
        
        relationship_data["table"]=table_names
        relationship_data['columns']=list(df.columns)
        relationship_data['saved_data']=False
        relationship_data['table_order']=rel_tbl_drpdwn

        table_data_rel=table_data_format=df.to_dict('records')
        table_columns_rel=table_columns_format=[{"name": c, "id": c} for c in df.columns]

        column_dtypes = get_columns_dtypes(df.dtypes.to_dict().items())
        table_columns_fil=[{"name": c, "id": c} for c in column_dtypes]

        trans_col = {}
        [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]

        col_rename={}
        [col_rename.update({i:j}) for i,j in zip(df.columns,column_dtypes)]
        df = df.rename(columns=col_rename)
        # print(f"{df.columns}")
        table_data_fil = df.to_dict('records')


        # col = [{"name": i, "id": i} for i in ["column-1","column-2","column-3"]]
        # rel = dict(table=[],columns=None,saved_data=False)
        fil_data = dict(
                    select_or_drop_columns=dict(),
                    filters=dict(),
                    index_k=None,
                )
        # return [],col,[],col,[],col,rel,0,{},None,'',fil_data,[]
        
            
        return table_data_rel, table_columns_rel,table_data_format, table_columns_format,\
            table_data_fil, table_columns_fil,relationship_data, table_rows_no,\
            trans_col,None,csv_string,fil_data,table_row
    

    elif triggred_compo == 'retrived-data' and ret_data is not None:
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

        # df = df.fillna('None')
        table_row = ret_data['tables_rows']
        
        table_data_rel=df.to_dict('records')
        table_columns_rel=[{"name": c, "id": c} for c in df.columns]     
        relationship_data["table"]=table_names
        relationship_data['columns']=df.columns
        relationship_data['saved_data']=True
        relationship_data['table_order']=tbl_order

        if ret_data['filters_data']['index_k'] is not None:
            df,sql_qry,rows,csv_string = get_transformations(relationship_data,ret_data['filters_data'],col)
            # df = df.fillna('None')

            table_data=df.to_dict('records')
            table_columns=[{"name": c, "id": c} for c in df.columns]
            
            column_dtypes = get_columns_dtypes(df.dtypes.to_dict().items())
            table_columns_fil=[{"name": c, "id": c} for c in column_dtypes]
                
            trans_col = {}
            [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]

            col_rename={}
            [col_rename.update({i:j}) for i,j in zip(df.columns,column_dtypes)]
            df = df.rename(columns=col_rename)
            table_data_fil = df.to_dict('records')
            filters_data = ret_data['filters_data']


            if ret_data['format_map_data'] != {}:
                d = {'column_names':[]}
                d["column_names"]=list(ret_data['format_map_data'].values())
                # col={}
                # [col.update({j:i}) for i,j in ret_data['format_map_data'].items()]
                # print(col)

                df, csv_string = get_format_mapping(relationship_data,d,sql_qry,col)
                # df = df.fillna('None')
                if df is not None:
                    z={}
                    [z.update({i:df[j]}) for i,j in ret_data['format_map_data'].items()]

                    # trans_col = {}
                    # [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]

                    df = DataFrame(z)
                    table_data_format=df.to_dict('records')
                    table_columns_format=[{"name": c, "id": c} for c in df.columns]

                    return table_data_rel,table_columns_rel,table_data_format,\
                        table_columns_format, table_data_fil, table_columns_fil,\
                        relationship_data,rows,trans_col,sql_qry,csv_string,filters_data,table_row
                else:
                    return table_data_rel,table_columns_rel,table_data, table_columns,\
                        table_data_fil, table_columns_fil,\
                        relationship_data,rows,trans_col, sql_qry,csv_string,filters_data,table_row
            else:
                return table_data_rel,table_columns_rel,table_data, table_columns,\
                    table_data_fil, table_columns_fil,\
                    relationship_data,rows,trans_col, sql_qry,csv_string,filters_data,table_row

        else:
            print('Second Condition',flush=True)
            if relationship_data['table']!=[] and relationship_data['table'] is not None:
                
                rel_tbl_drpdwn=list(filter(None,relationship_data['table_order']))

                df,rows,csv_string=get_table_from_sql_query(relationship_data['table'],rel_tbl_drpdwn)
                # df = df.fillna('None')

                table_data_rel=df.to_dict('records')
                table_columns_rel=[{"name": c, "id": c} for c in df.columns]

                table_data_format=df.to_dict('records')
                table_columns_format=[{"name": c, "id": c} for c in df.columns]

                column_dtypes = get_columns_dtypes(df.dtypes.to_dict().items())
                table_columns_fil=[{"name": c, "id": c} for c in column_dtypes]

                trans_col = {}
                [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]

                col_rename={}
                [col_rename.update({i:j}) for i,j in zip(df.columns,column_dtypes)]
                df = df.rename(columns=col_rename)
                table_data_fil = df.to_dict('records')

                if ret_data['format_map_data'] != {}:
                    d = {'column_names':[]}
                    d["column_names"]=list(ret_data['format_map_data'].values())
                    # col={}
                    # [col.update({j:i}) for i,j in ret_data['format_map_data'].items()]
                    # print(col)

                    df, csv_string = get_format_mapping(relationship_data,d,None,col)
                    # df = df.fillna('None')
                    if df is not None:
                        z={}
                        [z.update({i:df[j]}) for i,j in ret_data['format_map_data'].items()]

                        # trans_col = {}
                        # [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]

                        df = DataFrame(z)
                        table_data_format=df.to_dict('records')
                        table_columns_format=[{"name": c, "id": c} for c in df.columns]

                        return table_data_rel,table_columns_rel,table_data_format,\
                            table_columns_format, table_data_fil, table_columns_fil,\
                            relationship_data,rows,trans_col,trans_fil_condi,csv_string,filters_data,table_row
                    else:
                        return table_data_rel,table_columns_rel,table_data, table_columns,\
                            table_data_fil, table_columns_fil,\
                            relationship_data,rows,trans_col, trans_fil_condi,csv_string,filters_data,table_row

            return table_data_rel,table_columns_rel,table_data_format,\
                table_columns_format,table_data_fil, table_columns_fil,\
                relationship_data,rows,trans_col,trans_fil_condi,csv_string,filters_data,table_row
    
    elif triggred_compo == 'format-map-data':
        d = {'column_names':[]}

        relationship_data['saved_data']=False

        if format_data != {} and format_data is not None:
            d["column_names"]=list(format_data.values())
            # col={}
            # [col.update({j:i}) for i,j in format_data.items()]

            df, csv_string = get_format_mapping(relationship_data,d,trans_fil_condi,col)

            
            # df = df.fillna('None')
            if df is not None:
                z={}
                [z.update({i:df[j]}) for i,j in format_data.items()]
                

                # trans_col = {}
                # [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]
                # sys.stderr.write(str(df.columns))
                # sys.stderr.write(str(z))
                # print(f"\n{df.columns}",flush=True)
                # print(f"\n{}",flush=True)

                df = DataFrame(z)
                table_data_format=df.to_dict('records')
                table_columns_format=[{"name": c, "id": c} for c in df.columns]
                #print(f"format map {df.columns}")
                return rel_tbl_data,rel_tbl_col,table_data_format,table_columns_format,\
                    data,columns, relationship_data,rows,trans_col,trans_fil_condi,\
                    csv_string,filters_data,table_row
            else:
               return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,data,columns,relationship_data,\
                   rows,trans_column_data,trans_fil_condi,csv_string,filters_data,table_row
        else:
            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,data,columns,relationship_data,\
                rows,trans_column_data, trans_fil_condi,csv_string,filters_data,table_row
    
    elif triggred_compo.rfind('applied-changes-menu') > -1:
        # print(f"{apply_menu_child}",flush=True)
        if any(menu_n_clicks):
            for idx,i in enumerate(menu_n_clicks):

                if i is not None and i > 0:
                    relationship_data['saved_data']=False
                    if apply_menu_child[idx].startswith('Table Relation') or apply_menu_child[idx].startswith('Clear'):
                        col = [{"name": i, "id": i} for i in ["column-1","column-2","column-3"]]
                        rel = dict(table=[],columns=None,saved_data=False)
                        fil_data = dict(
                                    select_or_drop_columns=dict(),
                                    filters=dict(),
                                    index_k=None,
                                )
                        return [],col,[],col,[],col,rel,0,{},None,'',fil_data,[]

                    elif apply_menu_child[idx].startswith('Select/Drop'):
                        indx = filters_data['index_k']
                        # sel_keys = list(filters_data['select_or_drop_columns'].keys())
                        fil_keys = list(filters_data['filters'].keys())

                        if int(indx) == 1 and filters_data['select_or_drop_columns'] != {}:
                            # delete the select_or_drop
                            filters_data['select_or_drop_columns'].popitem()
                            filters_data['index_k']=0

                        elif int(indx) > 1 and filters_data['select_or_drop_columns']:
                            # delete the select_or_drop
                            filters_data['select_or_drop_columns'].popitem()
                            new_indx = int(indx) - 1
                            
                            if abs(new_indx - int(fil_keys[0])) == 1:
                                pop_item = filters_data['filters'].popitem()
                                filters_data['filters']={new_indx:pop_item[1]}
                                
                            filters_data['index_k']=new_indx

                        if filters_data['index_k'] is not None:
                            df,sql_qry,rows, csv_string = get_transformations(relationship_data,filters_data,col)
                            # df = df.fillna('None')
                            table_data_format=df.to_dict('records')
                            table_columns_format=[{"name": c, "id": c} for c in df.columns]

                            column_dtypes =get_columns_dtypes(df.dtypes.to_dict().items())
                            table_columns_fil=[{"name": c, "id": c} for c in column_dtypes]

                            trans_col = {}
                            [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]

                            col_rename={}
                            [col_rename.update({i:j}) for i,j in zip(df.columns,column_dtypes)]
                            df = df.rename(columns=col_rename)
                            table_data_fil = df.to_dict('records')

                            return rel_tbl_data,rel_tbl_col,table_data_format, table_columns_format,\
                                table_data_fil, table_columns_fil,relationship_data,rows,\
                                trans_col, sql_qry,csv_string,filters_data,table_row
                        else:
                            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                            csv_string,filters_data,table_row

                    elif apply_menu_child[idx].startswith('Filters'):
                        indx = filters_data['index_k']
                        
                        sel_keys = list(filters_data['select_or_drop_columns'].keys())
                        # fil_keys = list(filters_data['filters'].keys())

                        if int(indx) == 1 and filters_data['filters'] != {}:
                            # delete the select_or_drop
                            filters_data['filters'].popitem()
                            filters_data['index_k']=0

                        elif int(indx) > 1 and filters_data['filters'] != {}:
                            # delete the select_or_drop
                            filters_data['filters'].popitem()
                            new_indx = int(indx) - 1
                            
                            if abs(new_indx - int(sel_keys[0])) == 1:
                                pop_item = filters_data['select_or_drop_columns'].popitem()
                                filters_data['select_or_drop_columns']={new_indx:pop_item[1]}
                                
                            filters_data['index_k']=new_indx
                        
                        

                        if filters_data['index_k'] is not None:

                            df,sql_qry,rows, csv_string = get_transformations(relationship_data,filters_data,col)
                            # df = df.fillna('None')
                            table_data_format=df.to_dict('records')
                            table_columns_format=[{"name": c, "id": c} for c in df.columns]

                            column_dtypes =get_columns_dtypes(df.dtypes.to_dict().items())
                            table_columns_fil=[{"name": c, "id": c} for c in column_dtypes]

                            trans_col = {}
                            [trans_col.update({i:str(j)}) for i,j in df.dtypes.to_dict().items()]

                            col_rename={}
                            [col_rename.update({i:j}) for i,j in zip(df.columns,column_dtypes)]
                            df = df.rename(columns=col_rename)
                            table_data_fil = df.to_dict('records')

                            return rel_tbl_data,rel_tbl_col,table_data_format, table_columns_format,\
                                table_data_fil, table_columns_fil,relationship_data,rows,\
                                trans_col, sql_qry,csv_string,filters_data,table_row
                        else:
                            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                            csv_string,filters_data,table_row

                    else:
                        return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                            csv_string,filters_data,table_row
        else:
            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                csv_string,filters_data,table_row
            # raise PreventUpdate

    else:
        return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,data,columns,relationship_data,\
            rows,trans_column_data, trans_fil_condi,csv_string,filters_data,table_row