# from dash_core_components import Dropdown, Input, RadioItems, Store,Checklist
# from dash_html_components import Br, Div, Label, H5, A, Img, I
from dash_bootstrap_components import Modal, ModalHeader, ModalFooter, ModalBody, \
    Button, Row, Col, Tooltip, Toast,Alert,FormGroup, FormText, Form, FormFeedback, Label, Collapse, Badge
# import dash_html_components as dhc

# from dash_table import DataTable
from ..server import app
from dash_extensions import Download

from dash import dcc, html, dash_table

def relationship_tab():
    return [
            Modal(
            [
                ModalHeader([
                    html.H5("Scheduled files renderd"),
                ]),
                ModalBody([
                    html.Div(
                        Row(
                            Col(
                                dcc.RadioItems(
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

                    # Col(html.A(html.I(className='fa fa-download'),id='schedule-fil-download',download='file.xlsx',target="_blank")),

                    Col(
                        Download(id="schedule-fil-download")
                    ,width=2)
                    
                ]),
            ],
            id='schedule-fil-modal',centered=True,size='lg',backdrop="static"),

            Modal(
            [
                ModalHeader([
                    html.H5("Saved Filters"),
                ]),
                ModalBody([
                    html.Div(
                        Row(
                            Col(
                                dcc.RadioItems(
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
            id='saved-fil-modal',centered=True,size='lg',backdrop="static"),

            Modal(
                [
                    ModalHeader("Header"),
                    ModalBody(
                        html.Div("Filter name already exists, click Save to update the changes."),
                        # html.Div(Alert("Saved Successfully!!",color='success',is_open=False,id='fil-exists-status'))
                    ),
                    ModalFooter([
                        Button("Close", id="fil-name-exists-close", className="ml-auto"),
                        Button("Save", id="fil-name-exists-save", className="ml-auto")
                    ]),
                ],
                id="fil-name-exists-modal",
                is_open=False,
            ),

            Modal(
                [
                    ModalHeader([
                        html.H5('Save changes'),
                    ]),
                    
                    ModalBody([
                        Form([
                            FormGroup([
                                Label("Filter Name",html_for="modal-sf-filter-name"),
                                dcc.Input(id='modal-sf-filter-name',value=None,required=True),
                                FormText(
                                    "filter names should not contain any special \
                                        characters including empty spaces, except '_'.",
                                    color="secondary",
                                ),
                            ]),

                            FormGroup([
                                dcc.Checklist(
                                    options=[
                                        {'label': 'Schedule', 'value': 'schedule'},
                                    ],
                                    value=[],
                                    id="schedule-cklist"
                                )  
                            ]),

                            html.Div([
                                FormGroup([
                                    Row([
                                        Col([
                                            dcc.RadioItems(
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
                                            html.Div([
                                                Label("Enter Minutes (0-59)"),
                                                dcc.Input(id="sch-hourly-min-input",placeholder="MM"),
                                            ],style={"display":"none"},id="sch-hourly-body"),

                                            #daily
                                            html.Div([
                                                Row([
                                                    Col([
                                                        Label("Enter Hours (0-23)"),
                                                        dcc.Input(id="sch-daily-hour-input",placeholder="HH")
                                                    ]),
                                                    Col([
                                                        Label("Enter Minutes (0-59)"),
                                                        dcc.Input(id="sch-daily-min-input",placeholder="MM")
                                                    ]),
                                                ])
                                            ],style={"display":"none"},id="sch-daily-body"),

                                            #weekly
                                            html.Div([
                                                Row([
                                                    Col([
                                                        Label("Select Day"),
                                                        dcc.Dropdown(
                                                        id="sch-weekly-week-input",
                                                        options=[{'label':i,'value':i} for i in ["SUN","MON","TUE","WED","THU","FRI","SAT"]],
                                                        value=[],
                                                        multi=True
                                                    )]),

                                                    Col([
                                                        Label("Enter Hours (0-23)"),
                                                        dcc.Input(id="sch-weekly-hour-input",placeholder="HH")
                                                    ]),
                                                    Col([
                                                        Label("Enter Minutes (0-59)"),
                                                        dcc.Input(id="sch-weekly-min-input",placeholder="MM")
                                                    ]),
                                                ])
                                            ],style={"display":"none"},id="sch-weekly-body"),

                                            #monthly
                                            html.Div([
                                                Row([
                                                    Col([
                                                        Label("Select Month"),
                                                        dcc.Dropdown(
                                                        id="sch-monthly-month-input",
                                                        options=[{'label':i,'value':i} for i in ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]],
                                                        value=[],
                                                        multi=True
                                                    )]),
                                                    Col([
                                                        Label("Enter date (1-31)"),
                                                        dcc.Input(id="sch-monthly-date-input",placeholder="1-31")
                                                    ]),

                                                    Col([
                                                        Label("Enter Hours (0-23)"),
                                                        dcc.Input(id="sch-monthly-hour-input",placeholder="HH")
                                                    ]),
                                                    Col([
                                                        Label("Enter Minutes (0-59)"),
                                                        dcc.Input(id="sch-monthly-min-input",placeholder="MM")
                                                    ]),
                                                ])
                                            ],style={"display":"none"},id="sch-monthly-body")
                                        ])
                                    ]),
                                    html.Br(),
                                    Row([
                                        Col([
                                            Label("Auto-Delete excel files after n days"),
                                            dcc.Input(id="sch-auto-del-input",placeholder="days in number..",
                                            type='number',inputMode="numeric",required=True)
                                        ]),
                                    ]),
                                    html.Br(),
                                    Row(
                                        Col(
                                            Button(
                                                "Compose mail",
                                                id="compose-mail-button",
                                                className="mb-3",
                                                color="primary",
                                                n_clicks=0,
                                            )
                                        )
                                    ),
                                    Row(
                                        Col(
                                            Collapse([
                                                    Form([
                                                        FormGroup([
                                                            html.Label("Email"),
                                                            dcc.Input(inputMode="email",type='email', id="sch-email-input", placeholder="Enter email")
                                                        ]),
                                                        FormGroup([
                                                            html.Label("Password"),
                                                            dcc.Input(type='password', id="sch-pass-input", placeholder="Enter password")
                                                        ])
                                                    ]),

                                                    Form([
                                                        FormGroup([
                                                            html.Label("TO"),
                                                            html.Div([
                                                                html.A(Badge("Primary", color="primary", className="mr-1"),
                                                                    id={'type':'to-emails-badge','index':0},style={'display':'none'},n_clicks=0),
                                                                # html.A(Badge("Primary", color="primary", className="mr-1")),
                                                                # html.A(Badge("Primary", color="primary", className="mr-1")),
                                                                # html.A(Badge("Primary", color="primary", className="mr-1")),
                                                                # html.A(Badge("Primary", color="primary", className="mr-1")),
                                                                # html.A(Badge("Primary", color="primary", className="mr-1")),
                                                                # html.A(Badge("Primary", color="primary", className="mr-1")),
                                                                # html.A(Badge("Primary", color="primary", className="mr-1")),
                                                            ],id='sch-to-email-div'),
                                                            html.Br(),
                                                            dcc.Input(inputMode="email",type='email',debounce=True, id="sch-to-email-input", placeholder="Enter email")
                                                        ]),

                                                        FormGroup([
                                                            html.Label("CC"),
                                                            html.Div([
                                                                html.A(Badge("Primary", color="primary", className="mr-1"),
                                                                    id={'type':'cc-emails-badge','index':0},style={'display':'none'},n_clicks=0),
                                                            ],id='sch-cc-email-div'),
                                                            html.Br(),
                                                            dcc.Input(inputMode="email",type='email', debounce=True,id="sch-cc-email-input", placeholder="Enter email")
                                                        ]),

                                                        FormGroup([
                                                            html.Label("Subject"),
                                                            dcc.Input(id="sch-subject-input", placeholder="Enter subject",required=True)
                                                        ]),

                                                        FormGroup([
                                                            html.Label("Message"),
                                                            dcc.Textarea(id="sch-message-input", placeholder="Enter Message",required=True)
                                                        ])
                                                    ])
                                                ],
                                                id='email-collapse',
                                                is_open=False
                                            )
                                        ,width=6)                                        
                                    )                                    
                                ]),
                            ],id='schedule-body',style={"display":"none"}),

                            html.Div(Alert("Saved Successfully!!",color='success',is_open=False,id='modal-sf-status'))
                        ])
                        # html.Div(Label("Saved Successfully!!",id='modal-sf-status',hidden=True)),
                    ],id='modal-sf-body'),

                    ModalFooter([
                        Button("Save",id='modal-sf-save',className='ml-auto'),
                        Button("Close",id='modal-sf-close',className='ml-auto'),
                    ]),
                ],id='sf-modal',centered=True,size='lg',backdrop="static"),
           
            html.Br(),
            html.Div(
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
            
            html.Br(),
                        
            html.Div(Row(Col(Alert("Please fill in all dropdowns!",id="table-dropdown-alert",color="danger",is_open=False),width=4))),
            html.Div([
                Row([
                    Col(
                        dcc.Dropdown(
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
                        html.A(
                            html.Img(
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

                    dcc.Store(id={'type':'sql-joins-query','index':0},data=None),

                    Modal(
                        [
                            ModalHeader(html.H5('Join on')),
                            ModalBody([
                                html.Div([
                                    Row(Col(dcc.Dropdown(id={'type':'sql-join-modal','index':0}))),
                                    html.Br(),
                                    Row([
                                        Col(html.H5(id={'type':'left-table-name','index':0})),
                                        Col(html.H5(id={'type':'right-table-name','index':0}))
                                    ]),
                                    Row([
                                        Col(dcc.Dropdown(id={'type':'left-table-join-modal','index':0})),
                                        Col(dcc.Dropdown(id={'type':'right-table-join-modal','index':0}))
                                    ]),
                                    # Row(
                                    #     Col(
                                    #         html.H5(id={'type':'join-status','index':0})
                                    #     )
                                    # )

                                ]),
                                html.Div(Alert("Error",color='danger',is_open=False,id={"type":'join-status','index':0}))
                            ]),
                            ModalFooter([
                                # Toast(id={"type":'join-status','index':0}),
                                Button("Apply",id={'type':'apply-join-modal','index':0},className='ml-auto'),
                                Button("Close",id={'type':'close-join-modal','index':0},className='ml-auto'),
                            ])
                        ],id={'type':'join-modal','index':0},centered=True,size='lg',backdrop="static"
                    ),

                    Col(
                        html.A(
                            html.I(className='fa fa-times'),
                            id={'type':'relationship-table-close','index':0},
                        )
                    ,width=1,style={'display':'none'})
                ],id="tables-row")
            ],id='table-dropdown-div',className='pretty_container ten columns'),

            

            html.Div(
                Row(
                    Col(
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in ["column-1","column-2","column-3"]],
                            data= [],
                            style_table={'overflowX': 'scroll','minWidth': '100%'},
                        )
                    )
                )
            ,className='pretty_container nine columns'),
    ]
