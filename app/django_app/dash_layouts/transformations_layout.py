from dash_core_components import Dropdown, Textarea, DatePickerRange, DatePickerSingle,\
    Checklist
from dash_core_components import Input as TextInput
from dash_html_components import Br, Div, I, Br, H5, H6, A
import dash_html_components as dhc
from dash_bootstrap_components import Modal, ModalHeader, ModalFooter, ModalBody, \
    Button, Row, Col


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
                ModalHeader(H5('Filter rows')),
                ModalBody(
                    Div([
                        Row(Col(H6('Select or drop rows'),width=3)),
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
                        
                    ],id='filters-div')
                ),

                ModalFooter([
                    Button("Apply", id="filters-apply", className="ml-auto"),
                    Button("Close", id="filters-close", className="ml-auto"),
                ]),

            ],id='filters-modal',centered=True,size='xl'),

            Modal([
                ModalHeader(H5('Change columns datatype')),
                ModalBody(id='change-col-dtype-body'),
                ModalFooter([
                    Button("Apply", id="change-col-apply", className="ml-auto"),
                ]),
            ],id='change-col-dtype-modal',centered=True,size='xl'),
            

            Br(),
            Br(),

            Div(
                Row([
                    Col([
                        Dropdown(
                            id='transformations-dropdown',
                            value=None,
                            options=[{'label':i,'value':i} for i in \
                                ['Filter rows','Select or drop columns']],
                        ),
                    ],width=3),

                    # Col([
                    #     Button("Preview", color="primary",id='preview-filter-table-button', className="mr-1",size="sm"),
                    # ],width=1),

                    Col([
                        A(I(className="fa fa-plus"),id='add-col-btn')
                    ],width=1)
                ])
            ),

            Div(
                Row(
                    Col(
                        DataTable(
                            id='table-filter',
                            columns=[{"name": i, "id": i} for i in ["column-1","column-2","column-3"]],
                            data= [],
                        )
                    )
                )
            ,className='pretty_container nine columns'),
        ]
