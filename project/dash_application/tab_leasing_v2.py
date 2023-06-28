import dash_bootstrap_components as dbc

from dash import html, dcc
def tab_leasing_content():
    tab_leasing = html.Div(
        style={
            'marginTop': '10px',
        },
        children=[

            dbc.Row(
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div(style={'display':'None'},
                                        children=[
                                            dcc.Dropdown(
                                                multi=True,
                                                placeholder="Статус договора...",
                                                id='agreement_status_select_v2',
                                                # optionHeight=50,
                                            ),
                                        ]
                                    ),

                                    dbc.Row(
                                        [
                                            dbc.Col(md=8,
                                                children=[
                                                    html.Div(style={'margin-top': '10px'},
                                                             children=[
                                                                 dbc.Card(
                                                                     dbc.CardBody(
                                                                         children=[
                                                                             html.H4(
                                                                                 'Платежи по категориям',
                                                                                 className='custom_H4',
                                                                             ),
                                                                             html.Div(
                                                                                 dbc.Row(
                                                                                     [
                                                                                         dbc.Col(md=9,
                                                                                                 children=[
                                                                                                     html.Div(
                                                                                                         children=[

                                                                                                             dcc.Dropdown(
                                                                                                                 multi=True,
                                                                                                                 placeholder="Год...",
                                                                                                                 id='leasing_payments_by_month_year_select',
                                                                                                                 # optionHeight=50,
                                                                                                             ),
                                                                                                         ]
                                                                                                     )

                                                                                                 ]
                                                                                                 ),
                                                                                         dbc.Col(md=3, style={
                                                                                             # 'text-align': 'right'
                                                                                         },
                                                                                                 children=[
                                                                                                     html.Div(
                                                                                                         children=[
                                                                                                             dbc.Button(
                                                                                                                 "Excel",
                                                                                                                 id='leasing_payments_by_month_download_button',
                                                                                                                 color="secondary",
                                                                                                                 className="me-1"),
                                                                                                         ]
                                                                                                     )

                                                                                                 ]

                                                                                                 ),
                                                                                     ],

                                                                                 )
                                                                             ),
                                                                             html.Small(
                                                                                 id='leasing_payments_by_month_v2_period_text'
                                                                             ),
                                                                             html.Div(style={'margin-top': '10px'},
                                                                                      id='leasing_payments_by_month_v2'),
                                                                             html.Div(id='leasing_payments_by_month_options_error_message'),

                                                                             html.Div(style={'margin-top': '10px'},
                                                                                      id='leasing_data_test_div'),

                                                                         ]
                                                                     )
                                                                 ),
                                                             ]
                                                             ),


                                                    html.Div(style={'margin-top': '10px'},
                                                             id='leasing_payments_errors_v2'),
                                                ]
                                            ),
                                            dbc.Col(md=4,
                                                    children=[
                                                        html.Div(style={'margin-top': '10px'},
                                                            children=[
                                                                dbc.Card(
                                                                    children=[
                                                                        dbc.CardBody(
                                                                            children=[
                                                                                html.H4(
                                                                                    'Структура по категориям',
                                                                                    className='custom_H4',
                                                                                ),
                                                                                html.Div(
                                                                                    dbc.Row(
                                                                                        [
                                                                                            dbc.Col(md=12,
                                                                                                    children=[
                                                                                                        html.Div(
                                                                                                            children=[

                                                                                                                dcc.Dropdown(
                                                                                                                    multi=True,
                                                                                                                    placeholder="Год...",
                                                                                                                    id='leasing_payments_pie_chart_year_select',
                                                                                                                    # optionHeight=50,
                                                                                                                ),
                                                                                                            ]
                                                                                                        )

                                                                                                    ]
                                                                                                    ),

                                                                                        ],

                                                                                    )
                                                                                ),
                                                                                html.Small(
                                                                                    id='leasing_payments_pie_chart_v2_period_text'
                                                                                ),
                                                                                html.Div(id='leasing_payments_pie_chart_v2'),
                                                                                html.Div(id='leasing_payments_pie_chart_year_select_error_message')
                                                                            ]

                                                                        )]),
                                                            ]
                                                        ),



                                                    ]
                                                    )
                                        ]
                                    ),



                                ]
                            ),
                            className="mt-3",
                            style={'background-color': '#f8f8f8'}
                        ),
                    ]
                )
            ),
            ###################   БЛОК ТОП ПО КЛИЕНТАМ ############################
            dbc.Row(
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(md=6,
                                                    children=[
                                                        html.Div(style={'margin-top': '10px'},
                                                                 children=[
                                                                     dbc.Card(
                                                                         dbc.CardBody(
                                                                             children=[
                                                                                 html.H4(
                                                                                     'Группы компаний',
                                                                                     className='custom_H4',
                                                                                 ),
                                                                                 html.Div(
                                                                                     dbc.Row(
                                                                                         [
                                                                                             dbc.Col(md=9,
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[

                                                                                                                 dcc.Dropdown(
                                                                                                                     multi=True,
                                                                                                                     placeholder="Год...",
                                                                                                                     id='top_customers_year_select',
                                                                                                                     # optionHeight=50,
                                                                                                                 ),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]
                                                                                                     ),
                                                                                             dbc.Col(md=3, style={
                                                                                                 # 'text-align': 'right'
                                                                                             },
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[
                                                                                                                 dbc.Button(
                                                                                                                     "Excel",
                                                                                                                     id='top_company_groups_download_button',
                                                                                                                     color="secondary",
                                                                                                                     className="me-1"),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]

                                                                                                     ),
                                                                                         ],

                                                                                     )
                                                                                 ),
                                                                                 html.Small(
                                                                                     id='top_group_customers_barchart_v2_period_text'
                                                                                 ),
                                                                                 html.Div(style={'margin-top': '10px'},
                                                                                          id='top_group_customers_barchart_v2'),
                                                                                 html.Div(id='top_customers_year_select_error_message'),

                                                                             ]
                                                                         )
                                                                     ),
                                                                 ]
                                                                 ),
                                                    ]
                                                    ),
                                            dbc.Col(md=6,
                                                    children=[
                                                        html.Div(style={'margin-top': '10px'},
                                                                 children=[
                                                                     dbc.Card(
                                                                         children=[
                                                                             dbc.CardBody(
                                                                                 children=[
                                                                                     html.H4(
                                                                                         'Независимые компании',
                                                                                         className='custom_H4',
                                                                                     ),
                                                                                     html.Div(
                                                                                         dbc.Row(
                                                                                             [
                                                                                                 dbc.Col(md=9,
                                                                                                         children=[
                                                                                                             html.Div(
                                                                                                                 children=[

                                                                                                                     dcc.Dropdown(
                                                                                                                         multi=True,
                                                                                                                         placeholder="Год...",
                                                                                                                         id='top_independent_customers_year_select',
                                                                                                                         # optionHeight=50,
                                                                                                                     ),
                                                                                                                 ]
                                                                                                             )

                                                                                                         ]
                                                                                                         ),
                                                                                                 dbc.Col(md=3, style={
                                                                                                     # 'text-align': 'right'
                                                                                                 },
                                                                                                         children=[
                                                                                                             html.Div(
                                                                                                                 children=[
                                                                                                                     dbc.Button(
                                                                                                                         "Excel",
                                                                                                                         id='top_independent_company_download_button',
                                                                                                                         color="secondary",
                                                                                                                         className="me-1"),
                                                                                                                 ]
                                                                                                             )

                                                                                                         ]

                                                                                                         ),
                                                                                             ],

                                                                                         )
                                                                                     ),
                                                                                     html.Small(
                                                                                         id='top_independent_customers_barchart_v2_period_text'
                                                                                     ),
                                                                                     dcc.Loading(
                                                                                         html.Div(
                                                                                             id='top_independent_customers_barchart_v2')
                                                                                     ),

                                                                                     html.Div(id='top_independent_customers_year_select_error_message'),
                                                                                 ]

                                                                             )]),
                                                                 ]
                                                                 ),

                                                    ]
                                                    )
                                        ]
                                    ),

                                ]
                            ),
                            className="mt-3",
                            style={'background-color': '#f8f8f8'}
                        ),
                    ]
                )
            ),
            ################### КОНЕЦ БЛОКА ТОП ПО КЛИЕНТАМ #######################

            ###################   БЛОК ПО ПРОДУКТАМ И ТИПАМ ДОГОВОРОВ ############################
            dbc.Row(
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [


                                    dbc.Row(
                                        [
                                            dbc.Col(md=6,
                                                    children=[
                                                        html.Div(style={'margin-top': '10px'},
                                                                 children=[
                                                                     dbc.Card(
                                                                         dbc.CardBody(
                                                                             children=[
                                                                                 html.H4(
                                                                                     'По продуктам',
                                                                                     className='custom_H4',
                                                                                 ),
                                                                                 html.Div(
                                                                                     dbc.Row(
                                                                                         [
                                                                                             dbc.Col(md=9,
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[

                                                                                                                 dcc.Dropdown(
                                                                                                                     multi=True,
                                                                                                                     placeholder="Год...",
                                                                                                                     id='top_products_year_select',
                                                                                                                     # optionHeight=50,
                                                                                                                 ),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]
                                                                                                     ),
                                                                                             dbc.Col(md=3, style={
                                                                                                 # 'text-align': 'right'
                                                                                             },
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[
                                                                                                                 dbc.Button(
                                                                                                                     "Excel",
                                                                                                                     id='top_products_download_button',
                                                                                                                     color="secondary",
                                                                                                                     className="me-1"),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]

                                                                                                     ),
                                                                                         ],

                                                                                     )
                                                                                 ),
                                                                                 html.Small(
                                                                                     id='leasing_products_period_text'
                                                                                 ),
                                                                                 html.Div(style={'margin-top': '10px'},
                                                                                          id='leasing_products_barchart'),
                                                                                 html.Div(id='top_products_year_select_error_message'),

                                                                             ]
                                                                         )
                                                                     ),
                                                                 ]
                                                                 ),
                                                    ]
                                                    ),
                                            dbc.Col(md=6,
                                                    children=[
                                                        html.Div(style={'margin-top': '10px'},
                                                                 children=[
                                                                     dbc.Card(
                                                                         children=[
                                                                             dbc.CardBody(
                                                                                 children=[
                                                                                     html.H4(
                                                                                         'По типу договора',
                                                                                         className='custom_H4',
                                                                                     ),
                                                                                     html.Div(
                                                                                         dbc.Row(
                                                                                             [
                                                                                                 dbc.Col(md=9,
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[
                                                                                                                 dcc.Dropdown(
                                                                                                                     multi=True,
                                                                                                                     placeholder="Год...",
                                                                                                                     id='agreement_type_year_select',
                                                                                                                     # optionHeight=50,

                                                                                                                 ),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]
                                                                                                 ),
                                                                                                 dbc.Col(md=3, style={
                                                                                                     # 'text-align': 'right'
                                                                                                 },
                                                                                                         children=[
                                                                                                             html.Div(
                                                                                                                 children=[
                                                                                                                     dbc.Button(
                                                                                                                         "Excel",
                                                                                                                         id='agreement_type_download_button',
                                                                                                                         color="secondary",
                                                                                                                         className="me-1"),
                                                                                                                 ]
                                                                                                             )

                                                                                                         ]

                                                                                                         ),
                                                                                             ],

                                                                                         )
                                                                                     ),
                                                                                     html.Small(
                                                                                         id='leasing_agreement_type_barchart_period_text'
                                                                                     ),
                                                                                     dcc.Loading(
                                                                                        html.Div(id='leasing_agreement_type_barchart')
                                                                                     ),
                                                                                     html.Div(id='agreement_type_year_select_options_error_message')
                                                                                 ]

                                                                             )]),
                                                                 ]
                                                                 ),

                                                    ]
                                                    )
                                        ]
                                    ),

                                ]
                            ),
                            className="mt-3",
                            style={'background-color': '#f8f8f8'}
                        ),
                    ]
                )
            ),
            ################### КОНЕЦ БЛОКА ПО ПРОДУКТАМ И ТИПАМ ДОГОВОРОВ #######################

            ###################   БЛОК ПО ВИДАМ ВЗАИМОРАСЧЕТОВ И ТИПАМ ПРЕДМЕТА ЛИЗИНГА ############################
            dbc.Row(
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [

                                    dbc.Row(
                                        [
                                            dbc.Col(md=6,
                                                    children=[
                                                        html.Div(style={'margin-top': '10px'},
                                                                 children=[
                                                                     dbc.Card(
                                                                         dbc.CardBody(
                                                                             children=[
                                                                                 html.H4(
                                                                                     'По видам взаиморасчетов',
                                                                                     className='custom_H4',
                                                                                 ),
                                                                                 html.Div(
                                                                                     dbc.Row(
                                                                                         [
                                                                                             dbc.Col(md=9,
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[

                                                                                                                 dcc.Dropdown(
                                                                                                                     multi=True,
                                                                                                                     placeholder="Год...",
                                                                                                                     id='interpayment_type_year_select',
                                                                                                                     # optionHeight=50,
                                                                                                                 ),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]
                                                                                                     ),
                                                                                             dbc.Col(md=3, style={
                                                                                                 # 'text-align': 'right'
                                                                                             },
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[
                                                                                                                 dbc.Button(
                                                                                                                     "Excel",
                                                                                                                     id='interpayment_type_download_button',
                                                                                                                     color="secondary",
                                                                                                                     className="me-1"),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]

                                                                                                     ),
                                                                                         ],

                                                                                     )
                                                                                 ),
                                                                                 html.Small(
                                                                                     id='interpayment_type_period_text'
                                                                                 ),
                                                                                 html.Div(style={'margin-top': '10px'},
                                                                                          id='interpayment_type_barchart'),
                                                                                 html.Div(
                                                                                     id='interpayment_type_year_select_error_message'),

                                                                             ]
                                                                         )
                                                                     ),
                                                                 ]
                                                                 ),
                                                    ]
                                                    ),
                                            dbc.Col(md=6,
                                                    children=[
                                                        html.Div(style={'margin-top': '10px'},
                                                                 children=[
                                                                     dbc.Card(
                                                                         children=[
                                                                             dbc.CardBody(
                                                                                 children=[
                                                                                     html.H4(
                                                                                         'По видам предмета лизинга',
                                                                                         className='custom_H4',
                                                                                     ),
                                                                                     html.Div(
                                                                                         dbc.Row(
                                                                                             [
                                                                                                 dbc.Col(md=9,
                                                                                                         children=[
                                                                                                             html.Div(
                                                                                                                 children=[
                                                                                                                     dcc.Dropdown(
                                                                                                                         multi=True,
                                                                                                                         placeholder="Год...",
                                                                                                                         id='leasing_object_type_year_select',
                                                                                                                         # optionHeight=50,
                                                                                                                     ),
                                                                                                                 ]
                                                                                                             )

                                                                                                         ]
                                                                                                         ),
                                                                                                 dbc.Col(md=3, style={
                                                                                                     # 'text-align': 'right'
                                                                                                 },
                                                                                                         children=[
                                                                                                             html.Div(
                                                                                                                 children=[
                                                                                                                     dbc.Button(
                                                                                                                         "Excel",
                                                                                                                         id='leasing_object_type_download_button',
                                                                                                                         color="secondary",
                                                                                                                         className="me-1"),
                                                                                                                 ]
                                                                                                             )

                                                                                                         ]

                                                                                                         ),
                                                                                             ],

                                                                                         )
                                                                                     ),
                                                                                     html.Small(
                                                                                         id='leasing_object_type_barchart_period_text'
                                                                                     ),
                                                                                     dcc.Loading(
                                                                                         html.Div(
                                                                                             id='leasing_object_type_barchart')
                                                                                     ),
                                                                                     html.Div(
                                                                                         id='leasing_object_type_select_options_error_message')
                                                                                 ]

                                                                             )]),
                                                                 ]
                                                                 ),

                                                    ]
                                                    )
                                        ]
                                    ),

                                ]
                            ),
                            className="mt-3",
                            style={'background-color': '#f8f8f8'}
                        ),
                    ]
                )
            ),
            ################### КОНЕЦ БЛОКА ПО ПРОДУКТАМ И ..... #######################

            ###################   БЛОК ПО ставкам ЛИЗИНГА ############################
            dbc.Row(
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [

                                    dbc.Row(
                                        [
                                            dbc.Col(md=6,
                                                    children=[
                                                        html.Div(style={'margin-top': '10px'},
                                                                 children=[
                                                                     dbc.Card(
                                                                         dbc.CardBody(
                                                                             children=[
                                                                                 html.H4(
                                                                                     'По ставке',
                                                                                     className='custom_H4',
                                                                                 ),
                                                                                 html.Div(
                                                                                     dbc.Row(
                                                                                         [
                                                                                             dbc.Col(md=9,
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[

                                                                                                                 dcc.Dropdown(
                                                                                                                     multi=True,
                                                                                                                     placeholder="Год...",
                                                                                                                     id='leasing_rate_year_select',
                                                                                                                     # optionHeight=50,
                                                                                                                 ),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]
                                                                                                     ),
                                                                                             dbc.Col(md=3, style={
                                                                                                 # 'text-align': 'right'
                                                                                             },
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[
                                                                                                                 dbc.Button(
                                                                                                                     "Excel",
                                                                                                                     id='leasing_rate_download_button',
                                                                                                                     color="secondary",
                                                                                                                     className="me-1"),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]

                                                                                                     ),
                                                                                         ],

                                                                                     )
                                                                                 ),
                                                                                 html.Small(
                                                                                     id='leasing_rate_period_text'
                                                                                 ),
                                                                                 html.Div(style={'margin-top': '10px'},
                                                                                          id='leasing_rate_barchart'),
                                                                                 html.Div(
                                                                                     id='leasing_rate_year_select_error_message'),

                                                                             ]
                                                                         )
                                                                     ),
                                                                 ]
                                                                 ),
                                                    ]
                                                    ),
                                            dbc.Col(md=6,
                                                    children=[
                                                        html.Div(style={'margin-top': '10px'},
                                                                 children=[
                                                                     dbc.Card(
                                                                         dbc.CardBody(
                                                                             children=[
                                                                                 html.H4(
                                                                                     'Ставки лизинга по группам',
                                                                                     className='custom_H4',
                                                                                 ),
                                                                                 html.Div(
                                                                                     dbc.Row(
                                                                                         [
                                                                                             dbc.Col(md=9,
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[

                                                                                                                 dcc.Dropdown(
                                                                                                                     multi=True,
                                                                                                                     placeholder="Год...",
                                                                                                                     id='leasing_rate_distribution_barchart_year_select',
                                                                                                                     # optionHeight=50,
                                                                                                                 ),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]
                                                                                                     ),
                                                                                             dbc.Col(md=3, style={
                                                                                                 # 'text-align': 'right'
                                                                                             },
                                                                                                     children=[
                                                                                                         html.Div(
                                                                                                             children=[
                                                                                                                 dbc.Button(
                                                                                                                     "Excel",
                                                                                                                     id='leasing_rate_distribution_barchart_download_button',
                                                                                                                     color="secondary",
                                                                                                                     className="me-1"),
                                                                                                             ]
                                                                                                         )

                                                                                                     ]

                                                                                                     ),
                                                                                         ],

                                                                                     )
                                                                                 ),
                                                                                 html.Small(
                                                                                     id='leasing_rate_distribution_barchart_period_text'
                                                                                 ),
                                                                                 html.Div(style={'margin-top': '10px'},
                                                                                          id='leasing_rate_distribution_barchart'),
                                                                                 html.Div(
                                                                                     id='leasing_rate_distribution_barchart_year_select_error_message'),

                                                                             ]
                                                                         )
                                                                     ),
                                                                 ]
                                                                 ),
                                                    ]
                                                    ),

                                        ]
                                    ),

                                ]
                            ),
                            className="mt-3",
                            style={'background-color': '#f8f8f8'}
                        ),
                    ]
                )
            ),
            ################### КОНЕЦ БЛОКА  ..... ################################################################
            ################### БЛОК РАСПРЕДЕЛЕНИЕ СТАВОК ###################################
            dbc.Row(
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [

                                            # dbc.Col(md=6,
                                            #         children=[
                                            #             html.Div(style={'margin-top': '10px'},
                                            #                      children=[
                                            #                          dbc.Card(
                                            #                              children=[
                                            #                                  dbc.CardBody(
                                            #                                      children=[
                                            #                                          html.H4(
                                            #                                              'Ставки лизинга распределение',
                                            #                                              className='custom_H4',
                                            #                                          ),
                                            #                                          html.Div(
                                            #                                              dbc.Row(
                                            #                                                  [
                                            #                                                      dbc.Col(md=9,
                                            #                                                              children=[
                                            #                                                                  html.Div(
                                            #                                                                      children=[
                                            #
                                            #                                                                          dcc.Dropdown(
                                            #                                                                              multi=True,
                                            #                                                                              placeholder="Год...",
                                            #                                                                              id='leasing_rate_distribution_density_year_select',
                                            #                                                                              # optionHeight=50,
                                            #                                                                          ),
                                            #                                                                      ]
                                            #                                                                  )
                                            #
                                            #                                                              ]
                                            #                                                              ),
                                            #                                                      dbc.Col(md=3, style={
                                            #                                                          # 'text-align': 'right'
                                            #                                                      },
                                            #                                                              children=[
                                            #                                                                  html.Div(
                                            #                                                                      children=[
                                            #                                                                          dbc.Button(
                                            #                                                                              "Excel",
                                            #                                                                              id='leasing_rate_distribution_density_download_button',
                                            #                                                                              color="secondary",
                                            #                                                                              className="me-1"),
                                            #                                                                      ]
                                            #                                                                  )
                                            #
                                            #                                                              ]
                                            #
                                            #                                                              ),
                                            #                                                  ],
                                            #
                                            #                                              )
                                            #                                          ),
                                            #                                          html.Small(
                                            #                                              id='leasing_rate_distribution_density_period_text'
                                            #                                          ),
                                            #                                          dcc.Loading(
                                            #                                              html.Div(
                                            #                                                  id='leasing_rate_distribution_density')
                                            #                                          ),
                                            #
                                            #                                          html.Div(
                                            #                                              id='leasing_rate_distribution_density_year_select_error_message'),
                                            #                                      ]
                                            #
                                            #                                  )]),
                                            #                      ]
                                            #                      ),
                                            #
                                            #         ]
                                            #         )
                                        ]
                                    ),

                                ]
                            ),
                            className="mt-3",
                            style={'background-color': '#f8f8f8'}
                        ),
                    ]
                )
            ),
            ################### КОНЕЦ БЛОКА РАСПРЕДЕЛЕНИЕ СТАВОК ###################################




        ]
    )


    return tab_leasing