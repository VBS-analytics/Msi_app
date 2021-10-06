import sys
from ..server import app, server
from ..global_functions import get_downloaded_data, get_bool_on_col

from dash.dependencies import Output, Input, State, ALL
# from dash import callback_context
# from dash_core_components import Dropdown
# from dash_html_components import Label, Br
from dash_bootstrap_components import Col, Row

from dash import callback_context, dcc, html
from pandas import read_csv, read_excel
import io
import base64

from dash.exceptions import PreventUpdate

# download data from format table
@app.callback(
    Output('download-excel','data'),
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
        Output('upload-file-columns-data','data'),
    ],
    [
        Input('file_upload','contents'),
        Input('relationship-data','data'),
    ],
    [
        State('retrived-data','data'),
        State('file_upload', 'filename'),

        State('column-names-row','children'),
        State('upload-file-columns-data','data'),
        State('transformations-table-column-data','data'),
        State({'type': 'filter-dropdown', 'index': ALL}, 'value'),
        
    ]
)
def update_file_upload_columns(contents,relationship_data,ret_data,filename, \
    childs,upload_data,trans_columns,filter_dropdown_vals):

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
                Col(html.Label(k),width=3),

                Col(dcc.Dropdown(
                    id={
                        'type': 'filter-dropdown',
                        'index': j
                    },
                    options=[{'label':i,'value':i} for i in trans_columns.keys()],
                    value=None,
                ),width=3),
            ]))
            components.append(html.Br())
        
        but_status = True
        if components != []:
            but_status = False
        else:
            but_status = True

        return components, df.columns

    elif triggred_compo == 'relationship-data' and relationship_data is not None and \
        relationship_data['saved_data'] is True and ret_data is not None:
        but_status = True
        if ret_data['format_rows'] != [] and ret_data['format_rows'] is not None:
            but_status = False
        else:
            but_status = True
        return ret_data['format_rows'],ret_data['upload_file_columns_data']

    elif triggred_compo == 'relationship-data' and relationship_data is not None and \
        relationship_data['table']!=[] and upload_data is not None and upload_data != []:
            components = []
            for j,k in enumerate(upload_data):
                val =filter_dropdown_vals[j] if filter_dropdown_vals[j] in \
                    list(trans_columns.keys()) else None
                components.append(Row([
                    Col(html.Label(k),width=3),

                    Col(dcc.Dropdown(
                        id={
                            'type': 'filter-dropdown',
                            'index': j
                        },
                        options=[{'label':i,'value':i} for i in trans_columns.keys()],
                        value=val,
                    ),width=3),
                ]))
                components.append(html.Br())
            
            but_status = True
            if components != []:
                but_status = False
            else:
                but_status = True

            return components, upload_data
    else:
        return [], None


# disable preview button
@app.callback(
    Output('preview-table-format-button','disabled'),
    [
        Input({'type': 'filter-dropdown', 'index': ALL}, 'value')
    ],
    [
        State('download_data','data'), # stores all relations, filters and format mapping data
    ]
)
def disable_preview(values,download_data):
    if all(values) and values !=[]:
        stat,err_list,err_loc=get_bool_on_col(download_data,values)
        if stat is False and err_list != [] and err_loc != []:
            # for i in err_loc:
            #     fil_drop_style[i]={'border-color':'red'}
            
            return True
        else:
            return False
    else:
        return True


# stores the mapped data to memory.
app.clientside_callback(
    '''
    function display_output(n_clicks,values,data) {
        if (n_clicks != null && n_clicks != undefined && n_clicks > 0){
            if (data != null && data != undefined && data.length > 0) {
                let d = {}
                for (let i in data){
                    d[data[i]]=values[i]
                }
                return d
            }
        }
    }
        
    ''',
    Output('format-map-data', 'data'),
    Input('preview-table-format-button','n_clicks'),
    State({'type': 'filter-dropdown', 'index': ALL}, 'value'),
    State('upload-file-columns-data','data'),
    prevent_initial_call=True
)

# @app.callback(
#     Output('format-map-data', 'data'),
#     [
#         Input('preview-table-format-button','n_clicks'),
#     ],
    
#     [
#         State({'type': 'filter-dropdown', 'index': ALL}, 'value'),
#         State('upload-file-columns-data','data'),
#     ]
# )
# def display_output(n_clicks,values,data):
#     if n_clicks is not None:
#         if data != []:
#             d={}
#             [d.update({i:j}) for i,j in zip(data,values)]
#             return d
#     else:
#         raise PreventUpdate
