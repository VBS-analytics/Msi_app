from numpy.core.numeric import outer
from ..server import app, server
from dash.dependencies import Output, Input, State, ALL, MATCH
from dash import callback_context,dcc,html
# from dash_core_components import Dropdown, Textarea, DatePickerRange, DatePickerSingle,\
#     Checklist, RadioItems, Store
# from dash_core_components import Input as TextInput
# from dash_html_components import H6, Br, Div, I, Hr, A, Strong
from dash_bootstrap_components import Col, Row, Button, Form, FormGroup,FormText,\
    Label


# import dash_html_components as dhc


from ..global_functions import get_transformations,\
    get_format_mapping, get_columns_dtypes, get_table_from_sql_query, get_column_values


from pandas import DataFrame, Series

from itertools import chain

import sys

from dash.exceptions import PreventUpdate

from datetime import date
import re
import ast
from numpy import array

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
# def get_condition_rows(columns,indx):
#     # print(f"get condition rows {type(indx)}")
#     # print(f"get condition row {indx}")
#     return Row([
#         Col(
#             FormGroup([
#                 Label(html.Strong("Select column name"),html_for={'type':'filters-column-names','index':indx}),
#                 dcc.Dropdown(
#                     id={'type':'filters-column-names','index':indx},
#                     options=[{'label':i,'value':i} for i in columns.keys()],
#                     value=None
#                 )
#             ])
#         ,width=4),

#         Col(
#             FormGroup([
#                 Label(html.Strong("condition"),html_for={'type':'filters-conditions','index':indx}),
#                 dcc.Dropdown(
#                     id={'type':'filters-conditions','index':indx}
#                 )
#             ])
#         ,width=3),

#         Col(id={'type':'filters-text-drpdwn','index':indx},width=4),

#         Col(html.A(html.I(className="fa fa-trash-o"),id={'type':'logic-close','index':indx}),className="text-right"),
#         # Store(id={'type':'filters-rows-trash','index':indx},data=None)

#     ],id={'type':'condition-rows','index':indx})

app.clientside_callback(
    '''
    function update_add_new_col_apply(col_name_val, col_input_val) {
        if (col_name_val.includes(null) != true && col_name_val.includes(undefined) != true
            && col_name_val.length > 0 && col_input_val.includes(null) != true
            && col_input_val.length > 0 && col_input_val.includes(undefined) != true) {
            return false
        } else {
            return true
        }
    }
    ''',
    Output('add-new-col-modal-apply','disabled'),
    Input({"type":"add-new-col-name","index":ALL},'value'),
    Input({"type":'add-col-value-input',"index":ALL},'value')
)

# remove added new column
# @app.callback(
#     Output('add-new-col-modal-apply','disabled'),
#     [
#         Input({"type":"add-new-col-name","index":ALL},'value'),
#         Input({"type":'add-col-value-input',"index":ALL},'value'),
#     ]
# )
# def update_add_new_col_apply(col_name_val, col_input_val):
#     # print(f"WEWEEW {col_name_val}",flush=True)
#     # print(f"GHGHGH {col_input_val}",flush=True)
#     if all(col_name_val) and col_name_val != [] and all(col_input_val) and col_input_val != []:
#         return False
#     else:
#         return True

app.clientside_callback(
    '''
    function update_add_new_col_values(n_clicks,col_name_val,col_input_val,filters_data,add_new_col_id) {
        if (n_clicks != null && n_clicks != undefined && n_clicks > 0) {
            if (col_name_val.length > 0 && col_name_val.includes(null)!=true && col_name_val.includes(undefined)!=true
                && col_input_val.length > 0 && col_input_val.includes(null) != true && col_input_val.includes(undefined) != true) {
                let qry_str = ""
                let add_col_id = []

                for (i in col_name_val) {
                    if (qry_str == "") {
                        qry_str = qry_str + String(col_input_val[i]) + ' AS ' + String(col_name_val[i])
                    } else {
                        qry_str = qry_str + String(col_input_val[i]) + ' AS ' + String(col_name_val[i])
                    }
                    add_col_id.push(add_new_col_id[i]['index'])
                }

                return {"add_col_names":col_name_val,"add_col_qry":qry_str,"add_col_id":add_col_id,"add_col_input":col_input_val}
            } else {
                window.dash_clientside.no_update
            }
        } else {
            window.dash_clientside.no_update
        }
    }    
    ''',
    Output('add-new-col','data'),
    Input('add-new-col-modal-apply','n_clicks'),
    State({"type":"add-new-col-name","index":ALL},'value'),
    State({"type":'add-col-value-input',"index":ALL},'value'),
    State('filters-data','data'), # stores all applied filters
    State({"type":"add-new-col-name","index":ALL},'id')
)

# @app.callback(
#     Output('add-new-col','data'),
#     [
#         Input('add-new-col-modal-apply','n_clicks')
#     ],
#     [
#         State({"type":"add-new-col-name","index":ALL},'value'),
#         State({"type":'add-col-value-input',"index":ALL},'value'),
#         State('filters-data','data'), # stores all applied filters
#         State({"type":"add-new-col-name","index":ALL},'id')
#     ]
# )
# def update_add_new_col_values(n_clicks,col_name_val,col_input_val,filters_data,add_new_col_id):
#     if n_clicks is not None:
#         if all(col_name_val) and col_name_val != [] and all(col_input_val) and col_input_val != []:
#             qry_str = ""
#             add_col_id = []
#             for col_name, col_val, col_id in zip(col_name_val,col_input_val,add_new_col_id):
#                 if qry_str == "":
#                     qry_str = qry_str + str(col_val) + ' AS ' + str(col_name)
#                 else:
#                     qry_str = qry_str + ', ' + str(col_val) + ' AS ' + str(col_name)
#                 add_col_id.append(col_id['index'])
            
            
#             return dict(add_col_names=col_name_val,add_col_qry=qry_str,add_col_id = add_col_id,add_col_input=col_input_val)
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate

# add new column button
app.clientside_callback(
    '''
    function update_add_col_div(n_clicks,trash_n_clicks,childs,add_col_remove_id) {
        const triggered = dash_clientside.callback_context.triggered.map(t => t.prop_id)

        function anynull(arr) {
            return arr.some(el => el !== null && el !== undefined);
        }

        if (triggered.includes('add-col-new-col-but.n_clicks')
            && n_clicks != null && n_clicks != undefined && n_clicks > 0) {
            
            let indx = []
            for (i in add_col_remove_id) {
                indx.push(Number(add_col_remove_id[i]['index']))
            }

            if (indx.length > 0) {
                indx = Math.max.apply(null,indx)
            } else {
                indx = 0
            }

            indx = Number(indx+1)

            grp_1 = {
                'props':{
                    'children':[
                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':{
                                            'props':{
                                                'className':"fa fa-trash"
                                            },
                                            'type':'I',
                                            'namespace':'dash_html_components'
                                        },
                                        'id':{'type':'add-col-remove','index':indx}
                                    },
                                    'type':'A',
                                    'namespace':'dash_html_components'
                                },
                                'className':"text-right"
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{"children":"Enter column name"},
                            'type':'Label',
                            'namespace':'dash_html_components'
                        },

                        {
                            'props':{
                                'id':{"type":"add-new-col-name","index":indx},
                                'type':"text",
                                'minLength':5,
                                'required':true,
                            },
                            'type':'Input',
                            'namespace':'dash_core_components'
                        },

                        {
                            'props':{
                                "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
                                'color':"secondary"
                            },
                            'type':'FormText',
                            'namespace':'dash_bootstrap_components'
                        },
                    ],
                    'id':{"type":'add-col-grp-1','index':indx}
                },
                'type':'FormGroup',
                'namespace':'dash_bootstrap_components'
            }
            grp_2 = {
                'props':{
                    'children':[
                        {
                            'props':{'children':"Assign value to new column"},
                            'type':'Label',
                            'namespace':'dash_html_components'
                        },

                        {
                            'props':{
                                'id':{"type":'add-col-value-input',"index":indx},
                                'type':'text',
                                'required':true,
                            },
                            'type':'Input',
                            'namespace':'dash_core_components'
                        }
                    ],
                    'id':{"type":'add-col-grp-2','index':indx}
                },
                'type':'FormGroup',
                'namespace':'dash_bootstrap_components'
            }
            grp_3 = {
                'props':{
                    'id':{"type":'add-col-hr-3','index':indx}
                },
                'type':'Hr',
                'namespace':'dash_html_components'
            } 

            childs.push(grp_1)
            childs.push(grp_2)
            childs.push(grp_3)

            return childs
        } else if (triggered.includes(undefined) == false && triggered.includes(null) == false && triggered[0] != undefined
            && triggered.includes(triggered[triggered[0].search(/{.*"add-col-remove.*/g)])) {
            let indx = null

            if (anynull(trash_n_clicks)) {
                indx = []
                for (i in trash_n_clicks) {
                    if (trash_n_clicks[i] != null && trash_n_clicks[i] != undefined && trash_n_clicks[i] > 0) {
                        indx.push(i)
                    }
                }

                indx = add_col_remove_id[indx[0]]
                indx = indx['index']
            }
            childs_copy = childs.slice()

            if (indx != null && indx != undefined) {
                for (i in childs) {
                    for (j in childs_copy) {
                        if (childs_copy[j]['props']['id']['index'] == Number(indx)) {
                            childs_copy.splice(j,1)
                            break
                        }

                    }
                    
                }
                return childs_copy
            }
            window.dash_clientside.no_update
        } else {
            window.dash_clientside.no_update
        }
    }    
    ''',
    Output('add-col-form','children'),
    Input('add-col-new-col-but','n_clicks'),
    Input({'type':'add-col-remove','index':ALL},'n_clicks'),
    State('add-col-form','children'),
    State({'type':'add-col-remove','index':ALL},'id'),
    prevent_initial_call=True
)
# @app.callback(
#     Output('add-col-form','children'),
#     [
#         Input('add-col-new-col-but','n_clicks'),
#         Input({'type':'add-col-remove','index':ALL},'n_clicks'),
#     ],
#     [
#         State('add-col-form','children'),
#         State({'type':'add-col-remove','index':ALL},'id'),
#     ],
#     prevent_initial_call=True
# )
# def update_add_col_div(n_clicks,trash_n_clicks,childs,add_col_remove_id):
#     ctx = callback_context
#     triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

#     if triggred_compo == "add-col-new-col-but" and n_clicks is not None:
#         indx=[int(i['index']) for i in add_col_remove_id]
#         if indx != []:
#             indx=array(indx).max()
#         else:
#             indx=0

#         indx = int(indx+1)
        
#         grp_1 = FormGroup([
#                     Col(html.A(html.I(className="fa fa-trash"),id={'type':'add-col-remove','index':indx}),className="text-right"),
#                     html.Label("Enter column name"),
#                     dcc.Input(id={"type":"add-new-col-name","index":indx},type="text",minLength=5,required=True),
#                     FormText("Type column name without any spaces, special characters. Except 'underscore '_''",color="secondary"),
#                 ],id={"type":'add-col-grp-1','index':indx})
        
#         grp_2 = FormGroup([
#                     html.Label("Assign value to new column"),
#                     # RadioItems(
#                     #         options=[{'label':i,'value':i} for i in zip(["single value","conditional value"])],
#                     #         id={"type":"add-col-value-radio","index":indx},
#                     # ),
#                     dcc.Input(id={"type":'add-col-value-input',"index":indx},type='text',required=True),
#                 ],id={"type":'add-col-grp-2','index':indx})
        
        
#         # childs.append(trash_but)
#         childs.append(grp_1)
#         childs.append(grp_2)
#         childs.append(html.Hr(id={"type":'add-col-hr-3','index':indx}))
#         return childs

#     elif triggred_compo.rfind('add-col-remove') > -1:
#         indx=None
#         # print(f"add-col-remove n_clciks {trash_n_clicks}")
#         # print(f"add-col-remove id {trash_n_clicks}")
#         if any(trash_n_clicks):
#             indx = [idx for idx,i in enumerate(trash_n_clicks) if i is not None and i > 0]
#             indx = add_col_remove_id[indx[0]]
#             indx = indx['index']    

#         childs_copy = childs.copy()
                    

#         if indx is not None:
#             for idx,i in enumerate(childs):
#                 # print(f"add-col-remove childs {i['props']['id']}")
#                 if i['props']['id']['index'] == int(indx):
#                     childs_copy.remove(i)
#             return childs_copy
#         raise PreventUpdate
#     else:
#         raise PreventUpdate


# display the saved filters changes to front-end
app.clientside_callback(
    '''
    function update_filter_div(data,n_clicks,filters_data) {
        const triggered = dash_clientside.callback_context.triggered.map(t => t.prop_id)

        let empty_div = [
            {
                'props':{
                    'children':[
                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':{
                                            'props':{'className':"fa fa-refresh"},
                                            'type':'I',
                                            'namespace':'dash_html_components'
                                        },
                                        'id':'filters-clear-all',
                                        'className':"text-right"
                                    },
                                    'type':'A',
                                    'namespace':'dash_html_components'
                                }
                            },
                            'type':'Col',
                            'namespace':"dash_bootstrap_components"
                        },

                        {
                            'props':{
                                'children':'Select or drop rows'
                            },
                            'type':'Label',
                            'namespace':'dash_html_components'
                        },

                        {
                            'props':{
                                'id':'filters-select-drop',
                                'options':[{'label':'Select','value':'Select'},{'label':'Drop','value':'Drop'}],
                                'value':null,
                                'style':{"width":"50%"}
                            },
                            'type':'Dropdown',
                            'namespace':'dash_core_components'
                        }
                    ]
                },
                'type':'FormGroup',
                'namespace':'dash_bootstrap_components'
            },

            {
                'props':{
                    'children':{
                        'props':{
                            'children':'Where,'
                        },
                        'type':'Label',
                        'namespace':'dash_html_components'
                    }
                },
                'type':'FormGroup',
                'namespace':'dash_bootstrap_components'
            },

            {
                'props':{
                    'children':[
                        {
                            'props':{
                                'children':[
                                    {
                                        'props':{
                                            'children':{
                                                'props':{
                                                    'children':[
                                                        {
                                                            'props':{
                                                                'children':{
                                                                    'props':{'children':'Select column name'},
                                                                    'type':'Strong',
                                                                    'namespace':'dash_html_components'
                                                                },
                                                                'html_for':{'type':'filters-column-names','index':0}    
                                                            },
                                                            'type':'Label',
                                                            'namespace':'dash_bootstrap_components'
                                                        },

                                                        {
                                                            'props':{
                                                                'id':{'type':'filters-column-names','index':0},
                                                                'value':null
                                                            },
                                                            'type':'Dropdown',
                                                            'namespace':'dash_core_components'
                                                        }
                                                    ]
                                                },
                                                'type':'FormGroup',
                                                'namespace':'dash_bootstrap_components'
                                            },
                                            'width':4
                                        },
                                        'type':'Col',
                                        'namespace':'dash_bootstrap_components'
                                    },

                                    {
                                        'props':{
                                            'children':{
                                                'props':{
                                                    'children':[
                                                        {
                                                            'props':{
                                                                'children':{
                                                                    'props':{'children':'condition'},
                                                                    'type':'Strong',
                                                                    'namespace':'dash_html_components'
                                                                },
                                                                'html_for':{'type':'filters-conditions','index':0}    
                                                            },
                                                            'type':'Label',
                                                            'namespace':'dash_bootstrap_components'
                                                        },

                                                        {
                                                            'props':{
                                                                'id':{'type':'filters-conditions','index':0},
                                                            },
                                                            'type':'Dropdown',
                                                            'namespace':'dash_core_components'
                                                        }
                                                    ]
                                                },
                                                'type':'FormGroup',
                                                'namespace':'dash_bootstrap_components'
                                            },
                                            'width':3
                                        },
                                        'type':'Col',
                                        'namespace':'dash_bootstrap_components'
                                    },

                                    {
                                        'props':{
                                            'children':{
                                                'props':{
                                                    'children':[
                                                        {
                                                            'props':{
                                                                'children':{
                                                                    'props':{'children':'value'},
                                                                    'type':'Strong',
                                                                    'namespace':'dash_html_components'
                                                                }
                                                            },
                                                            'type':'Label',
                                                            'namespace':'dash_html_components'
                                                        },

                                                        {
                                                            'props':{
                                                                'id':{"type":'trans-multi-text','index':0},
                                                                'style':{'display':'none'}
                                                            },
                                                            'type':'Dropdown',
                                                            'namespace':'dash_core_components'
                                                        },

                                                        {
                                                            'props':{
                                                                'id':{"type":'trans-text','index':0},
                                                                'style':{'display':'none'},
                                                                'debounce':true
                                                            },
                                                            'type':'Input',
                                                            'namespace':'dash_core_components'
                                                        },

                                                        {
                                                            'props':{
                                                                'id':{'type':'trans-input','index':0},
                                                                'style':{'display':'none'},
                                                                'debounce':true
                                                            },
                                                            'type':'Input',
                                                            'namespace':'dash_core_components'
                                                        },

                                                        {
                                                            'props':{
                                                                'id':{'type':'trans-date-range','index':0},
                                                                'style':{'display':'none'}
                                                            },
                                                            'type':'DatePickerRange',
                                                            'namespace':'dash_core_components'
                                                        },

                                                        {
                                                            'props':{
                                                                'id':{'type':'trans-date-single','index':0},
                                                                'style':{'display':'none'}
                                                            },
                                                            'type':'DatePickerSingle',
                                                            'namespace':'dash_core_components'
                                                        },

                                                        {
                                                            'props':{
                                                                'id':{'type':'trans-days-single','index':0},
                                                                'style':{'display':'none'}
                                                            },
                                                            'type':'DatePickerSingle',
                                                            'namespace':'dash_core_components'
                                                        },

                                                        {
                                                            'props':{
                                                                'id':{'type':'trans-use-current-date','index':0},
                                                                'style':{'display':'none'}
                                                            },
                                                            'type':'Checklist',
                                                            'namespace':'dash_core_components'
                                                        }
                                                    ]
                                                },
                                                'type':'FormGroup',
                                                'namespace':'dash_bootstrap_components'
                                            },
                                            'id':{'type':'filters-text-drpdwn','index':0},
                                            'width':4
                                        },
                                        'type':'Col',
                                        'namespace':'dash_bootstrap_components'
                                    },

                                    {
                                        'props':{
                                            'children':{
                                                'props':{
                                                    'children':{
                                                        'props':{
                                                            'className':"fa fa-trash-o"
                                                        },
                                                        'type':'I',
                                                        'namespace':'dash_html_components'
                                                    },
                                                    'id':{'type':'logic-close','index':0}
                                                },
                                                'type':'A',
                                                'namespace':'dash_html_components'
                                            }
                                        },
                                        'type':'Col',
                                        'namespace':'dash_bootstrap_components'
                                    }
                                ],
                                'id':{'type':'condition-rows','index':0}
                            },
                            'type':'Row',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':'This is Temp column and row'
                                    },
                                    'type':'Col',
                                    'namespace':'dash_bootstrap_components'
                                },
                                'id':{"type":"filters-logic","index":0},
                                'style':{'display':'none'}
                            },
                            'type':'Row',
                            'namespace':'dash_bootstrap_components'
                        }
                    ],
                    'id':'filters-conditional-div'
                },
                'type':'Div',
                'namespace':'dash_html_components'
            },

            {
                'props':{
                    "children":{
                        'props':{
                            'children':{
                                'props':{
                                    'children':'add condition',
                                    'size':'sm',
                                    'id':'filters-add-condition'
                                },
                                'type':'Button',
                                'namespace':'dash_bootstrap_components'
                            }  
                        },
                        'type':'Col',
                        'namespace':'dash_bootstrap_components'
                    }
                },
                'type':'Row',
                'namespace':'dash_bootstrap_components'
            }

        ]

        let empty_div_add = [
            {
                'props':{
                    'children':[
                            {
                                'props':{
                                    'children':[
                                        {
                                            'props':{
                                                'children':{
                                                    'props':{
                                                        'children':{
                                                            'props':{
                                                                'className':"fa fa-trash"
                                                            },
                                                            'type':'I',
                                                            'namespace':'dash_html_components'
                                                        },
                                                        'id':{'type':'add-col-remove','index':0}
                                                    },
                                                    'type':'A',
                                                    'namespace':'dash_html_components'
                                                },
                                                'className':"text-right"
                                            },
                                            'type':'Col',
                                            'namespace':'dash_bootstrap_components'
                                        },

                                        {
                                            'props':{"children":"Enter column name"},
                                            'type':'Label',
                                            'namespace':'dash_html_components'
                                        },

                                        {
                                            'props':{
                                                'id':{"type":"add-new-col-name","index":0},
                                                'type':"text",
                                                'minLength':5,
                                                'required':true
                                            },
                                            'type':'Input',
                                            'namespace':'dash_core_components'
                                        },

                                        {
                                            'props':{
                                                "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
                                                'color':"secondary"
                                            },
                                            'type':'FormText',
                                            'namespace':'dash_bootstrap_components'
                                        },
                                    ],
                                    'id':{"type":'add-col-grp-1','index':0}
                                },
                                'type':'FormGroup',
                                'namespace':'dash_bootstrap_components'
                            },

                            {
                                'props':{
                                    'children':[
                                        {
                                            'props':{'children':"Assign value to new column"},
                                            'type':'Label',
                                            'namespace':'dash_html_components'
                                        },

                                        {
                                            'props':{
                                                'id':{"type":'add-col-value-input',"index":0},
                                                'type':'text',
                                                'required':true
                                            },
                                            'type':'Input',
                                            'namespace':'dash_core_components'
                                        }
                                    ],
                                    'id':{"type":'add-col-grp-2','index':0}
                                },
                                'type':'FormGroup',
                                'namespace':'dash_bootstrap_components'
                            },

                            {
                                'props':{
                                    'id':{"type":'add-col-hr-3','index':0}
                                },
                                'type':'Hr',
                                'namespace':'dash_html_components'
                            }
                        ],
                    'id':"add-col-form"
                },
                'type':'Form',
                'namespace':'dash_bootstrap_components'
            },

            {
                'props':{'children':null},
                'type':'Hr',
                'namespace':'dash_html_components'
            },

            {
                'props':{
                    'children':{
                        'props':{
                            'children':{
                                'props':{
                                    'children':"Add column",
                                    'id':"add-col-new-col-but"
                                },
                                'type':'Button',
                                'namespace':'dash_html_components'
                            }
                        },
                        'type':'Col',
                        'namespace':'dash_bootstrap_components'
                    }
                },
                'type':'Row',
                'namespace':'dash_bootstrap_components'
            }
        ]

        if (triggered.includes('retrived-data.data') && data != null && data != undefined && Object.entries(data['filters_data']['filters']).length !=  0) {
            return [data['filter_rows'], data['add_new_col_rows']]
        } else if (triggered.includes('preview-table-button.n_clicks')) {
            if (n_clicks != null && n_clicks != undefined && n_clicks > 0) {
                return [empty_div,empty_div_add]
            } else {
                window.dash_clientside.no_update
            }
        } else if (triggered.includes('filters-data.data') && Object.entries(filters_data['filters']).length != 0 && filters_data['status'] == true) {
            let fil_div = []
            let add_col_div=[]

            if (Object.entries(filters_data['filters']).length != 0) {
                let in_k = Object.keys(filters_data["filters"])[0]
                let fil_condition_rows = []

                for (i in filters_data['filters'][in_k]['index']) {
                    let form_grp = {
                        'props':{
                            'children':[
                                {
                                    'props':{'children':{
                                        'props':{'children':"value"},
                                        'type':'Strong',
                                        'namespace': 'dash_html_components'
                                    }},
                                    'type':'Label',
                                    'namespace': 'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{"type":'trans-multi-text','index':0},
                                        'style':{'display':'none'}
                                    },
                                    'type':'Dropdown',
                                    'namespace': 'dash_core_components'
                                },

                                {
                                    'props':{
                                        'id':{"type":'trans-text','index':0},
                                        'style':{'display':'none'},
                                        'debounce':true
                                    },
                                    'type':'Input',
                                    'namespace': 'dash_core_components'
                                },

                                {
                                    'props':{
                                        'id':{'type':'trans-input','index':0},
                                        'style':{'display':'none'},
                                        'debounce':true
                                    },
                                    'type':'Input',
                                    'namespace': 'dash_core_components'
                                },

                                {
                                    'props':{
                                        'id':{'type':'trans-date-range','index':0},
                                        'style':{'display':'none'},
                                    },
                                    'type':'DatePickerRange',
                                    'namespace': 'dash_core_components'
                                },

                                {
                                    'props':{
                                        'id':{'type':'trans-date-single','index':0},
                                        'style':{'display':'none'},
                                    },
                                    'type':'DatePickerSingle',
                                    'namespace': 'dash_core_components'
                                },

                                {
                                    'props':{
                                        'id':{'type':'trans-days-single','index':0},
                                        'style':{'display':'none'},
                                    },
                                    'type':'DatePickerSingle',
                                    'namespace': 'dash_core_components'
                                },

                                {
                                    'props':{
                                        'id':{'type':'trans-use-current-date','index':0},
                                        'style':{'display':'none'},
                                    },
                                    'type':'Checklist',
                                    'namespace': 'dash_core_components'
                                },
                            ]
                        },
                        'type':'FormGroup',
                        'namespace': 'dash_bootstrap_components'
                    }

                    if (filters_data['filters'][in_k]['values_vals'][i].constructor == Object
                        && Object.keys(filters_data['filters'][in_k]['values_vals'][i]).includes("trans-multi-text")) {
                        
                        form_grp = {
                            'props':{'children':[
                                {
                                    'props':{'children':{
                                        'props':{'children':"value"},
                                        'type':'Strong',
                                        'namespace': 'dash_html_components'
                                    }},
                                    'type':'Label',
                                    'namespace': 'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{"type":'trans-multi-text','index':filters_data['filters'][in_k]['index'][i]},
                                        'value':filters_data['filters'][in_k]['values'][i],
                                        'multi':true,
                                        'options':filters_data['filters'][in_k]['values_vals'][i]['trans-multi-text']
                                    },
                                    'type':'Dropdown',
                                    'namespace': 'dash_core_components'
                                },
                            ]},
                            'type':'FormGroup',
                            'namespace': 'dash_bootstrap_components'
                        }

                    } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == String
                        && filters_data['filters'][in_k]['values_vals'][i].includes('trans-text') ) {
                        
                        form_grp={
                            'props':{"children":[
                                {
                                    'props':{'children':{
                                        'props':{'children':"value"},
                                        'type':'Strong',
                                        'namespace': 'dash_html_components'
                                    }},
                                    'type':'Label',
                                    'namespace': 'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{"type":'trans-text','index':filters_data['filters'][in_k]['index'][i]},
                                        'debounce':true,
                                        'value':filters_data['filters'][in_k]['values'][i]
                                    },
                                    'type':'Input',
                                    'namespace': 'dash_core_components'
                                },
                            ]},
                            'type':'FormGroup',
                            'namespace': 'dash_bootstrap_components'
                        }

                    } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == String
                        && filters_data['filters'][in_k]['values_vals'][i].includes('trans-input') ) {
                        
                        form_grp={
                            'props':{'children':[
                                {
                                    'props':{'children':{
                                        'props':{'children':"value"},
                                        'type':'Strong',
                                        'namespace': 'dash_html_components'
                                    }},
                                    'type':'Label',
                                    'namespace': 'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{'type':'trans-input','index':filters_data['filters'][in_k]['index'][i]},
                                        'debounce':true,
                                        'value':filters_data['filters'][in_k]['values'][i]
                                    },
                                    'type':'Input',
                                    'namespace': 'dash_core_components'
                                },
                            ]},
                            'type':'FormGroup',
                            'namespace': 'dash_bootstrap_components'
                        }

                    } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == Object
                        && Object.keys(filters_data['filters'][in_k]['values_vals'][i]).includes('trans-date-range')) {
                        
                        form_grp={
                            'props':{'children':[
                                {
                                    'props':{'children':{
                                        'props':{'children':"value"},
                                        'type':'Strong',
                                        'namespace': 'dash_html_components'
                                    }},
                                    'type':'Label',
                                    'namespace': 'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{'type':'trans-date-range','index':filters_data['filters'][in_k]['index'][i]},
                                        'min_date_allowed':filters_data['filters'][in_k]['values_vals'][i]['trans-date-range']['min'],
                                        'max_date_allowed':filters_data['filters'][in_k]['values_vals'][i]['trans-date-range']['max'],
                                        'start_date':filters_data['filters'][in_k]['values'][i][0],
                                        'end_date':filters_data['filters'][in_k]['values'][i][1],
                                    },
                                    'type':'DatePickerRange',
                                    'namespace': 'dash_core_components'
                                },


                            ]},
                            'type':'FormGroup',
                            'namespace': 'dash_bootstrap_components'                    
                        }
                    } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == Object
                        && Object.keys(filters_data['filters'][in_k]['values_vals'][i]).includes('trans-date-single')) {
                        
                        form_grp={
                            'props':{'children':[
                                {
                                    'props':{'children':{
                                        'props':{'children':"value"},
                                        'type':'Strong',
                                        'namespace': 'dash_html_components'
                                    }},
                                    'type':'Label',
                                    'namespace': 'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{'type':'trans-date-single','index':filters_data['filters'][in_k]['index'][i]},
                                        'min_date_allowed':filters_data['filters'][in_k]['values_vals'][i]['trans-date-single']['min'],
                                        'max_date_allowed':filters_data['filters'][in_k]['values_vals'][i]['trans-date-single']['max'],
                                        'date':filters_data['filters'][in_k]['values'][i],
                                    },
                                    'type':'DatePickerSingle',
                                    'namespace': 'dash_core_components'
                                },

                            ]},
                            'type':'FormGroup',
                            'namespace': 'dash_bootstrap_components'                                        
                        }
        

                    } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == Array
                        && filters_data['filters'][in_k]['values_vals'][i].length > 0
                        && filters_data['filters'][in_k]['values_vals'][i].includes('trans-input')
                        && filters_data['filters'][in_k]['values_vals'][i].includes('trans-use-current-date')) {
                        
                        let ck=false
                        let val = null
                        let min_dt=null
                        let max_dt=null

                        let sig_dt={
                            'props':{
                                'id':{'type':'trans-days-single','index':filters_data['filters'][in_k]['index'][i]},
                            },
                            'type':'DatePickerSingle',
                            'namespace': 'dash_core_components'
                        }

                        if (filters_data['filters'][in_k]['values'][i][1].constructor == Array) {
                            ck=true
                            val=filters_data['filters'][in_k]['values'][i][1]
                            min_dt=filters_data['filters'][in_k]['values_vals'][i][2]['trans-days-single']['min']
                            max_dt=filters_data['filters'][in_k]['values_vals'][i][2]['trans-days-single']['max']

                            ck_val={
                                'props':{
                                    'id':{'type':'trans-use-current-date','index':filters_data['filters'][in_k]['index'][i]},
                                    'options':[
                                        {'label': 'Use current sys date', 'value': 'Use'},
                                    ],
                                    'value':val
                                },
                                'type':'Checklist',
                                'namespace': 'dash_core_components'
                            }
                            sig_dt={
                                    'props':{
                                        'id':{'type':'trans-days-single','index':filters_data['filters'][in_k]['index'][i]},
                                        'placeholder':'mm/dd/YYYY',
                                        'min_date_allowed':min_dt,
                                        'max_date_allowed':max_dt,
                                        'initial_visible_month':new Date(),
                                        'disabled':true
                                        
                                    },
                                    'type':'DatePickerSingle',
                                    'namespace': 'dash_core_components'
                                }
                        } else {
                            val=filters_data['filters'][in_k]['values'][i][1]
                            min_dt=filters_data['filters'][in_k]['values_vals'][i][2]['trans-days-single']['min']
                            max_dt=filters_data['filters'][in_k]['values_vals'][i][2]['trans-days-single']['max']

                            sig_dt={
                                'props':{
                                    'id':{'type':'trans-days-single','index':filters_data['filters'][in_k]['index'][i]},
                                    'placeholder':'mm/dd/YYYY',
                                    'min_date_allowed':min_dt,
                                    'max_date_allowed':max_dt,
                                    'date':val
                                },
                                'type':'DatePickerSingle',
                                'namespace': 'dash_core_components'
                            }
                            
                            ck_val={
                                    'props':{
                                        'id':{'type':'trans-use-current-date','index':filters_data['filters'][in_k]['index'][i]},
                                    },
                                    'type':'Checklist',
                                    'namespace': 'dash_core_components'
                            }
                        }
                        
                        form_grp={
                            'props':{'children':[
                                {
                                    'props':{'children':{
                                        'props':{'children':"value"},
                                        'type':'Strong',
                                        'namespace': 'dash_html_components'
                                    }},
                                    'type':'Label',
                                    'namespace': 'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{'type':'trans-input','index':filters_data['filters'][in_k]['index'][i]},
                                        'debounce':true,
                                        'value':filters_data['filters'][in_k]['values'][i][0],
                                        'type':'number',
                                        'required':true,
                                        'inputMode':'numeric'
                                    },
                                    'type':'Input',
                                    'namespace': 'dash_core_components'
                                },

                                sig_dt,
                                ck_val
                            ]},
                            'type':'FormGroup',
                            'namespace': 'dash_bootstrap_components'                    
                        }

                    }
                    
                    condi_row={
                        'props':{'children':[
                            {'props':{'children':{
                                'props':{'children':[
                                            {
                                                'props':{
                                                    'children':{
                                                            'props':{'children':"Select column name"},
                                                            'type':'Strong',
                                                            'namespace': 'dash_html_components'
                                                        },
                                                    'html_for':{'type':'filters-column-names','index':filters_data['filters'][in_k]['index'][i]}
                                                },
                                                'type':'Label',
                                                'namespace':'dash_bootstrap_components'
                                            },
                                            {
                                                'props':{
                                                    'id':{'type':'filters-column-names','index':filters_data['filters'][in_k]['index'][i]},
                                                    'value':filters_data['filters'][in_k]['columns'][i],
                                                    'options':filters_data['filters'][in_k]['columns_drpdwn_vals'][i]
                                                },
                                                'type':'Dropdown',
                                                'namespace':'dash_core_components'
                                            }

                                        ]},
                                    'type':'FormGroup',
                                    'namespace': 'dash_bootstrap_components'                    
                                    },'width':4},
                                'type':'Col',
                                'namespace': 'dash_bootstrap_components'
                            },

                            {
                                'props':{'children':{
                                        'props':{'children':[
                                            {
                                                'props':{
                                                    'children':{
                                                            'props':{'children':"condition"},
                                                            'type':'Strong',
                                                            'namespace': 'dash_html_components'
                                                        },
                                                    'html_for':{'type':'filters-conditions','index':filters_data['filters'][in_k]['index'][i]}
                                                },
                                                'type':'Label',
                                                'namespace':'dash_bootstrap_components'
                                            },

                                            {
                                                'props':{
                                                    'id':{'type':'filters-conditions','index':filters_data['filters'][in_k]['index'][i]},
                                                    'value':filters_data['filters'][in_k]['condition'][i],
                                                    'options':filters_data['filters'][in_k]['condition_drpdwn_vals'][i]
                                                },
                                                'type':'Dropdown',
                                                'namespace':'dash_core_components'
                                            }
                                            
                                        ]},
                                        'type':'FormGroup',
                                        'namespace': 'dash_bootstrap_components'    
                                },'width':3},
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            },

                            {
                                'props':{
                                    'children':form_grp,
                                    'id':{'type':'filters-text-drpdwn','index':filters_data['filters'][in_k]['index'][i]},
                                    'width':4
                                },
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            },

                            {
                                'props':{
                                    'children':{
                                        'props':{
                                            'children':{
                                                'props':{'className':"fa fa-trash-o"},
                                                'type':'I',
                                                'namespace':'dash_html_components'
                                            },
                                            'id':{'type':'logic-close','index':filters_data['filters'][in_k]['index'][i]}
                                        },
                                        'type':'A',
                                        'namespace':'dash_html_components'
                                    },
                                    
                                    'className':"text-right"
                                },
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            },   
                        ],'id':{'type':'condition-rows','index':filters_data['filters'][in_k]['index'][i]}},
                        'type':'Row',
                        'namespace': 'dash_bootstrap_components'
                    }

                    if (filters_data['filters'][in_k]['logic'][i] != null && filters_data['filters'][in_k]['logic'][i] != undefined) {
                        log_row={
                            'props':{'children':{
                                'props':{'children':{
                                    'props':{
                                        'id':{'type':'logic-dropdown','index':i},
                                        'options':[{'label':'And','value':'And'},{'label':'Or','value':'Or'}],
                                        'value':filters_data['filters'][in_k]['logic'][i]
                                    },
                                    'type':'Dropdown',
                                    'namespace':'dash_core_components'

                                },'width':3},
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            },'id':{'type':'filters-logic','index':filters_data['filters'][in_k]['index'][i]}},
                            'type':'Row',
                            'namespace':'dash_bootstrap_components'
                        }
                    } else {
                        log_row = {
                            'props':{'children':{
                                'props':{'children':"This is Temp column and row"},
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            },'id':{"type":"filters-logic","index":0},'style':{'display':'none'}},
                            'type':'Row',
                            'namespace':'dash_bootstrap_components'
                        }
                    }

                    fil_condition_rows.push(log_row)
                    fil_condition_rows.push(condi_row)
                    
                }

                fil_div = [
                    {
                        'props':{'children':[
                            {
                                'props':{'children':{
                                    'props':{
                                        'children':{
                                            'props':{'className':"fa fa-refresh"},
                                            'type':'I',
                                            'namespace':'dash_html_components'
                                        },
                                        'id':'filters-clear-all',
                                        'className':"text-right"
                                    },
                                    'type':'A',
                                    'namespace':'dash_html_components'
                                },'className': 'text-right'},
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            },


                            {
                                'props':{'children':'Select or drop rows'},
                                'type':'Label',
                                'namespace':'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':'filters-select-drop',
                                    'options':[{'label':"Select",'value':"Select"},{'label':"Drop",'value':"Drop"}],
                                    'value':filters_data['filters'][in_k]['select_drop'],
                                    'style':{"width":"50%"}
                                },
                                'type':'Dropdown',
                                'namespace':'dash_core_components'
                            }
                        ]},
                        'type': 'FormGroup',
                        'namespace': 'dash_bootstrap_components'
                    },


                    {
                        'props':{'children':
                            {
                                'props':{'children':"Where"},
                                'type':'Label',
                                'namespace':'dash_html_components'
                            }
                        },
                        'type':'FormGroup',
                        'namespace':'dash_bootstrap_components'
                    },

                    {
                        'props':{'children':fil_condition_rows,'id':'filters-conditional-div'},
                        'type':'Div',
                        'namespace':'dash_html_components'
                    },

                    {
                        'props':{'children':{
                            'props':{"children":{
                                'props':{
                                    'children':'add condition',
                                    'size':'sm',
                                    'id':'filters-add-condition',
                                    'n_clicks':0
                                },
                                'type':'Button',
                                'namespace':'dash_bootstrap_components'
                            }},
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        }},
                        'type':'Row',
                        'namespace':'dash_bootstrap_components'
                    }
                ]
            }
            let add_col_rows=[]
            if (Object.entries(filters_data['add_new_col']).length != 0) {
                let in_kk = Object.keys(filters_data["add_new_col"])[0]

                for (i in filters_data['add_new_col'][in_kk]['index']) {
                    add_col_grp1 = {
                        'props':{
                            'children':[
                                {
                                    'props':{
                                        'children':{
                                            'props':{
                                                'children':{
                                                    'props':{
                                                        'className':"fa fa-trash"
                                                    },
                                                    'type':'I',
                                                    'namespace':'dash_html_components'
                                                },
                                                'id':{'type':'add-col-remove','index':filters_data['add_new_col'][in_kk]['index'][i]}
                                            },
                                            'type':'A',
                                            'namespace':'dash_html_components'
                                        },
                                        'className':"text-right"
                                    },
                                    'type':'Col',
                                    'namespace':'dash_bootstrap_components'
                                },

                                {
                                    'props':{"children":"Enter column name"},
                                    'type':'Label',
                                    'namespace':'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{"type":"add-new-col-name","index":filters_data['add_new_col'][in_kk]['index'][i]},
                                        'type':"text",
                                        'minLength':5,
                                        'required':true,
                                        'value':filters_data['add_new_col'][in_kk]['col_names'][i]
                                    },
                                    'type':'Input',
                                    'namespace':'dash_core_components'
                                },

                                {
                                    'props':{
                                        "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
                                        'color':"secondary"
                                    },
                                    'type':'FormText',
                                    'namespace':'dash_bootstrap_components'
                                },
                            ],
                            'id':{"type":'add-col-grp-1','index':filters_data['add_new_col'][in_kk]['index'][i]}
                        },
                        'type':'FormGroup',
                        'namespace':'dash_bootstrap_components'
                    }
                    add_col_grp2 = {
                        'props':{
                            'children':[
                                {
                                    'props':{'children':"Assign value to new column"},
                                    'type':'Label',
                                    'namespace':'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{"type":'add-col-value-input',"index":filters_data['add_new_col'][in_kk]['index'][i]},
                                        'type':'text',
                                        'required':true,
                                        'value':filters_data['add_new_col'][in_kk]['col_input'][i]
                                    },
                                    'type':'Input',
                                    'namespace':'dash_core_components'
                                }
                            ],
                            'id':{"type":'add-col-grp-2','index':filters_data['add_new_col'][in_kk]['index'][i]}
                        },
                        'type':'FormGroup',
                        'namespace':'dash_bootstrap_components'
                    }
                    add_col_hr3 = {
                        'props':{
                            'id':{"type":'add-col-hr-3','index':filters_data['add_new_col'][in_kk]['index'][i]}
                        },
                        'type':'Hr',
                        'namespace':'dash_html_components'
                    } 

                    add_col_rows.push(add_col_grp1)
                    add_col_rows.push(add_col_grp2)
                    add_col_rows.push(add_col_hr3)
                }

                add_col_div =  [
                    {
                        'props':{
                            'children':add_col_rows,
                            'id':"add-col-form"
                        },
                        'type':'Form',
                        'namespace':'dash_bootstrap_components'
                    },

                    {
                        'props':{'children':null},
                        'type':'Hr',
                        'namespace':'dash_html_components'
                    },

                    {
                        'props':{
                            'children':{
                                'props':{
                                    'children':{
                                        'props':{
                                            'children':"Add column",
                                            'id':"add-col-new-col-but"
                                        },
                                        'type':'Button',
                                        'namespace':'dash_html_components'
                                    }
                                },
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            }
                        },
                        'type':'Row',
                        'namespace':'dash_bootstrap_components'
                    }
                ]

            }

            if (add_col_rows.length > 0 && fil_div.length > 0) {
                return [fil_div, add_col_div]
            } else if (add_col_rows.length == 0 && fil_div.length > 0) {
                return [fil_div, empty_div_add]
            } else if (add_col_rows.length > 0 && fil_div.length == 0) {
                return [empty_div, add_col_div]
            }
        
        } else if (triggered.includes('filters-data.data') && Object.entries(filters_data['filters']).length == 0
            && filters_data['status'] == true) {

            let add_col_rows = []
            let add_col_div=[]

            if (Object.entries(filters_data['add_new_col']).length > 0) {
                let in_kk=Object.keys(filters_data["add_new_col"])[0]

                for (i in filters_data['add_new_col'][in_kk]['index']) {
                    add_col_grp1 = {
                        'props':{
                            'children':[
                                {
                                    'props':{
                                        'children':{
                                            'props':{
                                                'children':{
                                                    'props':{
                                                        'className':"fa fa-trash"
                                                    },
                                                    'type':'I',
                                                    'namespace':'dash_html_components'
                                                },
                                                'id':{'type':'add-col-remove','index':filters_data['add_new_col'][in_kk]['index'][i]}
                                            },
                                            'type':'A',
                                            'namespace':'dash_html_components'
                                        },
                                        'className':"text-right"
                                    },
                                    'type':'Col',
                                    'namespace':'dash_bootstrap_components'
                                },

                                {
                                    'props':{"children":"Enter column name"},
                                    'type':'Label',
                                    'namespace':'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{"type":"add-new-col-name","index":filters_data['add_new_col'][in_kk]['index'][i]},
                                        'type':"text",
                                        'minLength':5,
                                        'required':true,
                                        'value':filters_data['add_new_col'][in_kk]['col_names'][i]
                                    },
                                    'type':'Input',
                                    'namespace':'dash_core_components'
                                },

                                {
                                    'props':{
                                        "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
                                        'color':"secondary"
                                    },
                                    'type':'FormText',
                                    'namespace':'dash_bootstrap_components'
                                },
                            ],
                            'id':{"type":'add-col-grp-1','index':filters_data['add_new_col'][in_kk]['index'][i]}
                        },
                        'type':'FormGroup',
                        'namespace':'dash_bootstrap_components'
                    }
                    add_col_grp2 = {
                        'props':{
                            'children':[
                                {
                                    'props':{'children':"Assign value to new column"},
                                    'type':'Label',
                                    'namespace':'dash_html_components'
                                },

                                {
                                    'props':{
                                        'id':{"type":'add-col-value-input',"index":filters_data['add_new_col'][in_kk]['index'][i]},
                                        'type':'text',
                                        'required':true,
                                        'value':filters_data['add_new_col'][in_kk]['col_input'][i]
                                    },
                                    'type':'Input',
                                    'namespace':'dash_core_components'
                                }
                            ],
                            'id':{"type":'add-col-grp-2','index':filters_data['add_new_col'][in_kk]['index'][i]}
                        },
                        'type':'FormGroup',
                        'namespace':'dash_bootstrap_components'
                    }
                    add_col_hr3 = {
                        'props':{
                            'id':{"type":'add-col-hr-3','index':filters_data['add_new_col'][in_kk]['index'][i]}
                        },
                        'type':'Hr',
                        'namespace':'dash_html_components'
                    } 

                    add_col_rows.push(add_col_grp1)
                    add_col_rows.push(add_col_grp2)
                    add_col_rows.push(add_col_hr3)
                }
                add_col_div =  [
                    {
                        'props':{
                            'children':add_col_rows,
                            'id':"add-col-form"
                        },
                        'type':'Form',
                        'namespace':'dash_bootstrap_components'
                    },

                    {
                        'props':{'children':null},
                        'type':'Hr',
                        'namespace':'dash_html_components'
                    },

                    {
                        'props':{
                            'children':{
                                'props':{
                                    'children':{
                                        'props':{
                                            'children':"Add column",
                                            'id':"add-col-new-col-but"
                                        },
                                        'type':'Button',
                                        'namespace':'dash_html_components'
                                    }
                                },
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            }
                        },
                        'type':'Row',
                        'namespace':'dash_bootstrap_components'
                    }
                ]
            }

            if (add_col_rows.length > 0) {
                return [empty_div, add_col_div]
            } else {
                return [empty_div, empty_div_add]
            }
        } else {
            window.dash_clientside.no_update
        }
    }
    ''',
    Output('filters-div','children'),
    Output('add-new-col-modal-body','children'),
    Input('retrived-data','data'),
    Input('preview-table-button','n_clicks'),
    Input('filters-data','data'),
)

# @app.callback(
#     [
#         Output('filters-div','children'),
#         Output('add-new-col-modal-body','children'),
#     ],
#     [
#         Input('retrived-data','data'),
#         Input('preview-table-button','n_clicks'),
#         # Input({'type':'applied-changes-menu','index':ALL},'n_clicks'),
#         # Input("filters-clear-all","n_clicks"),
#         # Input('add-new-col-modal-apply','n_clicks'),
#         Input('filters-data','data'),
#         # Input('transformations-dropdown','value'),
#         # Input('filters-modal','is_open'),
#     ],
#     [
#         State('filters-div','children'),
#         State('add-new-col-modal-body','children'),
#         State('filters-data','data'),
#     ],
# )
# def update_filter_div(data,n_clicks,\
#     filters_data,childs,add_childs,fil_data):#apply_menu_child,filters-clear-all
#     ctx = callback_context
#     triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

#     # print(f"FILTERS DIV {triggred_compo}",flush=True)
#     # print(f"FILTERS DATA {filters_data}",flush=True)
#     # print(f"FILTERS DIV {len(childs[2]['props']['children'])}",flush=True)
#     # print(f"FILTERS_DIV {filters_data['filters']}")
#     # print(f"FILTERS_DIVvvvv {fil_data['filters']}")

#     empty_div = [
#         FormGroup([
#             Col(html.A(html.I(className="fa fa-refresh"),id='filters-clear-all'),className="text-right"),
#             html.Label("Select or drop rows"),
#             dcc.Dropdown(
#                     id='filters-select-drop',
#                     options=[{'label':i,'value':i} for i in ['Select','Drop']],
#                     value=None,
#                     style={"width":"50%"}
#                 ),
#             # FormText("Type column name without any spaces, special characters. Except 'underscore '_''",color="secondary"),
#         ]),

#         FormGroup([
#             html.Label("Where,")
#         ]),

#         html.Div([
#             Row([
#                 Col(
#                     FormGroup([
#                         Label(html.Strong("Select column name"),html_for={'type':'filters-column-names','index':0}),
#                         dcc.Dropdown(
#                             id={'type':'filters-column-names','index':0},
#                             value=None
#                         )
#                     ])
#                 ,width=4),

#                 Col(
#                     FormGroup([
#                         Label(html.Strong("condition"),html_for={'type':'filters-conditions','index':0}),
#                         dcc.Dropdown(
#                             id={'type':'filters-conditions','index':0}
#                         )
#                     ])
#                 ,width=3),

#                 Col([
#                     FormGroup([
#                         html.Label(html.Strong("value")),
#                         dcc.Dropdown(id={"type":'trans-multi-text','index':0},style={'display':'none'}),
#                         dcc.Input(id={"type":'trans-text','index':0},style={'display':'none'},debounce=True),
#                         dcc.Input(id={'type':'trans-input','index':0},style={'display':'none'},debounce=True),
#                         dcc.DatePickerRange(id={'type':'trans-date-range','index':0},style={'display':'none'}),
#                         dcc.DatePickerSingle(id={'type':'trans-date-single','index':0},style={'display':'none'}),
#                         dcc.DatePickerSingle(id={'type':'trans-days-single','index':0},style={'display':'none'}),
#                         dcc.Checklist(id={'type':'trans-use-current-date','index':0},style={'display':'none'}),
#                     ])
                    
#                 ],id={'type':'filters-text-drpdwn','index':0},width=4),

#                 # Col(dhc.Button(id={'type':'logic-close','index':0},hidden=True))
#                 Col(html.A(html.I(className="fa fa-trash-o"),id={'type':'logic-close','index':0}),className="text-right"),
#                 # Store(id={'type':'filters-rows-trash','index':0},data=None)
            
#             ],id={'type':'condition-rows','index':0}),
#             Row(Col("This is Temp column and row"),id={"type":"filters-logic","index":0},style={'display':'none'}),
#         ],id='filters-conditional-div'),

#         Row(
#             Col(
#                 Button('add condition', size='sm', id='filters-add-condition')
#             )
#         ),
                
#     ]

#     empty_div_add =  [
#         {
#             'props':{
#             'children':[
#                     {
#                         'props':{
#                             'children':[
#                                 {
#                                     'props':{
#                                         'children':{
#                                             'props':{
#                                                 'children':{
#                                                     'props':{
#                                                         'className':"fa fa-trash"
#                                                     },
#                                                     'type':'I',
#                                                     'namespace':'dash_html_components'
#                                                 },
#                                                 'id':{'type':'add-col-remove','index':0}
#                                             },
#                                             'type':'A',
#                                             'namespace':'dash_html_components'
#                                         },
#                                         'className':"text-right"
#                                     },
#                                     'type':'Col',
#                                     'namespace':'dash_bootstrap_components'
#                                 },

#                                 {
#                                     'props':{"children":"Enter column name"},
#                                     'type':'Label',
#                                     'namespace':'dash_html_components'
#                                 },

#                                 {
#                                     'props':{
#                                         'id':{"type":"add-new-col-name","index":0},
#                                         'type':"text",
#                                         'minLength':5,
#                                         'required':True
#                                     },
#                                     'type':'Input',
#                                     'namespace':'dash_core_components'
#                                 },

#                                 {
#                                     'props':{
#                                         "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
#                                         'color':"secondary"
#                                     },
#                                     'type':'FormText',
#                                     'namespace':'dash_bootstrap_components'
#                                 },
#                             ],
#                             'id':{"type":'add-col-grp-1','index':0}
#                         },
#                         'type':'FormGroup',
#                         'namespace':'dash_bootstrap_components'
#                     },

#                     {
#                         'props':{
#                             'children':[
#                                 {
#                                     'props':{'children':"Assign value to new column"},
#                                     'type':'Label',
#                                     'namespace':'dash_html_components'
#                                 },

#                                 {
#                                     'props':{
#                                         'id':{"type":'add-col-value-input',"index":0},
#                                         'type':'text',
#                                         'required':True
#                                     },
#                                     'type':'Input',
#                                     'namespace':'dash_core_components'
#                                 }
#                             ],
#                             'id':{"type":'add-col-grp-2','index':0}
#                         },
#                         'type':'FormGroup',
#                         'namespace':'dash_bootstrap_components'
#                     },

#                     {
#                         'props':{'children':None},
#                         'type':'Hr',
#                         'namespace':'dash_html_components'
#                     }
#                 ],
#                 'id':"add-col-form"
#             },
#             'type':'Form',
#             'namespace':'dash_bootstrap_components'
#         },

#         {
#             'props':{'children':None},
#             'type':'Hr',
#             'namespace':'dash_html_components'
#         },

#         {
#             'props':{
#                 'children':{
#                     'props':{
#                         'children':{
#                             'props':{
#                                 'children':"Add column",
#                                 'id':"add-col-new-col-but"
#                             },
#                             'type':'Button',
#                             'namespace':'dash_html_components'
#                         }
#                     },
#                     'type':'Col',
#                     'namespace':'dash_bootstrap_components'
#                 }
#             },
#             'type':'Row',
#             'namespace':'dash_bootstrap_components'
#         }
#     ]

#     if triggred_compo == 'retrived-data' and data is not None and data['filters_data']['filters'] != {}:
#         return data['filter_rows'], data['add_new_col_rows']
#     elif triggred_compo == 'preview-table-button':
#         if n_clicks is not None:
#             return empty_div, empty_div_add
#         else:
#             raise PreventUpdate
    
#     elif triggred_compo == "filters-data" and filters_data['filters']!={} and \
#         filters_data['status'] is True:
#         fil_div=[]
#         add_col_div=[]
        
#         if len(filters_data['filters']) != 0:
#             in_k=list(filters_data["filters"].keys())[0]
#             fil_condition_rows = []
#             for j,i in enumerate(filters_data['filters'][in_k]['index']): # inside index

#                 form_grp = {
#                     'props':{
#                         'children':[
#                             {
#                                 'props':{'children':{
#                                     'props':{'children':"value"},
#                                     'type':'Strong',
#                                     'namespace': 'dash_html_components'
#                                 }},
#                                 'type':'Label',
#                                 'namespace': 'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{"type":'trans-multi-text','index':0},
#                                     'style':{'display':'none'}
#                                 },
#                                 'type':'Dropdown',
#                                 'namespace': 'dash_core_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{"type":'trans-text','index':0},
#                                     'style':{'display':'none'},
#                                     'debounce':True
#                                 },
#                                 'type':'Input',
#                                 'namespace': 'dash_core_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{'type':'trans-input','index':0},
#                                     'style':{'display':'none'},
#                                     'debounce':True
#                                 },
#                                 'type':'Input',
#                                 'namespace': 'dash_core_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{'type':'trans-date-range','index':0},
#                                     'style':{'display':'none'},
#                                 },
#                                 'type':'DatePickerRange',
#                                 'namespace': 'dash_core_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{'type':'trans-date-single','index':0},
#                                     'style':{'display':'none'},
#                                 },
#                                 'type':'DatePickerSingle',
#                                 'namespace': 'dash_core_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{'type':'trans-days-single','index':0},
#                                     'style':{'display':'none'},
#                                 },
#                                 'type':'DatePickerSingle',
#                                 'namespace': 'dash_core_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{'type':'trans-use-current-date','index':0},
#                                     'style':{'display':'none'},
#                                 },
#                                 'type':'Checklist',
#                                 'namespace': 'dash_core_components'
#                             },
#                         ]
#                     },
#                     'type':'FormGroup',
#                     'namespace': 'dash_bootstrap_components'
#                 }
                

#                 if type(filters_data['filters'][in_k]['values_vals'][j]) is dict and \
#                     'trans-multi-text' in filters_data['filters'][in_k]['values_vals'][j].keys():
                    
#                     form_grp = {
#                         'props':{'children':[
#                             {
#                                 'props':{'children':{
#                                     'props':{'children':"value"},
#                                     'type':'Strong',
#                                     'namespace': 'dash_html_components'
#                                 }},
#                                 'type':'Label',
#                                 'namespace': 'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{"type":'trans-multi-text','index':i},
#                                     'value':filters_data['filters'][in_k]['values'][j],
#                                     'multi':True,
#                                     'options':filters_data['filters'][in_k]['values_vals'][j]['trans-multi-text']
#                                 },
#                                 'type':'Dropdown',
#                                 'namespace': 'dash_core_components'
#                             },
#                         ]},
#                         'type':'FormGroup',
#                         'namespace': 'dash_bootstrap_components'
#                     }
                    
#                     # form_grp=FormGroup([
#                     #         dhc.Label(Strong("value")),
#                     #         Dropdown(id={"type":'trans-multi-text','index':i},value=filters_data['filters'][in_k]['values'][i]),
#                     #         ])
                            
#                 elif type(filters_data['filters'][in_k]['values_vals'][j]) is str and \
#                     filters_data['filters'][in_k]['values_vals'][j] in ['trans-text']:
                    
#                     form_grp={
#                         'props':{"children":[
#                             {
#                                 'props':{'children':{
#                                     'props':{'children':"value"},
#                                     'type':'Strong',
#                                     'namespace': 'dash_html_components'
#                                 }},
#                                 'type':'Label',
#                                 'namespace': 'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{"type":'trans-text','index':i},
#                                     'debounce':True,
#                                     'value':filters_data['filters'][in_k]['values'][j]
#                                 },
#                                 'type':'Input',
#                                 'namespace': 'dash_core_components'
#                             },


#                         ]},
#                         'type':'FormGroup',
#                         'namespace': 'dash_bootstrap_components'
#                     }
                    
#                     # form_grp=FormGroup([
#                     #         dhc.Label(Strong("value")),
#                     #         TextInput(id={"type":'trans-text','index':i},\
#                     #             value=filters_data['filters'][in_k]['values'][i],debounce=True),
#                     #         ])
                
#                 elif type(filters_data['filters'][in_k]['values_vals'][j]) is str and \
#                     filters_data['filters'][in_k]['values_vals'][j] in ['trans-input']:
                    
#                     form_grp={
#                         'props':{'children':[
#                             {
#                                 'props':{'children':{
#                                     'props':{'children':"value"},
#                                     'type':'Strong',
#                                     'namespace': 'dash_html_components'
#                                 }},
#                                 'type':'Label',
#                                 'namespace': 'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{'type':'trans-input','index':i},
#                                     'debounce':True,
#                                     'value':filters_data['filters'][in_k]['values'][j]
#                                 },
#                                 'type':'Input',
#                                 'namespace': 'dash_core_components'
#                             },
#                         ]},
#                         'type':'FormGroup',
#                         'namespace': 'dash_bootstrap_components'
#                     }
                    
#                     # form_grp=FormGroup([
#                     #         dhc.Label(Strong("value")),
#                     #         TextInput(id={"type":'trans-input','index':i},\
#                     #             value=filters_data['filters'][in_k]['values'][i],debounce=True),
#                     #         ])
                
#                 elif type(filters_data['filters'][in_k]['values_vals'][j]) is dict and \
#                     'trans-date-range' in filters_data['filters'][in_k]['values_vals'][j].keys():
                    
#                     form_grp={
#                         'props':{'children':[
#                             {
#                                 'props':{'children':{
#                                     'props':{'children':"value"},
#                                     'type':'Strong',
#                                     'namespace': 'dash_html_components'
#                                 }},
#                                 'type':'Label',
#                                 'namespace': 'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{'type':'trans-date-range','index':i},
#                                     'min_date_allowed':filters_data['filters'][in_k]['values_vals'][j]['trans-date-range']['min'],
#                                     'max_date_allowed':filters_data['filters'][in_k]['values_vals'][j]['trans-date-range']['max'],
#                                     'start_date':filters_data['filters'][in_k]['values'][j][0],
#                                     'end_date':filters_data['filters'][in_k]['values'][j][1],
#                                 },
#                                 'type':'DatePickerRange',
#                                 'namespace': 'dash_core_components'
#                             },


#                         ]},
#                         'type':'FormGroup',
#                         'namespace': 'dash_bootstrap_components'                    
#                     }

#                     # form_grp=FormGroup([
#                     #         dhc.Label(Strong("value")),
#                     #         DatePickerRange(id={'type':'trans-date-range','index':i},
#                     #             min_date_allowed=filters_data['filters'][in_k]['values_vals'][i]['trans-date-range']['min'],
#                     #             max_date_allowed=filters_data['filters'][in_k]['values_vals'][i]['trans-date-range']['max'],
#                     #             start_date=filters_data['filters'][in_k]['values'][i][0],
#                     #             end_date=filters_data['filters'][in_k]['values'][i][1],
#                     #         )
#                     #     ])
                
#                 elif type(filters_data['filters'][in_k]['values_vals'][j]) is dict and \
#                     'trans-date-single' in filters_data['filters'][in_k]['values_vals'][j].keys():
                    
#                     form_grp={
#                         'props':{'children':[
#                             {
#                                 'props':{'children':{
#                                     'props':{'children':"value"},
#                                     'type':'Strong',
#                                     'namespace': 'dash_html_components'
#                                 }},
#                                 'type':'Label',
#                                 'namespace': 'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{'type':'trans-date-single','index':i},
#                                     'min_date_allowed':filters_data['filters'][in_k]['values_vals'][j]['trans-date-single']['min'],
#                                     'max_date_allowed':filters_data['filters'][in_k]['values_vals'][j]['trans-date-single']['max'],
#                                     'date':filters_data['filters'][in_k]['values'][j],
#                                 },
#                                 'type':'DatePickerSingle',
#                                 'namespace': 'dash_core_components'
#                             },

#                         ]},
#                         'type':'FormGroup',
#                         'namespace': 'dash_bootstrap_components'                                        
#                     }
                    
#                     # form_grp=FormGroup([
#                     #         dhc.Label(Strong("value")),
#                     #         DatePickerRange(id={'type':'trans-date-single','index':i},
#                     #             min_date_allowed=filters_data['filters'][in_k]['values_vals'][i]['trans-date-single']['min'],
#                     #             max_date_allowed=filters_data['filters'][in_k]['values_vals'][i]['trans-date-single']['max'],
#                     #             date=filters_data['filters'][in_k]['values'][i],
#                     #         )
#                     #     ])

#                 elif type(filters_data['filters'][in_k]['values_vals'][j]) is list and \
#                     filters_data['filters'][in_k]['values_vals'][j] != [] and \
#                     all(t in filters_data['filters'][in_k]['values_vals'][j] for t in ['trans-input', 'trans-use-current-date']):

#                     ck=False
#                     val = None
#                     min_dt=None
#                     max_dt=None

#                     sig_dt={
#                                 'props':{
#                                     'id':{'type':'trans-days-single','index':i},
#                                     # 'style':{'display':'none'},
#                                 },
#                                 'type':'DatePickerSingle',
#                                 'namespace': 'dash_core_components'
#                             }
                    

#                     # sig_dt=DatePickerSingle(id={'type':'trans-days-single','index':0},style={'display':'none'})
#                     # ck_val=Checklist(id={'type':'trans-use-current-date','index':0},style={'display':'none'})
#                     if type(filters_data['filters'][in_k]['values'][j][1]) is list:
#                         ck=True
#                         val=filters_data['filters'][in_k]['values'][j][1]
#                         min_dt=filters_data['filters'][in_k]['values_vals'][j][2]['trans-days-single']['min']
#                         max_dt=filters_data['filters'][in_k]['values_vals'][j][2]['trans-days-single']['max']
#                         # ck_val=Checklist(
#                         #     id={'type':'trans-use-current-date','index':i},
#                         #     options=[
#                         #         {'label': 'Use current sys date', 'value': 'Use'},
#                         #     ],
#                         #     value=val
#                         # )
#                         ck_val={
#                                 'props':{
#                                     'id':{'type':'trans-use-current-date','index':i},
#                                     'options':[
#                                         {'label': 'Use current sys date', 'value': 'Use'},
#                                     ],
#                                     'value':val
#                                 },
#                                 'type':'Checklist',
#                                 'namespace': 'dash_core_components'
#                             }
#                         sig_dt={
#                                 'props':{
#                                     'id':{'type':'trans-days-single','index':i},
#                                     'placeholder':'mm/dd/YYYY',
#                                     'min_date_allowed':min_dt,
#                                     'max_date_allowed':max_dt,
#                                     'initial_visible_month':date.today(),
#                                     'disabled':True
#                                     # 'date':val
#                                 },
#                                 'type':'DatePickerSingle',
#                                 'namespace': 'dash_core_components'
#                             }
#                     else:
#                         val=filters_data['filters'][in_k]['values'][j][1]
#                         min_dt=filters_data['filters'][in_k]['values_vals'][j][2]['trans-days-single']['min']
#                         max_dt=filters_data['filters'][in_k]['values_vals'][j][2]['trans-days-single']['max']
#                         # sig_dt=DatePickerSingle(
#                         #     id={'type':'trans-days-single','index':i},
#                         #     placeholder='mm/dd/YYYY',
#                         #     min_date_allowed=min_dt,
#                         #     max_date_allowed=max_dt,
#                         #     # initial_visible_month=date.today(),
#                         #     date=val
#                         # )
#                         sig_dt={
#                                 'props':{
#                                     'id':{'type':'trans-days-single','index':i},
#                                     'placeholder':'mm/dd/YYYY',
#                                     'min_date_allowed':min_dt,
#                                     'max_date_allowed':max_dt,
#                                     # initial_visible_month=date.today(),
#                                     'date':val
#                                 },
#                                 'type':'DatePickerSingle',
#                                 'namespace': 'dash_core_components'
#                             }
                            
#                         ck_val={
#                                 'props':{
#                                     'id':{'type':'trans-use-current-date','index':i},
#                                     # 'style':{'display':'none'},
#                                 },
#                                 'type':'Checklist',
#                                 'namespace': 'dash_core_components'
#                             }

                    
#                     form_grp={
#                         'props':{'children':[
#                             {
#                                 'props':{'children':{
#                                     'props':{'children':"value"},
#                                     'type':'Strong',
#                                     'namespace': 'dash_html_components'
#                                 }},
#                                 'type':'Label',
#                                 'namespace': 'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{'type':'trans-input','index':i},
#                                     'debounce':True,
#                                     'value':filters_data['filters'][in_k]['values'][j][0],
#                                     'type':'number',
#                                     'required':True,
#                                     'inputMode':'numeric'
#                                 },
#                                 'type':'Input',
#                                 'namespace': 'dash_core_components'
#                             },

#                             sig_dt,
#                             ck_val
#                         ]},
#                         'type':'FormGroup',
#                         'namespace': 'dash_bootstrap_components'                    
#                     }


#                     # form_grp=FormGroup([
#                     #     dhc.Label(Strong("value")),
#                     #     TextInput(id={'type':'trans-input','index':i},persistence=True,\
#                     #         value=filters_data['filters'][in_k]['values'][i][0],debounce=True),
#                     #     sig_dt,
#                     #     ck_val
#                     # ]) 

#                 condi_row={
#                     'props':{'children':[


#                         {'props':{'children':{
#                             'props':{'children':[
#                                         {
#                                             'props':{
#                                                 'children':{
#                                                         'props':{'children':"Select column name"},
#                                                         'type':'Strong',
#                                                         'namespace': 'dash_html_components'
#                                                     },
#                                                 'html_for':{'type':'filters-column-names','index':i}
#                                             },
#                                             'type':'Label',
#                                             'namespace':'dash_bootstrap_components'
#                                         },
#                                         {
#                                             'props':{
#                                                 'id':{'type':'filters-column-names','index':i},
#                                                 'value':filters_data['filters'][in_k]['columns'][j],
#                                                 'options':filters_data['filters'][in_k]['columns_drpdwn_vals'][j]
#                                             },
#                                             'type':'Dropdown',
#                                             'namespace':'dash_core_components'
#                                         }

#                                     ]},
#                                 'type':'FormGroup',
#                                 'namespace': 'dash_bootstrap_components'                    
#                                 },'width':4},
#                             'type':'Col',
#                             'namespace': 'dash_bootstrap_components'
#                         },

#                         {
#                             'props':{'children':{
#                                     'props':{'children':[
#                                         {
#                                             'props':{
#                                                 'children':{
#                                                         'props':{'children':"condition"},
#                                                         'type':'Strong',
#                                                         'namespace': 'dash_html_components'
#                                                     },
#                                                 'html_for':{'type':'filters-conditions','index':i}
#                                             },
#                                             'type':'Label',
#                                             'namespace':'dash_bootstrap_components'
#                                         },

#                                         {
#                                             'props':{
#                                                 'id':{'type':'filters-conditions','index':i},
#                                                 'value':filters_data['filters'][in_k]['condition'][j],
#                                                 'options':filters_data['filters'][in_k]['condition_drpdwn_vals'][j]
#                                             },
#                                             'type':'Dropdown',
#                                             'namespace':'dash_core_components'
#                                         }
                                        
#                                     ]},
#                                     'type':'FormGroup',
#                                     'namespace': 'dash_bootstrap_components'    
#                             },'width':3},
#                             'type':'Col',
#                             'namespace':'dash_bootstrap_components'
#                         },

#                         {
#                             'props':{
#                                 'children':form_grp,
#                                 'id':{'type':'filters-text-drpdwn','index':i},
#                                 'width':4
#                             },
#                             'type':'Col',
#                             'namespace':'dash_bootstrap_components'
#                         },

#                         {
#                             'props':{
#                                 'children':{
#                                     'props':{
#                                         'children':{
#                                             'props':{'className':"fa fa-trash-o"},
#                                             'type':'I',
#                                             'namespace':'dash_html_components'
#                                         },
#                                         'id':{'type':'logic-close','index':i}
#                                     },
#                                     'type':'A',
#                                     'namespace':'dash_html_components'
#                                 },
                                
#                                 'className':"text-right"
#                             },
#                             'type':'Col',
#                             'namespace':'dash_bootstrap_components'
#                         },

#                         # {

#                         #     'props':{
#                         #         'id':{'type':'filters-rows-trash','index':0},
#                         #         'data':None
#                         #     },
#                         #     'type':'Store',
#                         #     'namespace':'dash_core_components'
#                         # },


#                     ],'id':{'type':'condition-rows','index':i}},
#                     'type':'Row',
#                     'namespace': 'dash_bootstrap_components'
#                 }
                
#                 if filters_data['filters'][in_k]['logic'][j] is not None:
#                     log_row={
#                         'props':{'children':{
#                             'props':{'children':{
#                                 'props':{
#                                     'id':{'type':'logic-dropdown','index':i},
#                                     'options':[{'label':v,'value':v} for v in ["And","Or"]],
#                                     'value':filters_data['filters'][in_k]['logic'][j]
#                                 },
#                                 'type':'Dropdown',
#                                 'namespace':'dash_core_components'

#                             },'width':3},
#                             'type':'Col',
#                             'namespace':'dash_bootstrap_components'
#                         },'id':{'type':'filters-logic','index':i}},
#                         'type':'Row',
#                         'namespace':'dash_bootstrap_components'
#                     }

#                 else:
#                     log_row = {
#                         'props':{'children':{
#                             'props':{'children':"This is Temp column and row"},
#                             'type':'Col',
#                             'namespace':'dash_bootstrap_components'
#                         },'id':{"type":"filters-logic","index":0},'style':{'display':'none'}},
#                         'type':'Row',
#                         'namespace':'dash_bootstrap_components'
#                     }
#                     # log_row=Row(Col("This is Temp column and row"),id={"type":"filters-logic","index":0},style={'display':'none'}),

#                 fil_condition_rows.append(log_row)
#                 fil_condition_rows.append(condi_row)
                

#             # print(f"DFD {fil_condition_rows}")
#             fil_div = [
#                 {
#                     'props':{'children':[
#                         {
#                             'props':{'children':{
#                                 'props':{
#                                     'children':{
#                                         'props':{'className':"fa fa-refresh"},
#                                         'type':'I',
#                                         'namespace':'dash_html_components'
#                                     },
#                                     'id':'filters-clear-all'
#                                 },
#                                 'type':'A',
#                                 'namespace':'dash_html_components'
#                             },'className': 'text-right'},
#                             'type':'Col',
#                             'namespace':'dash_bootstrap_components'
#                         },


#                         {
#                             'props':{'children':'Select or drop rows'},
#                             'type':'Label',
#                             'namespace':'dash_html_components'
#                         },

#                         {
#                             'props':{
#                                 'id':'filters-select-drop',
#                                 'options':[{'label':v,'value':v} for v in ['Select','Drop']],
#                                 'value':filters_data['filters'][in_k]['select_drop'],
#                                 'style':{"width":"50%"}
#                             },
#                             'type':'Dropdown',
#                             'namespace':'dash_core_components'
#                         }
#                     ]},
#                     'type': 'FormGroup',
#                     'namespace': 'dash_bootstrap_components'
#                 },


#                 {
#                     'props':{'children':
#                         {
#                             'props':{'children':"Where"},
#                             'type':'Label',
#                             'namespace':'dash_html_components'
#                         }
#                     },
#                     'type':'FormGroup',
#                     'namespace':'dash_bootstrap_components'
#                 },

#                 {
#                     'props':{'children':fil_condition_rows,'id':'filters-conditional-div'},
#                     'type':'Div',
#                     'namespace':'dash_html_components'
#                 },

#                 {
#                     'props':{'children':{
#                         'props':{"children":{
#                             'props':{
#                                 'children':'add condition',
#                                 'size':'sm',
#                                 'id':'filters-add-condition',
#                                 'n_clicks':0
#                             },
#                             'type':'Button',
#                             'namespace':'dash_bootstrap_components'
#                         }},
#                         'type':'Col',
#                         'namespace':'dash_bootstrap_components'
#                     }},
#                     'type':'Row',
#                     'namespace':'dash_bootstrap_components'
#                 }
#             ]
            
#         add_col_rows=[]
#         if len(filters_data['add_new_col']) != 0:
#             in_kk=list(filters_data["add_new_col"].keys())[0]
            

            
#             # add_col_rows=[]
#             for j,i in enumerate(filters_data['add_new_col'][in_kk]['index']):
#                 add_col_grp1 = {
#                     'props':{
#                         'children':[
#                             {
#                                 'props':{
#                                     'children':{
#                                         'props':{
#                                             'children':{
#                                                 'props':{
#                                                     'className':"fa fa-trash"
#                                                 },
#                                                 'type':'I',
#                                                 'namespace':'dash_html_components'
#                                             },
#                                             'id':{'type':'add-col-remove','index':i}
#                                         },
#                                         'type':'A',
#                                         'namespace':'dash_html_components'
#                                     },
#                                     'className':"text-right"
#                                 },
#                                 'type':'Col',
#                                 'namespace':'dash_bootstrap_components'
#                             },

#                             {
#                                 'props':{"children":"Enter column name"},
#                                 'type':'Label',
#                                 'namespace':'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{"type":"add-new-col-name","index":i},
#                                     'type':"text",
#                                     'minLength':5,
#                                     'required':True,
#                                     'value':filters_data['add_new_col'][in_kk]['col_names'][j]
#                                 },
#                                 'type':'Input',
#                                 'namespace':'dash_core_components'
#                             },

#                             {
#                                 'props':{
#                                     "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
#                                     'color':"secondary"
#                                 },
#                                 'type':'FormText',
#                                 'namespace':'dash_bootstrap_components'
#                             },
#                         ],
#                         'id':{"type":'add-col-grp-1','index':i}
#                     },
#                     'type':'FormGroup',
#                     'namespace':'dash_bootstrap_components'
#                 }
#                 add_col_grp2 = {
#                     'props':{
#                         'children':[
#                             {
#                                 'props':{'children':"Assign value to new column"},
#                                 'type':'Label',
#                                 'namespace':'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{"type":'add-col-value-input',"index":i},
#                                     'type':'text',
#                                     'required':True,
#                                     'value':filters_data['add_new_col'][in_kk]['col_input'][j]
#                                 },
#                                 'type':'Input',
#                                 'namespace':'dash_core_components'
#                             }
#                         ],
#                         'id':{"type":'add-col-grp-2','index':i}
#                     },
#                     'type':'FormGroup',
#                     'namespace':'dash_bootstrap_components'
#                 }
#                 add_col_hr3 = {
#                     'props':{'children':None},
#                     'type':'Hr',
#                     'namespace':'dash_html_components'
#                 }            

        

#                 add_col_rows.append(add_col_grp1)
#                 add_col_rows.append(add_col_grp2)
#                 add_col_rows.append(add_col_hr3)
            
#             # print(f"sdfsdf {fil_div}")
#             # print(f"dssdf {childs}")
#             add_col_div =  [
#                 {
#                     'props':{
#                         'children':add_col_rows,
#                         'id':"add-col-form"
#                     },
#                     'type':'Form',
#                     'namespace':'dash_bootstrap_components'
#                 },

#                 {
#                     'props':{'children':None},
#                     'type':'Hr',
#                     'namespace':'dash_html_components'
#                 },

#                 {
#                     'props':{
#                         'children':{
#                             'props':{
#                                 'children':{
#                                     'props':{
#                                         'children':"Add column",
#                                         'id':"add-col-new-col-but"
#                                     },
#                                     'type':'Button',
#                                     'namespace':'dash_html_components'
#                                 }
#                             },
#                             'type':'Col',
#                             'namespace':'dash_bootstrap_components'
#                         }
#                     },
#                     'type':'Row',
#                     'namespace':'dash_bootstrap_components'
#                 }
#             ]
#         if add_col_rows != [] and fil_div != []:
#             return fil_div, add_col_div
#         elif fil_div != [] and add_col_rows == []:
#             return fil_div, empty_div_add
#         elif fil_div == [] and add_col_rows != []:
#             return empty_div, add_col_div

#     elif triggred_compo == "filters-data" and filters_data['filters']=={} and \
#         filters_data['status'] is True:
#         add_col_rows=[]
#         add_col_div=[]
#         if len(filters_data['add_new_col']) != 0:
#             in_kk=list(filters_data["add_new_col"].keys())[0]
            
#             # add_col_rows=[]
#             for j,i in enumerate(filters_data['add_new_col'][in_kk]['index']):
#                 add_col_grp1 = {
#                     'props':{
#                         'children':[
#                             {
#                                 'props':{
#                                     'children':{
#                                         'props':{
#                                             'children':{
#                                                 'props':{
#                                                     'className':"fa fa-trash"
#                                                 },
#                                                 'type':'I',
#                                                 'namespace':'dash_html_components'
#                                             },
#                                             'id':{'type':'add-col-remove','index':i}
#                                         },
#                                         'type':'A',
#                                         'namespace':'dash_html_components'
#                                     },
#                                     'className':"text-right"
#                                 },
#                                 'type':'Col',
#                                 'namespace':'dash_bootstrap_components'
#                             },

#                             {
#                                 'props':{"children":"Enter column name"},
#                                 'type':'Label',
#                                 'namespace':'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{"type":"add-new-col-name","index":i},
#                                     'type':"text",
#                                     'minLength':5,
#                                     'required':True,
#                                     'value':filters_data['add_new_col'][in_kk]['col_names'][j]
#                                 },
#                                 'type':'Input',
#                                 'namespace':'dash_core_components'
#                             },

#                             {
#                                 'props':{
#                                     "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
#                                     'color':"secondary"
#                                 },
#                                 'type':'FormText',
#                                 'namespace':'dash_bootstrap_components'
#                             },
#                         ],
#                         'id':{"type":'add-col-grp-1','index':i}
#                     },
#                     'type':'FormGroup',
#                     'namespace':'dash_bootstrap_components'
#                 }
#                 add_col_grp2 = {
#                     'props':{
#                         'children':[
#                             {
#                                 'props':{'children':"Assign value to new column"},
#                                 'type':'Label',
#                                 'namespace':'dash_html_components'
#                             },

#                             {
#                                 'props':{
#                                     'id':{"type":'add-col-value-input',"index":i},
#                                     'type':'text',
#                                     'required':True,
#                                     'value':filters_data['add_new_col'][in_kk]['col_input'][j]
#                                 },
#                                 'type':'Input',
#                                 'namespace':'dash_core_components'
#                             }
#                         ],
#                         'id':{"type":'add-col-grp-2','index':i}
#                     },
#                     'type':'FormGroup',
#                     'namespace':'dash_bootstrap_components'
#                 }
#                 add_col_hr3 = {
#                     'props':{'children':None},
#                     'type':'Hr',
#                     'namespace':'dash_html_components'
#                 }            

        

#                 add_col_rows.append(add_col_grp1)
#                 add_col_rows.append(add_col_grp2)
#                 add_col_rows.append(add_col_hr3)
            
#             # print(f"sdfsdf {fil_div}")
#             # print(f"dssdf {childs}")
#             add_col_div =  [
#                 {
#                     'props':{
#                         'children':add_col_rows,
#                         'id':"add-col-form"
#                     },
#                     'type':'Form',
#                     'namespace':'dash_bootstrap_components'
#                 },

#                 {
#                     'props':{'children':None},
#                     'type':'Hr',
#                     'namespace':'dash_html_components'
#                 },

#                 {
#                     'props':{
#                         'children':{
#                             'props':{
#                                 'children':{
#                                     'props':{
#                                         'children':"Add column",
#                                         'id':"add-col-new-col-but"
#                                     },
#                                     'type':'Button',
#                                     'namespace':'dash_html_components'
#                                 }
#                             },
#                             'type':'Col',
#                             'namespace':'dash_bootstrap_components'
#                         }
#                     },
#                     'type':'Row',
#                     'namespace':'dash_bootstrap_components'
#                 }
#             ]
#         if add_col_rows != []:
#             return empty_div, add_col_div
#         else:
#             return empty_div, empty_div_add
#     else:
#         # return childs
#         raise PreventUpdate

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
app.clientside_callback(
    '''
    function update_filters_condition_div(n_clicks,childs,trans_columns,ret_stat,condi_id,fil_logic_id) {
        let childs_copy = childs
        let z = []
        for (let d in childs) {
            if (childs[d]['type'] != 'Br' && (childs[d]['props']['children'] == null
                || childs[d]['props']['children'] == undefined)) {
                childs_copy.splice(d,1)
            }
        }
        
        for (let d in childs) {
            if (childs[d]['type'] == 'Br') {
                childs_copy.splice(d,1)
            }
        }

        if (n_clicks != null && childs_copy.length > 0) {
            let indx = []
            for (let i in condi_id) {
                indx.push(Number(condi_id[i]['index']))
            }
            let idx = 0
            if (indx.length > 0) {
                let idx = Math.max.apply(null,indx)
            }

            indx = Number(idx)+1

            let col_val = []
            let col_keys = Object.keys(trans_columns)
            
            for (let i in col_keys) {
                col_val.push({'label':col_keys[i],'value':col_keys[i]})
            }

            let condition_row = {
                'props':{
                    'children':[
                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':[
                                            {
                                                'props':{
                                                    'children':{
                                                        'props':{'children':'Select column name'},
                                                        'type':'Strong',
                                                        'namespace':'dash_html_components'
                                                    },
                                                    'html_for':{'type':'filters-column-names','index':indx}
                                                },
                                                'type':'Label',
                                                'namespace':'dash_bootstrap_components'
                                            },

                                            {
                                                'props':{
                                                    'id':{'type':'filters-column-names','index':indx},
                                                    'options':col_val,
                                                    'value':null
                                                },
                                                'type':'Dropdown',
                                                'namespace':'dash_core_components'
                                            }
                                        ],
                                    },
                                    'type':'FormGroup',
                                        'namespace':'dash_bootstrap_components'
                                },
                                'width':4
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':[
                                            {
                                                'props':{
                                                    'children':{
                                                        'props':{'children':'condition'},
                                                        'type':'Strong',
                                                        'namespace':'dash_html_components'
                                                    },
                                                    'html_for':{'type':'filters-conditions','index':indx}
                                                },
                                                'type':'Label',
                                                'namespace':'dash_bootstrap_components'
                                            },

                                            {
                                                'props':{
                                                    'id':{'type':'filters-conditions','index':indx},
                                                },
                                                'type':'Dropdown',
                                                'namespace':'dash_core_components'
                                            }
                                        ],
                                    },
                                    'type':'FormGroup',
                                        'namespace':'dash_bootstrap_components'
                                },
                                'width':3
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'id':{'type':'filters-text-drpdwn','index':indx},
                                'width':4
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':{
                                            'props':{
                                                'className':"fa fa-trash-o"
                                            },
                                            'type':'I',
                                            'namespace':'dash_html_components'
                                        },
                                        'id':{'type':'logic-close','index':indx}
                                    },
                                    'type':'A',
                                    'namespace':'dash_html_components'
                                },
                                'className':"text-right"
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        }
                    ],
                    'id':{'type':'condition-rows','index':indx}
                },
                'type':'Row',
                'namespace':'dash_bootstrap_components'
            }

            let logic_and_or = {
                'props':{
                    'children':[
                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'id':{'type':'logic-dropdown','index':indx},
                                        'options':[{'label':'And','value':'And'},{'label':'Or','value':'Or'}]
                                    },
                                    'type':'Dropdown',
                                    'namespace':'dash_core_components'
                                },
                                'width':3
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        }
                    ],
                    'id':{'type':'filters-logic','index':indx}
                },
                'type':'Row',
                'namespace':'dash_bootstrap_components'
            }

            childs_copy.push({'props':{'children':null},'type':'Br','namespace':'dash_html_components'})
            childs_copy.push(logic_and_or)
            childs_copy.push(condition_row)

            return childs_copy
        } else if (n_clicks != null && childs_copy.length == 0) {
            let indx = []
            for (let i in fil_logic_id) {
                indx.push(Number(fil_logic_id[i]['index']))
            }

            let idx = 0
            if (indx.length > 0) {
                let idx = Math.max.apply(null,indx)
            }

            indx = Number(idx)+1

            let col_val = []
            let col_keys = Object.keys(trans_columns)
            
            for (let i in col_keys) {
                col_val.push({'label':col_keys[i],'value':col_keys[i]})
            }

            let condition_row = {
                'props':{
                    'children':[
                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':[
                                            {
                                                'props':{
                                                    'children':{
                                                        'props':{'children':'Select column name'},
                                                        'type':'Strong',
                                                        'namespace':'dash_html_components'
                                                    },
                                                    'html_for':{'type':'filters-column-names','index':indx}
                                                },
                                                'type':'Label',
                                                'namespace':'dash_bootstrap_components'
                                            },

                                            {
                                                'props':{
                                                    'id':{'type':'filters-column-names','index':indx},
                                                    'options':col_val,
                                                    'value':null
                                                },
                                                'type':'Dropdown',
                                                'namespace':'dash_core_components'
                                            }
                                        ],
                                    },
                                    'type':'FormGroup',
                                        'namespace':'dash_bootstrap_components'
                                },
                                'width':4
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':[
                                            {
                                                'props':{
                                                    'children':{
                                                        'props':{'children':'condition'},
                                                        'type':'Strong',
                                                        'namespace':'dash_html_components'
                                                    },
                                                    'html_for':{'type':'filters-conditions','index':indx}
                                                },
                                                'type':'Label',
                                                'namespace':'dash_bootstrap_components'
                                            },

                                            {
                                                'props':{
                                                    'id':{'type':'filters-conditions','index':indx},
                                                },
                                                'type':'Dropdown',
                                                'namespace':'dash_core_components'
                                            }
                                        ],
                                    },
                                    'type':'FormGroup',
                                        'namespace':'dash_bootstrap_components'
                                },
                                'width':3
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'id':{'type':'filters-text-drpdwn','index':indx},
                                'width':4
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':{
                                            'props':{
                                                'className':"fa fa-trash-o"
                                            },
                                            'type':'I',
                                            'namespace':'dash_html_components'
                                        },
                                        'id':{'type':'logic-close','index':indx}
                                    },
                                    'type':'A',
                                    'namespace':'dash_html_components'
                                },
                                'className':"text-right"
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        }
                    ],
                    'id':{'type':'condition-rows','index':indx}
                },
                'type':'Row',
                'namespace':'dash_bootstrap_components'
            }

            let logic_and_or = {
                'props':{
                    'children':[
                        {
                            'props':{
                                'children':"This is Temp column and row",
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        }
                    ],
                    'id':{"type":"filters-logic","index":indx},
                    'style':{'display':'none'}
                },
                'type':'Row',
                'namespace':'dash_bootstrap_components'
            }

            childs_copy.push({'props':{'children':null},'type':'Br','namespace':'dash_html_components'})
            childs_copy.push(logic_and_or)
            childs_copy.push(condition_row)

            return childs_copy
        }
    }
    ''',
    Output('filters-conditional-div','children'),
    Input('filters-add-condition','n_clicks'),
    State('filters-conditional-div','children'),
    State('transformations-table-column-data','data'),
    State('filters-retrived-status','data'),
    State({'type':'condition-rows','index':ALL},'id'),
    State({'type':'filters-logic','index':ALL},'id'),
    prevent_initial_call=True
)

# @app.callback(
#     Output('filters-conditional-div','children'),
#     [
#         Input('filters-add-condition','n_clicks'),
#     ],
#     [
#         State('filters-conditional-div','children'),
#         State('transformations-table-column-data','data'),
#         State('filters-retrived-status','data'),
#         State({'type':'condition-rows','index':ALL},'id'),
#         State({'type':'filters-logic','index':ALL},'id')
#     ],
# )
# def update_filters_condition_div(n_clicks,childs,trans_columns,ret_stat,condi_id,\
#     fil_logic_id):
#     ctx = callback_context
#     triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]
#     # print(f"Files list {childs}")
#     childs_copy=childs.copy()
#     z=[childs_copy.remove(d) for d in childs if d['type']!="Br" and d['props']['children']==None]
#     if set(z) == set([None]):
#         [childs_copy.remove(d) for d in childs if d['type']=="Br"]
    
#     if triggred_compo == 'filters-add-condition' and n_clicks is not None and childs_copy!=[]:
#         indx=[int(i['index']) for i in condi_id]
#         if indx != []:
#             indx=array(indx).max()
#         else:
#             indx=0

#         indx = int(indx+1)

#         # indx = n_clicks + 1
#         condition_row = get_condition_rows(trans_columns,indx)
#         logic_and_or = Row([
#             Col(
#                 dcc.Dropdown(id={'type':'logic-dropdown','index':indx},
#                     options=[{'label':i,'value':i} for i in ["And","Or"]]
#                 )
#             ,width=3),
#         ],id={'type':'filters-logic','index':indx})
#         childs_copy.append(html.Br())
#         childs_copy.append(logic_and_or)
#         childs_copy.append(condition_row)
#         # print(f"\n\n DIV list {childs_copy}")
#         return childs_copy
#     elif triggred_compo == 'filters-add-condition' and n_clicks is not None and childs_copy==[]:
#         indx=[int(i['index']) for i in fil_logic_id]
#         if indx != []:
#             indx=array(indx).max()
#         else:
#             indx=0

#         indx = int(indx+1)
#         # indx = n_clicks + 1
#         condition_row = get_condition_rows(trans_columns,indx)
#         # print("got columns")
#         logic_and_or = Row(Col("This is Temp column and row"),id={"type":"filters-logic",\
#             "index":indx},style={'display':'none'})
#         childs_copy.append(html.Br())
#         childs_copy.append(logic_and_or)
#         childs_copy.append(condition_row)
#         return childs_copy

#     else:
#         raise PreventUpdate

# @app.callback(
#     # Output('filters-rows-trash','data'),
#     Output('filter-trash-trigger','data'),
#     [
#        Input('filters-rows-trash','data'),
#     ]
# )
# def update_fil_rows_trash(data):
#     print(f"DFDFDDDDDD {data}")    
#     if data != [] and data is not None and any(data):
#         return int(next(item for item in data if item is not None))
#     else:
#         raise PreventUpdate
#     ctx = callback_context
#     triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]
#     print(f"DFDFDDDDDD {disabled}")
#     print(f"DFDFDDDDDD {data['filters']}")
#     print(f"DFDFDDDDDD {n_clicks}")
#     if data['filters']!={} and any(n_clicks) and disabled is False:
#         in_k=list(data["filters"].keys())[0]
#         for i,j in enumerate(n_clicks):
#             if j is not None and logic_close_id[i]['index'] in data['filters'][in_k]['index']:
#                 return logic_close_id[i]['index']
#             else:
#                 raise PreventUpdate
#     # if data['filters']!={} and any(n_clicks) and triggred_compo == "filters-close" and\
#     #     fil_close is not None:


#     else:
#         raise PreventUpdate
        
# clear added filter component
app.clientside_callback(
    '''
    function close_condition(n_clicks,condi_rows,fil_logic) {
        //console.log('logic-close',n_clicks)
        if (n_clicks != null && n_clicks != undefined && n_clicks > 0){
            return [null, null]
        } else {
            return [condi_rows,fil_logic]
        }
    }
    ''',
    Output({'type':'condition-rows','index':MATCH},'children'),
    Output({'type':'filters-logic','index':MATCH},'children'),
    Input({'type':'logic-close','index':MATCH},'n_clicks'),#filters trash icon click
    # State({'type':'logic-close','index':MATCH},'id'),
    State({'type':'condition-rows','index':MATCH},'children'),
    State({'type':'filters-logic','index':MATCH},'children'),
    # State('filters-data','data'),
    prevent_initial_call=True
)

# @app.callback(
#     [
#         Output({'type':'condition-rows','index':MATCH},'children'),
#         Output({'type':'filters-logic','index':MATCH},'children'),
#         # Output({'type':'filters-rows-trash','index':MATCH},'data'),
#     ],
#     [
#         Input({'type':'logic-close','index':MATCH},'n_clicks'),#filters trash icon click
#     ],
#     [
#         State({'type':'logic-close','index':MATCH},'id'),
#         State({'type':'condition-rows','index':MATCH},'children'),
#         State({'type':'filters-logic','index':MATCH},'children'),
#         State('filters-data','data'),
#     ]
# )
# def close_condition(n_clciks,id,childs,fil_childs,data):
#     ctx = callback_context
#     triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

#     # if triggred_compo.rfind('logic-close') > -1 and n_clciks is not None and data['filters']!={}:
#     #     in_k=list(data["filters"].keys())[0]
#     #     if data['filters']!={} and id['index'] in data['filters'][in_k]['index']:
#     #         return None, None #, id['index']
#     #     else:
#     #         return None, None #, None
#     if triggred_compo.rfind('logic-close') > -1 and n_clciks is not None:
#         return None, None
#     else:
#         raise PreventUpdate

# Update condition dropdown based on column selected Eg: >, <, ==..etc
app.clientside_callback(
    '''
    function update_filters_condition_dropdown(value,id,data,ret_data) {
        if (value != null && Object.entries(data).length > 0
            && (data[value] == 'float64' || data[value] == 'int64')) {
            
            let temp_vals = []
            let options = ['has value(s)','<','<=','==','!=','>','>=','is missing','is not missing']
            for (let i in options) {
                temp_vals.push({'label':options[i],'value':options[i]})
            }
            return temp_vals
        
        } else if (value != null && Object.entries(data).length > 0
            && (data[value] == 'object' || data[value] == 'category')) {
            
            let temp_vals = []
            let options = ['has value(s)', 'starts with','contains','ends with','is missing','is not missing']
            for (let i in options) {
                temp_vals.push({'label':options[i],'value':options[i]})
            }
            return temp_vals
        
        } else if (value != null && Object.entries(data).length > 0
            && (data[value] == 'datetime64[ns]' || data[value] == 'datetime64')) {
            
            let temp_vals = []
            let options = ['days','before','after','not','equals','range','is missing','is not missing']
            for (let i in options) {
                temp_vals.push({'label':options[i],'value':options[i]})
            }
            return temp_vals

        } else if (value != null && Object.entries(data).length == 0 && ret_data != null
            && ret_data != undefined
            && (ret_data['transformations_table_column_data'][value] == 'float64'
            || ret_data['transformations_table_column_data'][value] == 'int64')) {
            
            let temp_vals = []
            let options = ['has value(s)','<','<=','==','!=','>','>=','is missing','is not missing']
            for (let i in options) {
                temp_vals.push({'label':options[i],'value':options[i]})
            }
            return temp_vals
        } else if (value != null && Object.entries(data).length == 0 && ret_data != null
            && ret_data != undefined
            && (ret_data['transformations_table_column_data'][value] == 'object'
            || ret_data['transformations_table_column_data'][value] == 'category')) {
            
            let temp_vals = []
            let options = ['has value(s)', 'starts with','contains','ends with','is missing','is not missing']
            for (let i in options) {
                temp_vals.push({'label':options[i],'value':options[i]})
            }
            return temp_vals
        } else if (value != null && Object.entries(data).length == 0 && ret_data != null
            && ret_data != undefined
            && (ret_data['transformations_table_column_data'][value] == 'datetime64[ns]'
            || ret_data['transformations_table_column_data'][value] == 'datetime64')) {
            
            let temp_vals = []
            let options = ['days','before','after','not','equals','range','is missing','is not missing']
            for (let i in options) {
                temp_vals.push({'label':options[i],'value':options[i]})
            }
            return temp_vals
        } else {
            return []
        }
    }    
    ''',
    Output({'type':'filters-conditions','index':MATCH}, 'options'),
    Input({'type':'filters-column-names','index':MATCH}, 'value'),
    State({'type':'filters-column-names','index':MATCH},'id'),
    State('transformations-table-column-data','data'),
    State('retrived-data','data')
)

# @app.callback(
#     Output({'type':'filters-conditions','index':MATCH}, 'options'),
#     [
#         Input({'type':'filters-column-names','index':MATCH}, 'value'),
#     ],
#     [
#         State({'type':'filters-column-names','index':MATCH},'id'),
#         State('transformations-table-column-data','data'),
#         State('retrived-data','data')
#     ]
# )
# def update_filters_condition_dropdown(value,id,data,ret_data):
#     if value is not None and data != {} and (data[value] == 'float64' or data[value] == 'int64'):
#         return [{'label':i,'value':i} for i in ['has value(s)','<','<=','==','!=','>','>=', \
#             'is missing','is not missing']]
#     elif value is not None and data != {} and (data[value] == 'object' or data[value] == 'category'):
#         return [{'label':i,'value':i} for i in ['has value(s)', 'starts with', \
#             'contains','ends with','is missing','is not missing']]
#     elif value is not None and data != {} and (data[value] == 'datetime64[ns]' or data[value] == 'datetime64'):
#         return [{'label':i,'value':i} for i in ['days','before','after',\
#             'not','equals','range','is missing','is not missing']]

#     elif value is not None and data == {} and ret_data is not None and\
#         (ret_data['transformations_table_column_data'][value] == 'float64' or\
#             ret_data['transformations_table_column_data'][value] == 'int64'):
#         return [{'label':i,'value':i} for i in ['has value(s)','<','<=','==','!=','>','>=', \
#             'is missing','is not missing']]
#     elif value is not None and data == {} and ret_data is not None and\
#         (ret_data['transformations_table_column_data'][value] == 'object' or\
#             ret_data['transformations_table_column_data'][value] == 'category'):
#         return [{'label':i,'value':i} for i in ['has value(s)', 'starts with', \
#             'contains','ends with','is missing','is not missing']]
#     elif value is not None and data == {} and ret_data is not None and\
#         (ret_data['transformations_table_column_data'][value] == 'datetime64[ns]'or\
#             ret_data['transformations_table_column_data'][value] == 'datetime64'):
#         return [{'label':i,'value':i} for i in ['days','before','after',\
#             'not','equals','range','is missing','is not missing']]
#     else:       
#         return []

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
    ],
    prevent_initial_call=True
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
                html.Label(html.Strong("value")),
                dcc.Input(id={"type":'trans-text','index':indx},\
                    value=None,required=True,debounce=True,inputMode='numeric',
                    type='number')
            ])

        elif value in ['starts with','contains','ends with']:
            return FormGroup([
                html.Label(html.Strong("value")),
                dcc.Input(id={"type":'trans-text','index':indx},\
                value=None,required=True,debounce=True)
            ])

        elif value in ['has value(s)'] and relation_data['table']!=[]:
            
            df1=get_column_values(relation_data['table'],add_new_col,column_name)
            # print(f"columns .. {df1.columns}")

            if type(df1) is Series:
                col=df1.unique()
            else:
                col=df1[column_name].unique
            return FormGroup([
                    html.Label(html.Strong("value")),
                    dcc.Dropdown(id={"type":'trans-multi-text','index':indx},
                                options=[{'label':i,'value':i} for i in col],
                                multi=True),
                ])
        
        elif value in ['days'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)

            max_dt = df1.max()
            min_dt = df1.min()

            return FormGroup([
                html.Label(html.Strong("value")),
                dcc.Input(id={'type':'trans-input','index':indx},value=None,debounce=True,type='number',\
                            required=True,
                            inputMode='numeric'),
                dcc.DatePickerSingle(
                    id={'type':'trans-days-single','index':indx},
                    placeholder='mm/dd/YYYY',
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today(),
                    clearable=True,
                    # with_portal=True,
                ),
                dcc.Checklist(
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
                html.Label(html.Strong("value")),
                dcc.DatePickerSingle(
                    id={'type':'trans-date-single','index':indx},
                    placeholder='mm/dd/YYYY',
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today(),
                    clearable=True,
                    # with_portal=True,
                )
            ])
        
        elif value in ['range'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)
            max_dt = df1.max()
            min_dt = df1.min()

            return FormGroup([
                html.Label(html.Strong("value")),
                dcc.DatePickerRange(
                    id={'type':'trans-date-range','index':indx},
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today(),
                    clearable=True,
                    # with_portal=True,
                )
            ])
        else:
            return None
    elif value is not None and relation_data['table'] != []:
        
        if value in ['<','<=','==','>=','>','!=']:
            return FormGroup([
                html.Label(html.Strong("value")),
                dcc.Input(id={"type":'trans-text','index':indx},\
                    value=None,required=True,debounce=True,inputMode='numeric',
                    type='number')
            ])

        elif value in ['starts with','contains','ends with']:
            return FormGroup([
                html.Label(html.Strong("value")),
                dcc.Input(id={"type":'trans-text','index':indx},\
                value=None,required=True,debounce=True)
            ])

        elif value in ['has value(s)'] and relation_data['table']!=[]:
            
            df1=get_column_values(relation_data['table'],add_new_col,column_name)
            # print(f"columns .. {df1.columns}")

            if type(df1) is Series:
                col=df1.unique()
            else:
                col=df1[column_name].unique
            
            return FormGroup([
                    html.Label(html.Strong("value")),
                    dcc.Dropdown(id={"type":'trans-multi-text','index':indx},
                                options=[{'label':i,'value':i} for i in col],
                                multi=True),
                ])
        
        elif value in ['days'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)

            max_dt = df1.max()
            min_dt = df1.min()

            return FormGroup([
                html.Label(html.Strong("value")),
                dcc.Input(id={'type':'trans-input','index':indx},value=None,debounce=True,type='number',\
                            required=True,
                            inputMode='numeric'),
                dcc.DatePickerSingle(
                    id={'type':'trans-days-single','index':indx},
                    placeholder='mm/dd/YYYY',
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today(),
                    clearable=True,
                    # with_portal=True,
                ),
                dcc.Checklist(
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
                html.Label(html.Strong("value")),
                dcc.DatePickerSingle(
                    id={'type':'trans-date-single','index':indx},
                    placeholder='mm/dd/YYYY',
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today(),
                    clearable=True,
                    # with_portal=True,
                )
            ])
        
        elif value in ['range'] and relation_data['table']!=[]:
            df1=get_column_values(relation_data['table'],add_new_col,column_name)
            max_dt = df1.max()
            min_dt = df1.min()
            return FormGroup([
                html.Label(html.Strong("value")),
                dcc.DatePickerRange(
                    id={'type':'trans-date-range','index':indx},
                    min_date_allowed=min_dt,
                    max_date_allowed=max_dt,
                    initial_visible_month=date.today(),
                    clearable=True,
                    # with_portal=True,
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

# enable or disable the apply button in filters row client-side callback
app.clientside_callback(
    """
    function enab_disa_filters_apply(fil_sel_drop,fil_col_names,fil_condi,trans_txt,\
        trans_multi_txt,trans_input,trans_dt_start,trans_dt_end,trans_dt_single,\
        trans_days_single,trans_current_date,logic_dropdown) {

        
        if (fil_sel_drop != null && fil_sel_drop != undefined && fil_col_names.includes('undefined') != true 
            && fil_col_names.includes(null) != true && fil_condi.includes(undefined) != true && fil_condi.includes(null) != true
            && logic_dropdown.includes(undefined) != true && logic_dropdown.includes(null) != true) {
            
            let text_area=false
            let multi_drp=false
            let single_dt=false
            let txt_box=false
            let range_dt=false
            let sys_dt_chk=false
            let single_days=false

            for (let i in fil_condi){
                if (['starts with','contains','ends with','<','<=','==','>=','>','!='].indexOf(fil_condi[i]) > -1) {
                    text_area = true
                    break
                }
            }

            for (let i in fil_condi){
                if (['has value(s)'].indexOf(fil_condi[i]) > -1) {
                    multi_drp = true
                    break
                }
            }

            for (let i in fil_condi){
                if (['days'].indexOf(fil_condi[i]) > -1) {
                    single_days=true
                    txt_box=true
                    sys_dt_chk=true
                    break
                }
            }

            for (let i in fil_condi){
                if (['before','after','equals','not'].indexOf(fil_condi[i]) > -1) {
                    single_dt = true
                    break
                }
            }

            for (let i in fil_condi){
                if (['range'].indexOf(fil_condi[i]) > -1) {
                    range_dt = true
                    break
                }
            }

            let chk = []
            let chk2 = []

            if (single_days == true && txt_box == true && sys_dt_chk == true){
                chk2.push(trans_days_single)
                chk2.push(trans_input)
                chk2.push(trans_current_date)
            }

            if (text_area == true){
                chk.push(trans_txt)
            }

            if (multi_drp == true){
                chk.push(trans_multi_txt)
            }
            if (single_dt == true){
                chk.push(trans_dt_single)
            }
            if (range_dt == true){
                chk.push(trans_dt_start)
                chk.push(trans_dt_end)
            }

            let rt=false
            let rtt=false

            let rt2=false
            let rtt2=false

            if (chk.length != 0) {
                for (let i in chk) {
                    let chk_val = []
                    for (let k in chk[i]) {
                        
                        if (chk[i][k] != null && chk[i][k] != undefined && chk[i][k].length != 0 && chk[i][k] != '') {
                            chk_val.push(true)
                        } else {
                            chk_val.push(false)
                        }
                    }

                    if (chk_val.every(Boolean)==true && chk_val.length != 0) {
                        rt=true
                    } else {
                        rtt=true
                    }
                }
            }

            if (chk2.length != 0) {
                
                let z1 = []
                for (let i in chk2[0]) {
                    if (chk2[0][i] != null && chk2[0][i] != undefined && chk2[0][i] != '' && chk2[0][i].length != 0) {
                        z1.push(true)
                    }
                }
                for (let j in chk2[2]) {
                    if (chk2[2][j] != null && chk2[2][j] != undefined && chk2[2][j] != '' && chk2[2][j].length != 0) {
                        z1.push(true)
                    }
                }

                let chk2_val = []
                for (let i in chk2[1]) {
                    if (chk2[1][i] != null && chk2[1][i] != undefined && chk2[1][i] != '' && chk2[1][i].length != 0) {
                        chk2_val.push(true)
                    } else {
                        chk2_val.push(false)
                    }
                }

                if (chk2_val.every(Boolean) == true && chk2_val.length != 0 && 
                    chk2[0].length == z1.filter(Boolean).length) {
                        rt2=true
                } else {
                    rtt=true
                }
            }

            

            if (rt == true && rtt == false && rt2 == false && rtt2 == false) {
                return false
            } else if (rt == false && rtt == false && rt2 == true && rtt2 == false) {
                return false
            } else if (rt == true && rtt == false && rt2 == true && rtt2 == false) {
                return false
            } else {
                return true
            }

        } else {
            return true
        }
    }
    """,
    Output('filters-apply','disabled'),
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
    Input({'type':'logic-dropdown','index':ALL},'value')
)




# # enable or disable the apply button in filters row
# @app.callback(
#     Output('filters-apply','disabled'),
#     [
#         Input('filters-select-drop','value'),#select or drop rows
#         Input({'type':'filters-column-names','index':ALL},'value'),
#         Input({'type':'filters-conditions','index':ALL},'value'),
#         Input({"type":'trans-text','index':ALL},'value'),
#         Input({"type":'trans-multi-text','index':ALL},'value'),#dropdown
#         Input({'type':'trans-input','index':ALL},'value'), #date days
#         Input({'type':'trans-date-range','index':ALL},'start_date'),
#         Input({'type':'trans-date-range','index':ALL},'end_date'),
#         Input({'type':'trans-date-single','index':ALL},'date'),
#         Input({'type':'trans-days-single','index':ALL},'date'),
#         Input({'type':'trans-use-current-date','index':ALL},'value'),
#         Input({'type':'logic-dropdown','index':ALL},'value'),
#     ]
# )
# def enab_disa_filters_apply(fil_sel_drop,fil_col_names,fil_condi,trans_txt,\
#     trans_multi_txt,trans_input,trans_dt_start,trans_dt_end,trans_dt_single,\
#         trans_days_single,trans_current_date,logic_dropdown):
#         if fil_sel_drop is not None and None not in fil_col_names and None not in fil_condi:
#             text_area=False
#             multi_drp=False
#             single_dt=False
#             txt_box=False
#             range_dt=False
#             sys_dt_chk=False
#             single_days=False

            
#             if any([True for i in fil_condi if i in ['starts with','contains','ends with','<','<=','==','>=','>','!=']]):
#                 text_area=True
#             if any([True for i in fil_condi if i in ['has value(s)']]):
#                 multi_drp=True
#             if any([True for i in fil_condi if i in ['days']]):
#                 single_days=True
#                 txt_box=True
#                 sys_dt_chk=True
#             if any([True for i in fil_condi if i in ['before','after','equals','not']]):
#                 single_dt=True
#             if any([True for i in fil_condi if i in ['range']]):
#                 range_dt=True

#             chk=[]
#             chk2=[]
            
#             if single_days is True and txt_box is True and sys_dt_chk is True:
#                 chk2.append(trans_days_single)
#                 chk2.append(trans_input)
#                 chk2.append(trans_current_date)
            
            
#             if text_area is True:
#                 chk.append(trans_txt)
#             if multi_drp is True:
#                 chk.append(trans_multi_txt)
#             if single_dt is True:
#                 chk.append(trans_dt_single)
#             if range_dt is True:
#                 chk.append(trans_dt_start)
#                 chk.append(trans_dt_end)
            

#             rt=False
#             rtt=False

#             rt2=False
#             rtt2=False


#             if chk != []:
#                 for i in chk:
#                     chk_val=[True if k is not None and k !=[] and k != '' else False \
#                         for k in i]
#                     if all(chk_val) is True and chk_val != []:
#                         rt=True
#                     else:
#                         rtt=True

            
#             if chk2 != []:
#                 z1=[True for i,j in zip(chk2[0],chk2[2]) if i != [] and i is not None and i != '' or j != []]

#                 chk2_val = [True if i is not None and i != [] and i != '' else False for i in chk2[1]]
#                 if all(chk2_val) is True and chk2_val != [] and\
#                     len(chk2[0]) == z1.count(True):
#                     rt2=True
#                 else:
#                     rtt2=True

#             # print(chk)
#             # print(chk2)

#             if rt is True and rtt is False and rt2 is False and rtt2 is False:
#                 return False
#             elif rt is False and rtt is False and rt2 is True and rtt2 is False:
#                 return False
#             elif rt is True and rtt is False and rt2 is True and rtt2 is False:
#                 return False
#             else:
#                 return True
#         else:
#             return True

# get realtime data
#try to delete the trash when apply is disabled.
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
        State({'type':'logic-close','index':ALL},'id'),
    ]
)
def get_real_time_count(disabled,ret_data,filters_data,fil_col_id,fil_condi_id,trans_text_id,\
    trans_multi_id,trans_input_id,trans_dt_id,trans_dt_single_id,trans_days_id,\
    trans_use_curr_id,logic_val_id,relationship_data,fil_sel_drop,fil_col_names,fil_condi,trans_txt,\
    trans_multi_txt,trans_input,trans_dt_start,trans_dt_end,trans_dt_single,\
        trans_days_single,trans_current_date,logic_dropdown,id):


    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]
    # print(f"current date {triggred_compo}")

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
        # if filters_data['filters'] != {}:
        #     in_k=list(filters_data["filters"].keys())[0]
        #     print(in_k)
        #     print(filters_data['filters'][in_k]['index'])
        #     print([x['index'] for x in id])


        #     missng_list = list(sorted(set(filters_data['filters'][in_k]['index']) - set([x['index'] for x in id])))
        #     # print(f" MISS LIST {missng_list}")
        #     if missng_list != []:
        #         return no_of_rows, missng_list
        #     else:
        #         return no_of_rows, None
        return no_of_rows
    elif triggred_compo == "retrived-data":
        return ret_data['realtime_rows']
    else:
        return None


# enable or disable the date picker when current date is used.
app.clientside_callback(
    '''
    function update_state_date_picker(use_curr_date,date_pick) {
        if (use_curr_date != undefined && use_curr_date != null && use_curr_date.length < 1) {
            return false, date_pick
        } else {
            return true, null
        }
    }
    ''',
    Output({'type':'trans-days-single','index':MATCH},'disabled'),
    Output({'type':'trans-days-single','index':MATCH},'date'),
    Input({'type':'trans-use-current-date','index':MATCH},'value'),
    State({'type':'trans-days-single','index':MATCH},'date')
)

# @app.callback(
#     [
#         Output({'type':'trans-days-single','index':MATCH},'disabled'),
#         Output({'type':'trans-days-single','index':MATCH},'date'),
#     ],
#     [
#         Input({'type':'trans-use-current-date','index':MATCH},'value'),
#     ],
#     [
#         State({'type':'trans-days-single','index':MATCH},'date'),
#     ]
# )
# def update_state_date_picker(use_curr_date,date_pick):
    
#     if use_curr_date == []:
#         return False, date_pick
#     else:
#         return True, None


# transformations filters modal data feeding.
app.clientside_callback(
    '''
    function update_transformation_modal(value,data,trans_column_data) {
        if ((value != null || value != undefined) && Object.entries(data).length > 0) {
            if (value == 'Filter rows') {
                let temp_vals = []
                let key_vals = Object.keys(trans_column_data)
                for (i in key_vals) {
                    temp_vals.push({'label':key_vals[i],'value':key_vals[i]})
                }
                return temp_vals
            } else {
                return []
            }
        } else {
            return []
        }
    }
    ''',
    Output({'type':'filters-column-names','index':0},'options'),
    Input('transformations-dropdown','value'),
    State('relationship-data','data'),
    State('transformations-table-column-data','data'),
)
# @app.callback(
#     Output({'type':'filters-column-names','index':0},'options'),

#     [
#         Input('transformations-dropdown','value'),
#     ],
#     [
#         State('relationship-data','data'),
#         State('transformations-table-column-data','data'),
#     ]
# )
# def update_transformation_modal(value,data,trans_column_data):
#     if value is not None and data != {}:
#         if value == 'Filter rows':
#             # modal_head = H5(value)
#             return [{'label':i,'value':i} for i in trans_column_data.keys()]
#         else:
#             return []
#     else:
#         return []


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
# app.clientside_callback(
#     '''
#     function transformation_modal_expand(trans_drop_value, add_col_close,fil_close,
#         fil_status_data,add_col_status_data,add_col_is_open,fil_is_open) {
        
#         if (trans_drop_value != null && trans_drop_value != undefined
#             && trans_drop_value == 'Add new column') {
#             let ad_col_op = false
#             if (add_col_is_open == undefined|| add_col_is_open != true) {
#                 ad_col_op = true
#             }
#             if (add_col_close != null && add_col_close != undefined) {
#                 return ad_col_op, false
#             } else if (add_col_status_data == true) {
#                 return ad_col_op, false
#             }

#             return ad_col_op,false

#         } else if (trans_drop_value != null && trans_drop_value != undefined
#             && trans_drop_value == 'Filter rows') {
#             # console.log('fil_is',fil_is_open)
#             let fi_is_op = false
#             if (fil_is_open==undefined || fil_is_open != true) {
#                 fi_is_op = true
#             }
#             if (fil_close != null && fil_close != undefined) {
#                 return false, fi_is_op
#             } else if (fil_status_data == true) {
#                 return false, fi_is_op
#             }
#             # console.log('fil_op',Boolean(fi_is_op))
#             return false, fi_is_op
#         } else {
#             return false, false
#         }
#     }
#     ''',
#     Output("add-new-col-modal", "is_open"),
#     Output('filters-modal','is_open'),
#     Input('transformations-dropdown','value'),
#     Input("add-col-close", "n_clicks"),
#     Input('filters-close','n_clicks'),
#     Input('filters-modal-status','data'),
#     Input('add-col-modal-status','data'),
#     State("add-new-col-modal", "is_open"),
#     State('filters-modal','is_open'),
# )
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
        # Input({'type':'filters-rows-trash','index':ALL},'data'),
        # Input('filter-trash-trigger','data'),
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
        State({'type':'filters-conditions','index':ALL},'value'),
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

        State({'type':'filters-column-names','index':ALL},'options'),
        State({'type':'filters-conditions','index':ALL},'options'),
        State({'type':'trans-date-range','index':ALL},'min_date_allowed'),
        State({'type':'trans-date-single','index':ALL},'min_date_allowed'),
        State({'type':'trans-days-single','index':ALL},'min_date_allowed'),
        State({'type':'trans-date-range','index':ALL},'max_date_allowed'),
        State({'type':'trans-date-single','index':ALL},'max_date_allowed'),
        State({'type':'trans-days-single','index':ALL},'max_date_allowed'),
        State({"type":'trans-multi-text','index':ALL},'options'),
    ],
    prevent_initial_call=True
)

def update_table_all(rel_n_clicks,ret_data,menu_n_clicks,fil_clear_all_n_clicks,\
    sel_aply_n_clicks,fil_aply_n_clicks,format_data,add_col_data,\
    table_row,rel_tbl_data,rel_tbl_col,rel_tbl_drpdwn,rel_join,join_qry,\
    relationship_data,apply_menu_child,relation_rows,data,columns,trans_column_data,\
    trans_fil_condi,sel_drp_val,sel_drp_col_val,trans_value,fil_sel_val,fil_col,\
    fil_condi,trans_text,trans_multi,trans_input,trans_dt_start,trans_dt_end,\
    trans_dt_single,trans_days_single,trans_use_current_dt,logic_val,fil_col_id,\
    fil_condi_id,trans_text_id,trans_multi_id,trans_input_id,trans_dt_id,\
    trans_dt_single_id,trans_days_id,trans_use_curr_id,logic_val_id,filters_data,\
    formt_tbl_data,formt_tbl_col,download_data, fil_col_names_options,\
    fil_condi_options,trans_date_range_min,trans_date_single_min,\
    trans_days_single_min,trans_date_range_max,trans_date_single_max,\
    trans_days_single_max,trans_multi_options):

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
                    filters_data['filters'][idx]['columns_drpdwn_vals'].pop(ix)
                    filters_data['filters'][idx]['condition_drpdwn_vals'].pop(ix)
                    filters_data['filters'][idx]['values_vals'].pop(ix)
            
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
                    'col_names':add_col_data['add_col_names'],
                    'col_input':add_col_data['add_col_input'],
                    'index':add_col_data['add_col_id']
                }
            })
        filters_data['index_k']=k if i_k is None else i_k

        relationship_data['saved_data']=False
        # print(f"UPDATE_TABLE_ADD_COL {filters_data}")
        if filters_data['index_k'] is not None:
            filters_data['status']=True
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
            filters_data['status']=None
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
    
    elif triggred_compo == 'filters-apply': #or (triggred_compo == 'filter-trash-trigger' \
        #and fil_row_trash is not None):
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
                'logic':[],
                'columns_drpdwn_vals':[],
                'condition_drpdwn_vals':[],
                'values_vals':[],
            }
        })
        

        trans_text_type=[i['type'] for i in trans_text_id]
        trans_multi_type=[{i['type']:j} for i,j in zip(trans_multi_id,trans_multi_options)]
        fil_col_type=[i['type'] for i in fil_col_id]
        trans_input_type=[i['type'] for i in trans_input_id]
        trans_dt_type=[i['type'] for i in trans_dt_id]
        trans_dt_single_type = [i['type'] for i in trans_dt_single_id]
        trans_days_type = [i['type'] for i in trans_days_id]
        trans_use_curr_type = [i['type'] for i in trans_use_curr_id]     
        
        trans_text_id=[i['index'] for i in trans_text_id]
        trans_multi_id=[i['index'] for i in trans_multi_id]
        fil_col_id=[i['index'] for i in fil_col_id]
        trans_input_id=[i['index'] for i in trans_input_id]
        trans_dt_id=[i['index'] for i in trans_dt_id]
        trans_dt_single_id = [i['index'] for i in trans_dt_single_id]
        trans_days_id = [i['index'] for i in trans_days_id]
        trans_use_curr_id = [i['index'] for i in trans_use_curr_id]

        

        '''
        {'trans_single_date':{'min':0,max:0}}
        '''
        trans_dt_single_dict = [{st:{'min':mn,'max':mx}} for st,mn,mx in \
            zip(trans_dt_single_type,trans_date_single_min,trans_date_single_max)]
        trans_dt_range_dict = [{st:{'min':mn,'max':mx}} for st,mn,mx in \
            zip(trans_dt_type,trans_date_range_min,trans_date_range_max)]
        trans_days_single_dict = [{st:{'min':mn,'max':mx}} for st,mn,mx in \
            zip(trans_days_type,trans_days_single_min,trans_days_single_max)]

        # print(trans_dt_type)
        # print(trans_date_range_min)
        # print(trans_date_range_max)
        
        x={'index':[],'val':[],'type':[]}
        [(x['index'].append(i),x['val'].append(j),x['type'].append(k)) for i,j,k in \
            zip(trans_text_id,trans_text,trans_text_type)]

        [(x['index'].append(i),x['val'].append(j),x['type'].append(k)) for i,j,k in \
            zip(trans_multi_id,trans_multi,trans_multi_type)]

        [(x['index'].append(i),x['val'].append(j),x['type'].append(k)) for i,j,k in \
            zip(trans_dt_single_id,trans_dt_single,trans_dt_single_dict)]

        [(x['index'].append(i),x['val'].append(j),x['type'].append(k)) for i,j,k in \
            zip(trans_dt_id,zip(trans_dt_start,trans_dt_end),trans_dt_range_dict)]


        # print(trans_dt_start)
        # print(trans_dt_end)
        # print(trans_dt_range_dict)
        # print(trans_dt_id)

        '''
        {'trans-input':val,
        'chklist:val',
        'days':fgc}
        '''
        
        for indx, idx_1 in zip(range(len(trans_input_id)),trans_use_curr_id):
            if trans_use_current_dt[indx] != []:
                x['index'].append(idx_1)
                x['val'].append([trans_input[indx],trans_use_current_dt[indx]])
                x['type'].append([trans_input_type[indx],trans_use_curr_type[indx],trans_days_single_dict[indx]])
            elif trans_days_single[indx] is not None:
                x['index'].append(idx_1)
                x['val'].append([trans_input[indx],trans_days_single[indx]])
                x['type'].append([trans_input_type[indx],trans_use_curr_type[indx],trans_days_single_dict[indx]])

        
        indx_ismis = [i for i,v in zip(fil_col_id,fil_condi) if v == 'is missing']
        indx_isntmis = [i for i,v in zip(fil_col_id,fil_condi) if v == 'is not missing']

        if indx_ismis != []:
            [(x['index'].append(v),x['val'].append('IS-None'),x['type'].append(None)) for v in indx_ismis]
        if indx_isntmis != []:
            [(x['index'].append(v),x['val'].append('NOT-None'),x['type'].append(None)) for v in indx_isntmis]

        logic_val.insert(0,None)

        logic_val_id = [i['index'] for i in logic_val_id]
        logic_val_id.insert(0,00)

        y={
            'index':fil_col_id,
            'fil_condi':fil_condi,
            'fil_col':fil_col,
            'fil_col_vals':fil_col_names_options,
            'fil_condi_vals':fil_condi_options
        }

        z={
            'logi_id':logic_val_id,
            'logic_val':logic_val
        }

        # print(x)
        # print(y)
        # print(z)

        x1 = DataFrame(x).sort_values(by='index')['type'].to_list() 

        x = DataFrame(x).sort_values(by='index')['val'].to_list()
        y = DataFrame(y).sort_values(by='index').reset_index()
        z = DataFrame(z).sort_values(by='logi_id').reset_index()

        # print(f"FILROWS_TRASH {fil_row_trash}")
        for i,k,j,v,l,col_opt,cond_opt,x_type in \
            zip(y['fil_col'],y['fil_condi'],y['index'],x,z['logic_val'],y['fil_col_vals'],y['fil_condi_vals'],x1):
            
            filters_data['filters'][in_k]['index'].append(j)
            filters_data['filters'][in_k]['condition'].append(k)
            filters_data['filters'][in_k]['columns'].append(i)
            filters_data['filters'][in_k]['values'].append(v)
            filters_data['filters'][in_k]['logic'].append(l)
            filters_data['filters'][in_k]['columns_drpdwn_vals'].append(col_opt)
            filters_data['filters'][in_k]['condition_drpdwn_vals'].append(cond_opt)
            filters_data['filters'][in_k]['values_vals'].append(x_type)

        filters_data['filters'][in_k]['select_drop']=fil_sel_val
        
        # if filters_data['filters'][in_k]['index'] != []:

        filters_data['index_k']=in_k if i_k is None else i_k

        sel_keys = list(filters_data['add_new_col'].keys())

        # print(filters_data)

        # if filters_data['filters'][in_k]['index'] != [] and \
        #     fil_row_trash is not None and int(fil_row_trash) in filters_data['filters'][in_k]['index']:


        if int(filters_data['index_k']) == 1 and filters_data['filters'] != {} and\
            filters_data['filters'][in_k]['index'] == []:
            # delete the select_or_drop
            filters_data['filters'].popitem()
            filters_data['index_k']=None

        elif int(filters_data['index_k']) > 1 and filters_data['filters'] != {} and\
            filters_data['filters'][in_k]['index'] == []:
            # delete the select_or_drop
            filters_data['filters'].popitem()
            new_indx = int(indx) - 1
            
            if abs(new_indx - int(sel_keys[0])) == 1:
                pop_item = filters_data['add_new_col'].popitem()
                filters_data['add_new_col']={new_indx:pop_item[1]}
                
            filters_data['index_k']=new_indx

        relationship_data['saved_data']=False
        

        if filters_data['index_k'] is not None:
            filters_data['status']=True
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

            # print(f"ROWS {rows}")
            # print(f"SQL {sql_qry}")

            return rel_tbl_data,rel_tbl_col,table_data_format, table_columns_format,\
                table_data_fil, table_columns_fil,relationship_data,rows,\
                trans_col, sql_qry,csv_string,filters_data,table_row,True,None
        else:
            filters_data['status']=None
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
                    status=None
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
            filters_data['status']=True


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
            filters_data['status']=None
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
        filters_data['status']=None

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
                                    status=None
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
                            filters_data['status']=True

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
                            filters_data['status']=None
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
                        
                        
                        # print(f"NEW_COL apply_menu add_col {add_col_data}")
                        
                        k_f_id = None
                        if filters_data['filters'] != {}:
                            idx = list(filters_data['filters'].keys())[0]
                            cols_remove=[ix for ix,c in enumerate(filters_data['filters'][idx]['columns']) \
                                if c not in relationship_data['columns'] and c in add_col_data['add_col_names']]
                            
                            # removing the calulated column which are no more in use.
                            cols_remove = sorted(cols_remove, reverse=True)
                            for ix in cols_remove:
                                if ix < len(filters_data['filters'][idx]['columns']):
                                    filters_data['filters'][idx]['index'].pop(ix)
                                    filters_data['filters'][idx]['columns'].pop(ix)
                                    filters_data['filters'][idx]['condition'].pop(ix)
                                    filters_data['filters'][idx]['values'].pop(ix)
                                    filters_data['filters'][idx]['logic'].pop(ix)
                                    filters_data['filters'][idx]['columns_drpdwn_vals'].pop(ix)
                                    filters_data['filters'][idx]['condition_drpdwn_vals'].pop(ix)
                                    filters_data['filters'][idx]['values_vals'].pop(ix)

                        # print(f"NEW_COL apply_menu click {filters_data}")
                        if filters_data['index_k'] is not None:
                            filters_data['status']=True

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
                            filters_data['status']=None
                            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                            csv_string,filters_data,table_row,None,None

                    else:
                        filters_data['status']=None
                        return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
                            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
                            csv_string,filters_data,table_row,None,None
        else:
            filters_data['status']=None
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
            filters_data['status']=True

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
            filters_data['status']=None
            return rel_tbl_data,rel_tbl_col,formt_tbl_data,formt_tbl_col,table_data,\
            table_columns,relationship_data,rows,trans_column_data,trans_fil_condi,\
            csv_string,filters_data,table_row,None,None
    else:
        filters_data['status']=None
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