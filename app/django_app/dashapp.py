import os
from dash.dependencies import Output, Input
from dash_core_components import Location, Loading
from dash_html_components import Div,A, I, Br, H5, P, Img
from dash_bootstrap_components import Row, Col, Collapse, NavbarToggler, Navbar,\
    NavbarBrand, Nav, NavItem, Modal, ModalHeader, ModalBody, ModalFooter, Card,\
        CardBody, Button


from .server import app
from . import router

# callbacks could go here, or in another callback.py file with this at the top:
# from .server import app


app.layout = Loading(type='circle',children=[Div(children=[
    Div(id="output-clientside"),
    
    Navbar([
            Row([
                #height="40px",width='100px'
                Col(NavbarBrand([Img(src=app.get_asset_url('Valuestream-Logo.png'), style={"height": "40px","width": "auto","margin-bottom": "25px"})])),
                Col(NavbarBrand(H5("MIS Report Generator"),className="ml-2")),
            ],align="center",no_gutters=True),
            NavbarToggler(id="navbar-toggler2"),
            Collapse(
                Nav([
                    Row([
                        # Col(dropdown),
                        Col(NavItem(A(I(className="fas fa-filter"),id='saved-filters-btn'))),
                        Col(NavItem([A(I(className='fa fa-save'),id='run')])),
                        Col(NavItem([A(I(className='fa fa-download'),id='download',download='file.xlsx',target="_blank")])),
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
    ),
    Br(),
    Location(id='url', refresh=False),

    Row([
        Col(Card(
                # CardHeader("Card header"),
                CardBody([
                    H5(id='noofpolicies-card',className="card-title"),
                    P("Total No.of Policies",className="card-text"),
                ])
        ,color="light"),width=2)
    ]),
    Br(),
    Div(id='content',style={"display": "flex", "flex-direction": "column"}),
],id="mainContainer",style={"display": "flex", "flex-direction": "column"})])