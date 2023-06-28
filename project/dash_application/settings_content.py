import dash_bootstrap_components as dbc
from dash import html, dcc
import datetime
def settings_content():
    settings_data = html.Div(
        style={
            'marginTop': '10px',
        },
        children=[
            html.Div(style={'margin': '10px'},
                children=[
                    dbc.Alert("Нет данных",
                              color="danger",
                              id="alert_settings_nodata",
                              dismissable=True,
                              # fade=False,
                              is_open=False,
                              ),
                ]
            ),
            html.Div(style={'display':'none'},
                children=[
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.RadioItems(style={"margin-left": "20px"},
                                               options=[
                                                   {"label": "1C API", "value": "1с_api"},
                                                   {"label": "Excel demo", "value": "demo"},

                                                   # {"label": "1C API (credit endpoint)", "value": "prod_credit_api"},
                                               ],
                                               value="1с_api",

                                               id="data_input",
                                               ),
                                html.Div(style={'display': 'none'},
                                         children=[
                                             dcc.DatePickerRange(
                                                 id='data_daterange',
                                                 # min_date_allowed=date(1995, 8, 5),
                                                 # max_date_allowed=date(2017, 9, 19),
                                                 initial_visible_month=datetime.datetime.now(),
                                                 display_format='DD.MM.Y',
                                                 clearable=True,
                                                 start_date=datetime.date(2023, 1, 1),
                                                 end_date=datetime.date(2028, 12, 31)
                                             ),

                                         ]
                                         ),
                                html.Div(style={'margin-top': '10px', 'display': 'none'},
                                         children=[
                                             dbc.Button(
                                                 "Применить", id="update", outline=True, color="secondary",
                                                 className="me-1"
                                             ),
                                         ]
                                         ),

                                html.Div(id='1c_api_div', style={'display': 'none', 'margin': '10px'},
                                         children=[
                                             dbc.Input(id="1c_endpoint_url", placeholder="1c_endpoint_url...",
                                                       type="text"),
                                             html.Div(style={'margin-top': '10px'},
                                                      children=[dbc.Button(
                                                          "Connect to 1C endpoint", id='connect_to_1C', outline=True,
                                                          color="secondary", className="me-1"
                                                      ), ]
                                                      ),

                                         ]
                                         )
                            ]
                        ),
                        className="mt-3",
                    ),
                ]
            ),

            html.Div(
                id='message'
            ),

            html.Div(style={'margin-top': '10px'},
                     children=[dbc.Button(
                         "reload table", id='reload_leasing_table', outline=True, color="secondary",
                         className="me-1"
                     ), ]
                     ),

            html.Div(style={'margin-top': '10px'},
                     children=[dbc.Button(
                         "reload demo tables", id='reload_demo_tables_button', outline=True, color="secondary",
                         className="me-1"
                     ), ]
                     ),

            html.Div(style={'margin-top': '10px'},
                     children=[dbc.Button(
                         "set categories", id='set_categories_button', outline=True, color="secondary",
                         className="me-1"
                     ), ]
                     ),

            html.Div(style={'margin-top': '10px'},
                     children=[dbc.Button(
                         "set data", id='set_data_button', outline=True, color="secondary",
                         className="me-1"
                     ), ]
                     ),

            # html.I(className="fas fas fa-sign-out-alt"),  # Font Awesome icon

            html.Div(id='set_data_info'),

            html.Div(id='set_categories_info'),

            html.Div(id='reload_demo_tables_info'),

            html.Div(id='leasing_data_short_info'),

            dcc.Loading(
            html.Div(style={'margin-top': '10px', 'display':'None'},
                     id='reload_leasing_tables_button_output'

            )),


            # dcc.Loading(
            # html.Div(
            #     id='output_leasing_request_to_bd'
            # )),


            # html.Div(
            #     id='output_16'
            # ),
            # html.Div(
            #     id='leasing_payments_pie_chart_v2_div_temp_output'
            # ),



            # dcc.Loading(
            #     html.Div(id='create_leasing_tables_output_div')
            # ),



            # html.Div(id='credit_limit_check'),

            # html.Div(id='credit_avrate_check'),
            html.Div(id='logged_in_check'),

            html.Div(id='credit_limit_remainings_check'),
            html.Div(id='taken_vs_remain_v2_func_check'),
            html.Div(id='create_leasing_data_table_check'),
            dcc.Loading(
                html.Div(id='create_credit_data_table_check')
            )








        ])
    return settings_data