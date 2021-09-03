from numpy.core.multiarray import empty_like
from ..server import app, server
from dash.dependencies import Output, Input, State, ALL, MATCH
from dash import callback_context
from dash_core_components import Dropdown, Textarea, DatePickerRange, DatePickerSingle,\
    Checklist, RadioItems
from dash_core_components import Input as TextInput
from dash_html_components import H6, Br, Div, I, Hr, A, Strong
from dash_bootstrap_components import Col, Row, Button, Form, FormGroup,FormText,\
    Label


import dash_html_components as dhc


from ..global_functions import get_transformations,\
    get_format_mapping, get_columns_dtypes, get_table_from_sql_query, get_column_values


from pandas import DataFrame, Series

from itertools import chain

import sys

from dash.exceptions import PreventUpdate

from datetime import date
import re
import ast


def get_filter_records(filters_data,trans_text_id,trans_multi_id,fil_col_id,\
    trans_input_id,trans_dt_id,trans_dt_single_id,trans_days_id,trans_use_curr_id,
    trans_text,trans_multi,trans_dt_single,trans_dt_start,trans_dt_end,trans_use_current_dt,
    trans_input,trans_days_single,fil_condi,logic_val,logic_val_id,fil_col,fil_sel_val,
    relationship_data,col):

    index_k = 0 if filters_data['index_k'] is None else filters_data['index_k']
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
        return df,sql_qry,rows, csv_string
    else:
        return None,None,None,None

# add condition row
def get_condition_rows(columns,indx):
    return Row([
        Col(
            FormGroup([
                Label(Strong("Select column name"),html_for={'type':'filters-column-names','index':indx}),
                Dropdown(
                    id={'type':'filters-column-names','index':indx},
                    options=[{'label':i,'value':i} for i in columns.keys()],
                    value=None
                )
            ])
        ,width=4),

        Col(
            FormGroup([
                Label(Strong("condition"),html_for={'type':'filters-conditions','index':indx}),
                Dropdown(
                    id={'type':'filters-conditions','index':indx}
                )
            ])
        ,width=3),

        Col(id={'type':'filters-text-drpdwn','index':indx},width=4),

        Col(A(I(className="fa fa-trash-o"),id={'type':'logic-close','index':indx}),className="text-right"),

    ],id={'type':'condition-rows','index':indx})

# remove added new column
@app.callback(
    Output('add-new-col-modal-apply','disabled'),
    [
        Input({"type":"add-new-col-name","index":ALL},'value'),
        Input({"type":'add-col-value-input',"index":ALL},'value'),
    ]
)
def update_add_new_col_apply(col_name_val, col_input_val):
    if all(col_name_val) and col_name_val != [] and all(col_input_val) and col_input_val != []:
        return False
    else:
        return True

@app.callback(
    Output('add-new-col','data'),
    [
        Input('add-new-col-modal-apply','n_clicks')
    ],
    [
        State({"type":"add-new-col-name","index":ALL},'value'),
        State({"type":'add-col-value-input',"index":ALL},'value'),
        State('filters-data','data'), # stores all applied filters
    ]
)
def update_add_new_col_values(n_clicks,col_name_val,col_input_val,filters_data):
    if n_clicks is not None:
        if all(col_name_val) and col_name_val != [] and all(col_input_val) and col_input_val != []:
            qry_str = ""
            for col_name, col_val in zip(col_name_val,col_input_val):
                if qry_str == "":
                    qry_str = qry_str + str(col_val) + ' AS ' + str(col_name)
                else:
                    qry_str = qry_str + ', ' + str(col_val) + ' AS ' + str(col_name)
            
            
            return dict(add_col_names=col_name_val,add_col_qry=qry_str)
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# add new column button
@app.callback(
    Output('add-col-form','children'),
    [
        Input('add-col-new-col-but','n_clicks'),
        Input({'type':'add-col-remove','index':ALL},'n_clicks'),
    ],
    [
        State('add-col-form','children'),
        State({'type':'add-col-remove','index':ALL},'id'),
    ]
)
def update_add_col_div(n_clicks,trash_n_clicks,childs,add_col_remove_id):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo == "add-col-new-col-but" and n_clicks is not None:
        indx = n_clicks+1
        
        grp_1 = FormGroup([
                    Col(A(I(className="fa fa-trash"),id={'type':'add-col-remove','index':indx}),className="text-right"),
                    dhc.Label("Enter column name"),
                    TextInput(id={"type":"add-new-col-name","index":indx},type="text",minLength=5,required=True),
                    FormText("Type column name without any spaces, special characters. Except 'underscore '_''",color="secondary"),
                ],id={"type":'add-col-grp-1','index':indx})
        
        grp_2 = FormGroup([
                    dhc.Label("Assign value to new column"),
                    # RadioItems(
                    #         options=[{'label':i,'value':i} for i in zip(["single value","conditional value"])],
                    #         id={"type":"add-col-value-radio","index":indx},
                    # ),
                    TextInput(id={"type":'add-col-value-input',"index":indx},type='text',required=True),
                ],id={"type":'add-col-grp-2','index':indx})
        
        
        # childs.append(trash_but)
        childs.append(grp_1)
        childs.append(grp_2)
        childs.append(Hr(id={"type":'add-col-hr-3','index':indx}))
        return childs

    elif triggred_compo.rfind('add-col-remove') > -1:
        indx=None
        if any(trash_n_clicks):
            indx = [idx for idx,i in enumerate(trash_n_clicks) if i is not None and i > 0]
            indx = add_col_remove_id[indx[0]]
            indx = indx['index']    

        childs_copy = childs.copy()
                    

        if indx is not None:
            for idx,i in enumerate(childs):
                if i['props']['id']['index'] == int(indx):
                    childs_copy.remove(i)
            return childs_copy
        raise PreventUpdate
    else:
        raise PreventUpdate

    # return Row([
    #             Col(
    #                 Dropdown(
    #                     id={'type':'filters-column-names','index':indx},
    #                     options=[{'label':i,'value':i} for i in columns.keys()],
    #                     value=None
    #                 )
    #             ,width=4),

    #             Col(
    #                 Dropdown(id={'type':'filters-conditions','index':indx})
    #             ,width=3),

    #             Col(id={'type':'filters-text-drpdwn','index':indx},width=4),
    #         ],id={'type':'condition-rows','index':indx})

# # generates the body for filter rows
# def get_filter_rows(table_names,columns):
#     col = columns
#     return Div([
#         Row(Col(H6('Select or drop rows'),width=3)),
#         Row(
#             Col(
#                 Dropdown(
#                     id='select_or_drop_rows_select_drop',
#                     options=[{'label':i,'value':i} for i in ['Select','Drop']],
#                     value=None
#                 )
#             ,width=3),
#         ),
#         Row(Col(H6('where'),width=3)),

        
#         Div([
#             Row([
                
#                 Col(
#                     Dropdown(
#                         id={'type':'trans-column-names','index':0},
#                         options=[{'label':i,'value':i} for i in columns.keys()],
#                         value=None
#                     )
#                 ,width=4),

#                 Col(
#                     Dropdown(id={'type':'trans-conditions','index':0})
#                 ,width=3),

                
#             ], id={'type':'condition-rows','index':0}),

#         ],id='trans-conditional-div'),

#         Row(Col(Button("add condition", size="sm",id='trans-add-condition'))),
        
#     ])

# display the saved filters changes to front-end
@app.callback(
    Output('filters-div','children'),
    [
        Input('retrived-data','data'),
        Input('preview-table-button','n_clicks'),
        Input({'type':'applied-changes-menu','index':ALL},'n_clicks'),
        Input("filters-clear-all","n_clicks"),
        # Input('add-new-col-modal-apply','n_clicks'),
        Input('filters-data','data'),
    ],
    [
        State('filters-div','children'),
        State({'type':'applied-changes-menu','index':ALL},'children'),
        # State('filters-data','data'),
    ],
)
def update_filter_div(data,n_clicks,menu_n_clicks,fil_clear_n_clicks,\
    filters_data,childs,apply_menu_child):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    print(f"FILTERS DIV {triggred_compo}",flush=True)
    print(f"FILTERS DIV {len(childs[2]['props']['children'])}",flush=True)
    print(f"FILTERS_DIV {filters_data['filters']}")

    empty_div = [
        FormGroup([
            Col(A(I(className="fa fa-refresh"),id='filters-clear-all'),className="text-right"),
            dhc.Label("Select or drop rows"),
            Dropdown(
                    id='filters-select-drop',
                    options=[{'label':i,'value':i} for i in ['Select','Drop']],
                    value=None,
                    style={"width":"50%"}
                ),
            # FormText("Type column name without any spaces, special characters. Except 'underscore '_''",color="secondary"),
        ]),

        FormGroup([
            dhc.Label("Where,")
        ]),

        Div([
            Row([
                Col(
                    FormGroup([
                        Label(Strong("Select column name"),html_for={'type':'filters-column-names','index':0}),
                        Dropdown(
                            id={'type':'filters-column-names','index':0},
                            value=None
                        )
                    ])
                ,width=4),

                Col(
                    FormGroup([
                        Label(Strong("condition"),html_for={'type':'filters-conditions','index':0}),
                        Dropdown(
                            id={'type':'filters-conditions','index':0}
                        )
                    ])
                ,width=3),

                Col([
                    FormGroup([
                        dhc.Label(Strong("value")),
                        Dropdown(id={"type":'trans-multi-text','index':0},style={'display':'none'}),
                        Textarea(id={"type":'trans-text','index':0},style={'display':'none'}),
                        TextInput(id={'type':'trans-input','index':0},style={'display':'none'}),
                        DatePickerRange(id={'type':'trans-date-range','index':0},style={'display':'none'}),
                        DatePickerSingle(id={'type':'trans-date-single','index':0},style={'display':'none'}),
                        DatePickerSingle(id={'type':'trans-days-single','index':0},style={'display':'none'}),
                        Checklist(id={'type':'trans-use-current-date','index':0},style={'display':'none'}),
                    ])
                    
                ],id={'type':'filters-text-drpdwn','index':0},width=4),

                # Col(dhc.Button(id={'type':'logic-close','index':0},hidden=True))
                Col(A(I(className="fa fa-trash-o"),id={'type':'logic-close','index':0}),className="text-right"),
            
            ],id={'type':'condition-rows','index':0}),
            Row(Col("This is Temp column and row"),id={"type":"filters-logic","index":0},style={'display':'none'}),
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
                    # print(f"{i}",flush=True)
                    # print(f"{idx}",flush=True)
                    if apply_menu_child[idx].startswith('Filters'):
                        return empty_div
            raise PreventUpdate
        else:
            raise PreventUpdate
    elif triggred_compo == 'filters-clear-all' and fil_clear_n_clicks is not None:
        return empty_div
    elif triggred_compo == "filters-data" and filters_data['filters']!={}:
        
        d= dict(
            indexs = [],
            location = []
        )
        print(f"INSIDE FILTERS_DIV")
        for ix,i in enumerate(childs[2]['props']['children']):
            if re.search('\'id\': \{\'type\':\ \'condition\-rows\',\ \'index\':\ ',str(i)) is not None:
                d['location'].append(ix)
                s=re.findall('\'id\': \{\'type\':\ \'condition\-rows\',\ \'index\':\ \d*}',str(i))[0]
                d['indexs'].append(re.search('\d+',s).group())
                
            elif re.search('\'id\': \{\'type\':\ \'filters\-logic\',\ \'index\':\ ',str(i)) is not None:
                d['location'].append(ix)
                s=re.findall('\'id\': \{\'type\':\ \'filters\-logic\',\ \'index\':\ \d*}',str(i))[0]
                d['indexs'].append(re.search('\d+',s).group())
        
        d=DataFrame(d)
        k=list(filters_data["filters"].keys())[0]

        remov_list = []
        # for i in filters_data['filters'][k]['index']:
        #     if str(i) not in d['indexs'].to_list():
        #         remov_list.append(d[d['indexs']==str(i)]['location'].to_list())

        for i in set(d['indexs'].to_list()):
            if int(i) not in filters_data['filters'][k]['index']:
                remov_list.append(d[d['indexs']==str(i)]['location'].to_list())
        
        print(f"INSIDE FILTERS_DIV {remov_list}")        
        if remov_list != []:
            flatten_list = list(chain.from_iterable(remov_list))
            flatten_list = sorted(flatten_list, reverse=True)
            for ix in flatten_list:
                if ix < len(childs[2]['props']['children']):
                    childs[2]['props']['children'].pop(ix)
            
            childs=str(childs)
            childs=re.sub("'n_clicks': [\d|None]*","'n_clicks': None",childs)
            childs=ast.literal_eval(str(childs))
            print(f"FILTERS_DIV {len(childs[2]['props']['children'])}")
            return childs
        else:
            raise PreventUpdate
    else:
        return childs
        # raise PreventUpdate

# retrived status
@app.callback(
    Output('filters-retrived-status','data'),
    [
        Input('filters-add-condition','n_clicks'),
        Input('preview-table-button','n_clicks'),
        Input('filters-apply','n_clicks'),
        Input('select-drop-apply','n_clicks'),
        Input('add-new-col','data'),
    ],
    [
        State('filters-retrived-status','data')
    ]
)
def update_retrived_stat(fil_add_condi_n_clicks,previ_n_clicks,fil_apply_n_clicks,\
    sel_apply_n_clicks,add_new_n_clicks,data):
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
    elif triggred_compo == "add-new-col" and add_new_n_clicks is not None:
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
    # print(f"Files list {childs}")
    childs_copy=childs.copy()
    z=[childs_copy.remove(d) for d in childs if d['type']!="Br" and d['props']['children']==None]
    if set(z) == set([None]):
        [childs_copy.remove(d) for d in childs if d['type']=="Br"]
    # print(childs_copy)
    # print(triggred_compo)
    # print(n_clicks)
    # print(trans_columns)

    if triggred_compo == 'filters-add-condition' and n_clicks is not None and childs_copy!=[]:
        indx = n_clicks + 1
        condition_row = get_condition_rows(trans_columns,indx)
        logic_and_or = Row([
            Col(
                Dropdown(id={'type':'logic-dropdown','index':indx},
                    options=[{'label':i,'value':i} for i in ["And","Or"]]
                )
            ,width=3),
        ],id={'type':'filters-logic','index':indx})
        childs_copy.append(Br())
        childs_copy.append(logic_and_or)
        childs_copy.append(condition_row)
        # print(f"\n\n DIV list {childs_copy}")
        return childs_copy
    elif triggred_compo == 'filters-add-condition' and n_clicks is not None and childs_copy==[]:
        indx = n_clicks + 1
        condition_row = get_condition_rows(trans_columns,indx)
        # print("got columns")
        logic_and_or = Row(Col("This is Temp column and row"),id={"type":"filters-logic",\
            "index":indx},style={'display':'none'})

        # print("value init")

        # logic_and_or = Row([
        #     Col(
        #         Dropdown(id={'type':'logic-dropdown','index':indx},
        #             options=[{'label':i,'value':i} for i in ["And","Or"]]
        #         )
        #     ,width=3),
        # ],id={'type':'filters-logic','index':indx})
        childs_copy.append(Br())
        childs_copy.append(logic_and_or)
        childs_copy.append(condition_row)
        # print(childs_copy)
        # print(f"\n\n DIV list {childs_copy}")
        return childs_copy

    else:
        raise PreventUpdate

# clear added filter component
@app.callback(
    [
        Output({'type':'condition-rows','index':MATCH},'children'),
        Output({'type':'filters-logic','index':MATCH},'children')
    ],
    [
        Input({'type':'logic-close','index':MATCH},'n_clicks'),
    ],
    [
        State({'type':'logic-close','index':MATCH},'id'),
        State({'type':'condition-rows','index':MATCH},'children'),
        State({'type':'filters-logic','index':MATCH},'children'),
    ]
)
def close_condition(n_clciks,id,childs,fil_childs):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo.rfind('logic-close') > -1 and n_clciks is not None:
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
        return [{'label':i,'value':i} for i in ['has value(s)','<','<=','==','!=','>','>=', \
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
        return [{'label':i,'value':i} for i in ['has value(s)','<','<=','==','!=','>','>=', \
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
        State('filters-retrived-status','data'),
        State('add-new-col','data'), # stores all applied filters
    ]
)
def update_multi_drop_or_text(value,id,childs,column_name,relation_data,ret_data,ret_stat,add_new_col):
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
            return FormGroup([
                dhc.Label(Strong("value")),
                Textarea(id={"type":'trans-text','index':indx},\
                    persistence=True,value=None,required=True)
            ])

        elif value in ['starts with','contains','ends with']:
            return FormGroup([
                dhc.Label(Strong("value")),
                Textarea(id={"type":'trans-text','index':indx},\
                persistence=True,value=None,required=True)
            ])

        elif value in ['has value(s)'] and relation_data['table']!=[]:
            
            df1=get_column_values(relation_data['table'],add_new_col,column_name)
            # print(f"columns .. {df1.columns}")

            if type(df1) is Series:
                col=df1.unique()
            else:
                col=df1[column_name].unique
            return FormGroup([
                    dhc.Label(Strong("value")),
                    Dropdown(id={"type":'trans-multi-text','index':indx},
                                options=[{'label':i,'value':i} for i in col],
                                multi=True,
                                persistence=True),
                ])
        
        elif value in ['days'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)

            max_dt = df1.max()
            min_dt = df1.min()

            return FormGroup([
                dhc.Label(Strong("value")),
                TextInput(id={'type':'trans-input','index':indx},persistence=True,value=None),
                DatePickerSingle(
                    id={'type':'trans-days-single','index':indx},
                    placeholder='mm/dd/YYYY',
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today()
                ),
                Checklist(
                    id={'type':'trans-use-current-date','index':indx},
                    options=[
                        {'label': 'Use current sys date', 'value': 'Use'},
                    ],
                    value=[]
                )
            ]) 
        
        elif value in ['before','after','equals','not'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)

            max_dt = df1.max()
            min_dt = df1.min()

            return FormGroup([
                dhc.Label(Strong("value")),
                DatePickerSingle(
                    id={'type':'trans-date-single','index':indx},
                    placeholder='mm/dd/YYYY',
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today()
                )
            ])
        
        elif value in ['range'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)
            max_dt = df1.max()
            min_dt = df1.min()

            return FormGroup([
                dhc.Label(Strong("value")),
                DatePickerRange(
                    id={'type':'trans-date-range','index':indx},
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                )
            ])
        else:
            return None
    elif value is not None and relation_data['table'] != []:
        
        if value in ['<','<=','==','>=','>','!=']:
            return FormGroup([
                dhc.Label(Strong("value")),
                Textarea(id={"type":'trans-text','index':indx},\
                    persistence=True,value=None,required=True)
            ])

        elif value in ['starts with','contains','ends with']:
            return FormGroup([
                dhc.Label(Strong("value")),
                Textarea(id={"type":'trans-text','index':indx},\
                persistence=True,value=None,required=True)
            ])

        elif value in ['has value(s)'] and relation_data['table']!=[]:
            
            df1=get_column_values(relation_data['table'],add_new_col,column_name)
            # print(f"columns .. {df1.columns}")

            if type(df1) is Series:
                col=df1.unique()
            else:
                col=df1[column_name].unique
            
            return FormGroup([
                    dhc.Label(Strong("value")),
                    Dropdown(id={"type":'trans-multi-text','index':indx},
                                options=[{'label':i,'value':i} for i in col],
                                multi=True,
                                persistence=True),
                ])
        
        elif value in ['days'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)

            max_dt = df1.max()
            min_dt = df1.min()

            return FormGroup([
                dhc.Label(Strong("value")),
                TextInput(id={'type':'trans-input','index':indx},persistence=True,value=None),
                DatePickerSingle(
                    id={'type':'trans-days-single','index':indx},
                    placeholder='mm/dd/YYYY',
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today()
                ),
                Checklist(
                    id={'type':'trans-use-current-date','index':indx},
                    options=[
                        {'label': 'Use current sys date', 'value': 'Use'},
                    ],
                    value=[]
                )
            ]) 
        
        elif value in ['before','after','equals','not'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)

            max_dt = df1.max()
            min_dt = df1.min()
            return FormGroup([
                dhc.Label(Strong("value")),
                DatePickerSingle(
                    id={'type':'trans-date-single','index':indx},
                    placeholder='mm/dd/YYYY',
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today()
                )
            ])
        
        elif value in ['range'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)
            max_dt = df1.max()
            min_dt = df1.min()
            return FormGroup([
                dhc.Label(Strong("value")),
                DatePickerRange(
                    id={'type':'trans-date-range','index':indx},
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                )
            ])
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
            raise PreventUpdate
        else:
            sys.stderr.write(str(menu_n_clicks))
            # print(f"PREVENT UPDATE",flush=True)
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
        Input({"type":'trans-multi-text','index':ALL},'value'),#dropdown
        Input({'type':'trans-input','index':ALL},'value'), #date days
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
            if multi_drp is True:
                chk.append(trans_multi_txt)
            if single_dt is True:
                chk.append(trans_dt_single)
            if range_dt is True:
                chk.append(trans_dt_start)
                chk.append(trans_dt_end)
            

            rt=False
            rtt=False

            rt2=False
            rtt2=False


            if chk != []:
                for i in chk:
                    chk_val=[True if k is not None and k !=[] and k != '' else False for k in i]
                    if all(chk_val) is True and chk_val != []:
                        rt=True
                    else:
                        rtt=True

            
            if chk2 != []:
                z1=[True for i,j in zip(chk2[0],chk2[2]) if i != [] and i is not None and i != '' or j != []]

                chk2_val = [True if i is not None and i != [] and i != '' else False for i in chk2[1]]
                if all(chk2_val) is True and chk2_val != [] and\
                    len(chk2[0]) == z1.count(True):
                    rt2=True
                else:
                    rtt2=True

            # print(chk)
            # print(chk2)

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

# get realtime data
@app.callback(
    Output('realtime-total-records','children'),
    [
        Input('filters-apply','disabled'),
        Input('retrived-data','data'),
    ],
    [
        State('filters-data','data'),

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
        State('relationship-data','data'),

        State('filters-select-drop','value'),#select or drop rows
        State({'type':'filters-column-names','index':ALL},'value'),
        State({'type':'filters-conditions','index':ALL},'value'),
        State({"type":'trans-text','index':ALL},'value'),
        State({"type":'trans-multi-text','index':ALL},'value'),#dropdown
        State({'type':'trans-input','index':ALL},'value'), #date days
        State({'type':'trans-date-range','index':ALL},'start_date'),
        State({'type':'trans-date-range','index':ALL},'end_date'),
        State({'type':'trans-date-single','index':ALL},'date'),
        State({'type':'trans-days-single','index':ALL},'date'),
        State({'type':'trans-use-current-date','index':ALL},'value'),
        State({'type':'logic-dropdown','index':ALL},'value'),
    ]
)
def get_real_time_count(disabled,ret_data,filters_data,fil_col_id,fil_condi_id,trans_text_id,\
    trans_multi_id,trans_input_id,trans_dt_id,trans_dt_single_id,trans_days_id,\
    trans_use_curr_id,logic_val_id,relationship_data,fil_sel_drop,fil_col_names,fil_condi,trans_txt,\
    trans_multi_txt,trans_input,trans_dt_start,trans_dt_end,trans_dt_single,\
        trans_days_single,trans_current_date,logic_dropdown):


    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo == "filters-apply" and disabled is False:
        # print(f"filters data {filters_data}")
        # print(f"current date {trans_current_date}")
        # print(f"trans input {trans_input}")
        # print(f"trans single {trans_days_single}")
        # print(f"trans days single {trans_days_single}")
        # print(f"filter condi {fil_condi}")
        # print(f"logic dropdown {logic_dropdown}")
        # print(f"relationship {relationship_data}")
        # print(f"fil col {fil_col_names}")
        # print(f"Multi Text {trans_multi_txt}")
            # ,logic_val_id,fil_col_names,fil_sel_drop,
            # relationship_data
        def local_func_get_rows():
            df,sql_qry,rows, csv_string = get_filter_records(filters_data,trans_text_id,trans_multi_id,fil_col_id,\
                trans_input_id,trans_dt_id,trans_dt_single_id,trans_days_id,trans_use_curr_id,
                trans_txt,trans_multi_txt,trans_dt_single,trans_dt_start,trans_dt_end,trans_current_date,
                trans_input,trans_days_single,fil_condi,logic_dropdown,logic_val_id,fil_col_names,fil_sel_drop,
                relationship_data,None)
            
            no_of_records=None
            if rows is not None:
                no_of_records = f"{rows} records"               
            return no_of_records

        no_of_rows = local_func_get_rows()
        return no_of_rows
    elif triggred_compo == "retrived-data":
        return ret_data['realtime_rows']
    else:
        return None


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
    Output({'type':'filters-column-names','index':0},'options'),

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
        if value == 'Filter rows':
            # modal_head = H5(value)
            return [{'label':i,'value':i} for i in trans_column_data.keys()]
        else:
            return []
    else:
        return []


# transformation dropdown
@app.callback(
    Output("transformations-dropdown","value"),
    [
        Input("add-col-close", "n_clicks"),
        Input('filters-close','n_clicks'),
        Input('filters-modal-status','data'),
        Input('add-col-modal-status','data'),
    ]
)
def update_trans_value(n_clicks_add,n_clicks_fil,filters_status_data,add_col_status_data):
    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo == "add-col-close" and n_clicks_add is not None:
        return []
    elif triggred_compo == "filters-close" and n_clicks_fil is not None:
        return []
    elif triggred_compo == "filters-modal-status" and filters_status_data is True:
        return []
    elif triggred_compo == "add-col-modal-status" and add_col_status_data is True:
        return []
    # elif triggred_compo == "add-new-col-modal" and add_col_is_open is False:
    #     return []
    # elif triggred_compo == "filters-modal" and fil_is_open is False:
    #     return []


# transformations filter modal open and close.
@app.callback(
    [
        Output("add-new-col-modal", "is_open"),
        Output('filters-modal','is_open'),
    ],
    [
        Input('transformations-dropdown','value'),
        Input("add-col-close", "n_clicks"),
        Input('filters-close','n_clicks'),
        Input('filters-modal-status','data'),
        Input('add-col-modal-status','data'),
    ],
    [
        State("add-new-col-modal", "is_open"),
        State('filters-modal','is_open'),
    ],
)
def transformation_modal_expand(trans_drop_value, add_col_close,\
    fil_close,fil_status_data,add_col_status_data,add_col_is_open,fil_is_open):

    if trans_drop_value is not None and trans_drop_value == 'Add new column':
        if add_col_close:
            return not add_col_is_open, False
        elif add_col_status_data is True:
            return not add_col_is_open, False
        return not add_col_is_open, False

    elif trans_drop_value is not None and trans_drop_value == 'Filter rows':
        if fil_close:
            return False, not fil_is_open
        elif fil_status_data is True:
            return False, not fil_is_open
        return False, not fil_is_open
    else:
        return False, False


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

        Output('filters-modal-status','data'),
        Output('add-col-modal-status','data'),
    ],
    [
        Input('preview-table-button','n_clicks'),
        Input('retrived-data','data'),
        Input({'type':'applied-changes-menu','index':ALL},'n_clicks'),
        Input("filters-clear-all","n_clicks"),

        Input('select-drop-apply','n_clicks'),
        Input('filters-apply','n_clicks'),
        Input('format-map-data','data'),
        Input('add-new-col','data'),
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

def update_table_all(rel_n_clicks,ret_data,menu_n_clicks,fil_clear_all_n_clicks,\
    sel_aply_n_clicks,fil_aply_n_clicks,format_data,add_col_data,table_row,rel_tbl_data,rel_tbl_col,\
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
    print(f"##### {triggred_compo}",flush=True)
    # print(f"##### {add_col_data}",flush=True)


    col={}
    
    if format_data is not None and format_data != {}:
        col={}
        [col.update({j:i}) for i,j in format_data.items()]
    elif ret_data is not None:
        if ret_data['format_map_data'] is not None and ret_data['format_map_data'] != {}:
            col={}
            [col.update({j:i}) for i,j in ret_data['format_map_data'].items()]
    
    index_k = 0 if filters_data['index_k'] is None else filters_data['index_k']

    
    
    if triggred_compo == "add-new-col" and  add_col_data is not None and \
        add_col_data['add_col_qry'] != "" and add_col_data['add_col_qry'] is not None and\
        relationship_data['table']!=[]:
        
        
        k_f_id = None
        if filters_data['filters'] != {}:
            idx = list(filters_data['filters'].keys())[0]
            cols_remove=[ix for ix,c in enumerate(filters_data['filters'][idx]['columns']) \
                if c not in relationship_data['columns'] and c not in add_col_data['add_col_names']]
            
            # removing the calulated column which are no more in use.
            cols_remove = sorted(cols_remove, reverse=True)
            for ix in cols_remove:
                if ix < len(filters_data['filters'][idx]['columns']):
                    filters_data['filters'][idx]['index'].pop(ix)
                    filters_data['filters'][idx]['columns'].pop(ix)
                    filters_data['filters'][idx]['condition'].pop(ix)
                    filters_data['filters'][idx]['values'].pop(ix)
                    filters_data['filters'][idx]['logic'].pop(ix)
            
            if filters_data['filters'][idx]['index'] == []:
                filters_data['filters'].pop(str(idx))
                k_f_id = int(idx)

        k = None
        if index_k != 0 and filters_data['add_new_col'] != {}:
            check_val = True if index_k in filters_data['add_new_col'].keys() else False

            if check_val is False:
                idx = list(filters_data['add_new_col'].keys())[0]
                filters_data['add_new_col'].pop(str(idx))
                k = int(idx)
            else:
                filters_data['add_new_col'].pop(str(index_k))
                k = int(index_k)
        
        if k is not None and k_f_id is not None and k_f_id < k:
            k = k_f_id

        i_k = None
        if k is not None and int(k) < filters_data['index_k']:
            i_k = filters_data['index_k']
        elif k is not None and int(k) >= filters_data['index_k']:
            i_k = k

        k = k if k is not None else index_k + 1

        filters_data['add_new_col'].update({
                k:{
                    'query':add_col_data['add_col_qry'],
                    'col_names':add_col_data['add_col_names']
                }
            })
        filters_data['index_k']=k if i_k is None else i_k

        relationship_data['saved_data']=False
        # print(f"UPDATE_TABLE_ADD_COL {filters_data}")
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
                trans_col, sql_qry,csv_string,filters_data,table_row,None,True
        else:
            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                csv_string,filters_data,table_row,None,False

    elif triggred_compo == 'select-drop-apply':
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
                    trans_col, sql_qry,csv_string,filters_data,table_row,None,None
            else:
                return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                    table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                    csv_string,filters_data,table_row,None,None
    
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
                trans_col, sql_qry,csv_string,filters_data,table_row,True,None
        else:
            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                csv_string,filters_data,table_row,False,None


    elif triggred_compo == 'preview-table-button':

        # result = check_if_all_none(join_qry)
        rel_tbl_drpdwn=list(filter(None,rel_tbl_drpdwn))
        # print(f"{rel_tbl_drpdwn}",flush=True)

        # for single table join qry will be none.
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
                    add_new_col=dict(),
                    index_k=None,
                )
        # return [],col,[],col,[],col,rel,0,{},None,'',fil_data,[]
        
            
        return table_data_rel, table_columns_rel,table_data_format, table_columns_format,\
            table_data_fil, table_columns_fil,relationship_data, table_rows_no,\
            trans_col,None,csv_string,fil_data,table_row,None,None
    

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
                        relationship_data,rows,trans_col,sql_qry,csv_string,filters_data,table_row,None,None
                else:
                    return table_data_rel,table_columns_rel,table_data, table_columns,\
                        table_data_fil, table_columns_fil,\
                        relationship_data,rows,trans_col, sql_qry,csv_string,filters_data,table_row,None,None
            else:
                return table_data_rel,table_columns_rel,table_data, table_columns,\
                    table_data_fil, table_columns_fil,\
                    relationship_data,rows,trans_col, sql_qry,csv_string,filters_data,table_row,None,None

        else:
            # print('Second Condition',flush=True)
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
                            relationship_data,rows,trans_col,trans_fil_condi,csv_string,filters_data,table_row,None,None
                    else:
                        return table_data_rel,table_columns_rel,table_data, table_columns,\
                            table_data_fil, table_columns_fil,\
                            relationship_data,rows,trans_col, trans_fil_condi,csv_string,filters_data,table_row,None,None

            return table_data_rel,table_columns_rel,table_data_format,\
                table_columns_format,table_data_fil, table_columns_fil,\
                relationship_data,rows,trans_col,trans_fil_condi,csv_string,filters_data,table_row,None,None
    
    elif triggred_compo == 'format-map-data':
        d = {'column_names':[]}

        relationship_data['saved_data']=False

        if format_data != {} and format_data is not None:
            d["column_names"]=list(format_data.values())
            # col={}
            # [col.update({j:i}) for i,j in format_data.items()]

            df, csv_string = get_format_mapping(relationship_data,d,trans_fil_condi,col)

            # print(format_data)
            # print(df.columns)
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
                    csv_string,filters_data,table_row,None,None
            else:
               return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,data,columns,relationship_data,\
                   rows,trans_column_data,trans_fil_condi,csv_string,filters_data,table_row,None,None
        else:
            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,data,columns,relationship_data,\
                rows,trans_column_data, trans_fil_condi,csv_string,filters_data,table_row,None,None
    
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
                                    add_new_col=dict(),
                                    index_k=None,
                                )
                        return [],col,[],col,[],col,rel,0,{},None,'',fil_data,[],None,None

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
                                trans_col, sql_qry,csv_string,filters_data,table_row,None,None
                        else:
                            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                            csv_string,filters_data,table_row,None,None

                    elif apply_menu_child[idx].startswith('Filters'):
                        indx = filters_data['index_k']
                        
                        sel_keys = list(filters_data['add_new_col'].keys())
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
                                pop_item = filters_data['add_new_col'].popitem()
                                filters_data['add_new_col']={new_indx:pop_item[1]}
                                
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
                                trans_col, sql_qry,csv_string,filters_data,table_row,None,None
                        else:
                            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                            csv_string,filters_data,table_row,None,None

                    elif apply_menu_child[idx].startswith('New column added'):
                        indx = filters_data['index_k']
                        
                        # sel_keys = list(filters_data['add_new_col'].keys())
                        fil_keys = list(filters_data['filters'].keys())

                        if int(indx) == 1 and filters_data['add_new_col'] != {}:
                            # delete the select_or_drop
                            filters_data['add_new_col'].popitem()
                            filters_data['index_k']=0

                        elif int(indx) > 1 and filters_data['add_new_col'] != {}:
                            # delete the select_or_drop
                            filters_data['add_new_col'].popitem()
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
                                trans_col, sql_qry,csv_string,filters_data,table_row,None,None
                        else:
                            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                            csv_string,filters_data,table_row,None,None

                    else:
                        return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                            csv_string,filters_data,table_row,None,None
        else:
            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                csv_string,filters_data,table_row,None,None
            # raise PreventUpdate
    
    elif triggred_compo == "filters-clear-all" and \
        fil_clear_all_n_clicks is not None and relationship_data is not None and \
        filters_data['index_k'] is not None:

        indx = filters_data['index_k']
                        
        sel_keys = list(filters_data['add_new_col'].keys())
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
                pop_item = filters_data['add_new_col'].popitem()
                filters_data['add_new_col']={new_indx:pop_item[1]}
                
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
                trans_col, sql_qry,csv_string,filters_data,table_row,None,None
        else:
            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
            csv_string,filters_data,table_row,None,None
    else:
        return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,data,columns,relationship_data,\
            rows,trans_column_data, trans_fil_condi,csv_string,filters_data,table_row,None,None


# # clear-all
# @app.callback(
#     Output('url','pathname'),
#     [
#         Input('clear-all','n_clicks')
#     ]
# )
# def update_url_path_name(n_clicks):
#     if n_clicks is not None:
#         print(f"PATH NAME {n_clicks}")
#         return "/"
#     else:
#         raise PreventUpdate

# # clear-all
# @app.callback(
#     Output('clear-alll','n_clicks'),
#     [
#         Input('url','pathname')
#     ]
# )
# def update_url_path_name(pathname):
#     if pathname is not None:
#         # print(f"PATH NAME {n_clicks}")
#         return None
#     else:
#         raise PreventUpdate