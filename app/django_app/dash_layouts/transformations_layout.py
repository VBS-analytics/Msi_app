# from dash_core_components import Dropdown, Textarea, DatePickerRange, DatePickerSingle,\
#     Checklist, RadioItems, Loading, Store
# from dash_core_components import Input as TextInput
# from dash_html_components import Br, Div, I, Br, H5, H6, A
# import dash_html_components as dhc
from dash_bootstrap_components import Modal, ModalHeader, ModalFooter, ModalBody, \
    Button, Row, Col, FormGroup, FormText, Form, FormFeedback, Label

# from dash_table import DataTable
# import dash_table

from dash import dcc, html, dash_table

def transform_tab():
    return [
            Modal(
            [
                ModalHeader(id='transformations-modal-head'),
                ModalBody(id='transformations-modal-body'),
                ModalFooter([
                    Button("Apply", id="transformations-modal-apply", className="ml-auto"),
                ]),
            ],
            id='transformations-modal',centered=True,size='xl'),

            Modal([
                ModalHeader(html.H5('Select or drop columns')),
                ModalBody(
                    Row([
                        Col(dcc.Dropdown(
                            id='select-drop-select-drop',
                            options=[{'label':i,'value':i} for i in ['Select','Drop']],
                            value=None
                        ),width=3),

                        Col(dcc.Dropdown(
                            id='select-drop-col-names',
                            value=[],
                            multi=True
                        ),width=5)
                    ])
                ),

                ModalFooter([
                    Button("Apply", id="select-drop-apply", className="ml-auto"),
                    Button("Close", id="select-drop-close", className="ml-auto"),
                ]),
            ],id='select-drop-modal',centered=True,size='xl'),

            Modal([
                ModalHeader(
                    html.Div(
                        Row([
                            Col(html.H5('Filter rows')),
                            Col(html.Div("0 records",style={"font-size":"15px"},id="realtime-total-records"))
                        ],justify="end")
                    )
                ),
                ModalBody(dcc.Loading([
                    Form([
                        FormGroup([
                            Col(html.A(html.I(className="fa fa-refresh"),id='filters-clear-all'),className="text-right"),
                            html.Label("Select or drop rows"),
                            dcc.Dropdown(
                                    id='filters-select-drop',
                                    options=[{'label':i,'value':i} for i in ['Select','Drop']],
                                    value=None,
                                    style={"width":"50%"}
                                ),
                            # FormText("Type column name without any spaces, special characters. Except 'underscore '_''",color="secondary"),
                        ]),

                        FormGroup([
                            html.Label("Where,")
                        ]),

                        html.Div([
                            Row([
                                Col(
                                    FormGroup([
                                        Label("Select column name",html_for={'type':'filters-column-names','index':0}),
                                        dcc.Dropdown(
                                            id={'type':'filters-column-names','index':0},
                                            value=None
                                        )
                                    ])
                                ,width=4),

                                Col(
                                    FormGroup([
                                        Label("condition",html_for={'type':'filters-conditions','index':0}),
                                        dcc.Dropdown(
                                            id={'type':'filters-conditions','index':0}
                                        )
                                    ])
                                ,width=3),

                                Col([
                                    FormGroup([
                                        html.Label("value"),
                                        dcc.Dropdown(id={"type":'trans-multi-text','index':0},style={'display':'none'}),
                                        dcc.Textarea(id={"type":'trans-text','index':0},style={'display':'none'}),
                                        dcc.Input(id={'type':'trans-input','index':0},style={'display':'none'},debounce=True),
                                        dcc.DatePickerRange(id={'type':'trans-date-range','index':0},style={'display':'none'}),
                                        dcc.DatePickerSingle(id={'type':'trans-date-single','index':0},style={'display':'none'}),
                                        dcc.DatePickerSingle(id={'type':'trans-days-single','index':0},style={'display':'none'}),
                                        dcc.Checklist(id={'type':'trans-use-current-date','index':0},style={'display':'none'}),
                                    ])
                                    
                                ],id={'type':'filters-text-drpdwn','index':0},width=4),

                                # Col(html.Button(id={'type':'logic-close','index':0},hidden=True))
                                Col(html.A(html.I(className="fa fa-trash-o"),id={'type':'logic-close','index':0}),className="text-right"),
                                # Store(id={'type':'filters-rows-trash','index':0},data=None)
                            
                            ],id={'type':'condition-rows','index':0}),
                            Row(Col("This is Temp column and row"),id={"type":"filters-logic","index":0},style={'display':'none'}),
                        ],id='filters-conditional-div'),

                        Row(
                            Col(
                                Button('add condition', size='sm', id='filters-add-condition')
                            )
                        ),
                    ],id='filters-div'),
                ],type="dot")),

                ModalFooter([
                    Button("Apply", id="filters-apply", className="ml-auto"),
                    Button("Close", id="filters-close", className="ml-auto"),
                ]),

            ],id='filters-modal',centered=True,size='xl',backdrop="static"),

            Modal([
                
                    ModalHeader(html.H5('Add new column')),
                    
                    ModalBody([
                        Form([                           
                            FormGroup([
                                Col(html.A(html.I(className="fa fa-trash"),id={'type':'add-col-remove','index':0}),className="text-right"),
                                html.Label("Enter column name"),
                                dcc.Input(id={"type":"add-new-col-name","index":0},type="text",minLength=5,required=True),
                                FormText("Type column name without any spaces, special characters. Except 'underscore '_''",color="secondary"),
                            ],id={"type":'add-col-grp-1','index':0}),

                            FormGroup([
                                html.Label("Assign value to new column"),
                                # RadioItems(
                                #         options=[{'label':i,'value':i} for i in zip(["single value","conditional value"])],
                                #         id={"type":"add-col-value-radio","index":0},
                                # ),
                                dcc.Input(id={"type":'add-col-value-input',"index":0},type='text',required=True),
                            ],id={"type":'add-col-grp-2','index':0}),

                            html.Hr(id={"type":'add-col-hr-3','index':0}),
                        ],id="add-col-form"),
                        html.Hr(),
                        Row([
                            Col(html.Button('Add column',id="add-col-new-col-but")) 
                        ]),
                    ],id='add-new-col-modal-body'),
                    ModalFooter([
                        Button("Apply", disabled=True, id="add-new-col-modal-apply", className="ml-auto"),
                        Button("Close", id="add-col-close", className="ml-auto"),
                    ]),
                
            ],id='add-new-col-modal',centered=True,size='xl',backdrop="static"),
            
            html.Br(),

            html.Div(
                Row([
                    Col([
                        dcc.Dropdown(
                            id='transformations-dropdown',
                            value=None,
                            options=[{'label':i,'value':i} for i in \
                                ['Filter rows','Add new column']],
                            clearable=True
                        ),
                    ],width=3)
                ])
            ),

            html.Div(
                Row(
                    Col(
                        dash_table.DataTable(
                            id='table-filter',
                            columns=[{"name": i, "id": i} for i in ["column-1","column-2","column-3"]],
                            data= [],
                            style_table={'overflowX': 'scroll'},
                        )
                    )
                )
            ,className='pretty_container nine columns'),
        ]
