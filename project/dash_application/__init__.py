import datetime
import json
import os
import xmltodict
import psycopg2
from sqlalchemy import create_engine
from dash import dash_table
import dash
from dash import dcc, Input, Output, State
from dash import html, ctx
from pathlib import Path
import dash_bootstrap_components as dbc
# from flask_login.utils import login_required
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import base64
from dash_bootstrap_templates import load_figure_template
# import dash_application.data_functions as data_functions
# import dash_application.functions.json_demo_data as json_demo_data
# import dash_application.functions.sample_data as sample_data
# import dash_application.tab_leasing as tab_leasing
import dash_application.tab_leasing_v2 as tab_leasing_v2

import dash_application.tab_credit as tab_credit
import dash_application.settings_content as settings_content

import dash_application.functions.credit_request_to_bd as credit_request_to_bd
import dash_application.functions.leasing_request_to_bd as leasing_request_to_bd
import dash_application.functions.credit_calendar_to_bd as credit_calendar_to_bd
import dash_application.functions.credit_calendar_to_bd_v2 as credit_calendar_to_bd_v2

import dash_application.functions.credit_calendar_to_bd_v3 as credit_calendar_to_bd_v3



import dash_application.functions.df_credit_from_db_module as df_credit_from_db_module

import dash_application.functions.convert_ral_excel_to_datafile as convert_ral_excel_to_datafile
# import dash_application.functions.df_filter_list as df_filter_list
import dash_application.functions.creditor_select_2_options as creditor_selector_2_options # создание фильтра из полученного на вход df
import dash_application.functions.credit_contract_select_options as credit_contract_select_options
import dash_application.functions.credit_tab_year_select_options as credit_tab_year_select_options
import dash_application.functions.credit_tab_quarter_select_options as credit_tab_quarter_select_options
import dash_application.functions.credit_tab_month_select_options as credit_tab_month_select_options
# import dash_application.functions.taken_tranch_year_select_options as taken_tranch_year_select_options
import dash_application.functions.calendar_data_store as calendar_data_store
import dash_application.functions.report_date_borders as report_date_borders
import dash_application.functions.leasing_tables_create as leasing_tables_create
import dash_application.dash_objects.initial_values as initial_values
import dash_application.dash_objects.credit_filter_creditor as credit_filter_creditor
import dash_application.dash_objects.credit_filter_credit_agreement as credit_filter_credit_agreement
import dash_application.dash_objects.credit_filter_year as credit_filter_year
import dash_application.dash_objects.credit_filter_quarter as credit_filter_quarter
import dash_application.dash_objects.credit_filter_month as credit_filter_month
import dash_application.dash_objects.period_text as period_text
import dash_application.dash_objects.credit_tab_payment_grapf_year as credit_tab_payment_grapf_year
import dash_application.dash_objects.credit_tab_payment_grapf_month as credit_tab_payment_grapf_month
import dash_application.dash_objects.credit_tab_av_rate_graph as credit_tab_av_rate_graph
import dash_application.dash_objects.credit_treemap_graph as credit_tab_treemap_graph
import dash_application.dash_objects.credit_remain_bar as credit_remain_bar
# import dash_application.dash_objects.remains_bar_chart_period_text as remains_bar_chart_period_text
import dash_application.dash_objects.credit_remain_piechart as credit_remain_piechart
import dash_application.dash_objects.credit_tab_credit_payment_by_bank as credit_tab_credit_payment_by_bank
# import dash_application.dash_objects.credit_taken_tranch_year_filter as credit_taken_tranch_year_filter
import dash_application.dash_objects.low_block_creditor_select_options as low_block_creditor_select_options
import dash_application.dash_objects.credit_limit_remain_by_today_content_ as credit_limit_remain_by_today_content_
import dash_application.dash_objects.credit_limit_remain_by_today_below_text_content_ as credit_limit_remain_by_today_below_text_content_
# import dash_application.dash_objects.credit_tab_taken_tranch_content as credit_tab_taken_tranch_content
import dash_application.dash_objects.credit_totals_by_today_content_ as credit_totals_by_today_content_
import dash_application.dash_objects.credit_totals_by_today_below_text_content_ as credit_totals_by_today_below_text_content_
import dash_application.dash_objects.credit_taken_by_today_content_ as credit_taken_by_today_content_
import dash_application.dash_objects.credit_taken_by_today_below_text_content_ as credit_taken_by_today_below_text_content_
import dash_application.dash_objects.taken_vs_remain_graph_div_content_ as taken_vs_remain_graph_div_content_
import dash_application.dash_objects.credit_by_bank_download_excel_data_df as credit_by_bank_download_excel_data_df
import dash_application.leasing_dash_objects.reload_leasing_tables_module as reload_leasing_tables_module
import dash_application.leasing_dash_objects.leasing_short_table_create as leasing_short_table_create
import dash_application.leasing_dash_objects.leasing_payments_by_month_v3_div_ as leasing_payments_by_month_v3_div_
import dash_application.leasing_dash_objects.leasing_payments_pie_chart_v3_div_ as leasing_payments_pie_chart_v3_div_
import dash_application.leasing_dash_objects.top_group_customers_barchart_v2_div_ as top_group_customers_barchart_v2_div_
import dash_application.leasing_dash_objects.top_independent_customers_barchart_v2_div_ as top_independent_customers_barchart_v2_div_
import dash_application.leasing_dash_objects.leasing_products_barchart_div as leasing_products_barchart_div
import dash_application.leasing_dash_objects.leasing_agreement_type_barchart_div as leasing_agreement_type_barchart_div
import dash_application.leasing_dash_objects.leasing_agreement_type_year_select_options_ as leasing_agreement_type_year_select_options_
import dash_application.leasing_dash_objects.leasing_payments_by_month_year_select_options_ as leasing_payments_by_month_year_select_options_
import dash_application.leasing_dash_objects.leasing_payments_by_month_download as leasing_payments_by_month_download
import dash_application.leasing_dash_objects.leasing_payments_pie_chart_year_select_options_ as leasing_payments_pie_chart_year_select_options_
import dash_application.leasing_dash_objects.top_customers_year_select_options_ as top_customers_year_select_options_
import dash_application.leasing_dash_objects.top_company_group_download as top_company_group_download
import dash_application.leasing_dash_objects.top_independent_customers_year_select_options as top_independent_customers_year_select_options
import dash_application.leasing_dash_objects.top_independent_company_download as top_independent_company_download
import dash_application.leasing_dash_objects.top_products_year_select_options as top_products_year_select_options
import dash_application.leasing_dash_objects.top_products_download as top_products_download
import dash_application.leasing_dash_objects.agreement_type_download as agreement_type_download
import dash_application.leasing_dash_objects.interpayment_type_barchart_div as interpayment_type_barchart_div
import dash_application.leasing_dash_objects.interpayment_type_year_select_options as interpayment_type_year_select_options
import dash_application.leasing_dash_objects.interpayment_type_download as interpayment_type_download
import dash_application.leasing_dash_objects.leasing_object_type_barchart_div as leasing_object_type_barchart_div
import dash_application.leasing_dash_objects.leasing_object_type_year_select_options as leasing_object_type_year_select_options
import dash_application.leasing_dash_objects.leasing_object_type_download as leasing_object_type_download
import dash_application.leasing_dash_objects.leasing_rate_barchart_div as leasing_rate_barchart_div
import dash_application.leasing_dash_objects.leasing_rate_year_select_options as leasing_rate_year_select_options
import dash_application.leasing_dash_objects.leasing_rate_download as leasing_rate_download
import dash_application.leasing_dash_objects.leasing_rate_distribution_barchart_div as leasing_rate_distribution_barchart_div
import dash_application.leasing_dash_objects.leasing_rate_distribution_barchart_year_select_options as leasing_rate_distribution_barchart_year_select_options
import dash_application.leasing_dash_objects.leasing_rate_distribution_download as leasing_rate_distribution_download
import dash_application.leasing_dash_objects.leasing_rate_distribution_density_div as leasing_rate_distribution_density_div
import dash_application.credit_data_objects.transhi_i_crediti_block_creditor_select_options as transhi_i_crediti_block_creditor_select_options
import dash_application.credit_data_objects.credit_treemap_div_content_ as credit_treemap_div_content_
import dash_application.credit_data_objects.creditor_select_options as creditor_select_options
import dash_application.credit_data_objects.credit_contract_select_options_ as credit_contract_select_options_
import dash_application.credit_data_objects.credit_tab_year_select_opt as credit_tab_year_select_opt
import dash_application.credit_data_objects.credit_tab_quarter_select_options_div as credit_tab_quarter_select_options_div
import dash_application.credit_data_objects.credit_tab_month_select_options_div as credit_tab_month_select_options_div
import dash_application.credit_data_objects.credit_av_rate_graph_div_content_ as credit_av_rate_graph_div_content_
import dash_application.credit_data_objects.credit_avrate_download as credit_avrate_download
import dash_application.credit_data_objects.credit_remainings_bar_graph_content_ as credit_remainings_bar_graph_content_
import dash_application.credit_data_objects.credit_remainings_by_years_bar_graph_content_ as credit_remainings_by_years_bar_graph_content_
import dash_application.credit_data_objects.credit_remainings_piechart_graph_content_ as credit_remainings_piechart_graph_content_
import dash_application.credit_data_objects.fig_credit_type_month as fig_credit_type_month
import dash_application.credit_data_objects.fig_credit_type_year as fig_credit_type_year
import dash_application.credit_data_objects.credit_bymonth_download as credit_bymonth_download
import dash_application.credit_data_objects.credit_by_banks_month as credit_by_banks_month
import dash_application.credit_data_objects.credit_line_type_select_options as credit_line_type_select_options
import dash_application.credit_data_objects.taken_vs_remain_v2_ as taken_vs_remain_v2_
import dash_application.credit_data_objects.taken_vs_remain_v3_ as taken_vs_remain_v3_
import dash_application.credit_data_objects.taken_vs_remain_v4_ as taken_vs_remain_v4_
import dash_application.credit_data_objects.taken_vs_remain_v5_ as taken_vs_remain_v5_

import dash_application.demo_data_functions.create_leasing_data_table_ as create_leasing_data_table_
import dash_application.demo_data_functions.credit_data_convert as credit_data_convert
import dash_application.demo_data_functions.leasing_data_convert as leasing_data_convert


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



def create_dash_application(flask_app):
    # dash_app = dash.Dash(server=flask_app, name="Дашборд Росагролизинг", url_base_pathname="/dash/", external_stylesheets=[dbc.themes.CERULEAN])
    # server = dash_app.server
    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
    )
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash_leasing/", external_stylesheets=[
        # url_theme2,
        # dbc_css
    ])
    dash_app.title = "Дашборд"

    # leasing_tab_content = tab_leasing.tab_leasing_content()
    leasing_tab_content_v2 = tab_leasing_v2.tab_leasing_content()
    credit_tab_content = tab_credit.credit_tab_content()
    settings_tab_content = settings_content.settings_content()

    project_folder = Path(__file__).resolve().parent.parent
    logo_path = str(project_folder) + '/assets/Logo_FACECOM_(2018)_OR.png'
    logo_png = logo_path
    test_base64 = base64.b64encode(open(logo_png, 'rb').read()).decode('ascii')

    dash_app.layout = html.Div(
        dbc.Container(

            [html.Div(style={'paddingLeft': '15px', 'paddingRight': '20px', 'paddingTop': '5px', 'paddingBottom': '5px',
                             # 'color': 'white'
                             },
                      children=[
                          # укладываем на всю ширину ряда заголовок
                          dbc.Row([
                              dbc.Col(
                                  children=[
                                      ######### header ###########
                                      html.Div(style={'margin-top': '15px'},
                                          children=[
                                              dbc.Row(
                                                  children=[
                                                      dbc.Col(md=4,
                                                          children=[
                                                              html.Img(src='data:image/png;base64,{}'.format(test_base64), height='30px'),

                                                          ]
                                                      ),
                                                      dbc.Col(md=8,
                                                              children=[
                                                                html.H3('Основные финансовые показатели', className='custom_H3')
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
                                                      dbc.Tab(credit_tab_content,
                                                              label="Кредитный портфель",
                                                              tab_class_name="custom_tab_css",
                                                              label_class_name="custom_labelClassName",
                                                              active_tab_class_name = "active_custom_tab_css"

                                                              ),

                                                      dbc.Tab(leasing_tab_content_v2,
                                                              label="Лизинговый портфель",
                                                              tab_class_name="custom_tab_css",
                                                              label_class_name="custom_labelClassName",
                                                              active_tab_class_name="active_custom_tab_css"
                                                              ),
                                                      dbc.Tab(settings_tab_content,
                                                              label="Настройки",
                                                              tab_class_name="custom_tab_css",
                                                              label_class_name="custom_labelClassName",
                                                              active_tab_class_name="active_custom_tab_css"
                                                              )

                                                  ]),
                                              dcc.Store(id='intermediate-value'),
                                              dcc.Store(id='leasing_data_store_1'),
                                              dcc.Store(id='leasing_payment_graph_data'),
                                              dcc.Store(id='calendar_store'),
                                              dcc.Store(id='leasing_data'),

                                              dcc.Interval(
                                                  id="load_interval",
                                                  n_intervals=0,
                                                  max_intervals=0,  # <-- only run once
                                                  interval=1
                                              ),
                                              dcc.Interval(
                                                  id="load_interval_2",
                                                  n_intervals=0,
                                                  max_intervals=0,  # <-- only run once
                                                  interval=1
                                              ),
                                              dcc.Download(id="download_excel_month"),
                                              dcc.Download(id="download_excel_credit_by_bank_month"),
                                              dcc.Download(id="leasing_current_agreement_status_excel_download"),
                                              dcc.Download(id="leasing_company_group_excel_download"),
                                              dcc.Download(id="leasing_independent_company_excel_download"),
                                              dcc.Download(id="leasing_top_products_excel_download"),
                                              dcc.Download(id="leasing_agreement_type_excel_download"),
                                              dcc.Download(id="leasing_interpayment_type_excel_download"),
                                              dcc.Download(id="leasing_object_type_excel_download"),
                                              dcc.Download(id="leasing_rate_excel_download"),
                                              dcc.Download(id="leasing_rate_distribution_barchart_download"),
                                              dcc.Download(id="credit_avrate_download"),
                                              dcc.Download(id="credit_bymonth_download"),
                                              dcc.Download(id="credit_download_excel_credit_by_banks_month_download"),


                                            ]),
                                  ])
                          ]),
                      ]),
             ],


            fluid=True,
            className="dbc",
            style={
              "min-width":"700px",
            },
            # className='custom_container'
        )
    )
    # init_callback_data_source_v2(dash_app)
    # init_callback_data_source_leasing_v2(dash_app)
    # init_callbacks_tab_1(dash_app)
    # init_callback_data_source(dash_app)
    # init_callback_credit_tab(dash_app)

    # init_callback_download_excel_month_credit(dash_app)
    init_callback_download_excel_credit_by_banks_month_credit(dash_app)
    # init_callback_data_source_leasing(dash_app)
    # init_callback_leasing_tab(dash_app)
    # init_callback_reload_leasing_tables_button(dash_app)
    # init_callback_create_leasing_tables(dash_app)
    init_callback_leasing_inputs(dash_app)
    init_callback_leasing_current_agreement_status(dash_app)
    init_callback_leasing_current_agreement_status_excel_download(dash_app)
    init_callback_payments_pie_chart(dash_app)
    init_callback_top_group_companies(dash_app)
    init_callback_company_group_excel_download(dash_app)
    init_callback_top_independent_companies(dash_app)
    init_callback_independent_company_excel_download(dash_app)
    init_callback_top_products(dash_app)
    init_callback_top_products_excel_download(dash_app)
    init_callback_agreement_type(dash_app)
    init_callback_agreement_type_excel_download(dash_app)
    init_callback_interpayment_type(dash_app)
    init_callback_interpayment_type_excel_download(dash_app)
    init_callback_leasing_object_type(dash_app)
    init_callback_leasing_object_type_excel_download(dash_app)
    init_callback_leasing_rate(dash_app)
    init_callback_leasing_rate_excel_download(dash_app)
    init_callback_leasing_rate_distribution_barchart(dash_app)
    init_callback_leasing_rate_distribution_excel_download(dash_app)
    # init_callback_leasing_rate_distribution_density_barchart(dash_app)
    init_callback_credit_inputs(dash_app)
    init_callback_credit_totals_by_today(dash_app)
    init_callback_credit_taken_by_today(dash_app)
    # init_callback_credit_limit_remain_by_today(dash_app)
    # init_callback_credit_taken_vs_remain(dash_app)
    init_callback_credit_credit_treemap(dash_app)
    init_callback_credit_credit_av_rate(dash_app)
    init_callback_credit_avrate_excel_download(dash_app)
    init_callback_credit_remainings_bar_graph(dash_app)
    init_callback_credit_remainings_piechart(dash_app)
    init_callback_credit_next_payments_by_credittype(dash_app)
    init_callback_credit_bymonth_excel_download(dash_app)
    init_callback_taken_vs_remain_v2_div(dash_app)
    init_callback_create_leasing_data_table(dash_app)
    init_callback_create_credit_data_table(dash_app)

    return dash_app



def init_callback_create_credit_data_table(dash_app):
    @dash_app.callback(
        [
            Output('create_credit_data_table_check', 'children'),
        ],
        [
            Input('reload_leasing_table', 'n_clicks'),

        ]
    )
    def create_leasing_data_table(reload_leasing_table):
        output_list = []
        output = credit_data_convert.credit_data_convert(reload_leasing_table)
        output_list.append(output)

        output_leasing_convert = leasing_data_convert.leasing_data_convert_func(reload_leasing_table)
        output_list.append(output_leasing_convert)

        credit_calendar_to_bd_v3.credit_calendar_to_bd_func('1с_api')

        return [str(output_list)]



def init_callback_create_leasing_data_table(dash_app):
    @dash_app.callback(
        [
            Output('create_leasing_data_table_check', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('reload_leasing_table', 'n_clicks'),

        ]
    )
    def create_leasing_data_table(data_input, reload_leasing_table):

        output = create_leasing_data_table_.create_leasing_data_table_func(reload_leasing_table)

        return [output]




def init_callback_credit_inputs(dash_app):
    @dash_app.callback(
        [
            Output('transhi_i_crediti_block_creditor_select', 'options'),
            Output('transhi_i_crediti_block_creditor_select_options_error_message', 'children'),
            Output('creditor_select', 'options'),
            Output('creditor_select_error_message', 'children'),
            Output('credit_contract_select', 'options'),  # список в селект
            Output('credit_contract_select_error_message', 'children'),
            Output('credit_year_select', 'options'),  # список в селект
            Output('credit_tab_year_select_error_message', 'children'),
            Output('credit_tab_quarter_select', 'options'),  # список в селект
            Output('credit_tab_month_select', 'options'),  # список в селект
            Output('credit_tab_month_select_error_message', 'children'),

         ],
        [
            Input('load_interval_2', 'n_intervals'),
            Input('data_input', 'value'),
            Input('creditor_select', 'value'),
        ]
    )
    def credit_inputs(n_intervals, data_input, creditor_select):
        transhi_i_crediti_block_creditor_select_ = {1:1}
        transhi_i_crediti_block_creditor_select_options_error_message_ = ""
        creditor_select_ = {1:1}
        creditor_select_error_message_ = ""
        credit_contract_select_ = {1:1}
        credit_contract_select_error_message_ = ""
        credit_year_select_ = {1:1}
        credit_tab_year_select_error_message_ = ""
        credit_tab_quarter_select_options_ = {1:1}
        credit_tab_month_select_options_ = {1:1}
        credit_tab_month_select_error_message_ = ""

        try:
            transhi_i_crediti_block_creditor_select_ = transhi_i_crediti_block_creditor_select_options.transhi_i_crediti_block_creditor_select_options_func(data_input)
        except Exception as e:
            transhi_i_crediti_block_creditor_select_options_error_message_ = f"ошибка при создании фильтра по кредиторам: {e}"

        try:
            creditor_select_ = creditor_select_options.creditor_select_options_func(data_input)
        except Exception as e:
            creditor_select_error_message_ = f"ошибка при создании фильтра по кредиторам: {e}"

        try:
            credit_contract_select_ = credit_contract_select_options_.credit_contract_select_options_func(data_input, creditor_select)
        except Exception as e:
            credit_contract_select_error_message_ = f"ошибка при создании фильтра по credit_contract: {e}"

        try:
            credit_year_select_ = credit_tab_year_select_opt.credit_tab_year_select_options_func(data_input)
        except Exception as e:
            credit_tab_year_select_error_message_ = f"ошибка при создании фильтра по годам: {e}"

        try:
            credit_tab_quarter_select_options_ = credit_tab_quarter_select_options_div.credit_tab_quarter_select_options_func(data_input)
        except Exception as e:
            credit_tab_quarter_select_error_message_ = f"ошибка при создании фильтра по кварталам: {e}"

        try:
            credit_tab_month_select_options_ = credit_tab_month_select_options_div.credit_tab_month_select_options_func(data_input)
        except Exception as e:
            credit_tab_month_select_error_message_ = f"ошибка при создании фильтра по месяцам: {e}"


        return [
            transhi_i_crediti_block_creditor_select_,
            transhi_i_crediti_block_creditor_select_options_error_message_,
            creditor_select_,
            creditor_select_error_message_,
            credit_contract_select_,
            credit_contract_select_error_message_,
            credit_year_select_,
            credit_tab_year_select_error_message_,
            credit_tab_quarter_select_options_,
            credit_tab_month_select_options_,
            credit_tab_month_select_error_message_,
            ]


def init_callback_leasing_inputs(dash_app):
    @dash_app.callback(
        [
            Output('agreement_type_year_select', 'options'),
            Output('agreement_type_year_select_options_error_message', 'children'),
            Output('leasing_payments_by_month_year_select', 'options'),
            Output('leasing_payments_by_month_options_error_message', 'children'),
            Output('leasing_payments_pie_chart_year_select', 'options'),
            Output('leasing_payments_pie_chart_year_select_error_message', 'children'),
            Output('top_customers_year_select', 'options'),
            Output('top_customers_year_select_error_message', 'children'),
            Output('top_independent_customers_year_select', 'options'),
            Output('top_independent_customers_year_select_error_message', 'children'),
            Output('top_products_year_select', 'options'),
            Output('top_products_year_select_error_message', 'children'),
            Output('interpayment_type_year_select', 'options'),
            Output('interpayment_type_year_select_error_message', 'children'),
            Output('leasing_object_type_year_select', 'options'),
            Output('leasing_object_type_select_options_error_message', 'children'),
            Output('leasing_rate_year_select', 'options'),
            Output('leasing_rate_year_select_error_message', 'children'),
            Output('leasing_rate_distribution_barchart_year_select', 'options'),
            Output('leasing_rate_distribution_barchart_year_select_error_message', 'children'),
            Output('credit_line_type_select', 'options'),
            Output('credit_line_type_select_error_message', 'children'),

         ],
        [
            Input('load_interval_2', 'n_intervals'),
            Input('data_input', 'value'),
        ]
    )
    def leasing_inputs(n_intervals, data_input):
        agreement_type_year_select_options = {1:1}
        agreement_type_year_select_options_error_message_ = ""
        leasing_payments_by_month_year_select_options = {1:1}
        leasing_payments_by_month_options_error_message_ = ""
        leasing_payments_pie_chart_year_select_options = {1:1}
        leasing_payments_pie_chart_year_select_error_message_ = ""
        top_customers_year_select_ = {1:1}
        top_customers_year_select_error_message_ = ""
        top_independent_customers_year_select_ = {1:1}
        top_independent_customers_year_select_error_message_ = ""
        top_products_year_select_ = {1:1}
        top_products_year_select_error_message_ = ""
        interpayment_type_year_select_ = {1:1}
        interpayment_type_year_select_error_message_ = ""
        leasing_object_type_year_select_ = {1:1}
        leasing_object_type_select_options_error_message_ = ""
        leasing_rate_year_select_ = {1:1}
        leasing_rate_year_select_error_message_ = ""
        leasing_rate_distribution_barchart_year_select_ = {1:1}
        leasing_rate_distribution_barchart_year_select_error_message_ = ""
        credit_line_type_select_ = {1:1}
        credit_line_type_select_error_message_ = ""

        if data_input == '1с_api':
            try:
                agreement_type_year_select_options = leasing_agreement_type_year_select_options_.leasing_agreement_type_year_select_options_func(data_input, leasing_table)
            except Exception as e:
                agreement_type_year_select_options_error_message_ = f"ошибка при создании фильтра по годам: {e}"

            try:
                leasing_payments_by_month_year_select_options = leasing_payments_by_month_year_select_options_.leasing_payments_by_month_year_select_options_func(data_input, leasing_table)
            except Exception as e:
                leasing_payments_by_month_options_error_message_ = f"ошибка при создании фильтра по годам: {e}"

            try:
                leasing_payments_pie_chart_year_select_options = leasing_payments_pie_chart_year_select_options_.leasing_payments_pie_chart_year_select_options_func(data_input, leasing_table)
            except Exception as e:
                leasing_payments_pie_chart_year_select_error_message_ = f"ошибка при создании фильтра по годам: {e}"

            try:
                top_customers_year_select_ = top_customers_year_select_options_.top_customers_year_select_options_func(data_input, leasing_table)
            except Exception as e:
                top_customers_year_select_error_message_ = f"ошибка при создании фильтра по годам: {e}"


            try:
                top_independent_customers_year_select_ = top_independent_customers_year_select_options.top_independent_customers_year_select_options_func(data_input, leasing_table)
            except Exception as e:
                top_independent_customers_year_select_error_message_ = f"ошибка при создании фильтра по годам: {e}"

            try:
                top_products_year_select_ = top_products_year_select_options.top_products_year_select_options_func(data_input, leasing_table)
            except Exception as e:
                top_products_year_select_error_message_ = f"ошибка при создании фильтра по годам: {e}"


            try:
                interpayment_type_year_select_ = interpayment_type_year_select_options.interpayment_type_year_select_optionsfunc(data_input, leasing_table)
            except Exception as e:
                interpayment_type_year_select_error_message_ = f"ошибка при создании фильтра по годам: {e}"


            try:
                leasing_object_type_year_select_ = leasing_object_type_year_select_options.leasing_object_type_year_select_options_func(data_input, leasing_table)
            except Exception as e:
                leasing_object_type_select_options_error_message_ = f"ошибка при создании фильтра по годам: {e}"

            try:
                leasing_rate_year_select_ = leasing_rate_year_select_options.leasing_rate_year_select_options_func(data_input, leasing_table)
            except Exception as e:
                leasing_rate_year_select_error_message_ = f"ошибка при создании фильтра по годам: {e}"
            try:
                leasing_rate_distribution_barchart_year_select_ = leasing_rate_distribution_barchart_year_select_options.leasing_rate_distribution_barchart_year_select_options_func(data_input, leasing_table)
            except Exception as e:
                leasing_rate_distribution_barchart_year_select_error_message_ = f"ошибка при создании фильтра по годам: {e}"
            try:
                credit_line_type_select_ = credit_line_type_select_options.credit_line_type_select_options_func(data_input)
            except Exception as e:
                credit_line_type_select_error_message_ = f"ошибка при создании фильтра по типам линий: {e}"



        return [agreement_type_year_select_options,
                agreement_type_year_select_options_error_message_,
                leasing_payments_by_month_year_select_options,
                leasing_payments_by_month_options_error_message_,
                leasing_payments_pie_chart_year_select_options,
                leasing_payments_pie_chart_year_select_error_message_,
                top_customers_year_select_,
                top_customers_year_select_error_message_,
                top_independent_customers_year_select_,
                top_independent_customers_year_select_error_message_,
                top_products_year_select_,
                top_products_year_select_error_message_,
                interpayment_type_year_select_,
                interpayment_type_year_select_error_message_,
                leasing_object_type_year_select_,
                leasing_object_type_select_options_error_message_,
                leasing_rate_year_select_,
                leasing_rate_year_select_error_message_,
                leasing_rate_distribution_barchart_year_select_,
                leasing_rate_distribution_barchart_year_select_error_message_,
                credit_line_type_select_,
                credit_line_type_select_error_message_
                ]


def init_callback_leasing_current_agreement_status_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('leasing_current_agreement_status_excel_download', 'data')
        ],
        [
            Input('leasing_payments_by_month_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('leasing_payments_by_month_year_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(leasing_payments_by_month_download_button, data_input, leasing_payments_by_month_year_select):
        data = {
            "Данные": ["Это заглушка"],
        }
        # load data into a DataFrame object:
        df = pd.DataFrame(data)
        if data_input == '1с_api':
            try:
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    query = f'SELECT current_agreement_status, year, month, month_first_date, SUM(payment_amount)  FROM {leasing_table} GROUP BY current_agreement_status, year, month ,month_first_date;'
                    df_raw = pd.read_sql(query, con)
                df_raw.rename(columns={
                    'sum': 'payment_amount'
                }, inplace=True)
                df = leasing_payments_by_month_download.leasing_payments_by_month_download_func(df_raw, data_input, leasing_payments_by_month_year_select)
            except:
                pass

        if leasing_payments_by_month_download_button:
            return [dcc.send_data_frame(df.to_excel, "agreement_status.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate


def init_callback_company_group_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('leasing_company_group_excel_download', 'data')
        ],
        [
            Input('top_company_groups_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('top_customers_year_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(top_company_groups_download_button, data_input, top_customers_year_select):
        data = {
            "Данные": ["Это заглушка"],
        }

        df = pd.DataFrame(data)
        if data_input == '1с_api':
            try:
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    query = f'SELECT current_agreement_status, company_group, year, month, SUM(payment_amount)  FROM {leasing_table} GROUP BY current_agreement_status, company_group, year, month;'
                    df_raw = pd.read_sql(query, con)
                df_raw.rename(columns={
                    'sum': 'payment_amount'
                }, inplace=True)
                df = top_company_group_download.top_company_group_download_func(df_raw, data_input, top_customers_year_select)
            except:
                pass

        if top_company_groups_download_button:
            return [dcc.send_data_frame(df.to_excel, "company groups.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate


def init_callback_independent_company_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('leasing_independent_company_excel_download', 'data')
        ],
        [
            Input('top_independent_company_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('top_independent_customers_year_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(top_independent_company_download_button, data_input, top_independent_customers_year_select):
        data = {
            "Данные": ["Это заглушка"],
        }

        df = pd.DataFrame(data)
        if data_input == '1с_api':
            try:
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    query = f'SELECT customer_name, year, SUM(payment_amount)  FROM {leasing_table} GROUP BY customer_name, year;'
                    df_raw = pd.read_sql(query, con)
                df_raw.rename(columns={
                    'sum': 'payment_amount'
                }, inplace=True)
                df = top_independent_company_download.top_independent_company_download_func(df_raw, data_input, top_independent_customers_year_select)
            except:
                pass

        if top_independent_company_download_button:
            return [dcc.send_data_frame(df.to_excel, "independent company.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate


def init_callback_top_products_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('leasing_top_products_excel_download', 'data')
        ],
        [
            Input('top_products_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('top_products_year_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(top_products_download_button, data_input, top_products_year_select):
        data = {
            "Данные": ["Это заглушка"],
        }

        df = pd.DataFrame(data)
        if data_input == '1с_api':
            try:
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    query = f'SELECT leasing_product, year, month, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_product, year, month;'
                    df_raw = pd.read_sql(query, con)
                df_raw.rename(columns={
                    'sum': 'payment_amount'
                }, inplace=True)
                df = top_products_download.top_products_download_func(df_raw, data_input, top_products_year_select)
            except:
                pass

        if top_products_download_button:
            return [dcc.send_data_frame(df.to_excel, "top products.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate


def init_callback_agreement_type_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('leasing_agreement_type_excel_download', 'data')
        ],
        [
            Input('agreement_type_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('agreement_type_year_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(agreement_type_download_button, data_input, agreement_type_year_select):
        data = {
            "Данные": ["Это заглушка"],
        }

        df = pd.DataFrame(data)
        if data_input == '1с_api':
            try:
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    query = f'SELECT agreement_type, year, SUM(payment_amount)  FROM {leasing_table} GROUP BY agreement_type, year;'
                    df_raw = pd.read_sql(query, con)
                df_raw.rename(columns={
                    'sum': 'payment_amount'
                }, inplace=True)
                df = agreement_type_download.agreement_type_download_func(df_raw, data_input, agreement_type_year_select)
            except:
                pass

        if agreement_type_download_button:
            return [dcc.send_data_frame(df.to_excel, "agreement type.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate


def init_callback_interpayment_type_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('leasing_interpayment_type_excel_download', 'data')
        ],
        [
            Input('interpayment_type_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('interpayment_type_year_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(interpayment_type_download_button, data_input, interpayment_type_year_select):
        data = {
            "Данные": ["Это заглушка"],
        }

        df = pd.DataFrame(data)
        if data_input == '1с_api':
            try:
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    query = f'SELECT leasing_category_2, year, month, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_category_2, year, month;'
                    df_raw = pd.read_sql(query, con)
                df_raw.rename(columns={
                    'sum': 'payment_amount'
                }, inplace=True)
                df_raw.rename(columns={
                    'leasing_category_2': 'interpayment_type'
                }, inplace=True)
                df = interpayment_type_download.interpayment_type_download_func(df_raw, data_input, interpayment_type_year_select)
            except Exception as e:
                print(f'ошибка при создании excel interpayment_type_download_func: {e}')

        if interpayment_type_download_button:
            return [dcc.send_data_frame(df.to_excel, "interpayment type.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate


def init_callback_leasing_object_type_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('leasing_object_type_excel_download', 'data')
        ],
        [
            Input('leasing_object_type_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('leasing_object_type_year_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(leasing_object_type_download_button, data_input, leasing_object_type_year_select):
        data = {
            "Данные": ["Это заглушка"],
        }

        df = pd.DataFrame(data)
        if data_input == '1с_api':
            try:
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    query = f'SELECT leasing_object_type, year, month, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_object_type, year, month;'
                    df_raw = pd.read_sql(query, con)
                df_raw.rename(columns={
                    'sum': 'payment_amount'
                }, inplace=True)
                df = leasing_object_type_download.leasing_object_type_download_func(df_raw, data_input, leasing_object_type_year_select)
            except:
                pass

        if leasing_object_type_download_button:
            return [dcc.send_data_frame(df.to_excel, "leasing object type.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate



def init_callback_leasing_rate_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('leasing_rate_excel_download', 'data')
        ],
        [
            Input('leasing_rate_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('leasing_rate_year_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(leasing_rate_download_button, data_input, leasing_rate_year_select):
        data = {
            "Данные": ["Это заглушка"],
        }

        df = pd.DataFrame(data)
        if data_input == '1с_api':
            try:
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    query = f'SELECT leasing_product, leasing_rate, year, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_product, leasing_rate, year;'
                    df_raw = pd.read_sql(query, con)
                df_raw.rename(columns={
                    'sum': 'payment_amount'
                }, inplace=True)
                df = leasing_rate_download.leasing_rate_download_download_func(df_raw, data_input, leasing_rate_year_select)
            except:
                pass

        if leasing_rate_download_button:
            return [dcc.send_data_frame(df.to_excel, "leasing rate.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate



def init_callback_leasing_rate_distribution_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('leasing_rate_distribution_barchart_download', 'data')
        ],
        [
            Input('leasing_rate_distribution_barchart_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('leasing_rate_distribution_barchart_year_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(leasing_rate_distribution_barchart_download_button, data_input, leasing_rate_distribution_barchart_year_select):
        data = {
            "Данные": ["Это заглушка"],
        }

        df = pd.DataFrame(data)
        if data_input == '1с_api':
            try:
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    query = f'SELECT leasing_rate, year, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_rate, year;'
                    df_raw = pd.read_sql(query, con)
                df_raw.rename(columns={
                    'sum': 'payment_amount'
                }, inplace=True)
                df = leasing_rate_distribution_download.leasing_rate_distribution_download_download_func(df_raw, data_input, leasing_rate_distribution_barchart_year_select)
            except:
                pass

        if leasing_rate_distribution_barchart_download_button:
            return [dcc.send_data_frame(df.to_excel, "leasing_rate_distribution.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate


def init_callback_credit_avrate_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('credit_avrate_download', 'data')
        ],
        [
            Input('credit_avrate_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('creditor_select', 'value'),
            Input('credit_contract_select', 'value'),
            Input('credit_year_select', 'value'),
            Input('credit_tab_quarter_select', 'value'),
            Input('credit_tab_month_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(credit_avrate_download_button, data_input, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):
        data = {
            "Данные": ["Это заглушка"],
        }
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == 'credit_avrate_download_button':

            df = pd.DataFrame(data)
            if data_input == '1с_api':
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    # query = 'SELECT *  FROM "creditDB";'
                    query = 'SELECT *  FROM "creditdb_2";'
                    df = pd.read_sql(query, con)
                df.rename(columns={
                    'sum': 'amount'
                }, inplace=True)
                updated_df = credit_avrate_download.credit_avrate_download_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)
                df = updated_df
            elif data_input == 'demo':
                df = convert_ral_excel_to_datafile.get_credit_type_df()
                if "int" in str(df['date'].dtype):
                    df['date'] = pd.to_datetime(df['date'], unit='ms')
                else:
                    df['date'] = pd.to_datetime(df['date'])


            return [dcc.send_data_frame(df.to_excel, "credit_avrate_data.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate


def init_callback_credit_bymonth_excel_download(dash_app):
    @dash_app.callback(
        [
            Output('credit_bymonth_download', 'data')
        ],
        [
            Input('btn_download_month_to_excel', 'n_clicks'),
            Input('data_input', 'value'),
            Input('creditor_select', 'value'),
            Input('credit_contract_select', 'value'),
            Input('credit_year_select', 'value'),
            Input('credit_tab_quarter_select', 'value'),
            Input('credit_tab_month_select', 'value'),
        ],
        prevent_initial_call=True,
    )
    def download_excel(btn_download_month_to_excel, data_input, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):
        data = {
            "Данные": ["Это заглушка"],
        }

        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == 'btn_download_month_to_excel':
            df = pd.DataFrame(data)
            if data_input == '1с_api':
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    # query = 'SELECT *  FROM "creditDB";'
                    query = 'SELECT *  FROM "creditdb_2";'
                    df = pd.read_sql(query, con)
                df.rename(columns={
                    'sum': 'amount'
                }, inplace=True)
                updated_df = credit_bymonth_download.credit_bymonth_download_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)
                df = updated_df
            elif data_input == 'demo':
                df = convert_ral_excel_to_datafile.get_credit_type_df()
                if "int" in str(df['date'].dtype):
                    df['date'] = pd.to_datetime(df['date'], unit='ms')
                else:
                    df['date'] = pd.to_datetime(df['date'])

        # if btn_download_month_to_excel:
            return [dcc.send_data_frame(df.to_excel, "credit_by_month_data.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate


def init_callback_credit_totals_by_today(dash_app):
    @dash_app.callback(
        [
            Output('credit_totals_by_today', 'children'),
            Output('credit_totals_by_today_below_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('transhi_i_crediti_block_creditor_select', 'value'),
            Input('credit_line_type_select', 'value'),
        ]
    )
    def credit_totals_by_today(data_input, transhi_i_crediti_block_creditor_select, credit_line_type_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА agreement_type #########
        df = pd.DataFrame()
        credit_totals_by_today_content = "txt"
        credit_totals_by_today_below_text_content = "credit_totals_by_today_below_text_content"
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT creditor, agreement_code, date, year, quarter, month_first_date, SUM(amount)  FROM "creditDB" GROUP BY creditor, agreement_code, date, year, quarter, month_first_date;'
                query = 'SELECT * FROM "creditdb_2";'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'amount'
            }, inplace=True)
            credit_totals_by_today_content = credit_totals_by_today_content_.credit_totals_by_today_content_func(df, transhi_i_crediti_block_creditor_select, credit_line_type_select)
            credit_totals_by_today_below_text_content = credit_totals_by_today_below_text_content_.credit_totals_by_today_below_text_content_func()


        return [
            credit_totals_by_today_content,
                    credit_totals_by_today_below_text_content
        ]


def init_callback_credit_taken_by_today(dash_app):
    @dash_app.callback(
        [
            Output('credit_taken_by_today', 'children'),
            Output('credit_taken_by_today_below_text', 'children'),

        ],
        [
            Input('data_input', 'value'),
            Input('transhi_i_crediti_block_creditor_select', 'value'),
            Input('credit_line_type_select', 'value'),
        ]
    )
    def credit_taken_by_today(data_input, transhi_i_crediti_block_creditor_select, credit_line_type_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА credit_taken_by_today #########
        credit_taken_by_today_content = 'txt'
        credit_taken_by_today_below_text_content = 'txt'
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT creditor, agreement_code,transh_id, credit_tranch_date,credit_volume, date, year, quarter, month_first_date, SUM(amount)  FROM "creditDB" GROUP BY creditor, agreement_code,transh_id, credit_tranch_date,credit_volume, date, year, quarter, month_first_date;'
                query = 'SELECT * FROM "creditdb_2";'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'amount'
            }, inplace=True)

            credit_taken_by_today_content = credit_taken_by_today_content_.credit_taken_by_today_content_func(df, transhi_i_crediti_block_creditor_select, credit_line_type_select)
            credit_taken_by_today_below_text_content = credit_taken_by_today_below_text_content_.credit_taken_by_today_below_text_content_func()

        return [credit_taken_by_today_content,
                credit_taken_by_today_below_text_content
                ]


def init_callback_credit_limit_remain_by_today(dash_app):
    @dash_app.callback(
        [
            Output('credit_limit_remain_by_today', 'children'),
            Output('credit_limit_remain_by_today_below_text', 'children'),
            Output('credit_limit_remainings_check', 'children'),


        ],
        [
            Input('data_input', 'value'),
            Input('transhi_i_crediti_block_creditor_select', 'value'),
            Input('credit_line_type_select', 'value'),

        ]
    )
    def credit_limit_remain_by_today(data_input, transhi_i_crediti_block_creditor_select, credit_line_type_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА  #########
        credit_limit_remain_by_today_content = 'txt'
        credit_limit_remain_by_today_below_text_content = 'txt'
        credit_limit_remainings_check_content_ = ""
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT *  FROM "creditDB";'
                query = 'SELECT *  FROM "creditdb_2";'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'amount'
            }, inplace=True)


            credit_limit_remain_by_today_content = credit_limit_remain_by_today_content_.credit_limit_remain_by_today_content_func(df, transhi_i_crediti_block_creditor_select, credit_line_type_select)[0]

            credit_limit_by_today_content = credit_limit_remain_by_today_content_.credit_limit_remain_by_today_content_func(df, transhi_i_crediti_block_creditor_select, credit_line_type_select)[1]
            credit_limit_remainings_check_content_ = credit_limit_remain_by_today_content_.credit_limit_remain_by_today_content_func(df, transhi_i_crediti_block_creditor_select, credit_line_type_select)[2]
            credit_limit_remain_by_today_below_text_content = credit_limit_remain_by_today_below_text_content_.credit_limit_remain_by_today_below_text_content_func()

        return [
            credit_limit_remain_by_today_content,
            credit_limit_remain_by_today_below_text_content,
            credit_limit_remainings_check_content_
                ]




def init_callback_taken_vs_remain_v2_div(dash_app):
    @dash_app.callback(
        [
            Output('taken_vs_remain_graph_v2_div', 'children'),
            Output('taken_vs_remain_v2_func_check', 'children'),
            Output('credit_limit_remain_by_today', 'children'),
            Output('credit_limit_remain_by_today_below_text', 'children'),


        ],
        [
            Input('data_input', 'value'),
            Input('transhi_i_crediti_block_creditor_select', 'value'),
            Input('credit_line_type_select', 'value'),
        ]
    )
    def taken_vs_remain_v2(data_input, transhi_i_crediti_block_creditor_select, credit_line_type_select):
        output = '-'
        taken_vs_remain_v5_func_check_ = ""
        credit_limit_remain_by_today_content = ""
        credit_limit_remain_by_today_below_text_content = ""

        try:
            output = taken_vs_remain_v5_.taken_vs_remain_v5_func(data_input, transhi_i_crediti_block_creditor_select,
                                                             credit_line_type_select)[0]
            taken_vs_remain_v5_func_check_ = taken_vs_remain_v5_.taken_vs_remain_v5_func(data_input, transhi_i_crediti_block_creditor_select,
                                        credit_line_type_select)[1]
            free_remaining = \
            taken_vs_remain_v5_.taken_vs_remain_v5_func(data_input, transhi_i_crediti_block_creditor_select,
                                                        credit_line_type_select)[2]

            # credit_limit_remain_by_today_content = credit_limit_remain_by_today_content_.credit_limit_remain_by_today_content_func(free_remaining)

            credit_limit_remain_by_today_content = format(free_remaining, '.3f')


            credit_limit_remain_by_today_below_text_content = credit_limit_remain_by_today_below_text_content_.credit_limit_remain_by_today_below_text_content_func()

        except Exception as e:
            # pass
            output = str(f'output error: {e}')

        taken_vs_remain_v5_func_check_ = ""
        return [output,
                taken_vs_remain_v5_func_check_,
                credit_limit_remain_by_today_content,
                credit_limit_remain_by_today_below_text_content,

                ]



def init_callback_credit_taken_vs_remain(dash_app):
    @dash_app.callback(
        [
            Output('taken_vs_remain_graph_div', 'children'),

        ],
        [
            Input('data_input', 'value'),
            Input('transhi_i_crediti_block_creditor_select', 'value'),
        ]
    )
    def credit_taken_vs_remain(data_input, transhi_i_crediti_block_creditor_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА credit_totals_by_today #########
        taken_vs_remain_graph_div_content = 'txt'
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT *  FROM "creditDB";'
                query = 'SELECT *  FROM "creditdb_2";'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'amount'
            }, inplace=True)

            taken_vs_remain_graph_div_content = taken_vs_remain_graph_div_content_.taken_vs_remain_graph_div_content_func(df, transhi_i_crediti_block_creditor_select)

        return [
            taken_vs_remain_graph_div_content
            ]


def init_callback_credit_credit_treemap(dash_app):
    @dash_app.callback(
        [
            Output('credit_treemap_div', 'children'),
            Output('treeview_period_text_div', 'children'),

        ],
        [
            Input('data_input', 'value'),
            Input('creditor_select', 'value'),
            Input('credit_contract_select', 'value'),
            Input('credit_year_select', 'value'),
            Input('credit_tab_quarter_select', 'value'),
            Input('credit_tab_month_select', 'value'),


        ]
    )
    def credit_credit_treemap(data_input, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА credit_totals_by_today #########
        treeview_period_text_div_ = ""
        credit_treemap_div_content = "No data"
        df = pd.DataFrame()
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT *  FROM "creditDB";'
                query = 'SELECT *  FROM "creditdb_2";'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'amount'
            }, inplace=True)
        elif data_input == 'demo':
            df = convert_ral_excel_to_datafile.get_credit_type_df()
            if "int" in str(df['date'].dtype):
                df['date'] = pd.to_datetime(df['date'], unit='ms')
            else:
                df['date'] = pd.to_datetime(df['date'])

        try:
            credit_treemap_div_content = credit_treemap_div_content_.credit_treemap_div_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[0]
        except:
            pass

        try:
            treeview_period_text_first_date = credit_treemap_div_content_.credit_treemap_div_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[1]

            treeview_period_text_last_date = credit_treemap_div_content_.credit_treemap_div_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[2]
            treeview_period_text_div_ = period_text.credit_grapf_period_text_func(treeview_period_text_first_date, treeview_period_text_last_date)
        except:
            pass

        return [
            credit_treemap_div_content,
            treeview_period_text_div_,
            ]


def init_callback_credit_credit_av_rate(dash_app):
    @dash_app.callback(
        [
            Output('credit_av_rate_graph_div', 'children'),
            Output('credit_av_rate_text_div', 'children'),



        ],
        [
            Input('data_input', 'value'),
            Input('creditor_select', 'value'),
            Input('credit_contract_select', 'value'),
            Input('credit_year_select', 'value'),
            Input('credit_tab_quarter_select', 'value'),
            Input('credit_tab_month_select', 'value'),


        ]
    )
    def credit_credit_avrate(data_input, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА avrate #########
        credit_av_rate_text_div_ = 'no data'
        df = pd.DataFrame()
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT *  FROM "creditDB";'
                query = 'SELECT *  FROM "creditdb_2";'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'amount'
            }, inplace=True)
        elif data_input == 'demo':
            df = convert_ral_excel_to_datafile.get_credit_type_df()
            if "int" in str(df['date'].dtype):
                df['date'] = pd.to_datetime(df['date'], unit='ms')
            else:
                df['date'] = pd.to_datetime(df['date'])

        credit_av_rate_graph_div_content = html.Div(html.P("Нет данных"))
        try:
            credit_av_rate_graph_div_content = credit_av_rate_graph_div_content_.credit_av_rate_graph_div_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[0]

        except Exception as e:
            print(e)

        credit_av_rate_period_text_first_date = credit_av_rate_graph_div_content_.credit_av_rate_graph_div_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[1]
        credit_av_rate_period_text_last_date = credit_av_rate_graph_div_content_.credit_av_rate_graph_div_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[2]
        try:
            credit_av_rate_text_div_ = period_text.credit_grapf_period_text_func(credit_av_rate_period_text_first_date,
                                                                             credit_av_rate_period_text_last_date)
        except:
            pass
        check_output = credit_av_rate_graph_div_content_.credit_av_rate_graph_div_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[3]
        check_output = ""

        return [

            credit_av_rate_graph_div_content,
            credit_av_rate_text_div_,
            ]




def init_callback_credit_remainings_bar_graph(dash_app):
    @dash_app.callback(
        [
            Output('credit_remainings_bar_graph', 'figure'),
            Output('remains_bar_chart_period_text', 'children'),
            Output('credit_remainings_bar_graph', 'clickData'),
            Output('back-button', 'style'),  # to hide/unhide the back button
        ],
        [
            Input('data_input', 'value'),
            Input('creditor_select', 'value'),
            Input('credit_contract_select', 'value'),
            Input('credit_year_select', 'value'),
            Input('credit_tab_quarter_select', 'value'),
            Input('credit_tab_month_select', 'value'),
            Input('credit_remainings_bar_graph', 'clickData'),  # for getting the vendor name from graph
            Input('back-button', 'n_clicks'),
        ]
    )
    def credit_remainings_bar_graph(data_input, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select, click_data, n_clicks):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА avrate #########
        remains_bar_chart_period_text_ = ""
        df = pd.DataFrame()
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT *  FROM "creditDB";'
                query = 'SELECT *  FROM "creditdb_2";'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'amount'
            }, inplace=True)
        elif data_input == 'demo':
            df = convert_ral_excel_to_datafile.get_credit_type_df()
            if "int" in str(df['date'].dtype):
                df['date'] = pd.to_datetime(df['date'], unit='ms')
            else:
                df['date'] = pd.to_datetime(df['date'])

        credit_remainings_bar_graph_content = html.Div(html.P("Нет данных"))
        try:
            credit_remainings_bar_graph_content = credit_remainings_bar_graph_content_.credit_remainings_bar_graph_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[0]

        except Exception as e:
            print(e)
        try:
            remains_bar_chart_period_text_first_date = credit_remainings_bar_graph_content_.credit_remainings_bar_graph_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[1]
            remains_bar_chart_period_text_last_date = credit_remainings_bar_graph_content_.credit_remainings_bar_graph_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[2]

            remains_bar_chart_period_text_ = period_text.credit_grapf_period_text_func(remains_bar_chart_period_text_first_date, remains_bar_chart_period_text_last_date)
        except:
            pass
        ctx = dash.callback_context

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        check_trigger = 'by_banks' # проверка в каком графике мы находимся

        if trigger_id == 'back-button':
            check_trigger = 'by_banks'
            return [
                credit_remainings_bar_graph_content,
                remains_bar_chart_period_text_,
                click_data,
                {'display': 'none'},
            ]


        if trigger_id == 'credit_remainings_bar_graph':
            bank = click_data['points'][0]['label']
            list_of_banks = list(df['creditor'].unique())

            if click_data is not None and bank in list_of_banks:
                # график погашения по годам в кликнутом банке

                credit_remainings_bar_graph_content = credit_remainings_by_years_bar_graph_content_.credit_remainings_by_years_bar_graph_content_func(df, bank, creditor_select,
                                                                                              credit_contract_select,
                                                                                              credit_year_select,
                                                                                              credit_tab_quarter_select,
                                                                                              credit_tab_month_select)

                click_data = None

                return [
                    credit_remainings_bar_graph_content,
                    remains_bar_chart_period_text_,
                    click_data,
                    {'display':'block'},
                ]



        return [
            credit_remainings_bar_graph_content,
            remains_bar_chart_period_text_,
            click_data,
            {'display':'none'},
            ]



def init_callback_credit_remainings_piechart(dash_app):
    @dash_app.callback(
        [
            Output('credit_remainings_piechart_graph', 'children'),
            Output('period_text_piechart', 'children'),

        ],
        [
            Input('data_input', 'value'),
            Input('creditor_select', 'value'),
            Input('credit_contract_select', 'value'),
            Input('credit_year_select', 'value'),
            Input('credit_tab_quarter_select', 'value'),
            Input('credit_tab_month_select', 'value'),


        ]
    )
    def credit_credit_remainings_piechart(data_input, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА avrate #########
        df = pd.DataFrame()
        credit_remainings_piechart_period_text_ = ""
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT *  FROM "creditDB";'
                query = 'SELECT *  FROM "creditdb_2";'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'amount'
            }, inplace=True)
        elif data_input == 'demo':
            df = convert_ral_excel_to_datafile.get_credit_type_df()
            if "int" in str(df['date'].dtype):
                df['date'] = pd.to_datetime(df['date'], unit='ms')
            else:
                df['date'] = pd.to_datetime(df['date'])

        try:
            credit_remainings_piechart_graph = credit_remainings_piechart_graph_content_.credit_remainings_piechart_graph_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[0]
        except Exception as e:
            credit_remainings_piechart_graph = html.Div(f'{e}')
        try:
            credit_remainings_piechart_period_text_first_date = credit_remainings_piechart_graph_content_.credit_remainings_piechart_graph_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[1]
            credit_remainings_piechart_period_text_last_date = credit_remainings_piechart_graph_content_.credit_remainings_piechart_graph_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[2]

            credit_remainings_piechart_period_text_ = period_text.credit_grapf_period_text_func(
                credit_remainings_piechart_period_text_first_date,
                credit_remainings_piechart_period_text_last_date)
        except:
            pass

        return [

            credit_remainings_piechart_graph,
            credit_remainings_piechart_period_text_,
            ]


def init_callback_credit_next_payments_by_credittype(dash_app):
    @dash_app.callback(
        [
            Output('credit_next_payments_by_credittype_div', 'children'),
            Output('credit_grapf_period_text_div', 'children'),

        ],
        [
            Input('data_input', 'value'),
            Input('creditor_select', 'value'),
            Input('credit_contract_select', 'value'),
            Input('credit_year_select', 'value'),
            Input('credit_tab_quarter_select', 'value'),
            Input('credit_tab_month_select', 'value'),
            Input('year_month_selector', 'value'),


        ]
    )
    def credit_credit_credit_next_payments_by_credittype(data_input, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select, year_month_selector):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА avrate #########
        credit_grapf_period_text_div = ""
        df = pd.DataFrame()
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT *  FROM "creditDB";'
                query = 'SELECT *  FROM "creditdb_2";'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'amount'
            }, inplace=True)
        elif data_input == 'demo':
            df = convert_ral_excel_to_datafile.get_credit_type_df()
            if "int" in str(df['date'].dtype):
                df['date'] = pd.to_datetime(df['date'], unit='ms')
            else:
                df['date'] = pd.to_datetime(df['date'])

        try:
            fig_credit_type = fig_credit_type_month.fig_credit_type_month_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[0]

            credit_grapf_text_first_date = fig_credit_type_month.fig_credit_type_month_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[1]
            credit_grapf_text_last_date = fig_credit_type_month.fig_credit_type_month_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)[2]

            credit_grapf_period_text_div = period_text.credit_grapf_period_text_func(credit_grapf_text_first_date, credit_grapf_text_last_date)


            if year_month_selector == "years":
                fig_credit_type = fig_credit_type_year.fig_credit_type_year_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select)
            fig_credit_type_div = dcc.Graph(figure=fig_credit_type, config = {'displayModeBar': False})
        except Exception as e:
            fig_credit_type_div = html.P(f"Нет данных. Ошибка: {e}")

        return [
            fig_credit_type_div,
            credit_grapf_period_text_div,
            ]




def init_callback_leasing_current_agreement_status(dash_app):
    @dash_app.callback(
        [
            Output('leasing_payments_by_month_v2', 'children'),
            Output('leasing_payments_by_month_v2_period_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('leasing_payments_by_month_year_select', 'value'),

        ]
    )
    def leasing_current_agreement_status(data_input, leasing_payments_by_month_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА agreement_type #########
        leasing_payments_by_month_v2_div = 'txt'
        leasing_payments_by_month_v2_period_text_ = 'txt'
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                query = f'SELECT current_agreement_status, year, month, month_first_date, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY current_agreement_status, year, month ,month_first_date, date;'
                df_current_agreement_status = pd.read_sql(query, con)
            df_current_agreement_status.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)


            leasing_payments_by_month_v2_div = leasing_payments_by_month_v3_div_.leasing_payments_by_month_v3_div_func(df_current_agreement_status, data_input, leasing_payments_by_month_year_select)[0]
            leasing_payments_by_month_v2_period_text_ = leasing_payments_by_month_v3_div_.leasing_payments_by_month_v3_div_func(df_current_agreement_status, data_input, leasing_payments_by_month_year_select)[1]

        return leasing_payments_by_month_v2_div, \
            leasing_payments_by_month_v2_period_text_, \


def init_callback_payments_pie_chart(dash_app):
    @dash_app.callback(
        [
            Output('leasing_payments_pie_chart_v2', 'children'),
            Output('leasing_payments_pie_chart_v2_period_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('leasing_payments_pie_chart_year_select', 'value'),

        ]
    )
    def leasing_current_agreement_status(data_input, leasing_payments_pie_chart_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА agreement_type #########
        leasing_payments_pie_chart_div = 'txt'
        leasing_payments_pie_chart_v2_period_text_ = 'txt'
        if data_input == '1с_api':

            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                query = f'SELECT current_agreement_status, year, month, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY current_agreement_status, year, month, date;'
                df_current_agreement_status = pd.read_sql(query, con)
            df_current_agreement_status.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            leasing_payments_pie_chart_div = leasing_payments_pie_chart_v3_div_.leasing_payments_pie_chart_v3_div_func(df_current_agreement_status, data_input, leasing_payments_pie_chart_year_select)[0]
            leasing_payments_pie_chart_v2_period_text_ = leasing_payments_pie_chart_v3_div_.leasing_payments_pie_chart_v3_div_func(df_current_agreement_status, data_input, leasing_payments_pie_chart_year_select)[1]

        return [
            leasing_payments_pie_chart_div,
            leasing_payments_pie_chart_v2_period_text_
            ]


def init_callback_top_group_companies(dash_app):
    @dash_app.callback(
        [
            Output('top_group_customers_barchart_v2', 'children'),
            Output('top_group_customers_barchart_v2_period_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('top_customers_year_select', 'value'),

        ]
    )
    def top_group_companies(data_input, top_customers_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА top_customers #########
        top_group_customers_barchart_v2_ = 'txt'
        top_group_customers_barchart_v2_period_text_ = 'txt'
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                query = f'SELECT current_agreement_status, company_group, year, month, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY current_agreement_status, company_group, year, month, date;'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            top_group_customers_barchart_v2_ = top_group_customers_barchart_v2_div_.top_group_customers_barchart_v2__div_func(df, data_input, top_customers_year_select)[0]
            top_group_customers_barchart_v2_period_text_ = top_group_customers_barchart_v2_div_.top_group_customers_barchart_v2__div_func(df, data_input, top_customers_year_select)[1]

        return [
            top_group_customers_barchart_v2_,
            top_group_customers_barchart_v2_period_text_,
            ]


def init_callback_top_independent_companies(dash_app):
    @dash_app.callback(
        [
            Output('top_independent_customers_barchart_v2', 'children'),
            Output('top_independent_customers_barchart_v2_period_text', 'children'),


        ],
        [
            Input('data_input', 'value'),
            Input('top_independent_customers_year_select', 'value'),

        ]
    )
    def top_group_companies(data_input, top_independent_customers_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА independent_customers #########

        top_independent_customers_barchart_v2_ = 'txt'
        top_independent_customers_barchart_v2_period_text_ = 'txt'


        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT current_agreement_status, company_group, customer_name, year, month, SUM(payment_amount)  FROM "independent_company" GROUP BY current_agreement_status, company_group, customer_name, year, month;'
                query = f'SELECT current_agreement_status, company_group, customer_name, year, month, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY current_agreement_status, company_group, customer_name, year, month, date;'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            top_independent_customers_barchart_v2_ = top_independent_customers_barchart_v2_div_.top_independent_customers_barchart_v2_div_func(df, data_input, top_independent_customers_year_select)[0]
            top_independent_customers_barchart_v2_period_text_ = top_independent_customers_barchart_v2_div_.top_independent_customers_barchart_v2_div_func(df, data_input, top_independent_customers_year_select)[1]



        return [
            top_independent_customers_barchart_v2_,
            top_independent_customers_barchart_v2_period_text_,


            ]


def init_callback_top_products(dash_app):
    @dash_app.callback(
        [
            Output('leasing_products_barchart', 'children'),
            Output('leasing_products_period_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('top_products_year_select', 'value'),

        ]
    )
    def top_group_companies(data_input, top_products_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА top_products #########
        leasing_products_barchart_='txt'
        leasing_products_period_text_ = 'txt'

        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT leasing_product, year, month, SUM(payment_amount)  FROM "leasing_product" GROUP BY leasing_product, year, month;'
                query = f'SELECT leasing_product, year, month, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_product, year, month, date;'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            leasing_products_barchart_ = leasing_products_barchart_div.leasing_products_barchart_div_func(df, data_input, top_products_year_select)[0]
            leasing_products_period_text_ = leasing_products_barchart_div.leasing_products_barchart_div_func(df, data_input, top_products_year_select)[1]

        return [
            leasing_products_barchart_,
            leasing_products_period_text_,
            ]


def init_callback_agreement_type(dash_app):
    @dash_app.callback(
        [
            Output('leasing_agreement_type_barchart', 'children'),
            Output('leasing_agreement_type_barchart_period_text', 'children'),


        ],
        [
            Input('data_input', 'value'),
            Input('agreement_type_year_select', 'value'),

        ]
    )
    def agreement_type(data_input, agreement_type_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА agreement_type#########
        leasing_agreement_type_barchart_ = 'txt'
        leasing_agreement_type_barchart_period_text_ = 'txt'

        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                query = f'SELECT agreement_type, year, month, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY agreement_type, year, month, date;'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            leasing_agreement_type_barchart_ = leasing_agreement_type_barchart_div.agreement_type_barchart_div_func(df, data_input, agreement_type_year_select)[0]
            leasing_agreement_type_barchart_period_text_ = leasing_agreement_type_barchart_div.agreement_type_barchart_div_func(df, data_input, agreement_type_year_select)[1]

        return [
            leasing_agreement_type_barchart_,
            leasing_agreement_type_barchart_period_text_,
            ]

def init_callback_interpayment_type(dash_app):
    @dash_app.callback(
        [
            Output('interpayment_type_barchart', 'children'),
            Output('interpayment_type_period_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('interpayment_type_year_select', 'value'),

        ]
    )
    def interpayment_type(data_input, interpayment_type_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА interpayment_type#########
        interpayment_type_barchart_ = 'txt'
        interpayment_type_period_text_ = 'txt'
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT interpayment_type, year, month, SUM(payment_amount)  FROM "interpayment_type" GROUP BY interpayment_type, year, month;'
                query = f'SELECT leasing_category_2, year, month, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_category_2, year, month, date;'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            interpayment_type_barchart_ = interpayment_type_barchart_div.interpayment_type_barchart_div_func(df, data_input, interpayment_type_year_select)[0]
            interpayment_type_period_text_ = interpayment_type_barchart_div.interpayment_type_barchart_div_func(df, data_input, interpayment_type_year_select)[1]

        return [
            interpayment_type_barchart_,
            interpayment_type_period_text_,
            ]



def init_callback_leasing_object_type(dash_app):
    @dash_app.callback(
        [
            Output('leasing_object_type_barchart', 'children'),
            Output('leasing_object_type_barchart_period_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('leasing_object_type_year_select', 'value'),

        ]
    )
    def leasing_object_type(data_input, leasing_object_type_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА leasing_object_type#########
        leasing_object_type_barchart_ = 'txt'
        leasing_object_type_period_text_ = 'txt'
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                # query = 'SELECT leasing_object_type, year, month, SUM(payment_amount)  FROM "leasing_object_type" GROUP BY leasing_object_type, year, month;'
                query = f'SELECT leasing_object_type, year, month, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_object_type, year, month, date;'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            leasing_object_type_barchart_ = leasing_object_type_barchart_div.leasing_object_type_barchart_div_func(df, data_input, leasing_object_type_year_select)[0]
            leasing_object_type_period_text_ = leasing_object_type_barchart_div.leasing_object_type_barchart_div_func(df, data_input, leasing_object_type_year_select)[1]

        return [
            leasing_object_type_barchart_,
            leasing_object_type_period_text_,
            ]



def init_callback_leasing_rate(dash_app):
    @dash_app.callback(
        [
            Output('leasing_rate_barchart', 'children'),
            Output('leasing_rate_period_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('leasing_rate_year_select', 'value'),

        ]
    )
    def leasing_rate(data_input, leasing_rate_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА leasing_rate#########
        leasing_rate_barchart_ = 'txt'
        leasing_rate_period_text_ = 'txt'
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                query = f'SELECT leasing_product, leasing_rate, year, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_product, leasing_rate, year, date;'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            leasing_rate_barchart_ = leasing_rate_barchart_div.leasing_rate_barchart_div_func(df, data_input, leasing_rate_year_select)[0]
            leasing_rate_period_text_ = leasing_rate_barchart_div.leasing_rate_barchart_div_func(df, data_input, leasing_rate_year_select)[1]

        return [
            leasing_rate_barchart_,
            leasing_rate_period_text_,
            ]



def init_callback_leasing_rate_distribution_barchart(dash_app):
    @dash_app.callback(
        [
            Output('leasing_rate_distribution_barchart', 'children'),
            Output('leasing_rate_distribution_barchart_period_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('leasing_rate_distribution_barchart_year_select', 'value'),

        ]
    )
    def leasing_rate(data_input, leasing_rate_distribution_barchart_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА leasing_rate#########
        leasing_rate_distribution_barchart_ = 'txt'
        leasing_rate_distribution_barchart_period_text_ = 'txt'

        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                query = f'SELECT leasing_rate, year, date, SUM(payment_amount)  FROM {leasing_table} GROUP BY leasing_rate, year, date;'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            leasing_rate_distribution_barchart_ = leasing_rate_distribution_barchart_div.leasing_rate_distribution_barchart_div_func(df, data_input, leasing_rate_distribution_barchart_year_select)[0]
            leasing_rate_distribution_barchart_period_text_ = leasing_rate_distribution_barchart_div.leasing_rate_distribution_barchart_div_func(df, data_input, leasing_rate_distribution_barchart_year_select)[1]

        return [
            leasing_rate_distribution_barchart_,
            leasing_rate_distribution_barchart_period_text_,
            ]


def init_callback_leasing_rate_distribution_density_barchart(dash_app):
    @dash_app.callback(
        [
            Output('leasing_rate_distribution_density', 'children'),
            Output('leasing_rate_distribution_density_period_text', 'children'),
        ],
        [
            Input('data_input', 'value'),
            Input('leasing_rate_distribution_density_year_select', 'value'),

        ]
    )
    def leasing_rate_distribution(data_input, leasing_rate_distribution_density_year_select):
        ############################# ПОЛУЧЕНИЕ ДАННЫХ И ПОСТРОЕНИЕ ВИДЖЕТА leasing_rate_distribution_density#########
        leasing_rate_distribution_density_ = 'txt'
        leasing_rate_distribution_density_period_text_ = 'txt'
        if data_input == '1с_api':
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = create_engine(url_db, pool_recycle=3600)
            with engine.connect() as con:
                query = 'SELECT leasing_rate, year, COUNT(leasing_rate)  FROM "leasing_temp_db_2" GROUP BY leasing_rate, year;'
                df = pd.read_sql(query, con)
            df.rename(columns={
                'count': 'leasing_rate_count'
            }, inplace=True)

            leasing_rate_distribution_density_ = leasing_rate_distribution_density_div.leasing_rate_distribution_density_div_func(df, data_input, leasing_rate_distribution_density_year_select)[0]
            leasing_rate_distribution_density_period_text_ = leasing_rate_distribution_density_div.leasing_rate_distribution_density_div_func(df, data_input, leasing_rate_distribution_density_year_select)[1]

        return [
            leasing_rate_distribution_density_,
            leasing_rate_distribution_density_period_text_,
            ]








def init_callback_download_excel_credit_by_banks_month_credit(dash_app):
    @dash_app.callback(
        [
            Output('credit_download_excel_credit_by_banks_month_download', 'data')
        ],
        [
            Input('credit_by_bank_download_button', 'n_clicks'),
            Input('data_input', 'value'),
            Input('transhi_i_crediti_block_creditor_select', 'value'),

        ],
        prevent_initial_call=True,
    )
    def download_excel(credit_by_bank_download_button, data_input, transhi_i_crediti_block_creditor_select):
        data = {
            "Данные": ["Это заглушка"],
        }
        df = pd.DataFrame()
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == 'credit_by_bank_download_button':
            df = pd.DataFrame(data)
            if data_input == '1с_api':
                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = create_engine(url_db, pool_recycle=3600)
                with engine.connect() as con:
                    # query = 'SELECT *  FROM "creditDB";'
                    query = 'SELECT *  FROM "creditdb_2";'
                    df = pd.read_sql(query, con)
                df.rename(columns={
                    'sum': 'amount'
                }, inplace=True)
                updated_df = credit_by_banks_month.credit_by_banks_month_func(data_input, transhi_i_crediti_block_creditor_select)
                df = updated_df
            elif data_input == 'demo':
                df = convert_ral_excel_to_datafile.get_credit_type_df()
                if "int" in str(df['date'].dtype):
                    df['date'] = pd.to_datetime(df['date'], unit='ms')
                else:
                    df['date'] = pd.to_datetime(df['date'])


        # df_to_excel = credit_by_bank_download_excel_data_df.credit_by_bank_download_excel_data_df_func(data)

        if credit_by_bank_download_button:
            return [dcc.send_data_frame(df.to_excel, "credit data.xlsx", sheet_name="Sheet_name_1", index=False)]
        raise PreventUpdate







