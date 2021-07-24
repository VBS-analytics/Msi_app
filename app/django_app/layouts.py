from dash_core_components import Store
from dash_bootstrap_components import Tabs, Tab
from .global_functions import get_table_names

import dash_bootstrap_components as dbc
import dash_html_components as html
from .server import app

def get_help_page():
    return html.Div([
        dbc.Row(
            dbc.Col([
                html.Div("MIS report generating application", className="display-1"),
                html.Div(["A simple web application to ",html.B("join tables, apply filters"),\
                    " and ",html.B("select or drop columns"),\
                    " from the database tables without writing any SQL queries."], className="display-5"),
                
                dbc.Alert([html.B("Note: "),"Changes made in application does not \
                    affect the original databases used for creating the reports. \
                    This application doesn't have write,update or delete \
                    permissions on the databases used."], color="info"),
                
                html.Hr(),
                html.Div("Accessing the application", className='display-4'),
                html.Div([
                    "Right now the application is running at ",html.B("172.21.12.19 "),
                    html.A("Click here",href="http://172.21.12.19/")
                ],className="display-5"),
                
                html.Hr(),
                html.Div("Running a single table", className='display-4'),
                html.Div([
                    "Make sure the ",html.B("Table relationship")," tab is selected and \
                    from the dropdown select the required table and click on \
                    ",html.B("RUN")," to make the table available for operations."
                ],className="display-5"),
                html.Img(src=app.get_asset_url("single-table-add.gif")),
                html.Hr(),

                html.Div("Joining tables", className='display-4'),
                html.Div([
                    "Click on ",html.B("ADD TABLE")," a new dropdown will appear then select \
                    the table names in both the dropdown before clicking on the join icon"
                ],className="display-5"),
                html.Img(src=app.get_asset_url("add-multiple-table.gif")),
                html.Hr(),

                html.Div("Adding filters to the table or the relationship made", className='display-4'),
                html.Div([
                    "First make sure you're in ",html.B("Table transformations")," tab, \
                    clear the dropdown textbox by pressing `x` and then select \
                    `Filter rows` from the dropdown menu."
                ],className="display-5"),
                dbc.Alert([html.B("Issue: "),"There is an issue here when you \
                    click on `ADD CONDITION` the pop-up refreshes so the \
                    previously entered values disappears. In future i try to \
                    come-up with an solution soon."], color="warning"),
                html.Img(src=app.get_asset_url("add-filter.gif")),
                html.Hr(),

                html.Div("Select or drop columns", className='display-4'),
                html.Div([
                    "Before selecting first clear the dropdown by clicking `x` \
                    then select the `select or drop columns` from the dropdown menu."
                ],className="display-5"),
                html.Img(src=app.get_asset_url("select-columns.gif")),
                html.Hr(),

                html.Div("Remove applied transformations", className='display-4'),
                html.Div([
                    "removing a applied transforamation can be done by clicking at the top right corner."
                ],className="display-5"),
                html.Img(src=app.get_asset_url("removing-filter.gif")),
                html.Hr(),

                html.Div("Format-mapping", className='display-4'),
                html.Div([
                    "Changing the column names with the column names in .csv file. Then click on ",html.B("PREVIEW")," to make the chanages take effect."
                ],className="display-5"),
                html.Img(src=app.get_asset_url("format-mapping.gif")),
                html.Hr(),

                html.Div("Generate excel for downloading", className='display-4'),
                html.Div([
                    "to download the final data as .excel, first it needs to be generated so that a download link will be available in the the top right download icon."
                ],className="display-5"),
                html.Img(src=app.get_asset_url("generate-excel.gif")),
                html.Hr(),

                html.Div("Save the Report", className='display-4'),
                html.Div([
                    "Click on save icon to open a pop-up just enter a name and click save, to save the changes in internal DB."
                ],className="display-5"),
                html.Img(src=app.get_asset_url("save-report.gif")),
                html.Hr(),
                              
                ],width={"size": 6, "offset": 3},
            )
        ),
    ])
    
def index():
    
    import uuid
    
    '''importing the layouts'''
    from .dash_layouts.relationship_layout import relationship_tab
    from .dash_layouts.transformations_layout import transform_tab
    from .dash_layouts.formatmapping_layout import formatmap_tab


    '''importing the callbacks'''
    from .dash_callbacks import relationship_callback
    from .dash_callbacks import transform_callback
    from .dash_callbacks import formatmap_callback
        

    
    session_id = str(uuid.uuid4())
    if session_id is not None:
        db_table_names = get_table_names()
        return [            
                Store(id='db-table-names',data=db_table_names),
                Store(id='relationship-data',data=dict(table=[],columns=None,saved_data=False,table_order=[])),
                Store(id='filters-data',data=dict(
                    select_or_drop_columns=dict(),
                    filters=dict(),
                    index_k=None,
                    )
                ),
                Store(id='format-map-data',data={}),
                Store(id='upload-file-columns-data',data=[]),
                Store(id='transformations-table-column-data',data={}),
                # Store(id='transformations-table-sql-query',data=None),
                Store(id='transformations-filters-condi',data=None),
                # Store(id='relationship-table-sql-query',data=None),
                # Store(id='filters-text-area',data=[]),
                Store(id='retrived-data',data=None),
                Store(id='index_k',data=None),
                # Store(id={'type':'saved_status','index':1},data=False),
                # {'type':'filters-text-drpdwn','index':0},width=4
                Store(id='total-rows',data=None),
                Store(id='relation-rows',data=None),
                Store(id='transformations-rows',data=None),
                Store(id='filter-condi-index',data=None),
                Store(id='table-rows-save',data={}),
                Store(id='main-sql-query',data=None),

                Store(
                    id='save-changes',
                    data={
                        'relationship_data':{},
                        'filters_data':{},
                        'format_map_data':{},
                        'upload_file_columns_data':[],
                        'transformations_table_column_data':{},
                        'transformations_filters_condi':None,
                        'tables_rows':{},
                        'filter_rows':[],
                        'format_rows':[],
                        'sel_val':None,
                        'sel_col':None,
                    }
                ),

                Store(id='download_data',data=None),
                Store(id='session-id',data=session_id),
                Store(id='filters-retrived-status',data=None),

                # html.Div([
                #     dbc.Row(
                #         dbc.Col([
                Tabs([
                    Tab(relationship_tab(),label='Table relationship'),
                    Tab(transform_tab(),label='Table transformations'),
                    Tab(formatmap_tab(),label='Format Mapping'),
                    # Tab(sal_hier_layout(),label='Pivot table'),
                    #         ]),
                    #     ],width={"size": 12, "offset": 1})
                    # )
                ]),
            ]
    else:
        return []