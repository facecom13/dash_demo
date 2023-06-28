import dash_bootstrap_components as dbc
from dash import html, dcc
import datetime
def settings_content():
    settings_data = html.Div(
        style={
            'marginTop': '10px',
        },
        children=[
            html.Div(style={'margin-top': '10px'},
                     children=[dbc.Button(
                         "Cоздать демо-данные", id='create_demo_data_button', outline=True, color="secondary",
                         className="me-1"
                     ), ]
                     ),

            html.Div(id='create_demo_data_info'),


            # html.Div(style={'margin-top': '10px'},
            #          children=[dbc.Button(
            #              "reload table", id='reload_leasing_table', outline=True, color="secondary",
            #              className="me-1"
            #          ), ]
            #          ),

            # html.Div(style={'margin-top': '10px'},
            #          children=[dbc.Button(
            #              "reload demo tables", id='reload_demo_tables_button', outline=True, color="secondary",
            #              className="me-1"
            #          ), ]
            #          ),
            #
            # html.Div(style={'margin-top': '10px'},
            #          children=[dbc.Button(
            #              "set categories", id='set_categories_button', outline=True, color="secondary",
            #              className="me-1"
            #          ), ]
            #          ),
            #
            # html.Div(style={'margin-top': '10px'},
            #          children=[dbc.Button(
            #              "set data", id='set_data_button', outline=True, color="secondary",
            #              className="me-1"
            #          ), ]
            #          ),
            #
            # # html.I(className="fas fas fa-sign-out-alt"),  # Font Awesome icon
            #
            # html.Div(id='set_data_info'),
            #
            # html.Div(id='set_categories_info'),
            #
            # html.Div(id='reload_demo_tables_info'),
            #
            # html.Div(id='leasing_data_short_info'),
            #
            # dcc.Loading(
            # html.Div(style={'margin-top': '10px', 'display':'None'},
            #          id='reload_leasing_tables_button_output'
            #
            # )),


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
            # html.Div(id='logged_in_check'),
            #
            # html.Div(id='credit_limit_remainings_check'),
            # html.Div(id='taken_vs_remain_v2_func_check'),
            # html.Div(id='create_leasing_data_table_check'),
            # dcc.Loading(
            #     html.Div(id='create_credit_data_table_check')
            # )








        ])
    return settings_data