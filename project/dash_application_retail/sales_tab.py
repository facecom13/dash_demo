import dash_bootstrap_components as dbc
from flask_login import LoginManager, current_user

from dash import html, dcc
def sales_tab_content():
    sales_tab = html.Div(
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
                                                                id='sales_tab_product_category_select',

                                                                optionHeight=50,
                                                                style={
                                                                    "font-size": "small"},
                                                            ),
                                                            html.Div(
                                                                id='sales_tab_product_category_select_error_message')
                                                        ]
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
                                                        html.Div(id='sales_accumulative_year')
                                                    ),
                                                    html.Div(id='sales_accumulative_year_check'),
                                                    # html.Div(f"User ID: {current_user.id if current_user.is_authenticated else 'Not logged in'}")

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

    return sales_tab