import dash_bootstrap_components as dbc
import datetime
from dash import html, dcc
import plotly.graph_objs as go

def customers_tab_content():
    customers_tab = html.Div(
            style={
                'marginTop': '10px',
            },
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
                                                                    placeholder="Продуктовая категория...",
                                                                    id='product_category_select',

                                                                    optionHeight=50,
                                                                    style={
                                                                        "font-size": "small"},
                                                                ),
                                                                html.Div(
                                                                    id='product_category_select_error_message')
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
                                                                    placeholder="Оборот...",
                                                                    id='revenue_range_select',

                                                                    optionHeight=50,
                                                                    style={
                                                                        "font-size": "small"},
                                                                ),
                                                                html.Div(
                                                                    # id='credit_line_type_select_error_message'
                                                                )
                                                            ]
                                                        ),

                                                    ]
                                                ),

                                            ]
                                            ),
                                    # dbc.Col(md=2,
                                    #         children=[
                                    #             html.Div(style={'display': 'inline-block'},
                                    #                      children=[
                                    #                          dbc.Button(
                                    #                              "Excel",
                                    #                              # id='credit_by_bank_download_button',
                                    #                              color="secondary",
                                    #                              className="me-1"),
                                    #                      ]
                                    #                      )
                                    #         ])
                                ]
                            ),



                        ]

                    ),
                    className="mt-3",
                    style={'background-color': '#f8f8f8'}
                ),



                dbc.Row(
                    dbc.Col(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            children=[
                                                dbc.Col(
                                                    children=[

                                                        dcc.Loading(
                                                            html.Div(id='customer_map')
                                                        ),
                                                        html.Div(id = 'customer_map_check'),

                                                    ]
                                                )
                                            ]

                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ),



            ]
        )


    return customers_tab




