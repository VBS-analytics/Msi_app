
from dash_core_components import Dropdown, Input, RadioItems, Store
from dash_html_components import Br, Div, Label, H5, A, Img
from dash_bootstrap_components import Modal, ModalHeader, ModalFooter, ModalBody, \
    Button, Row, Col

from dash_table import DataTable
from ..server import app

def relationship_tab():
    return [
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
                    
                ]),
            ],
            id='saved-fil-modal',centered=True,size='lg'),

            Modal(
                [
                    ModalHeader([
                        H5('Save changes'),
                    ]),
                    
                    ModalBody([
                        Input(id='modal-sf-filter-name',value=None),
                        Label("Saved Successfully!!",id='modal-sf-status',hidden=True)
                    ],id='modal-sf-body'),

                    ModalFooter([
                        Button("Save",id='modal-sf-save',className='ml-auto'),
                    ]),
                ],id='sf-modal',centered=True,size='sm'),
            
            

            Div(
                Row([
                    Col([
                        Button("Add Table", color="primary",id='add-table-button', className="mr-1",size="sm",disabled=True),
                    ],width=3),

                    Col([
                        Button("Run", color="primary",id='preview-table-button', className="mr-1",size="sm",disabled=True),
                        # Button("Save relation", color="primary",id='save-relationship-button', className="mr-1",size="sm"),
                    ],width=3)
                ])
            ),
            
            Br(),
            Br(),

            
            Div([
                Row([
                    Col(
                        Dropdown(
                            id={'type':'relationship-table-dropdown','index':0},
                            value=None,
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
                                    Row(
                                        Col(
                                            H5(id={'type':'join-status','index':0})
                                        )
                                    )

                                ])
                            ]),
                            ModalFooter([Button("Apply",id={'type':'apply-join-modal','index':0},className='ml-auto')])
                        ],id={'type':'join-modal','index':0},centered=True,size='lg'
                    ),
                ],id="tables-row")
            ],id='table-dropdown-div',className='pretty_container ten columns'),

            

            Div(
                Row(
                    Col(
                        DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in ["column-1","column-2","column-3"]],
                            data= [],
                        )
                    )
                )
            ,className='pretty_container nine columns',id='relationship-table-div'),
    ]
