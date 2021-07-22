import sys
from ..server import app, server
from ..global_functions import get_downloaded_data

from dash.dependencies import Output, Input, State, ALL
from dash import callback_context
from dash_core_components import Dropdown
from dash_html_components import Label, Br
from dash_bootstrap_components import Col, Row

from dash import callback_context
from pandas import read_csv, read_excel
import io
import base64

# download data from format table
@app.callback(
    Output('download','href'),
    [
        Input('generate-excel-format-button','n_clicks'),
    ],
    [
        State('download_data','data')
    ]
)
def update_download_link(n_clicks,data):
    if data is not None:
        download_link = get_downloaded_data(data)
        return download_link
    else:
        return None


# upload the format file which accepts csv only.
@app.callback(
    [
        Output('column-names-row','children'),
        Output('preview-table-format-button','disabled'),
        Output('upload-file-columns-data','data'),
    ],
    [
        Input('file_upload','contents'),
        Input('retrived-data','data'),
    ],
    [
        State('file_upload', 'filename'),
        State('relationship-data','data'),

        State('column-names-row','children'),
        State('preview-table-format-button','disabled'),
        State('upload-file-columns-data','data'),
        State('transformations-table-column-data','data'),
        
    ]
)
def update_file_upload_columns(contents,ret_data,filename,relationship_data, \
    childs,disabled,upload_data,trans_columns):

    ctx = callback_context
    triggred_compo = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggred_compo == 'file_upload' and contents is not None:

        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        df=None
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xlsx' in filename:
                # Assume that the user uploaded an excel file
                df = read_excel(io.BytesIO(decoded))
        except Exception as e:
            sys.stderr.write(e)
            print(e,flush=True)
        
        components = []
        for j,k in enumerate(df.columns):
            components.append(Row([
                Col(Label(k),width=3),

                Col(Dropdown(
                    id={
                        'type': 'filter-dropdown',
                        'index': j
                    },
                    options=[{'label':i,'value':i} for i in trans_columns.keys()],
                    value=None,
                ),width=3),
            ]))
            components.append(Br())
        
        but_status = True
        if components != []:
            but_status = False
        else:
            but_status = True

        return components, but_status, df.columns

    elif triggred_compo == 'retrived-data' and ret_data is not None:
        but_status = True
        if ret_data['format_rows'] != [] and ret_data['format_rows'] is not None:
            but_status = False
        else:
            but_status = True


        return ret_data['format_rows'],but_status,ret_data['upload_file_columns_data']

    else:
        return childs, disabled, upload_data


# stores the mapped data to memory.
@app.callback(
    Output('format-map-data', 'data'),
    [
        Input('preview-table-format-button','n_clicks'),
    ],
    
    [
        State({'type': 'filter-dropdown', 'index': ALL}, 'value'),
        State('upload-file-columns-data','data'),
    ]
)
def display_output(n_clicks,values,data):
    if data != []:
        d={}
        [d.update({i:j}) for i,j in zip(data,values)]
        return d
