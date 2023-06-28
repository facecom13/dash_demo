import datetime

from dash import dcc, html
import dash_bootstrap_components as dbc



def credit_tab_content():
    loading_style_low_cards = {'position': 'absolute','left':'400px', 'top':'50vw'}
    tab_credit = html.Div(
        style={
            'marginTop': '10px',
        },
        children=[
            html.Div(style={'marginTop': '10px', },
                     children=[
                         dbc.Row(
                             [
                                 dbc.Col(
                                     children=[
                                         # блок с фильтрами
                                         dbc.Card(
                                             dbc.CardBody(
                                                 children=[
                                                     dbc.Row(
                                                         [
                                                             dbc.Col(md=5,
                                                                     children=[
                                                                         html.Div(style={
                                                                         #    'display':'inline-block'
                                                                         },
                                                                             children=[
                                                                                 html.Div(style={
                                                                                 # 'display':'None'
                                                                                 },
                                                                                     children=[
                                                                                         dcc.Dropdown(
                                                                                             multi=True,
                                                                                             placeholder="Кредитор...",
                                                                                             id='transhi_i_crediti_block_creditor_select',

                                                                                             optionHeight=50,
                                                                                             style={
                                                                                                 "font-size": "small"},
                                                                                         ),
                                                                                         html.Div(id='transhi_i_crediti_block_creditor_select_options_error_message')
                                                                                     ]
                                                                                 ),

                                                                             ]
                                                                         ),


                                                                     ]
                                                                     ),
                                                             dbc.Col(md=5,
                                                                     children=[
                                                                         html.Div(style={
                                                                             #    'display':'inline-block'
                                                                         },
                                                                             children=[
                                                                                 html.Div(style={
                                                                                     # 'display':'None'
                                                                                 },
                                                                                     children=[
                                                                                         dcc.Dropdown(
                                                                                             multi=True,
                                                                                             placeholder="Тип линии...",
                                                                                             id='credit_line_type_select',

                                                                                             optionHeight=50,
                                                                                             style={
                                                                                                 "font-size": "small"},
                                                                                         ),
                                                                                         html.Div(
                                                                                             id='credit_line_type_select_error_message')
                                                                                     ]
                                                                                 ),

                                                                             ]
                                                                         ),

                                                                     ]
                                                                     ),
                                                             dbc.Col(md=2,
                                                                     children=[
                                                                         html.Div(style={'display': 'inline-block'},
                                                                                  children=[
                                                                                      dbc.Button(
                                                                                          "Excel",
                                                                                          id='credit_by_bank_download_button',
                                                                                          color="secondary",
                                                                                          className="me-1"),
                                                                                  ]
                                                                                  )
                                                                     ])
                                                         ]
                                                     ),


                                                             dbc.Row(
                                                                 [
                                                                     dbc.Col(md=4,
                                                                             children=[
                                                                                 html.Div(style={'marginTop': '10px', },
                                                                                          children=[
                                                                                              dbc.Card(
                                                                                                  children=[
                                                                                                      dbc.CardBody(
                                                                                                          style={
                                                                                                              'padding-bottom': '0px'},
                                                                                                          children=[
                                                                                                              html.Div(
                                                                                                                  html.P(
                                                                                                                      'Кредитный портфель:'),
                                                                                                                  style={
                                                                                                                      "display": "inline-block",
                                                                                                                      'fontWeight': 'bold',
                                                                                                                      'fontSize': '20px'}),
                                                                                                          ]

                                                                                                          ),
                                                                                                      dbc.CardBody(
                                                                                                          style={
                                                                                                              'padding-top': '0px',
                                                                                                              'padding-bottom': '0px'},
                                                                                                          children=[
                                                                                                              dcc.Loading(
                                                                                                              html.Div(
                                                                                                                  style={
                                                                                                                      "display": "inline-block",
                                                                                                                      # "width": "20%"
                                                                                                                  },
                                                                                                                  children=[

                                                                                                                          html.Div(
                                                                                                                              id='credit_totals_by_today',

                                                                                                                              style={
                                                                                                                                  "display": "inline-block",
                                                                                                                                  # 'fontWeight': 'bold',
                                                                                                                                  'fontSize': '50px',
                                                                                                                                  # 'color': '#FFC000',
                                                                                                                                  'color': '#32935F',
                                                                                                                                  'marginLeft': '7px'}),


                                                                                                                      html.Div(
                                                                                                                          html.P(
                                                                                                                              f'млрд'),
                                                                                                                          style={
                                                                                                                              "display": "inline-block",
                                                                                                                              # 'fontWeight': 'bold',
                                                                                                                              'fontSize': '15px',
                                                                                                                              # 'color': '#FFC000',
                                                                                                                              'color': '#32935F',
                                                                                                                              'marginLeft': '3px'}),
                                                                                                                  ]
                                                                                                              )),
                                                                                                          ]

                                                                                                          ),
                                                                                                      html.Div(
                                                                                                          style={
                                                                                                              'fontSize': '10px',
                                                                                                              'color': 'grey',
                                                                                                              'margin-left': '20px'},
                                                                                                          id='credit_totals_by_today_below_text'

                                                                                                      )
                                                                                                  ]

                                                                                              ),
                                                                                          ]
                                                                                          ),

                                                                             ]
                                                                             ),
                                                                     dbc.Col(md=4,
                                                                             children=[
                                                                                 html.Div(style={'marginTop': '10px', },
                                                                                          children=[
                                                                                              dbc.Card(
                                                                                                  children=[
                                                                                                      dbc.CardBody(
                                                                                                          style={
                                                                                                              'padding-bottom': '0px', },
                                                                                                          children=[
                                                                                                              html.Div(
                                                                                                                  html.P(
                                                                                                                      f'Привлечено в {datetime.datetime.now().year} г.:'),
                                                                                                                  style={
                                                                                                                      "display": "inline-block",
                                                                                                                      'fontWeight': 'bold',
                                                                                                                      'fontSize': '20px'}),
                                                                                                          ]

                                                                                                      ),
                                                                                                      dbc.CardBody(
                                                                                                          style={
                                                                                                              'padding-top': '0px',
                                                                                                              'padding-bottom': '0px'},
                                                                                                          children=[
                                                                                                              dcc.Loading(
                                                                                                              html.Div(
                                                                                                                  style={
                                                                                                                      "display": "inline-block",
                                                                                                                      # "width": "20%"
                                                                                                                  },
                                                                                                                  children=[

                                                                                                                          html.Div(
                                                                                                                              id='credit_taken_by_today',

                                                                                                                              style={
                                                                                                                                  "display": "inline-block",
                                                                                                                                  # 'fontWeight': 'bold',
                                                                                                                                  'fontSize': '50px',
                                                                                                                                  'color': '#32935F',
                                                                                                                                  'marginLeft': '7px'}),

                                                                                                                      html.Div(
                                                                                                                          html.P(
                                                                                                                              f'млрд'),
                                                                                                                          style={
                                                                                                                              "display": "inline-block",
                                                                                                                              # 'fontWeight': 'bold',
                                                                                                                              'fontSize': '15px',
                                                                                                                              'color': '#32935F',
                                                                                                                              'marginLeft': '3px'}),
                                                                                                                  ]
                                                                                                              )),
                                                                                                          ]

                                                                                                      ),
                                                                                                      html.Div(style={
                                                                                                          'fontSize': '10px',
                                                                                                          'color': 'grey',
                                                                                                          'margin-left': '20px'},
                                                                                                               id='credit_taken_by_today_below_text'

                                                                                                               )

                                                                                                  ]

                                                                                              ),
                                                                                          ]
                                                                                          ),

                                                                             ]
                                                                             ),
                                                                     dbc.Col(md=4,
                                                                             children=[
                                                                                 html.Div(style={'marginTop': '10px', },
                                                                                          children=[
                                                                                              dbc.Card(
                                                                                                  children=[
                                                                                                      dbc.CardBody(
                                                                                                          style={
                                                                                                              'padding-bottom': '0px', },
                                                                                                          children=[
                                                                                                              html.Div(
                                                                                                                  html.P(
                                                                                                                      'Свободный остаток:'),
                                                                                                                  style={
                                                                                                                      "display": "inline-block",
                                                                                                                      'fontWeight': 'bold',
                                                                                                                      'fontSize': '20px'}),
                                                                                                          ]

                                                                                                      ),
                                                                                                      dbc.CardBody(
                                                                                                          style={
                                                                                                              'padding-top': '0px',
                                                                                                              'padding-bottom': '0px'},
                                                                                                          children=[
                                                                                                              dcc.Loading(
                                                                                                              html.Div(
                                                                                                                  style={
                                                                                                                      "display": "inline-block",
                                                                                                                      # "width": "20%"
                                                                                                                  },
                                                                                                                  children=[

                                                                                                                          html.Div(
                                                                                                                              id='credit_limit_remain_by_today',

                                                                                                                              style={
                                                                                                                                  "display": "inline-block",
                                                                                                                                  # 'fontWeight': 'bold',
                                                                                                                                  'fontSize': '50px',
                                                                                                                                  'color': '#32935F',
                                                                                                                                  'marginLeft': '7px'}),


                                                                                                                      html.Div(
                                                                                                                          html.P(
                                                                                                                              f'млрд'),
                                                                                                                          style={
                                                                                                                              "display": "inline-block",
                                                                                                                              # 'fontWeight': 'bold',
                                                                                                                              'fontSize': '15px',
                                                                                                                              'color': '#32935F',
                                                                                                                              'marginLeft': '3px'}),
                                                                                                                  ]
                                                                                                              )),
                                                                                                          ]

                                                                                                      ),
                                                                                                      html.Div(
                                                                                                          style={
                                                                                                              'fontSize': '10px',
                                                                                                              'color': 'grey',
                                                                                                              'margin-left': '20px'},
                                                                                                          id='credit_limit_remain_by_today_below_text'

                                                                                                      )

                                                                                                  ]

                                                                                              ),
                                                                                          ]
                                                                                          ),

                                                                             ]
                                                                             ),

                                                                 ]

                                                             ),
                                                             dbc.Row(
                                                                 [
                                                                     dbc.Col(
                                                                         children=[
                                                                             dbc.Card(
                                                                                 dbc.CardBody(
                                                                                     children=[
                                                                                         html.Div(
                                                                                             style={
                                                                                                 'marginTop': '10px', },
                                                                                             children=[
                                                                                                 html.H4(
                                                                                                     'Транши и лимиты',
                                                                                                     className='custom_H4',
                                                                                                     ),
                                                                                                 dcc.Loading(
                                                                                                     html.Div(
                                                                                                         id='taken_vs_remain_graph_div')
                                                                                                 ),
                                                                                                 dcc.Loading(
                                                                                                     html.Div(
                                                                                                         id='taken_vs_remain_graph_v2_div')
                                                                                                 ),

                                                                                             ]
                                                                                         )
                                                                                     ]

                                                                                 ),
                                                                                 className="mt-3", )
                                                                         ]
                                                                     ),
                                                                 ]

                                                             ),

                                                 ]

                                             ),
                                             className="mt-3",
                                             style={'background-color': '#f8f8f8'}
                                         )

                                     ]
                                 )
                             ]
                         ),
                     ]
                     ),
            dbc.Card(

                dbc.CardBody(
                    [
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        html.Div(style={'fontColor': 'blue'},
                                                 children=[
                                                     dcc.Dropdown(
                                                         multi=True,
                                                         placeholder="Кредитор...",
                                                         id='creditor_select',
                                                         style={"font-size": "small"},
                                                         # optionHeight=50,
                                                     ),
                                                 ]),
                                        html.Div(id='creditor_select_error_message')
                                    ]


                                ),

                                dbc.Col(
                                    children=[
                                        dcc.Dropdown(
                                            # options
                                            multi=True,
                                            placeholder="Кредитный договор...",
                                            id='credit_contract_select',
                                            optionHeight=80,
                                            style={"font-size": "small"},
                                        ),
                                        html.Div(id='credit_contract_select_error_message')
                                    ]

                                ),
                                dbc.Col(
                                    children=[
                                        html.Div(style={'display':'None'},
                                            children=[
                                                dcc.Dropdown(
                                                    # options=,
                                                    # multi=True,
                                                    placeholder="Год...",
                                                    id='credit_tab_year_select',
                                                    # optionHeight=50,
                                                    style={"font-size": "small"},
                                                ),
                                            ]
                                        ),
                                        dcc.Dropdown(
                                            # options=,
                                            # multi=True,
                                            placeholder="Год...",
                                            id='credit_year_select',
                                            # optionHeight=50,
                                            style={"font-size": "small"},
                                        ),

                                        html.Div(id='credit_tab_year_select_error_message')
                                    ]

                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        # options=,
                                        # multi=True,
                                        placeholder="Квартал...",
                                        id='credit_tab_quarter_select',
                                        # optionHeight=50,
                                        style={"font-size": "small"},
                                    ),
                                ),
                                dbc.Col(
                                    children=[
                                        dcc.Dropdown(
                                            # options=,
                                            # multi=True,
                                            placeholder="Месяц...",
                                            id='credit_tab_month_select',
                                            style={"font-size": "small"},
                                            # optionHeight=50,
                                        ),
                                        html.Div(id='credit_tab_month_select_error_message')
                                    ]

                                )
                            ],



                        ),


                        dbc.Row(
                            [
                                dbc.Col(md=7,
                                        children=[
                                            html.Div(style={'margin-top': '15px'},
                                                     children=[
                                                         dbc.Card(
                                                             dbc.CardBody(
                                                                 children=[
                                                                     html.H4(
                                                                         'Погашение кредитного портфеля по кредиторам',
                                                                         className='custom_H4',
                                                                         ),
                                                                     # DIV с подтекстом периода
                                                                     dcc.Loading(
                                                                         html.Div(
                                                                             children=[
                                                                                 html.Div(
                                                                                     id="treeview_period_text_div"),
                                                                                 html.Div(id='credit_treemap_div')
                                                                             ]
                                                                         )
                                                                     ),


                                                                 ]

                                                             )
                                                         )
                                                     ]

                                                     )
                                        ]

                                        ),
                                #####################################################
                                dbc.Col(md=5,
                                        children=[
                                            html.Div(
                                                ######################### Блок с графиком Средневзвешенная ставка ##############
                                                dbc.Card(
                                                    dbc.CardBody(
                                                        [
                                                            dbc.Row(
                                                                dbc.Col(
                                                                    children=[
                                                                        html.Div(
                                                                            dbc.Row(
                                                                                [
                                                                                    dbc.Col(md=9,
                                                                                            children=[
                                                                                                html.Div(
                                                                                                    children=[
                                                                                                        html.H4(
                                                                                                            'Средневзвешенная ставка',
                                                                                                            className='custom_H4',
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
                                                                                                            id='credit_avrate_download_button',
                                                                                                            color="secondary",
                                                                                                            className="me-1"),
                                                                                                    ]
                                                                                                )

                                                                                            ]

                                                                                            ),
                                                                                ],

                                                                            )
                                                                        ),

                                                                        html.Div(
                                                                            id="credit_av_rate_text_div"),
                                                                    ])
                                                            ),
                                                            dcc.Loading(
                                                                html.Div(id='credit_av_rate_graph_div'),
                                                            ),

                                                            # dcc.Graph(id="credit_av_rate_graph", config = {'displayModeBar': False}),
                                                        ]
                                                    ),
                                                    className="mt-3",
                                                ),
                                            )
                                        ]
                                        ),
                            ]

                        ),

                    ]
                ),
                className="mt-3",
                style={'background-color': '#f8f8f8'}
            ),



            dbc.Row(
                [
                    dbc.Col(md=6,
                        children=[
                            html.Div(
                                ######################### Блок с графиком Сумма остатка ##############
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                dbc.Col(
                                                [
                                                    html.H4('Сумма долга',
                                                            className='custom_H4',
                                                            ),
                                                    html.Div(id='remains_bar_chart_period_text'),
                                                ]

                                                )
                                            ),
                                            dbc.Button('🡠 Назад', id='back-button',
                                                       outline=True,
                                                       color="secondary",
                                                       size="sm",
                                                       # className='mt-2 ml-2 col-1',
                                                       style={'display': 'none'}
                                                       ),
                                            dcc.Loading(
                                                dcc.Graph(id="credit_remainings_bar_graph",
                                                          config={'displayModeBar': False})
                                            ),

                                        ]
                                    ),
                                    className="mt-3",
                                ),
                            )
                        ]
                    ),
                    dbc.Col(md=6,
                            children=[
                                html.Div(
                                    ######################### Блок с графиком Сумма остатка Pie chart ##############
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    dbc.Col(
                                                        [
                                                            html.H4('Структура кредитного портфеля',
                                                                    className='custom_H4',
                                                                    ),
                                                            html.Div(id='period_text_piechart'),
                                                        ]

                                                    )
                                                ),
                                                dcc.Loading(
                                                    html.Div(id="credit_remainings_piechart_graph"),

                                                ),

                                            ]
                                        ),
                                        className="mt-3",
                                    ),
                                )
                            ]
                            ),

                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        # md=7,
                        children=[
                            html.Div(style={"min-width": "450px", },
                                     children=[
                                         # блок с графиком Погашение кредитного портфеля
                                         dbc.Card(
                                             dbc.CardBody(
                                                 [
                                                     html.Div(
                                                         children=[
                                                             dbc.Row(
                                                                 children=[
                                                                     dbc.Col(
                                                                         md=4,
                                                                         children=[
                                                                             html.Div(
                                                                                 children=[
                                                                                     dbc.RadioItems(
                                                                                         id="year_month_selector",
                                                                                         className="btn-group",
                                                                                         inputClassName="btn-check",
                                                                                         labelClassName="btn btn-outline-secondary",
                                                                                         labelCheckedClassName="active",
                                                                                         options=[
                                                                                             {
                                                                                                 "label": "Месяцы",
                                                                                                 "value": "month"},
                                                                                             {
                                                                                                 "label": "Годы",
                                                                                                 "value": "years"},
                                                                                         ],
                                                                                         value="month",
                                                                                     )
                                                                                 ]

                                                                             ),
                                                                         ]
                                                                     ),
                                                                     dbc.Col(
                                                                         md=6,
                                                                         children=[
                                                                             html.Div(
                                                                                 children=[
                                                                                     html.H4(
                                                                                         "Погашение кредитного портфеля",
                                                                                         className='custom_H4',
                                                                                         # style={'display': 'inline'}
                                                                                     ),
                                                                                     html.Div(
                                                                                         id='credit_grapf_period_text_div'),

                                                                                 ]

                                                                             ),

                                                                         ]
                                                                     ),
                                                                     dbc.Col(
                                                                         md=2,
                                                                         children=[
                                                                             html.Div(
                                                                                 children=[
                                                                                     dbc.Button(
                                                                                         "Excel",
                                                                                         id='btn_download_month_to_excel',
                                                                                         outline=True,
                                                                                         color="secondary",
                                                                                         className="me-1"
                                                                                     ),
                                                                                     dcc.Loading(
                                                                                         html.Div(
                                                                                             id='download_month_to_excel_loading')
                                                                                     ),


                                                                                 ]

                                                                             ),

                                                                         ]
                                                                     )
                                                                 ],

                                                             ),
                                                         ]),
                                                     dcc.Loading(
                                                         html.Div(
                                                             id="credit_next_payments_by_credittype_div",
                                                         )
                                                     ),

                                                     html.Div(style={'display':'None'},
                                                         children=[
                                                             dcc.RangeSlider(marks=None,
                                                                                 id='credit_grapf_range_slider'),
                                                         ]

                                                     )
                                                 ]
                                             ),
                                             className="mt-3",
                                         ),
                                     ]

                                     )
                        ]
                    ),

                ]
            ),


        ]
    )

    return tab_credit