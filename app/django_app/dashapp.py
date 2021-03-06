import os
from dash.dependencies import Output, Input
# from dash_core_components import Location, Loading
# from dash_html_components import Div,A, I, Br, H5, P, Img
from dash_bootstrap_components import Row, Col, Collapse, NavbarToggler, Navbar,\
    NavbarBrand, Nav, NavItem, Modal, ModalHeader, ModalBody, ModalFooter, Card,\
        CardBody, Button, DropdownMenu, DropdownMenuItem, Tooltip
from dash import dcc, html

from .server import app
from . import router

# callbacks could go here, or in another callback.py file with this at the top:
# from .server import app
bolt = html.I(className="fa fa-bolt")
dropdown = DropdownMenu(
        children=[
            # Div([
            #     Row([],id="filters-row"),
            # ],id="applied-filters-div"),

            # Div([
            #     Row([],id="add-filters-row"),
            # ],id="add-applied-filters-div"),

            # Div([
            #     Row([],id="treemap-filters-row")
            # ],id="treemap-applied-filters-div"),
            
            # Div([
            #     Label('Filters'),I(className='fa fa-times')
            # ],id='add-applied-filters-div'),
            # DropdownMenuItem(style={'display':'none'},id={'type':'applied-changes-menu','index':0}),

            # Div([],id='applied-filters-div'),

            # DropdownMenuItem('Clear All',className='fa fa-trash',\
            #     id="clear-all"),
            DropdownMenuItem('none',className='fa fa-trash',\
                id={'type':'applied-changes-menu','index':0},style={'display':'none'}),
                # Button("Clear Fliters", color="success", className="mr-1",id="clear-filters"),

            # DropdownMenuItem([
            #     I('     Clear All',className='fa fa-trash',id='clear-filters')
            #     # Button("Clear Fliters", color="success", className="mr-1",id="clear-filters"),
            # ]),
            
            DropdownMenuItem(divider=True,id='menu-divider'),
        ],
        nav=True,
        in_navbar=True,
        id='applied-changes-dropdown',
        label='Applied changes',
        # className='fa fa-bolt',
        direction="left")


app.layout = dcc.Loading(type='circle',children=[html.Div(children=[
    html.Div(id="output-clientside"),
    
    Navbar([
            Row([
                #height="40px",width='100px'
                Col(NavbarBrand([html.Img(src=app.get_asset_url('Valuestream-Logo.png'), style={"height": "40px","width": "auto","margin-bottom": "25px"})])),
                Col(NavbarBrand(html.H5("MIS Report Generator (beta)"),className="ml-2")),
            ],align="center",no_gutters=True),
            NavbarToggler(id="navbar-toggler2"),
            Collapse(
                Nav([
                    Row([
                        Col(dropdown),
                    ]),
                 
                    Row([
                        Col(NavItem(html.A(html.I(className="fa fa-clock-o"),id='scheduled-outputs'))),
                        Col(NavItem(html.A(html.I(className="fa fa-filter",style={"font-size":"15px"}),id='saved-filters-btn'))),
                        Col(NavItem([html.A(html.I(className='fa fa-save'),id='run')])),
                        # Col(NavItem([A(I(className='fa fa-download'),id='download',download='file.xlsx',target="_blank")])),
                        Col(NavItem([html.A(html.I(className='fa fa-question'),id='help',href='/help',target="_blank")])),
                        Tooltip(
                            f"help",
                            target='help',
                            placement="top",
                        ),
                        Tooltip(
                            f"Save changes",
                            target='run',
                            placement="top",
                        ),
                        Tooltip(
                            f"view saved filters",
                            target='saved-filters-btn',
                            placement="top",
                        ),
                        Tooltip(
                            f"scheduled outputs",
                            target='scheduled-outputs',
                            placement="top",
                        ),
                    ],className="ml-auto flex-nowrap mt-3 mt-md-0",align="center"),
                ], className="ml-auto", navbar=True),
                id="navbar-collapse2",
                navbar=True,
            )
        ],
        color="white",
        light=True,
        id='navbar_top',
        # fixed="top",#mb-5
        style={"box-shadow":"0px 8px 8px -6px rgba(0,0,0,.5)",'margin-bottom':'5px'}
    ),
    Modal(
        [
            ModalHeader("Filters"),
            ModalBody(id='filters-body'),
            ModalFooter([
                Button("Close", id="close-body-scroll", className="ml-auto"),
                Button("Apply", id="apply-filter", className="ml-auto")
            ]),
        ],
        id="modal-body-scroll",
        scrollable=True,
        centered=True,
        size="lg",
        backdrop="static"
    ),
    html.Br(),
    dcc.Location(id='url', refresh=False),

    
    
    # Br(),
    html.Div(id='content',style={"display": "flex", "flex-direction": "column"}),
],id="mainContainer",style={"display": "flex", "flex-direction": "column"})])