
from dash_core_components import Dropdown, Input, RadioItems, Store,Checklist
from dash_html_components import Br, Div, Label, H5, A, Img, I
from dash_bootstrap_components import Modal, ModalHeader, ModalFooter, ModalBody, \
    Button, Row, Col, Tooltip, Toast,Alert
import dash_html_components as dhc

from dash_table import DataTable
from ..server import app
from dash_extensions import Download

def relationship_tab():
    return [
            Modal(
            [
                ModalHeader([
                    H5("Scheduled files renderd"),
                ]),
                ModalBody([
                    Div(
                        Row(
                            Col(
                                RadioItems(
                                    id='schedule-radio-btn'
                                )
                            )

                        )
                    ,className='pretty_container ten columns')
                ],id='schedule-fil-modal-body'),
                ModalFooter([
                    Col(
                        Button("Delete", id="schedule-fil-modal-delete", className="ml-auto")
                    ,width=2),

                    Col(
                        Button("Download", id="schedule-fil-modal-download", className="ml-auto")
                    ,width=2),

                    Col(
                        Button("Close", id="schedule-fil-modal-close",className="ml-auto")
                    ,width=2),

                    # Col(A(I(className='fa fa-download'),id='schedule-fil-download',download='file.xlsx',target="_blank")),

                    Col(
                        Download(id="schedule-fil-download")
                    ,width=2)
                    
                ]),
            ],
            id='schedule-fil-modal',centered=True,size='lg'),

            Modal(
            [
                ModalHeader([
                    H5("Saved Filters"),
                ]),
                ModalBody([
                    Div(
                        Row(
                            Col(
                                RadioItems(
                                    id='filter-radio-btn'
                                )
                            )
                        )
                    ,className='pretty_container ten columns')
                ],id='saved-fil-modal-body'),
                ModalFooter([
                    Col(
                        Button("Apply", id="saved-fil-modal-apply", className="ml-auto")
                    ,width=2),

                    Col(
                        Button("Delete", id="saved-fil-modal-delete", className="ml-auto")
                    ,width=2),

                    Col(
                        Button("Close", id="saved-fil-modal-close",className="ml-auto")
                    ,width=2),
                    
                ]),
            ],
            id='saved-fil-modal',centered=True,size='lg'),

            Modal(
                [
                    ModalHeader([
                        H5('Save changes'),
                    ]),
                    
                    ModalBody([
                        Div([
                            Input(id='modal-sf-filter-name',value=None),
                        ]),
                        Div([
                            Checklist(
                                options=[
                                    {'label': 'Schedule', 'value': 'schedule'},
                                ],
                                value=[],
                                id="schedule-cklist"
                            )  
                        ]),
                        Div([
                            Row([
                                Col([
                                    RadioItems(
                                        options=[
                                            {'label': 'Hourly', 'value': 'hourly'},
                                            {'label': 'Daily', 'value': 'daily'},
                                            {'label': 'Weekly', 'value': 'weekly'},
                                            {'label': 'Monthly', 'value': 'monthly'},
                                            # {'label': 'Yearly', 'value': 'yearly'},
                                        ],
                                        value=[],
                                        id="schedule-radio"
                                    )
                                ],width=2),
                                Col([
                                    #hourly
                                    Div([
                                        Label("Enter Minutes (0-59)"),
                                        Input(id="sch-hourly-min-input",placeholder="MM"),
                                    ],style={"display":"none"},id="sch-hourly-body"),

                                    #daily
                                    Div([
                                        Row([
                                            Col([
                                                Label("Enter Hours (0-23)"),
                                                Input(id="sch-daily-hour-input",placeholder="HH")
                                            ]),
                                            Col([
                                                Label("Enter Minutes (0-59)"),
                                                Input(id="sch-daily-min-input",placeholder="MM")
                                            ]),
                                        ])
                                    ],style={"display":"none"},id="sch-daily-body"),

                                    #weekly
                                    Div([
                                        Row([
                                            Col([
                                                Label("Select Day"),
                                                Dropdown(
                                                id="sch-weekly-week-input",
                                                options=[{'label':i,'value':i} for i in ["SUN","MON","TUE","WED","THU","FRI","SAT"]],
                                                value=[],
                                                multi=True
                                            )]),

                                            Col([
                                                Label("Enter Hours (0-23)"),
                                                Input(id="sch-weekly-hour-input",placeholder="HH")
                                            ]),
                                            Col([
                                                Label("Enter Minutes (0-59)"),
                                                Input(id="sch-weekly-min-input",placeholder="MM")
                                            ]),
                                        ])
                                    ],style={"display":"none"},id="sch-weekly-body"),

                                    #monthly
                                    Div([
                                        Row([
                                            Col([
                                                Label("Select Month"),
                                                Dropdown(
                                                id="sch-monthly-month-input",
                                                options=[{'label':i,'value':i} for i in ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]],
                                                value=[],
                                                multi=True
                                            )]),
                                            Col([
                                                Label("Enter date (1-31)"),
                                                Input(id="sch-monthly-date-input",placeholder="1-31")
                                            ]),

                                            Col([
                                                Label("Enter Hours (0-23)"),
                                                Input(id="sch-monthly-hour-input",placeholder="HH")
                                            ]),
                                            Col([
                                                Label("Enter Minutes (0-59)"),
                                                Input(id="sch-monthly-min-input",placeholder="MM")
                                            ]),
                                        ])
                                    ],style={"display":"none"},id="sch-monthly-body")
                                ])
                            ]),
                            Row([
                                Col([
                                    Label("Auto-Delete after n days"),
                                    Input(id="sch-auto-del-input",placeholder="days in number..",type='number')
                                ]),
                            ]),
                            Row([
                                Col([
                                    Label("Enter E-mail for alerts"),
                                    Input(id="sch-email-input",placeholder="Email..")
                                ]),
                            ])
                        ],id='schedule-body',style={"display":"none"}),

                        # Div(Label("Saved Successfully!!",id='modal-sf-status',hidden=True)),
                        Div(Alert("Saved Successfully!!",color='success',is_open=False,id='modal-sf-status'))


                    ],id='modal-sf-body'),

                    ModalFooter([
                        Button("Save",id='modal-sf-save',className='ml-auto'),
                        Button("Close",id='modal-sf-close',className='ml-auto'),
                    ]),
                ],id='sf-modal',centered=True,size='lg'),
           
            Br(),
            Div(
                Row([
                    Col([
                        Button("Add Table", id='add-table-button',color="primary",\
                            outline=True, className="mr-1",disabled=True),
                    ],width={"size": 3}),

                    Col([    
                        Button("Run", id='preview-table-button',color="primary",\
                            outline=True, className="mr-1",disabled=True),
                    ],width={"size": 3, "offset": 1}),
                ])
            ),
            
            Br(),
                        
            Div(Row(Col(Alert("Please fill in all dropdowns!",id="table-dropdown-alert",color="danger",is_open=False),width=4))),
            Div([
                Row([
                    Col(
                        Dropdown(
                            id={'type':'relationship-table-dropdown','index':0},
                            value=None,
                            # style={'border-color':'red',
                            #     'box-shadow':'inset 0 1px 1px rgba(0,0,0,0.075),\
                            #                 0 0 0 3px rgba(0,126,255,0.1);',
                            #     'background':'#fff;'
                            # },
                            # style={'z-index':'999'},
                        )
                    ,width=3),
                    Col(
                        A(
                            Img(
                                src=app.get_asset_url('sql-join-icon.png'),
                                
                                # hidden=True
                            ),
                            id={'type':'relationship-sql-joins','index':0},
                        )
                        # Dropdown(
                        #     id={'type':'relationship-sql-joins','index':0},
                        #     options=[{'label':i,'value':i} for i in ['IJ','LJ','RJ','FJ']],
                        #     value=None',
                        #     style={'display':'none'}
                        # )
                    ,width=1,style={'display':'none'}),

                    Store(id={'type':'sql-joins-query','index':0},data=None),

                    Modal(
                        [
                            ModalHeader(H5('Join on')),
                            ModalBody([
                                Div([
                                    Row(Col(Dropdown(id={'type':'sql-join-modal','index':0}))),
                                    Br(),
                                    Row([
                                        Col(H5(id={'type':'left-table-name','index':0})),
                                        Col(H5(id={'type':'right-table-name','index':0}))
                                    ]),
                                    Row([
                                        Col(Dropdown(id={'type':'left-table-join-modal','index':0})),
                                        Col(Dropdown(id={'type':'right-table-join-modal','index':0}))
                                    ]),
                                    # Row(
                                    #     Col(
                                    #         H5(id={'type':'join-status','index':0})
                                    #     )
                                    # )

                                ]),
                                Div(Alert("Error",color='danger',is_open=False,id={"type":'join-status','index':0}))
                            ]),
                            ModalFooter([
                                # Toast(id={"type":'join-status','index':0}),
                                Button("Apply",id={'type':'apply-join-modal','index':0},className='ml-auto'),
                                Button("Close",id={'type':'close-join-modal','index':0},className='ml-auto'),
                            ])
                        ],id={'type':'join-modal','index':0},centered=True,size='lg'
                    ),

                    Col(
                        A(
                            I(className='fa fa-times'),
                            id={'type':'relationship-table-close','index':0},
                        )
                    ,width=1,style={'display':'none'})
                ],id="tables-row")
            ],id='table-dropdown-div',className='pretty_container ten columns'),

            

            Div(
                Row(
                    Col(
                        DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in ["column-1","column-2","column-3"]],
                            data= [],
                            style_table={'overflowX': 'scroll','minWidth': '100%'},
                        )
                    )
                )
            ,className='pretty_container nine columns'),
    ]
