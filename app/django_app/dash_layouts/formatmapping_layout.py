# from dash_core_components import Upload
# from dash_html_components import A, Div, Br
from dash_bootstrap_components import Button, Row, Col
# from dash_table import DataTable
from dash_extensions import Download

from dash import dcc,html,dash_table

def formatmap_tab():
    return [
        html.Br(),
        html.Div([
            Row(
                Col(
                    dcc.Upload([
                        'Drag and Drop or ',
                        html.A('Select a File')
                    ], style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center'
                    },id='file_upload')

                )
            ),

            html.Div([],id='column-names-row'),

            html.Div(
                Row([
                    Col(
                        Button("Preview", color="primary",id='preview-table-format-button', className="mr-1",size="sm",disabled=True)
                    ,width={"size": 3}),
                    Col(
                        [
                            Button("Download Excel", color="primary",id='generate-excel-format-button', className="mr-1",size="sm"),
                            Download(id='download-excel')
                        ]
                    ,width={"size": 3, "offset": 1}),
                ])
            ),

            html.Div(
                Row(
                    Col(
                        dash_table.DataTable(
                            id='format-table',
                            columns=[{"name": i, "id": i} for i in ["column-1","column-2","column-3"]],
                            data= [],
                            style_table={'overflowX': 'scroll'},
                        )
                    )
                )
            ,className='pretty_container nine columns'),
        ])
    ]