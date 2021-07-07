from dash_core_components import Store
from dash_bootstrap_components import Tabs, Tab
from .global_functions import get_table_names

lazy_import = None
def index():
    global lazy_import
    if lazy_import is None:
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
        db_table_names = get_table_names(session_id)
        return [            
                Store(id='db-table-names',data=db_table_names),
                Store(id='relationship-data',data=dict(table=[],columns=None,saved_data=False)),
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

                Tabs([
                    Tab(relationship_tab(),label='Table relationship'),
                    Tab(transform_tab(),label='Table transformations'),
                    Tab(formatmap_tab(),label='Format Mapping'),
                    # Tab(sal_hier_layout(),label='Pivot table'),
                ]),
            ]
    else:
        return []