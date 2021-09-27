function asdasd (adas) {
    [
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
                            'required':True
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
                            'required':True
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
            'props':{'children':None},
            'type':'Hr',
            'namespace':'dash_html_components'
        }
    ]
}