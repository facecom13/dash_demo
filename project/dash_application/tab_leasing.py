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
                                    dcc.Dropdown(
                                        multi=True,
                                        placeholder="Статус договора...",
                                        id='agreement_status_select',
                                        # optionHeight=50,
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
                                                                             html.Div(style={'margin-top': '10px'},
                                                                                      id='leasing_payments_by_month'),

                                                                         ]
                                                                     )
                                                                 ),
                                                             ]
                                                             ),


                                                    html.Div(style={'margin-top': '10px'},
                                                             id='leasing_payments_errors'),
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
                                                                                html.Div(id='leasing_payments_pie_chart'),
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
                                    dcc.Dropdown(
                                        multi=True,
                                        placeholder="Год...",
                                        id='top_customers_year_select',
                                        # optionHeight=50,
                                    ),
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
                                                                                 html.Div(style={'margin-top': '10px'},
                                                                                          id='top_group_customers_barchart'),

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
                                                                                         id='top_independent_customers_barchart'),
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


        ]
    )


    return tab_leasing