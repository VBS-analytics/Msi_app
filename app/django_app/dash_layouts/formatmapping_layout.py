from dash_core_components import Upload
from dash_html_components import A, Div
from dash_bootstrap_components import Button, Row, Col
from dash_table import DataTable

def formatmap_tab():
    return [
        Div([
            Row(
                Col(
                    Upload([
                        'Drag and Drop or ',
                        A('Select a File')
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

            Div([],id='column-names-row'),

            Div(
                Row([
                    Col(
                        Button("Preview", color="primary",id='preview-table-format-button', className="mr-1",size="sm",disabled=True)
                    ),
                    Col(
                        Button("Generate Excel", color="primary",id='generate-excel-format-button', className="mr-1",size="sm")
                    )
                ])
            ),

            Div(
                Row(
                    Col(
                        DataTable(
                            id='format-table',
                            columns=[{"name": i, "id": i} for i in ["column-1","column-2","column-3"]],
                            data= [],
                        )
                    )
                )
            ,className='pretty_container nine columns'),
        ])
    ]