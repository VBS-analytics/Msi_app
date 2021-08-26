from typing import Text
from dash_core_components import Dropdown, Textarea, DatePickerRange, DatePickerSingle,\
    Checklist, RadioItems, Loading
from dash_core_components import Input as TextInput
from dash_html_components import Br, Div, I, Br, H5, H6, A
import dash_html_components as dhc
from dash_bootstrap_components import Modal, ModalHeader, ModalFooter, ModalBody, \
    Button, Row, Col, FormGroup, FormText, Form, FormFeedback, Label


from dash_table import DataTable
# import dash_table

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
                ModalHeader(H5('Select or drop columns')),
                ModalBody(
                    Row([
                        Col(Dropdown(
                            id='select-drop-select-drop',
                            options=[{'label':i,'value':i} for i in ['Select','Drop']],
                            value=None
                        ),width=3),

                        Col(Dropdown(
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
                    Div(
                        Row([
                            Col(H5('Filter rows')),
                            Col(Div("0 records",style={"font-size":"15px"},id="realtime-total-records"))
                        ],justify="end")
                    )
                ),
                ModalBody(Loading([
                    Form([
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
                                        Label("Select column name",html_for={'type':'filters-column-names','index':0}),
                                        Dropdown(
                                            id={'type':'filters-column-names','index':0},
                                            value=None
                                        )
                                    ])
                                ,width=4),

                                Col(
                                    FormGroup([
                                        Label("condition",html_for={'type':'filters-conditions','index':0}),
                                        Dropdown(
                                            id={'type':'filters-conditions','index':0}
                                        )
                                    ])
                                ,width=3),

                                Col([
                                    FormGroup([
                                        dhc.Label("value"),
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
                    ],id='filters-div'),


                    # Div([
                    #     Row(Col(Button("Clear all",id='filters-clear-all',color='link')))
                    # ]),

                    # Div([
                        # Row(Col(H6('Select or drop rows'),width=3)),
                        # Row(
                        #     Col(
                        #         Dropdown(
                        #             id='filters-select-drop',
                        #             options=[{'label':i,'value':i} for i in ['Select','Drop']],
                        #             value=None
                        #         )
                        #     ,width=3)
                        # ),

                        # Row(Col(H6('where'),width=3)),

                    #     Div([
                    #         Row([
                    #             Col(
                    #                 Dropdown(
                    #                     id={'type':'filters-column-names','index':0},
                    #                     value=None
                    #                 )
                    #             ,width=4),

                    #             Col(
                    #                 Dropdown(
                    #                     id={'type':'filters-conditions','index':0}
                    #                 )
                    #             ,width=3),

                    #             Col([
                    #                 Dropdown(id={"type":'trans-multi-text','index':0},style={'display':'none'}),
                    #                 Textarea(id={"type":'trans-text','index':0},style={'display':'none'}),
                    #                 TextInput(id={'type':'trans-input','index':0},style={'display':'none'}),
                    #                 DatePickerRange(id={'type':'trans-date-range','index':0},style={'display':'none'}),
                    #                 DatePickerSingle(id={'type':'trans-date-single','index':0},style={'display':'none'}),
                    #                 DatePickerSingle(id={'type':'trans-days-single','index':0},style={'display':'none'}),
                    #                 Checklist(id={'type':'trans-use-current-date','index':0},style={'display':'none'}),
                    #             ],id={'type':'filters-text-drpdwn','index':0},width=4),

                    #         ],id={'type':'condition-rows','index':0}),

                    #         Row([
                    #             dhc.Button(id={'type':'logic-close','index':0},hidden=True)
                    #         ],
                    #         id={'type':'filters-logic','index':0}),


                    #     ],id='filters-conditional-div'),

                    #     Row(
                    #         Col(
                    #             Button('add condition', size='sm', id='filters-add-condition')
                    #         )
                    #     ),
                        
                    # ],id='filters-div')
                ],type="dot")),

                ModalFooter([
                    Button("Apply", id="filters-apply", className="ml-auto"),
                    Button("Close", id="filters-close", className="ml-auto"),
                ]),

            ],id='filters-modal',centered=True,size='xl'),

            Modal([
                
                    ModalHeader(H5('Add new column')),
                    
                    ModalBody([
                        Form([                           
                            FormGroup([
                                Col(A(I(className="fa fa-trash"),id={'type':'add-col-remove','index':0}),className="text-right"),
                                dhc.Label("Enter column name"),
                                TextInput(id={"type":"add-new-col-name","index":0},type="text",minLength=5,required=True),
                                FormText("Type column name without any spaces, special characters. Except 'underscore '_''",color="secondary"),
                            ],id={"type":'add-col-grp-1','index':0}),

                            FormGroup([
                                dhc.Label("Assign value to new column"),
                                # RadioItems(
                                #         options=[{'label':i,'value':i} for i in zip(["single value","conditional value"])],
                                #         id={"type":"add-col-value-radio","index":0},
                                # ),
                                TextInput(id={"type":'add-col-value-input',"index":0},type='text',required=True),
                            ],id={"type":'add-col-grp-2','index':0}),

                            dhc.Hr(id={"type":'add-col-hr-3','index':0}),
                        ],id="add-col-form"),
                        dhc.Hr(),
                        Row([
                            Col(dhc.Button('Add column',id="add-col-new-col-but")) 
                        ]),
                    ],id='add-new-col-modal-body'),
                    ModalFooter([
                        Button("Apply", disabled=True, id="add-new-col-modal-apply", className="ml-auto"),
                        Button("Close", id="add-col-close", className="ml-auto"),
                    ]),
                
            ],id='add-new-col-modal',centered=True,size='xl'),
            
            Br(),

            Div(
                Row([
                    Col([
                        Dropdown(
                            id='transformations-dropdown',
                            value=None,
                            options=[{'label':i,'value':i} for i in \
                                ['Filter rows','Add new column']],
                            clearable=True
                        ),
                    ],width=3)
                ])
            ),

            Div(
                Row(
                    Col(
                        DataTable(
                            id='table-filter',
                            columns=[{"name": i, "id": i} for i in ["column-1","column-2","column-3"]],
                            data= [],
                            style_table={'overflowX': 'scroll'},
                        )
                    )
                )
            ,className='pretty_container nine columns'),
        ]
