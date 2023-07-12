import datetime
import plotly.graph_objs as go
import json
import os
import xmltodict
import psycopg2
from sqlalchemy import create_engine
from dash import dash_table
import pandas as pd
import dash
from dash import dcc, Input, Output, State
from dash import html, ctx
from pathlib import Path
import dash_bootstrap_components as dbc
import base64
import plotly.express as px
from flask_login import current_user
from dash_bootstrap_templates import load_figure_template
import dash_application.tab_leasing_v2 as tab_leasing_v2
import dash_application.tab_credit as tab_credit
import dash_application.settings_content as settings_content
import dash_application_retail.tab_finance as tab_finance
import dash_application_retail.sales_tab as sales_tab
import dash_application_retail.customers_tab as customers_tab

import dash_application_retail.settings_content_2 as settings_content_2

import dash_application.functions.credit_calendar_to_bd_v3 as credit_calendar_to_bd_v3
import dash_application.demo_data_functions.credit_data_convert as credit_data_convert
import dash_application.demo_data_functions.leasing_data_convert as leasing_data_convert
import dash_application.demo_data_functions.set_salesdata as set_salesdata

import dash_application_retail.finance_tab_dash_objects.resources_and_plans_div as resources_and_plans_div
import dash_application_retail.finance_tab_dash_objects.revenue_treemap_div as revenue_treemap_div
import dash_application_retail.finance_tab_dash_objects.retail_income_by_customers_barchart_div as retail_income_by_customers_barchart_div
import dash_application_retail.finance_tab_dash_objects.managers_sales_bar_graph as managers_sales_bar_graph
import dash_application_retail.finance_tab_dash_objects.managers_by_month_bar as managers_by_month_bar
import dash_application_retail.finance_tab_dash_objects.demo_credit_by_bank_piechart_graph as demo_credit_by_bank_piechart_graph
import dash_application_retail.finance_tab_dash_objects.marketing_cost_div as marketing_cost_div
import dash_application_retail.customers_tab_dash_objects.product_category_select_options as product_category_select_options
import dash_application_retail.customers_tab_dash_objects.revenue_range_select_options as revenue_range_select_options
import dash_application_retail.sales_tab_dash_objects.sales_accumulative_year as sales_accumulative_year
import dash_application_retail.functions.create_demo_data_module as create_demo_data_module

import dash_application_retail.customers_tab_v2 as customers_tab_v2
import sqlalchemy
import numpy as np

import dash_application.dash_objects.period_text as period_text

from dash.exceptions import PreventUpdate

leasing_table = 'leasing_temp_db'
# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
# template_theme1 = "sketchy"
template_theme1 = "flatly"
template_theme2 = "darkly"
# url_theme1 = dbc.themes.SKETCHY
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY
url_theme3 = dbc.themes.LITERA


available_graph_templates: ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark',
                            'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']

templates = ["bootstrap", "minty", "pulse", "flatly", "quartz", "cyborg", "darkly", "vapor",]

load_figure_template(templates)



def create_dash_application_retail(flask_app):
    # dash_app = dash.Dash(server=flask_app, name="Дашборд Росагролизинг", url_base_pathname="/dash/", external_stylesheets=[dbc.themes.CERULEAN])
    # server = dash_app.server
    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
    )
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/demo/", external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css',
        # url_theme2,
        # dbc_css
    ])
    dash_app.title = "Дашборд"


    finance_tab_content = tab_finance.tab_finance_content()
    # sales_tab_content = sales_tab.sales_tab_content()
    customers_tab_content = customers_tab.customers_tab_content()
    sales_tab_content = sales_tab.sales_tab_content()
    settings_tab_content = settings_content.settings_content()

    settings_tab_content_2 = settings_content_2.settings_content()

    project_folder = Path(__file__).resolve().parent.parent
    logo_path = str(project_folder) + '/assets/Logo_FACECOM_(2018)_OR_cut.png'
    logo_png = logo_path
    test_base64 = base64.b64encode(open(logo_png, 'rb').read()).decode('ascii')

    exit_icon = html.I(className="fas fas fa-sign-out-alt")

    exit_text = html.Div(style=dict(display='inline-block'),
        children=[
            dbc.NavItem(dbc.NavLink("Выход", href="/logout", id="logout-link", external_link=True, ))
        ]
    )

    exit_content = html.Span([exit_text, exit_icon])

    dash_app.layout = html.Div(
        dbc.Container(

            [html.Div(style={'paddingLeft': '15px', 'paddingRight': '20px', 'paddingTop': '5px', 'paddingBottom': '5px',
                             # 'color': 'white'
                             },
                      children=[
                          dbc.Navbar(
                              dbc.Container(
                                  [
                                      html.A(
                                          # Use row and col to control vertical alignment of logo / brand
                                          dbc.Row(
                                              [
                                                  dbc.Col(html.Img(src='data:image/png;base64,{}'.format(test_base64), height="30px")),
                                                  # dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                                              ],
                                              align="center",
                                              className="g-0",
                                          ),
                                          href="https://plotly.com",
                                          style={"textDecoration": "none"},
                                      ),
                                      dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                                      dbc.Collapse(
                                          dbc.Row(
                                              [
                                                  dbc.Col(
                                                      # dbc.Input(type="search", placeholder="Search")
                                                  ),
                                                  dbc.Col(
                                                      dbc.NavItem(

                                                          dbc.NavLink("Выход", href="/logout", id="logout-link",external_link=True, )
                                                          # exit_content
                                                      ),

                                                      # dbc.Button("Search", color="primary", className="ms-2", n_clicks=0),
                                                      width="auto",
                                                  ),
                                              ],
                                              className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                                              align="center",
                                          ),
                                          id="navbar-collapse",
                                          is_open=False,
                                          navbar=True,
                                      ),
                                  ]
                              ),
                              color="light",
                              dark=False,
                          ),
                          # укладываем на всю ширину ряда заголовок
                          dbc.Row([
                              dbc.Col(
                                  children=[
                                      ######### header ###########
                                      html.Div(style={'margin-top': '15px'},
                                          children=[
                                              # dbc.Row(
                                              #     children=[
                                              #         dbc.Col(md=12,
                                              #             children=[
                                              #                 html.Img(src='data:image/png;base64,{}'.format(test_base64), height='60px'),
                                              #
                                              #             ]
                                              #         ),
                                              #
                                              #     ]
                                              # ),
                                              dbc.Row(
                                                  [
                                                      dbc.Col(md=12,
                                                              children=[
                                                                  html.H2(
                                                                      'Основные финансовые показатели компании',
                                                                      className='custom_H3')
                                                              ]

                                                              )
                                                  ]
                                              )
                                          ]
                                      ),

                                      html.Div(
                                          style={
                                              # 'paddingLeft': '15px',
                                              # 'paddingRight': '20px',
                                              # 'paddingTop': '5px',
                                              # 'paddingBottom': '5px',
                                              'marginTop': '10px',
                                              # 'color': 'white'
                                          },
                                          children=[

                                              dbc.Tabs(
                                                  [
                                                      dbc.Tab(finance_tab_content,
                                                              label="Финансы",
                                                              tab_class_name="custom_tab_css",
                                                              label_class_name="custom_labelClassName",
                                                              active_tab_class_name = "active_custom_tab_css"

                                                              ),
                                                      dbc.Tab(customers_tab_content,
                                                          label="Клиенты",
                                                          tab_class_name="custom_tab_css",
                                                          label_class_name="custom_labelClassName",
                                                          active_tab_class_name="active_custom_tab_css",
                                                          disabled=False
                                                      ),
                                                      dbc.Tab(sales_tab_content,
                                                              label="Продажи",
                                                              tab_class_name="custom_tab_css",
                                                              label_class_name="custom_labelClassName",
                                                              active_tab_class_name="active_custom_tab_css",
                                                              # disabled=True
                                                              ),


                                                      # dbc.Tab(
                                                      #         label="Сотрудники",
                                                      #         tab_class_name="custom_tab_css",
                                                      #         label_class_name="custom_labelClassName",
                                                      #         active_tab_class_name="active_custom_tab_css",
                                                      #         disabled=True
                                                      #         ),
                                                      # dbc.Tab(settings_tab_content,
                                                      #         label="Настройки",
                                                      #         tab_class_name="custom_tab_css",
                                                      #         label_class_name="custom_labelClassName",
                                                      #         active_tab_class_name="active_custom_tab_css"
                                                      #         ),
                                                      # dbc.Tab(settings_tab_content_2,
                                                      #         label="Настройки",
                                                      #         tab_class_name="custom_tab_css",
                                                      #         label_class_name="custom_labelClassName",
                                                      #         active_tab_class_name="active_custom_tab_css"
                                                      #         )

                                                  ]),



                                            ]),
                                  ])
                          ]),
                      ]),
             dcc.Interval(
                 id="load_interval_demo",
                 n_intervals=0,
                 max_intervals=0,  # <-- only run once
                 interval=1
             ),
             ],


            fluid=True,
            className="dbc",
            style={
              "min-width":"700px",
            },
            # className='custom_container'
        )
    )

    init_callback_inputs(dash_app)
    init_callback_resources_and_plans(dash_app)
    init_callback_treeview(dash_app)
    init_callback_retail_income_by_customers_barchart(dash_app)
    init_callback_managers_sales_bar_graph(dash_app)
    init_callback_reload_demo_tables(dash_app)
    init_callback_demo_credit_by_bank(dash_app)
    init_callback_demo_marketing_cost(dash_app)
    init_callback_demo_customer_map(dash_app)
    # init_callback_map(dash_app)
    init_callback_set_categories(dash_app)
    init_set_sales_data(dash_app)
    init_callback_demo_sales_accumulative_year(dash_app)
    init_callback_auth_menu(dash_app)
    init_callback_navbar(dash_app)
    init_callback_create_demo_data(dash_app)
    return dash_app

def init_callback_navbar(dash_app):
    @dash_app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open



def init_callback_create_demo_data(dash_app):
    @dash_app.callback(
        [
            Output('create_demo_data_info', 'children'),
         ],
        [
            Input('create_demo_data_button', 'n_clicks'),
        ]
    )
    def create_demo_data(n_clicks):
        create_demo_data_info_ = ''
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == 'create_demo_data_button':
            create_demo_data_module.create_demo_data_func()




        return [
            create_demo_data_info_,
            ]






def init_callback_inputs(dash_app):
    @dash_app.callback(
        [
            Output('product_category_select', 'options'),
            Output('revenue_range_select', 'options'),

            Output('product_category_select_error_message', 'children'),


         ],
        [
            Input('load_interval_demo', 'n_intervals'),
        ]
    )
    def credit_inputs(n_intervals):
        product_category_select_ = {1:1}
        product_category_select_error_message_ = ""
        revenue_range_select_ = {1:1}

        try:
            product_category_select_ = product_category_select_options.product_category_select_options_func()
        except Exception as e:
            product_category_select_error_message_ = f"ошибка при создании фильтра: {e}"


        try:
            revenue_range_select_ = revenue_range_select_options.revenue_range_select_options_func()
        except Exception as e:
            product_category_select_error_message_ = f"ошибка при создании фильтра: {e}"




        return [
            product_category_select_,
            revenue_range_select_,
            product_category_select_error_message_,
            ]


def init_callback_resources_and_plans(dash_app):
    @dash_app.callback(
        [
            Output('resources_and_plans_div', 'children'),
            Output('revenue_card', 'children'),
            Output('revenue_card_by_today_below_text', 'children'),
            Output('ebitda_by_today_v2', 'children'),
            Output('ebitda_by_today_below_text', 'children'),
            Output('profit_by_today', 'children'),
            Output('profit_by_today_below_text', 'children'),

        ],
        [
            Input('finance_tab_top_client_filter', 'value'),
        ]
    )
    def resources_and_plans(finance_tab_top_client_filter):
        resources_and_plans_div_ = 'txt'
        revenue_card_ = 'txt'
        ebitda_by_today_ = 'txt'
        profit_by_today_ = 'txt'

        try:
            resources_and_plans_div_ = resources_and_plans_div.resources_and_plans_div_func(finance_tab_top_client_filter)[0]
            revenue_card_ = resources_and_plans_div.resources_and_plans_div_func(finance_tab_top_client_filter)[3]
        except Exception as e:
            resources_and_plans_div_ = f'error resources_and_plans_div_: {e}'

        today = datetime.datetime.now()
        current_year = today.year
        today_str = today.strftime('%d.%m.%Y')
        text_output = html.P(f'На {today_str} с начала {str(current_year)}г.')
        revenue_card_by_today_below_text_ = text_output

        ebitda_by_today_ = resources_and_plans_div.resources_and_plans_div_func(finance_tab_top_client_filter)[4]

        ebitda_by_today_below_text_ = text_output
        profit_by_today_ = resources_and_plans_div.resources_and_plans_div_func(finance_tab_top_client_filter)[5]
        profit_by_today_below_text_ = text_output
        return [
            resources_and_plans_div_,
            revenue_card_,
            revenue_card_by_today_below_text_,
            ebitda_by_today_,
            ebitda_by_today_below_text_,
            profit_by_today_,
            profit_by_today_below_text_
            ]




def init_callback_treeview(dash_app):
    @dash_app.callback(
        [
            Output('revenue_treemap_div', 'children'),
            Output('treeview_retail_period_text_div', 'children'),


        ],
        [
            Input('retail_customer_select', 'value'),
        ]
    )
    def treeview(retail_customer_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА credit_totals_by_today #########
        revenue_treemap_div_ = 'txt'
        treeview_retail_period_text_div_ = 'txt'

        try:
            revenue_treemap_div_ = revenue_treemap_div.revenue_treemap_div_func(retail_customer_select)[0]
        except Exception as e:
            revenue_treemap_div_ = f'error revenue_treemap: {e}'

        first_date = datetime.datetime(2023, 1, 1)
        last_date = revenue_treemap_div.revenue_treemap_div_func(retail_customer_select)[1]
        try:
            treeview_retail_period_text_div_ = period_text.credit_grapf_period_text_func(first_date, last_date)
        except:
            pass

        return [
            revenue_treemap_div_,
            treeview_retail_period_text_div_
            ]


def init_callback_retail_income_by_customers_barchart(dash_app):
    @dash_app.callback(
        [
            Output('retail_income_by_customers_barchart_div', 'children'),
            Output('retail_income_by_customers_barchart_div_period_text_div', 'children'),


        ],
        [
            Input('retail_customer_select', 'value'),
        ]
    )
    def resources_and_plans(retail_customer_select):
        retail_income_by_customers_barchart_div_ = 'txt'
        retail_income_by_customers_barchart_div_period_text_div_ = 'txt'

        try:
            retail_income_by_customers_barchart_div_ = retail_income_by_customers_barchart_div.retail_income_by_customers_barchart_div_func(retail_customer_select)[0]
        except Exception as e:
            retail_income_by_customers_barchart_div_ = f'error resources_and_plans_div_: {e}'

        first_date = datetime.datetime(2023,1,1)
        last_date = retail_income_by_customers_barchart_div.retail_income_by_customers_barchart_div_func(retail_customer_select)[1]
        try:
            retail_income_by_customers_barchart_div_period_text_div_ = period_text.credit_grapf_period_text_func(first_date, last_date)
        except:
            pass



        return [
            retail_income_by_customers_barchart_div_,
            retail_income_by_customers_barchart_div_period_text_div_
            ]




def init_callback_auth_menu(dash_app):
    @dash_app.callback(
        [
            Output('logged_in_check', 'children'),
        ],
        [
            Input('retail_customer_select', 'value'),
        ]
    )
    def auth_menu(retail_customer_select):
        logged_in_check_ = 'output'
        if current_user.is_authenticated:
            logged_in_check_ = f"User ID: {current_user.id}"
        else:
            logged_in_check_ = "Not logged in"

        return [
            logged_in_check_
            ]




def init_callback_managers_sales_bar_graph(dash_app):
    @dash_app.callback(
        [
            Output('managers_sales_bar_graph', 'figure'),
            Output('managers_sales_bar_chart_period_text', 'children'),
            Output('managers_sales_bar_graph', 'clickData'),
            Output('back-button', 'style'),  # to hide/unhide the back button
        ],
        [
            Input('retail_customer_select', 'value'),
            Input('managers_sales_bar_graph', 'clickData'),
            Input('back-button', 'n_clicks'),
        ]
    )
    def managers_sales(retail_customer_select, click_data, n_clicks):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА managers_sales #########
        managers_sales_bar_chart_period_text_ = ""
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)
        with engine.connect() as con:
            # query = 'SELECT *  FROM "creditDB";'
            query = 'SELECT *  FROM "retail";'
            df = pd.read_sql(query, con)
        df.rename(columns={
            'sum': 'amount'
        }, inplace=True)



        managers_sales_bar_graph_ = html.Div(html.P("Нет данных"))
        try:
            managers_sales_bar_graph_ = managers_sales_bar_graph.managers_sales_bar_graph_func(df, retail_customer_select)[0]

        except Exception as e:
            print(e)
        try:
            first_date = datetime.datetime(2023,1,1)
            last_date = managers_sales_bar_graph.managers_sales_bar_graph_func(df, retail_customer_select)[1]

            managers_sales_bar_chart_period_text_ = period_text.credit_grapf_period_text_func(first_date, last_date)
        except:
            pass
        ctx = dash.callback_context

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        check_trigger = 'by_banks' # проверка в каком графике мы находимся

        if trigger_id == 'back-button':
            check_trigger = 'by_banks'
            return [
                managers_sales_bar_graph_,
                managers_sales_bar_chart_period_text_,
                click_data,
                {'display': 'none'},
            ]


        if trigger_id == 'managers_sales_bar_graph':
            manager = click_data['points'][0]['label']
            list_of_managers = list(df['manager'].unique())

            if click_data is not None and manager in list_of_managers:
                # график погашения по месяцам в кликнутом менеджере

                managers_sales_bar_graph_ = managers_by_month_bar.managers_by_month_func(df, retail_customer_select, manager)

                click_data = None

                return [
                    managers_sales_bar_graph_,
                    managers_sales_bar_chart_period_text_,
                    click_data,
                    {'display':'block'},
                ]



        return [
            managers_sales_bar_graph_,
            managers_sales_bar_chart_period_text_,
            click_data,
            {'display':'none'},
            ]




def init_callback_demo_credit_by_bank(dash_app):
    @dash_app.callback(
        [
            Output('demo_credit_by_bank_piechart_graph', 'children'),
            Output('period_text_demo_credit_by_bank_piechart', 'children'),
        ],
        [
            Input('retail_customer_select', 'value'),
        ]
    )
    def treeview(retail_customer_select):
        demo_credit_by_bank_piechart_graph_ = 'txt'
        period_text_demo_credit_by_bank_piechart_ = 'txt'

        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)
        with engine.connect() as con:
            # query = 'SELECT *  FROM "creditDB";'
            query = 'SELECT *  FROM "creditdb_2";'
            df = pd.read_sql(query, con)
        df.rename(columns={
            'sum': 'amount'
        }, inplace=True)



        try:
            demo_credit_by_bank_piechart_graph_ = demo_credit_by_bank_piechart_graph.demo_credit_by_bank_piechart_graph_func(df, retail_customer_select)[0]
        except Exception as e:
            revenue_treemap_div_ = f'error revenue_treemap: {e}'

        first_date = demo_credit_by_bank_piechart_graph.demo_credit_by_bank_piechart_graph_func(df, retail_customer_select)[1]
        last_date = demo_credit_by_bank_piechart_graph.demo_credit_by_bank_piechart_graph_func(df, retail_customer_select)[2]
        try:
            period_text_demo_credit_by_bank_piechart_ = period_text.credit_grapf_period_text_func(first_date, last_date)
        except:
            pass

        return [
            demo_credit_by_bank_piechart_graph_,
            period_text_demo_credit_by_bank_piechart_
            ]



def init_callback_demo_marketing_cost(dash_app):
    @dash_app.callback(
        [
            Output('marketing_cost_div', 'children'),
            Output('marketing_cost_div_period_text', 'children'),
        ],
        [
            Input('retail_customer_select', 'value'),
        ]
    )
    def demo_marketing_cost(retail_customer_select):
        marketing_cost_div_ = 'txt'
        marketing_cost_div_period_text_ = 'txt'

        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)
        with engine.connect() as con:
            query = 'SELECT *  FROM "retail";'
            df = pd.read_sql(query, con)
        df.rename(columns={
            'sum': 'amount'
        }, inplace=True)



        try:
            marketing_cost_div_ = marketing_cost_div.marketing_cost_div_func(df, retail_customer_select)[0]
        except Exception as e:
            marketing_cost_div_ = f'error revenue_treemap: {e}'

        first_date = datetime.datetime(2023,1,1)
        last_date = marketing_cost_div.marketing_cost_div_func(df, retail_customer_select)[1]
        try:
            period_text_demo_credit_by_bank_piechart_ = period_text.credit_grapf_period_text_func(first_date, last_date)
        except:
            pass

        return [
            marketing_cost_div_,
            marketing_cost_div_period_text_
            ]



def init_callback_demo_sales_accumulative_year(dash_app):
    @dash_app.callback(
        [
            Output('sales_accumulative_year', 'children'),
            Output('sales_accumulative_year_check', 'children'),
            Output('sales_tab_product_category_select', 'options'),
        ],
        [
            Input('sales_tab_product_category_select', 'value'),
        ]
    )
    def sales_accumulative(sales_tab_product_category_select):
        sales_accumulative_year_ = ''
        sales_accumulative_year_check_ = ''

        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)
        with engine.connect() as con:
            query = 'SELECT *  FROM "calendar_sales_v3";'
            df = pd.read_sql(query, con)
        df.rename(columns={
            'sum': 'amount'
        }, inplace=True)

        sales_accumulative_year_ = sales_accumulative_year.sales_accumulative_year_func(df, sales_tab_product_category_select)[0]
        sales_tab_product_category_select_ = sales_accumulative_year.sales_accumulative_year_func(df, sales_tab_product_category_select)[1]

        return [
            sales_accumulative_year_,
            sales_accumulative_year_check_,
            sales_tab_product_category_select_
            ]


def init_callback_demo_customer_map(dash_app):
    @dash_app.callback(
        [
            Output('customer_map', 'children'),
            Output('customer_map_check', 'children'),

        ],
        [
            Input('product_category_select', 'value'),
            Input('revenue_range_select', 'value'),
        ]
    )
    def customer_map(product_category_select, revenue_range_select):
        marketing_cost_div_ = 'txt'
        marketing_cost_div_period_text_ = 'txt'

        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)
        with engine.connect() as con:
            query = 'SELECT *  FROM "customer_address";'
            df = pd.read_sql(query, con)
        df.rename(columns={
            'sum': 'amount'
        }, inplace=True)

        df['customer_name'].fillna("test", inplace=True)
        df['customer_name'] = df['customer_name'].replace('', 'test', regex=True)
        df_temp = df.loc[df['customer_name'] != "test"]

        # определяем список клиентов, которые остались после фильтрации в фильтре product_category_select
        with engine.connect() as con:
            query = 'SELECT *  FROM "customer_product_category";'
            df_customers_product_categories = pd.read_sql(query, con)


        customer_product_category_full_list = list(df_customers_product_categories['product_category'].unique())
        product_category_filter = customer_product_category_full_list
        if product_category_select:
            if 'list' in str(type(product_category_select)):
                product_category_filter = product_category_select
            else:
                product_category_filter = list(product_category_select)

        # режем выборку
        df_customer_product_category_filtered = df_customers_product_categories.loc[df_customers_product_categories['product_category'].isin(product_category_filter)]



        # Получаем список клиентов, которые остались в выборке
        filtered_list_of_customers = list(df_customer_product_category_filtered['customer_name'].unique())

        # режем выборку по оставшимся клиентам
        df_temp_filtered = df_temp.loc[df_temp['customer_name'].isin(filtered_list_of_customers)]




        with engine.connect() as con:
            query = 'SELECT *  FROM "revenue_ranges";'
            df_revenue_ranges = pd.read_sql(query, con)


        revenue_range_full_list = list(df_revenue_ranges['range_name'].unique())
        revenue_range_filter = revenue_range_full_list
        if revenue_range_select:
            if 'list' in str(type(revenue_range_select)):
                revenue_range_filter = revenue_range_select
            else:
                revenue_range_filter = list(revenue_range_select)


        df_customer_address_filtered = df_temp_filtered
        df_amount_filtered = pd.DataFrame()
        # итерируемся по полученному фильтру
        if revenue_range_filter != revenue_range_full_list:
            for revenue_filter_item in revenue_range_filter:
                temp_revenue_filter_df = df_revenue_ranges.loc[df_revenue_ranges['range_name']==revenue_filter_item]
                range_min_value = temp_revenue_filter_df.iloc[0]['range_min_value']
                range_max_value = temp_revenue_filter_df.iloc[0]['range_max_value']

                # режем выборку по диапазону значений фильтра

                df_temp_customer_address_filtered = df_customer_address_filtered.loc[df_customer_address_filtered['payment_amount']>=range_min_value]
                df_temp_customer_address_filtered = df_temp_customer_address_filtered.loc[df_temp_customer_address_filtered['payment_amount'] < range_max_value]
                df_amount_filtered = pd.concat([df_amount_filtered, df_temp_customer_address_filtered])

            df_temp_filtered = df_amount_filtered
        # datatable = dash_table.DataTable(data=df_amount_filtered.to_dict('records'), )




        df_temp_filtered_groupped = df_temp_filtered.groupby(['latitude', 'longitude', 'size', 'customer_name', 'payment_amount', 'margin_rate'], as_index=False).agg({'address_id': 'count'})
        df_temp_filtered_groupped.rename(columns={
            'margin_rate': 'Маржинальность, %'
        }, inplace=True)
        df_temp_filtered_groupped['payment_amount'] = df_temp_filtered_groupped['payment_amount']  / 1000000
        df_temp_filtered_groupped['payment_amount']  = df_temp_filtered_groupped['payment_amount'].round(decimals=0)
        df_temp_filtered_groupped['Маржинальность, %'] = df_temp_filtered_groupped['Маржинальность, %'].round(decimals=0)
        x1 = df_temp_filtered_groupped['latitude'].min()
        x2 = df_temp_filtered_groupped['latitude'].max()
        y1 = df_temp_filtered_groupped['longitude'].min()
        y2 = df_temp_filtered_groupped['longitude'].max()

        max_bound = max(abs(x1 - x2), abs(y1 - y2)) * 111
        zoom = 11.5 - np.log(max_bound)
        fig = px.scatter_mapbox(
            df_temp_filtered_groupped,
            lat="latitude",
            lon="longitude",
            color="Маржинальность, %",
            # hover_name='customer_name',
            zoom=3,
            size=df_temp_filtered_groupped['size'],
            # hover_data={'customer_name': True},
            custom_data=['customer_name', 'payment_amount', 'Маржинальность, %'],
            color_continuous_scale=px.colors.sequential.deep,

        )
        fig.update_traces(cluster=dict(enabled=True))

        fig.update_traces(hovertemplate="%{customdata[0]}:<br>Выручка: %{customdata[1]} млн. руб<br>Средняя маржинальность: %{customdata[2]}%")

        # us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
        # fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
        #                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)

        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )


        # customer_map_ = datatable

        # customer_map_check_ = html.Div(
        #     children=[
        #         str(len(df_temp_filtered_groupped)),
        #         datatable
        #     ]
        # )
        customer_map_check_ = ""



        customer_map_ = dcc.Graph(figure=fig, config={'displayModeBar': False})


        return [
            customer_map_,
            customer_map_check_
            ]




def init_callback_reload_demo_tables(dash_app):
    @dash_app.callback(
        [
            Output('reload_demo_tables_info', 'children'),

        ],
        [
            Input('reload_demo_tables_button', 'n_clicks'),
        ]
    )
    def reload_demo_tables(reload_demo_tables_button):
        ctx = dash.callback_context
        output_list = []
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == 'reload_demo_tables_button':

            output = credit_data_convert.credit_data_convert(reload_demo_tables_button)
            output_list.append(output)

            output_leasing_convert = leasing_data_convert.leasing_data_convert_func(reload_demo_tables_button)
            output_list.append(output_leasing_convert)

            credit_calendar_to_bd_v3.credit_calendar_to_bd_func('1с_api')

        return [str(output_list)]


def init_callback_set_categories(dash_app):
    @dash_app.callback(
        [
            Output('set_categories_info', 'children'),

        ],
        [
            Input('set_categories_button', 'n_clicks'),
        ]
    )
    def set_categories(set_categories_button):
        ctx = dash.callback_context
        output_list = []
        output = ''
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == 'set_categories_button':

            # Получаем таблицу с клиентами

            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                query = 'SELECT *  FROM "leasing_temp_db";'
                df = pd.read_sql(query, con)
            # df.rename(columns={
            #     'sum': 'amount'
            # }, inplace=True)

            # добавляем поле со значением выручки
            #
            df['customer_name'].fillna("test", inplace=True)
            df['customer_name'] = df['customer_name'].replace('', 'test', regex=True)
            df_temp = df.loc[df['customer_name'] != "test"]

            df = df_temp
            # агрегируем по payment_amount
            df_revenue = df.groupby(['customer_name'], as_index=False).agg({'payment_amount': 'sum'})



            # соединяем с таблицей адресов
            with engine.connect() as con:
                query = 'SELECT *  FROM "customer_address";'
                df_address = pd.read_sql(query, con)

            if 'payment_amount' not in list(df_address.columns):
                df_address = df_address.merge(df_revenue, how='left', on='customer_name')


            df_address['payment_amount'].fillna(989200, inplace=True)
            df_address['payment_amount'] = df_address['payment_amount'].replace('', 989200, regex=True)

            all_data_diffq = (df_address["payment_amount"].max() - df_address["payment_amount"].min()) / 16

            df_address["size"] = (df_address["payment_amount"] - df_address["payment_amount"].min()) / all_data_diffq + 1


            # datatable = dash_table.DataTable(data=df_address.to_dict('records'), )

            # перезаписываем таблицу df_address

            if_exists = 'replace'
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = sqlalchemy.create_engine(url_db)

            with engine.connect() as con:
                df_address.to_sql(
                    name='customer_address',
                    con=con,
                    chunksize=5000,
                    method='multi',
                    index=False,
                    if_exists=if_exists
                )

            # готовим селект по выручке
            # делим выручку на 5 диапазонов

            max_payment_amount = df_address["payment_amount"].max()
            min_payment_amount = df_address["payment_amount"].min()
            delta = max_payment_amount - min_payment_amount

            sector_delta = delta / 5

            revenue_diapasons_list = []
            temp_payment_value = 0
            while temp_payment_value <= max_payment_amount:
                temp_dict = {}
                range_min = '{:.0f}'.format(round(temp_payment_value/1000000, 0))
                range_max = '{:.0f}'.format(round((temp_payment_value+ sector_delta)/1000000, 0))
                temp_dict['range_name'] = f'{range_min} - {range_max} млн'
                temp_dict['range_min_value'] = temp_payment_value
                temp_dict['range_max_value'] = temp_payment_value + sector_delta
                revenue_diapasons_list.append(temp_dict)
                temp_payment_value = temp_payment_value + sector_delta

            revenue_diapasons_df = pd.DataFrame(revenue_diapasons_list)

            with engine.connect() as con:
                revenue_diapasons_df.to_sql(
                    name='revenue_ranges',
                    con=con,
                    # chunksize=5000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )



            # Получаем данные о маржинальности
            with engine.connect() as con:
                query = 'SELECT *  FROM "customers";'
                customers_df = pd.read_sql(query, con)

            customers_df['margin_rate'] = np.random.uniform(8, 18, size=len(customers_df))

            if 'margin_rate' not in list(customers_df.columns):
                with engine.connect() as con:
                    customers_df.to_sql(
                        name='customers',
                        con=con,
                        # chunksize=5000,
                        # method='multi',
                        index=False,
                        if_exists='replace'
                    )

            with engine.connect() as con:
                query = 'SELECT *  FROM "customer_address";'
                df_address = pd.read_sql(query, con)

            customers_margin_rate_df = customers_df.loc[:, ['customer_name', 'margin_rate']]
            if 'margin_rate' not in list(df_address.columns):
                df_address = df_address.merge(customers_margin_rate_df, how='left', on='customer_name')

            df_address['margin_rate'].fillna(9, inplace=True)
            df_address['margin_rate'] = df_address['margin_rate'].replace('', 9, regex=True)

            with engine.connect() as con:
                df_address.to_sql(
                    name='customer_address',
                    con=con,
                    chunksize=5000,
                    method='multi',
                    index=False,
                    if_exists=if_exists
                )



            # делим значения маржинальности на 5 диапазонов

            max_margin_amount = df_address["margin_rate"].max()
            min_margin_amount = df_address["margin_rate"].min()
            delta_margin = max_margin_amount - min_margin_amount

            sector_margin_delta = delta_margin / 5

            margin_diapasons_list = []
            temp_margin_value = min_margin_amount
            while temp_margin_value <= max_margin_amount:
                temp_dict = {}
                range_min = '{:.0f}'.format(round(temp_margin_value, 0))
                range_max = '{:.0f}'.format(round((temp_margin_value + sector_margin_delta), 0))
                temp_dict['margin_range_name'] = f'{range_min} - {range_max} %'
                temp_dict['range_min_value'] = temp_margin_value
                temp_dict['range_max_value'] = temp_margin_value + sector_margin_delta
                margin_diapasons_list.append(temp_dict)
                temp_margin_value = temp_margin_value + sector_margin_delta

            margin_diapasons_df = pd.DataFrame(margin_diapasons_list)
            with engine.connect() as con:
                margin_diapasons_df.to_sql(
                    name='margin_ranges',
                    con=con,
                    # chunksize=5000,
                    # method='multi',
                    index=False,
                    if_exists='replace'
                )



            return [output]
        return [output]



def init_set_sales_data(dash_app):
    @dash_app.callback(
        [
            Output('set_data_info', 'children'),

        ],
        [
            Input('set_data_button', 'n_clicks'),
        ]
    )
    def set_sales_data(set_data_button):
        ctx = dash.callback_context
        output_list = []
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == 'set_data_button':

            output = set_salesdata.set_salesdata_func()
            output_list.append(output)

        return [output_list]