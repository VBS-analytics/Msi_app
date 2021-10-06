function update_filter_div(data,n_clicks,filters_data,childs,add_childs,fil_data) {
  const triggered = dash_clientside.callback_context.triggered.map(t => t.prop_id)

    let empty_div = [
        {
            'props':{
                'children':[
                    {
                        'props':{
                            'children':{
                                'props':{
                                    'children':{
                                        'props':{'className':"fa fa-refresh"},
                                        'type':'I',
                                        'namespace':'dash_html_components'
                                    },
                                    'id':'filters-clear-all'
                                },
                                'type':'A',
                                'namespace':'dash_html_components'
                            }
                        },
                        'type':'Col',
                        'namespace':"dash_bootstrap_components"
                    },

                    {
                        'props':{
                            'children':'Select or drop rows'
                        },
                        'type':'Label',
                        'namespace':'dash_html_components'
                    },

                    {
                        'props':{
                            'id':'filters-select-drop',
                            'options':[{'label':'Select','value':'Select'},{'label':'Drop','value':'Drop'}],
                            'value':null,
                            'style':{"width":"50%"}
                        },
                        'type':'Dropdown',
                        'namespace':'dash_core_components'
                    }
                ]
            },
            'type':'FormGroup',
            'namespace':'dash_bootstrap_components'
        },

        {
            'props':{
                'children':{
                    'props':{
                        'children':'Where,'
                    },
                    'type':'Label',
                    'namespace':'dash_html_components'
                }
            },
            'type':'FormGroup',
            'namespace':'dash_bootstrap_components'
        },

        {
            'props':{
                'children':[
                    {
                        'props':{
                            'children':[
                                {
                                    'props':{
                                        'children':{
                                            'props':{
                                                'children':[
                                                    {
                                                        'props':{
                                                            'children':{
                                                                'props':{'children':'Select column name'},
                                                                'type':'Strong',
                                                                'namespace':'dash_html_components'
                                                            },
                                                            'html_for':{'type':'filters-column-names','index':0}    
                                                        },
                                                        'type':'Label',
                                                        'namespace':'dash_bootstrap_components'
                                                    },

                                                    {
                                                        'props':{
                                                            'id':{'type':'filters-column-names','index':0},
                                                            'value':null
                                                        },
                                                        'type':'Dropdown',
                                                        'namespace':'dash_core_components'
                                                    }
                                                ]
                                            },
                                            'type':'FormGroup',
                                            'namespace':'dash_bootstrap_components'
                                        },
                                        'width':4
                                    },
                                    'type':'Col',
                                    'namespace':'dash_bootstrap_components'
                                },

                                {
                                    'props':{
                                        'children':{
                                            'props':{
                                                'children':[
                                                    {
                                                        'props':{
                                                            'children':{
                                                                'props':{'children':'condition'},
                                                                'type':'Strong',
                                                                'namespace':'dash_html_components'
                                                            },
                                                            'html_for':{'type':'filters-conditions','index':0}    
                                                        },
                                                        'type':'Label',
                                                        'namespace':'dash_bootstrap_components'
                                                    },

                                                    {
                                                        'props':{
                                                            'id':{'type':'filters-conditions','index':0},
                                                        },
                                                        'type':'Dropdown',
                                                        'namespace':'dash_core_components'
                                                    }
                                                ]
                                            },
                                            'type':'FormGroup',
                                            'namespace':'dash_bootstrap_components'
                                        },
                                        'width':3
                                    },
                                    'type':'Col',
                                    'namespace':'dash_bootstrap_components'
                                },

                                {
                                    'props':{
                                        'children':{
                                            'props':{
                                                'children':[
                                                    {
                                                        'props':{
                                                            'children':{
                                                                'props':{'children':'value'},
                                                                'type':'Strong',
                                                                'namespace':'dash_html_components'
                                                            }
                                                        },
                                                        'type':'Label',
                                                        'namespace':'dash_html_components'
                                                    },

                                                    {
                                                        'props':{
                                                            'id':{"type":'trans-multi-text','index':0},
                                                            'style':{'display':'none'}
                                                        },
                                                        'type':'Dropdown',
                                                        'namespace':'dash_core_components'
                                                    },

                                                    {
                                                        'props':{
                                                            'id':{"type":'trans-text','index':0},
                                                            'style':{'display':'none'},
                                                            'debounce':True
                                                        },
                                                        'type':'Input',
                                                        'namespace':'dash_core_components'
                                                    },

                                                    {
                                                        'props':{
                                                            'id':{'type':'trans-input','index':0},
                                                            'style':{'display':'none'},
                                                            'debounce':True
                                                        },
                                                        'type':'Input',
                                                        'namespace':'dash_core_components'
                                                    },

                                                    {
                                                        'props':{
                                                            'id':{'type':'trans-date-range','index':0},
                                                            'style':{'display':'none'}
                                                        },
                                                        'type':'DatePickerRange',
                                                        'namespace':'dash_core_components'
                                                    },

                                                    {
                                                        'props':{
                                                            'id':{'type':'trans-date-single','index':0},
                                                            'style':{'display':'none'}
                                                        },
                                                        'type':'DatePickerSingle',
                                                        'namespace':'dash_core_components'
                                                    },

                                                    {
                                                        'props':{
                                                            'id':{'type':'trans-days-single','index':0},
                                                            'style':{'display':'none'}
                                                        },
                                                        'type':'DatePickerSingle',
                                                        'namespace':'dash_core_components'
                                                    },

                                                    {
                                                        'props':{
                                                            'id':{'type':'trans-use-current-date','index':0},
                                                            'style':{'display':'none'}
                                                        },
                                                        'type':'Checklist',
                                                        'namespace':'dash_core_components'
                                                    }
                                                ]
                                            },
                                            'type':'FormGroup',
                                            'namespace':'dash_bootstrap_components'
                                        },
                                        'id':{'type':'filters-text-drpdwn','index':0},
                                        'width':4
                                    },
                                    'type':'Col'
                                },

                                {
                                    'props':{
                                        'children':{
                                            'props':{
                                                'children':{
                                                    'props':{
                                                        'className':"fa fa-trash-o"
                                                    },
                                                    'type':'I',
                                                    'namespace':'dash_html_components'
                                                },
                                                'id':{'type':'logic-close','index':0}
                                            },
                                            'type':'A',
                                            'namespace':'dash_html_components'
                                        }
                                    },
                                    'type':'Col',
                                    'namespace':'dash_bootstrap_components'
                                }
                            ],
                            'id':{'type':'condition-rows','index':0}
                        },
                        'type':'Row',
                        'namespace':'dash_bootstrap_components'
                    },

                    {
                        'props':{
                            'children':{
                                'props':{
                                    'children':'This is Temp column and row'
                                },
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            },
                            'id':{"type":"filters-logic","index":0},
                            'style':{'display':'none'}
                        },
                        'type':'Row',
                        'namespace':'dash_bootstrap_components'
                    }
                ],
                'id':'filters-conditional-div'
            },
            'type':'Div',
            'namespace':'dash_html_components'
        },

        {
            'props':{
                "children":{
                    'props':{
                        'children':{
                            'props':{
                                'children':'add condition',
                                'size':'sm',
                                'id':'filters-add-condition'
                            },
                            'type':'Button',
                            'namespace':'dash_bootstrap_components'
                        }  
                    },
                    'type':'Col',
                    'namespace':'dash_bootstrap_components'
                }
            },
            'type':'Row',
            'namespace':'dash_bootstrap_components'
        }

    ]

    let empty_div_add = [
        {
            'props':{
                'children':[
                        {
                            'props':{
                                'children':[
                                    {
                                        'props':{
                                            'children':{
                                                'props':{
                                                    'children':{
                                                        'props':{
                                                            'className':"fa fa-trash"
                                                        },
                                                        'type':'I',
                                                        'namespace':'dash_html_components'
                                                    },
                                                    'id':{'type':'add-col-remove','index':0}
                                                },
                                                'type':'A',
                                                'namespace':'dash_html_components'
                                            },
                                            'className':"text-right"
                                        },
                                        'type':'Col',
                                        'namespace':'dash_bootstrap_components'
                                    },

                                    {
                                        'props':{"children":"Enter column name"},
                                        'type':'Label',
                                        'namespace':'dash_html_components'
                                    },

                                    {
                                        'props':{
                                            'id':{"type":"add-new-col-name","index":0},
                                            'type':"text",
                                            'minLength':5,
                                            'required':true
                                        },
                                        'type':'Input',
                                        'namespace':'dash_core_components'
                                    },

                                    {
                                        'props':{
                                            "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
                                            'color':"secondary"
                                        },
                                        'type':'FormText',
                                        'namespace':'dash_bootstrap_components'
                                    },
                                ],
                                'id':{"type":'add-col-grp-1','index':0}
                            },
                            'type':'FormGroup',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'children':[
                                    {
                                        'props':{'children':"Assign value to new column"},
                                        'type':'Label',
                                        'namespace':'dash_html_components'
                                    },

                                    {
                                        'props':{
                                            'id':{"type":'add-col-value-input',"index":0},
                                            'type':'text',
                                            'required':true
                                        },
                                        'type':'Input',
                                        'namespace':'dash_core_components'
                                    }
                                ],
                                'id':{"type":'add-col-grp-2','index':0}
                            },
                            'type':'FormGroup',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{'children':null},
                            'type':'Hr',
                            'namespace':'dash_html_components'
                        }
                    ],
                'id':"add-col-form"
            },
            'type':'Form',
            'namespace':'dash_bootstrap_components'
        },

        {
            'props':{'children':null},
            'type':'Hr',
            'namespace':'dash_html_components'
        },

        {
            'props':{
                'children':{
                    'props':{
                        'children':{
                            'props':{
                                'children':"Add column",
                                'id':"add-col-new-col-but"
                            },
                            'type':'Button',
                            'namespace':'dash_html_components'
                        }
                    },
                    'type':'Col',
                    'namespace':'dash_bootstrap_components'
                }
            },
            'type':'Row',
            'namespace':'dash_bootstrap_components'
        }
    ]

    if (triggered.includes('retrived-data.data') && data != null && data != undefined && Object.entries(data['filters_data']['filters']).length !=  0) {
        return [data['filter_rows'], data['add_new_col_rows']]
    } else if (triggered.includes('preview-table-button.n_clicks')) {
        if (n_clicks != null && n_clicks != undefined && n_clicks > 0) {
            return [empty_div,empty_div_add]
        } else {
            window.dash_clientside.no_update
        }
    } else if (triggered.includes('filters-data.data') && Object.entries(filters_data['filters']).length != 0 && filters_data['status'] == true) {
        let fil_div = []
        let add_col_div=[]

        if (Object.entries(filters_data['filters']).length != 0) {
            let in_k = Object.keys(filters_data["filters"])[0]
            let fil_condition_rows = []

            for (i in filters_data['filters'][in_k]['index']) {
                let form_grp = {
                    'props':{
                        'children':[
                            {
                                'props':{'children':{
                                    'props':{'children':"value"},
                                    'type':'Strong',
                                    'namespace': 'dash_html_components'
                                }},
                                'type':'Label',
                                'namespace': 'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{"type":'trans-multi-text','index':0},
                                    'style':{'display':'none'}
                                },
                                'type':'Dropdown',
                                'namespace': 'dash_core_components'
                            },

                            {
                                'props':{
                                    'id':{"type":'trans-text','index':0},
                                    'style':{'display':'none'},
                                    'debounce':true
                                },
                                'type':'Input',
                                'namespace': 'dash_core_components'
                            },

                            {
                                'props':{
                                    'id':{'type':'trans-input','index':0},
                                    'style':{'display':'none'},
                                    'debounce':true
                                },
                                'type':'Input',
                                'namespace': 'dash_core_components'
                            },

                            {
                                'props':{
                                    'id':{'type':'trans-date-range','index':0},
                                    'style':{'display':'none'},
                                },
                                'type':'DatePickerRange',
                                'namespace': 'dash_core_components'
                            },

                            {
                                'props':{
                                    'id':{'type':'trans-date-single','index':0},
                                    'style':{'display':'none'},
                                },
                                'type':'DatePickerSingle',
                                'namespace': 'dash_core_components'
                            },

                            {
                                'props':{
                                    'id':{'type':'trans-days-single','index':0},
                                    'style':{'display':'none'},
                                },
                                'type':'DatePickerSingle',
                                'namespace': 'dash_core_components'
                            },

                            {
                                'props':{
                                    'id':{'type':'trans-use-current-date','index':0},
                                    'style':{'display':'none'},
                                },
                                'type':'Checklist',
                                'namespace': 'dash_core_components'
                            },
                        ]
                    },
                    'type':'FormGroup',
                    'namespace': 'dash_bootstrap_components'
                }

                if (filters_data['filters'][in_k]['values_vals'][i].constructor == Object
                    && Object.keys(filters_data['filters'][in_k]['values_vals'][i]).includes("trans-multi-text")) {
                    
                    form_grp = {
                        'props':{'children':[
                            {
                                'props':{'children':{
                                    'props':{'children':"value"},
                                    'type':'Strong',
                                    'namespace': 'dash_html_components'
                                }},
                                'type':'Label',
                                'namespace': 'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{"type":'trans-multi-text','index':filters_data['filters'][in_k]['index'][i]},
                                    'value':filters_data['filters'][in_k]['values'][i],
                                    'multi':true,
                                    'options':filters_data['filters'][in_k]['values_vals'][i]['trans-multi-text']
                                },
                                'type':'Dropdown',
                                'namespace': 'dash_core_components'
                            },
                        ]},
                        'type':'FormGroup',
                        'namespace': 'dash_bootstrap_components'
                    }

                } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == String
                    && filters_data['filters'][in_k]['values_vals'][i].includes('trans-text') ) {
                    
                    form_grp={
                        'props':{"children":[
                            {
                                'props':{'children':{
                                    'props':{'children':"value"},
                                    'type':'Strong',
                                    'namespace': 'dash_html_components'
                                }},
                                'type':'Label',
                                'namespace': 'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{"type":'trans-text','index':filters_data['filters'][in_k]['index'][i]},
                                    'debounce':true,
                                    'value':filters_data['filters'][in_k]['values'][i]
                                },
                                'type':'Input',
                                'namespace': 'dash_core_components'
                            },
                        ]},
                        'type':'FormGroup',
                        'namespace': 'dash_bootstrap_components'
                    }

                } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == String
                    && filters_data['filters'][in_k]['values_vals'][i].includes('trans-input') ) {
                    
                    form_grp={
                        'props':{'children':[
                            {
                                'props':{'children':{
                                    'props':{'children':"value"},
                                    'type':'Strong',
                                    'namespace': 'dash_html_components'
                                }},
                                'type':'Label',
                                'namespace': 'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{'type':'trans-input','index':filters_data['filters'][in_k]['index'][i]},
                                    'debounce':true,
                                    'value':filters_data['filters'][in_k]['values'][i]
                                },
                                'type':'Input',
                                'namespace': 'dash_core_components'
                            },
                        ]},
                        'type':'FormGroup',
                        'namespace': 'dash_bootstrap_components'
                    }

                } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == Object
                    && Object.keys(filters_data['filters'][in_k]['values_vals'][i]).includes('trans-date-range')) {
                    
                    form_grp={
                        'props':{'children':[
                            {
                                'props':{'children':{
                                    'props':{'children':"value"},
                                    'type':'Strong',
                                    'namespace': 'dash_html_components'
                                }},
                                'type':'Label',
                                'namespace': 'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{'type':'trans-date-range','index':filters_data['filters'][in_k]['index'][i]},
                                    'min_date_allowed':filters_data['filters'][in_k]['values_vals'][i]['trans-date-range']['min'],
                                    'max_date_allowed':filters_data['filters'][in_k]['values_vals'][i]['trans-date-range']['max'],
                                    'start_date':filters_data['filters'][in_k]['values'][i][0],
                                    'end_date':filters_data['filters'][in_k]['values'][i][1],
                                },
                                'type':'DatePickerRange',
                                'namespace': 'dash_core_components'
                            },


                        ]},
                        'type':'FormGroup',
                        'namespace': 'dash_bootstrap_components'                    
                    }
                } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == Object
                    && Object.keys(filters_data['filters'][in_k]['values_vals'][i]).includes('trans-date-single')) {
                    
                    form_grp={
                        'props':{'children':[
                            {
                                'props':{'children':{
                                    'props':{'children':"value"},
                                    'type':'Strong',
                                    'namespace': 'dash_html_components'
                                }},
                                'type':'Label',
                                'namespace': 'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{'type':'trans-date-single','index':filters_data['filters'][in_k]['index'][i]},
                                    'min_date_allowed':filters_data['filters'][in_k]['values_vals'][i]['trans-date-single']['min'],
                                    'max_date_allowed':filters_data['filters'][in_k]['values_vals'][i]['trans-date-single']['max'],
                                    'date':filters_data['filters'][in_k]['values'][i],
                                },
                                'type':'DatePickerSingle',
                                'namespace': 'dash_core_components'
                            },

                        ]},
                        'type':'FormGroup',
                        'namespace': 'dash_bootstrap_components'                                        
                    }
    

                } else if (filters_data['filters'][in_k]['values_vals'][i].constructor == Array
                    && filters_data['filters'][in_k]['values_vals'][i].length > 0
                    && filters_data['filters'][in_k]['values_vals'][i].includes('trans-input')
                    && filters_data['filters'][in_k]['values_vals'][i].includes('trans-use-current-date')) {
                    
                    let ck=false
                    let val = null
                    let min_dt=null
                    let max_dt=null

                    let sig_dt={
                        'props':{
                            'id':{'type':'trans-days-single','index':filters_data['filters'][in_k]['index'][i]},
                        },
                        'type':'DatePickerSingle',
                        'namespace': 'dash_core_components'
                    }

                    if (filters_data['filters'][in_k]['values'][i][1].constructor == Array) {
                        ck=true
                        val=filters_data['filters'][in_k]['values'][i][1]
                        min_dt=filters_data['filters'][in_k]['values_vals'][i][2]['trans-days-single']['min']
                        max_dt=filters_data['filters'][in_k]['values_vals'][i][2]['trans-days-single']['max']

                        ck_val={
                            'props':{
                                'id':{'type':'trans-use-current-date','index':filters_data['filters'][in_k]['index'][i]},
                                'options':[
                                    {'label': 'Use current sys date', 'value': 'Use'},
                                ],
                                'value':val
                            },
                            'type':'Checklist',
                            'namespace': 'dash_core_components'
                        }
                        sig_dt={
                                'props':{
                                    'id':{'type':'trans-days-single','index':filters_data['filters'][in_k]['index'][i]},
                                    'placeholder':'mm/dd/YYYY',
                                    'min_date_allowed':min_dt,
                                    'max_date_allowed':max_dt,
                                    'initial_visible_month':new Date(),
                                    'disabled':true
                                    
                                },
                                'type':'DatePickerSingle',
                                'namespace': 'dash_core_components'
                            }
                    } else {
                        val=filters_data['filters'][in_k]['values'][i][1]
                        min_dt=filters_data['filters'][in_k]['values_vals'][i][2]['trans-days-single']['min']
                        max_dt=filters_data['filters'][in_k]['values_vals'][i][2]['trans-days-single']['max']

                        sig_dt={
                            'props':{
                                'id':{'type':'trans-days-single','index':filters_data['filters'][in_k]['index'][i]},
                                'placeholder':'mm/dd/YYYY',
                                'min_date_allowed':min_dt,
                                'max_date_allowed':max_dt,
                                'date':val
                            },
                            'type':'DatePickerSingle',
                            'namespace': 'dash_core_components'
                        }
                        
                        ck_val={
                                'props':{
                                    'id':{'type':'trans-use-current-date','index':filters_data['filters'][in_k]['index'][i]},
                                },
                                'type':'Checklist',
                                'namespace': 'dash_core_components'
                        }
                    }
                    
                    form_grp={
                        'props':{'children':[
                            {
                                'props':{'children':{
                                    'props':{'children':"value"},
                                    'type':'Strong',
                                    'namespace': 'dash_html_components'
                                }},
                                'type':'Label',
                                'namespace': 'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{'type':'trans-input','index':filters_data['filters'][in_k]['index'][i]},
                                    'debounce':true,
                                    'value':filters_data['filters'][in_k]['values'][i][0],
                                    'type':'number',
                                    'required':true,
                                    'inputMode':'numeric'
                                },
                                'type':'Input',
                                'namespace': 'dash_core_components'
                            },

                            sig_dt,
                            ck_val
                        ]},
                        'type':'FormGroup',
                        'namespace': 'dash_bootstrap_components'                    
                    }

                }
                
                condi_row={
                    'props':{'children':[
                        {'props':{'children':{
                            'props':{'children':[
                                        {
                                            'props':{
                                                'children':{
                                                        'props':{'children':"Select column name"},
                                                        'type':'Strong',
                                                        'namespace': 'dash_html_components'
                                                    },
                                                'html_for':{'type':'filters-column-names','index':filters_data['filters'][in_k]['index'][i]}
                                            },
                                            'type':'Label',
                                            'namespace':'dash_bootstrap_components'
                                        },
                                        {
                                            'props':{
                                                'id':{'type':'filters-column-names','index':filters_data['filters'][in_k]['index'][i]},
                                                'value':filters_data['filters'][in_k]['columns'][i],
                                                'options':filters_data['filters'][in_k]['columns_drpdwn_vals'][i]
                                            },
                                            'type':'Dropdown',
                                            'namespace':'dash_core_components'
                                        }

                                    ]},
                                'type':'FormGroup',
                                'namespace': 'dash_bootstrap_components'                    
                                },'width':4},
                            'type':'Col',
                            'namespace': 'dash_bootstrap_components'
                        },

                        {
                            'props':{'children':{
                                    'props':{'children':[
                                        {
                                            'props':{
                                                'children':{
                                                        'props':{'children':"condition"},
                                                        'type':'Strong',
                                                        'namespace': 'dash_html_components'
                                                    },
                                                'html_for':{'type':'filters-conditions','index':filters_data['filters'][in_k]['index'][i]}
                                            },
                                            'type':'Label',
                                            'namespace':'dash_bootstrap_components'
                                        },

                                        {
                                            'props':{
                                                'id':{'type':'filters-conditions','index':filters_data['filters'][in_k]['index'][i]},
                                                'value':filters_data['filters'][in_k]['condition'][i],
                                                'options':filters_data['filters'][in_k]['condition_drpdwn_vals'][i]
                                            },
                                            'type':'Dropdown',
                                            'namespace':'dash_core_components'
                                        }
                                        
                                    ]},
                                    'type':'FormGroup',
                                    'namespace': 'dash_bootstrap_components'    
                            },'width':3},
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'children':form_grp,
                                'id':{'type':'filters-text-drpdwn','index':filters_data['filters'][in_k]['index'][i]},
                                'width':4
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },

                        {
                            'props':{
                                'children':{
                                    'props':{
                                        'children':{
                                            'props':{'className':"fa fa-trash-o"},
                                            'type':'I',
                                            'namespace':'dash_html_components'
                                        },
                                        'id':{'type':'logic-close','index':filters_data['filters'][in_k]['index'][i]}
                                    },
                                    'type':'A',
                                    'namespace':'dash_html_components'
                                },
                                
                                'className':"text-right"
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },   
                    ],'id':{'type':'condition-rows','index':filters_data['filters'][in_k]['index'][i]}},
                    'type':'Row',
                    'namespace': 'dash_bootstrap_components'
                }

                if (filters_data['filters'][in_k]['logic'][i] != null && filters_data['filters'][in_k]['logic'][i] != undefined) {
                    log_row={
                        'props':{'children':{
                            'props':{'children':{
                                'props':{
                                    'id':{'type':'logic-dropdown','index':i},
                                    'options':[{'label':'And','value':'And'},{'label':'Or','value':'Or'}],
                                    'value':filters_data['filters'][in_k]['logic'][i]
                                },
                                'type':'Dropdown',
                                'namespace':'dash_core_components'

                            },'width':3},
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },'id':{'type':'filters-logic','index':filters_data['filters'][in_k]['index'][i]}},
                        'type':'Row',
                        'namespace':'dash_bootstrap_components'
                    }
                } else {
                    log_row = {
                        'props':{'children':{
                            'props':{'children':"This is Temp column and row"},
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },'id':{"type":"filters-logic","index":0},'style':{'display':'none'}},
                        'type':'Row',
                        'namespace':'dash_bootstrap_components'
                    }
                }

                fil_condition_rows.push(log_row)
                fil_condition_rows.push(condi_row)
                
            }

            fil_div = [
                {
                    'props':{'children':[
                        {
                            'props':{'children':{
                                'props':{
                                    'children':{
                                        'props':{'className':"fa fa-refresh"},
                                        'type':'I',
                                        'namespace':'dash_html_components'
                                    },
                                    'id':'filters-clear-all'
                                },
                                'type':'A',
                                'namespace':'dash_html_components'
                            },'className': 'text-right'},
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        },


                        {
                            'props':{'children':'Select or drop rows'},
                            'type':'Label',
                            'namespace':'dash_html_components'
                        },

                        {
                            'props':{
                                'id':'filters-select-drop',
                                'options':[{'label':"Select",'value':"Select"},{'label':"Drop",'value':"Drop"}],
                                'value':filters_data['filters'][in_k]['select_drop'],
                                'style':{"width":"50%"}
                            },
                            'type':'Dropdown',
                            'namespace':'dash_core_components'
                        }
                    ]},
                    'type': 'FormGroup',
                    'namespace': 'dash_bootstrap_components'
                },


                {
                    'props':{'children':
                        {
                            'props':{'children':"Where"},
                            'type':'Label',
                            'namespace':'dash_html_components'
                        }
                    },
                    'type':'FormGroup',
                    'namespace':'dash_bootstrap_components'
                },

                {
                    'props':{'children':fil_condition_rows,'id':'filters-conditional-div'},
                    'type':'Div',
                    'namespace':'dash_html_components'
                },

                {
                    'props':{'children':{
                        'props':{"children":{
                            'props':{
                                'children':'add condition',
                                'size':'sm',
                                'id':'filters-add-condition',
                                'n_clicks':0
                            },
                            'type':'Button',
                            'namespace':'dash_bootstrap_components'
                        }},
                        'type':'Col',
                        'namespace':'dash_bootstrap_components'
                    }},
                    'type':'Row',
                    'namespace':'dash_bootstrap_components'
                }
            ]
        }
        let add_col_rows=[]
        if (Object.entries(filters_data['add_new_col']).length != 0) {
            let in_kk = Object.keys(filters_data["add_new_col"])[0]

            for (i in filters_data['add_new_col'][in_kk]['index']) {
                add_col_grp1 = {
                    'props':{
                        'children':[
                            {
                                'props':{
                                    'children':{
                                        'props':{
                                            'children':{
                                                'props':{
                                                    'className':"fa fa-trash"
                                                },
                                                'type':'I',
                                                'namespace':'dash_html_components'
                                            },
                                            'id':{'type':'add-col-remove','index':filters_data['add_new_col'][in_kk]['index'][i]}
                                        },
                                        'type':'A',
                                        'namespace':'dash_html_components'
                                    },
                                    'className':"text-right"
                                },
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            },

                            {
                                'props':{"children":"Enter column name"},
                                'type':'Label',
                                'namespace':'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{"type":"add-new-col-name","index":filters_data['add_new_col'][in_kk]['index'][i]},
                                    'type':"text",
                                    'minLength':5,
                                    'required':true,
                                    'value':filters_data['add_new_col'][in_kk]['col_names'][i]
                                },
                                'type':'Input',
                                'namespace':'dash_core_components'
                            },

                            {
                                'props':{
                                    "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
                                    'color':"secondary"
                                },
                                'type':'FormText',
                                'namespace':'dash_bootstrap_components'
                            },
                        ],
                        'id':{"type":'add-col-grp-1','index':filters_data['add_new_col'][in_kk]['index'][i]}
                    },
                    'type':'FormGroup',
                    'namespace':'dash_bootstrap_components'
                }
                add_col_grp2 = {
                    'props':{
                        'children':[
                            {
                                'props':{'children':"Assign value to new column"},
                                'type':'Label',
                                'namespace':'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{"type":'add-col-value-input',"index":filters_data['add_new_col'][in_kk]['index'][i]},
                                    'type':'text',
                                    'required':true,
                                    'value':filters_data['add_new_col'][in_kk]['col_input'][i]
                                },
                                'type':'Input',
                                'namespace':'dash_core_components'
                            }
                        ],
                        'id':{"type":'add-col-grp-2','index':filters_data['add_new_col'][in_kk]['index'][i]}
                    },
                    'type':'FormGroup',
                    'namespace':'dash_bootstrap_components'
                }
                add_col_hr3 = {
                    'props':{'children':null},
                    'type':'Hr',
                    'namespace':'dash_html_components'
                } 

                add_col_rows.push(add_col_grp1)
                add_col_rows.push(add_col_grp2)
                add_col_rows.push(add_col_hr3)
            }

            add_col_div =  [
                {
                    'props':{
                        'children':add_col_rows,
                        'id':"add-col-form"
                    },
                    'type':'Form',
                    'namespace':'dash_bootstrap_components'
                },

                {
                    'props':{'children':null},
                    'type':'Hr',
                    'namespace':'dash_html_components'
                },

                {
                    'props':{
                        'children':{
                            'props':{
                                'children':{
                                    'props':{
                                        'children':"Add column",
                                        'id':"add-col-new-col-but"
                                    },
                                    'type':'Button',
                                    'namespace':'dash_html_components'
                                }
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        }
                    },
                    'type':'Row',
                    'namespace':'dash_bootstrap_components'
                }
            ]

        }

        if (add_col_rows.length > 0 && fil_div.length > 0) {
            return [fil_div, add_col_div]
        } else if (add_col_rows.length == 0 && fil_div.length > 0) {
            return [fil_div, empty_div_add]
        } else if (add_col_rows.length > 0 && fil_div.length == 0) {
            return [empty_div, add_col_div]
        }
    
    } else if (triggered.includes('filters-data.data') && Object.entries(filters_data['filters']).length == 0
        && filters_data['status'] == true) {

        let add_col_rows = []
        let add_col_div=[]

        if (Object.entries(filters_data['add_new_col']).length > 0) {
            let in_kk=Object.keys(filters_data["add_new_col"])[0]

            for (i in filters_data['add_new_col'][in_kk]['index']) {
                add_col_grp1 = {
                    'props':{
                        'children':[
                            {
                                'props':{
                                    'children':{
                                        'props':{
                                            'children':{
                                                'props':{
                                                    'className':"fa fa-trash"
                                                },
                                                'type':'I',
                                                'namespace':'dash_html_components'
                                            },
                                            'id':{'type':'add-col-remove','index':filters_data['add_new_col'][in_kk]['index'][i]}
                                        },
                                        'type':'A',
                                        'namespace':'dash_html_components'
                                    },
                                    'className':"text-right"
                                },
                                'type':'Col',
                                'namespace':'dash_bootstrap_components'
                            },

                            {
                                'props':{"children":"Enter column name"},
                                'type':'Label',
                                'namespace':'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{"type":"add-new-col-name","index":filters_data['add_new_col'][in_kk]['index'][i]},
                                    'type':"text",
                                    'minLength':5,
                                    'required':true,
                                    'value':filters_data['add_new_col'][in_kk]['col_names'][i]
                                },
                                'type':'Input',
                                'namespace':'dash_core_components'
                            },

                            {
                                'props':{
                                    "children":"Type column name without any spaces, special characters. Except 'underscore '_''",
                                    'color':"secondary"
                                },
                                'type':'FormText',
                                'namespace':'dash_bootstrap_components'
                            },
                        ],
                        'id':{"type":'add-col-grp-1','index':filters_data['add_new_col'][in_kk]['index'][i]}
                    },
                    'type':'FormGroup',
                    'namespace':'dash_bootstrap_components'
                }
                add_col_grp2 = {
                    'props':{
                        'children':[
                            {
                                'props':{'children':"Assign value to new column"},
                                'type':'Label',
                                'namespace':'dash_html_components'
                            },

                            {
                                'props':{
                                    'id':{"type":'add-col-value-input',"index":filters_data['add_new_col'][in_kk]['index'][i]},
                                    'type':'text',
                                    'required':true,
                                    'value':filters_data['add_new_col'][in_kk]['col_input'][i]
                                },
                                'type':'Input',
                                'namespace':'dash_core_components'
                            }
                        ],
                        'id':{"type":'add-col-grp-2','index':filters_data['add_new_col'][in_kk]['index'][i]}
                    },
                    'type':'FormGroup',
                    'namespace':'dash_bootstrap_components'
                }
                add_col_hr3 = {
                    'props':{'children':null},
                    'type':'Hr',
                    'namespace':'dash_html_components'
                } 

                add_col_rows.push(add_col_grp1)
                add_col_rows.push(add_col_grp2)
                add_col_rows.push(add_col_hr3)
            }
            add_col_div =  [
                {
                    'props':{
                        'children':add_col_rows,
                        'id':"add-col-form"
                    },
                    'type':'Form',
                    'namespace':'dash_bootstrap_components'
                },

                {
                    'props':{'children':null},
                    'type':'Hr',
                    'namespace':'dash_html_components'
                },

                {
                    'props':{
                        'children':{
                            'props':{
                                'children':{
                                    'props':{
                                        'children':"Add column",
                                        'id':"add-col-new-col-but"
                                    },
                                    'type':'Button',
                                    'namespace':'dash_html_components'
                                }
                            },
                            'type':'Col',
                            'namespace':'dash_bootstrap_components'
                        }
                    },
                    'type':'Row',
                    'namespace':'dash_bootstrap_components'
                }
            ]
        }

        if (add_col_rows.length > 0) {
            return [empty_div, add_col_div]
        } else {
            return [empty_div, empty_div_add]
        }
    } else {
        window.dash_clientside.no_update
    }
}