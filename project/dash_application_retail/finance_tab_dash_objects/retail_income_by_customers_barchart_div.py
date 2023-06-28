import datetime
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
from dash import dash_table
import os
from sqlalchemy import create_engine
import dash_application_retail.colors as colors_file

def retail_income_by_customers_barchart_div_func(retail_customer_select):
    check = ""
    graph_output = ""
    first_date = ''
    last_date = ''

    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    with engine.connect() as con:
        query = 'SELECT *  FROM "retail";'
        df = pd.read_sql(query, con)

    df['year'] = df['year'].astype(float)
    df['year'] = df['year'].astype('int')
    # режем df по фильтрам

    # фильтр по customer_name ###########################################################################
    customer_name_full_list = list(df['customer_name'].unique())
    customer_name_filter = customer_name_full_list
    if retail_customer_select:
        if 'list' in str(type(retail_customer_select)):
            customer_name_filter = retail_customer_select
        else:
            customer_name_filter = list(retail_customer_select)

    # режем выборку по customer_name
    df = df.loc[df['customer_name'].isin(customer_name_filter)]



    # фильтр по годам ###########################################################################
    # year_full_list = list(df['year'].unique())
    # year_filter = year_full_list
    # if credit_year_select:
    #     if 'list' in str(type(credit_year_select)):
    #         year_filter = credit_year_select
    #     else:
    #         year_filter = [credit_year_select]
    #
    # year_filter_int_list = []
    # for year in year_filter:
    #     year = int(year)
    #     if year >= int(datetime.datetime.now().year):
    #         year_filter_int_list.append(year)
    #
    # # режем выборку по годам
    # df = df.loc[df['year'].isin(year_filter_int_list)]
    #####################################################################################################

    # фильтр по кварталам ###########################################################################
    # quarter_full_list = list(df['quarter'].unique())
    # quarter_filter = quarter_full_list
    # if credit_tab_quarter_select:
    #     if 'list' in str(type(credit_tab_quarter_select)):
    #         quarter_filter = credit_tab_quarter_select
    #     else:
    #         quarter_filter = [credit_tab_quarter_select]
    #
    # quarter_filter_int_list = []
    # for quarter in quarter_filter:
    #     quarter = int(quarter)
    #     quarter_filter_int_list.append(quarter)
    #
    # # режем выборку по кварталам
    # df = df.loc[df['quarter'].isin(quarter_filter_int_list)]
    #####################################################################################################

    # фильтр по месяцам ###########################################################################
    # month_full_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    # month_filter = month_full_list
    # if credit_tab_month_select:
    #     if 'list' in str(type(credit_tab_month_select)):
    #         month_filter = credit_tab_month_select
    #     else:
    #         month_filter = [credit_tab_month_select]
    #
    # month_filter_int_list = []
    # for month in month_filter:
    #     month = int(month)
    #     month_filter_int_list.append(month)
    #
    # df['date_2'] = pd.to_datetime(df['date'])
    # if "int" in str(df['date'].dtype):
    #     df['date_2'] = pd.to_datetime(df['date'], unit='ms')
    # df['month'] = df['date_2'].dt.month
    # # режем выборку по месяцам
    # df = df.loc[df['month'].isin(month_filter_int_list)]
    #####################################################################################################



    today = datetime.datetime.now()

    try:
        df = df.loc[df['date'] >= today]
    except:
        df = df.loc[df['date'] >= today.date()]


    # print('len_df: ', len(df))
    if len(df)>0:


        # необходимо посчитать текущий остаток обязательств
        # это сумма по полю amount в будущее



        df = df.loc[:, ['date', 'customer_name', 'credit_tranch_date', 'credit_annual_rate', 'credit_amount', 'agreement_code', 'amount']]

        customer_name_list = list(df['customer_name'].unique())



        # data = df.to_dict('records')
        # credit_datatable = dash_table.DataTable(
        #
        #     data=data,)

        result_list = []


        # Поллучаем колонки с выручкой клиентов

        revenue_by_customers_df = df.groupby(['customer_name'], as_index=False).agg({'amount': 'sum'})
        revenue_by_customers_df.sort_values(['amount'], ascending=True, inplace=True)
        revenue_by_customers_df = revenue_by_customers_df.head(20)


        average_avount = revenue_by_customers_df['amount'].mean()
        df1 = pd.DataFrame([{"customer_name": "Среднее", "amount": average_avount}])
        common_df = pd.concat([revenue_by_customers_df, df1])



        revenue_list = common_df['amount']/1000000
        customer_name_list = common_df['customer_name']

        ave_index = 0
        i = 0
        for customer_name in customer_name_list:
            if customer_name == "Среднее":
                ave_index = i
            i = i + 1

        first_main_color = colors_file.colors_dict[0]
        second_main_color = colors_file.colors_dict[1]

        colors = [first_main_color, ] * len(customer_name_list)
        colors[ave_index] = second_main_color

        ave_max_value = max(revenue_list) * 1.02
        ave_rate_min_value = min(revenue_list) - min(revenue_list) * 0.06


        fig_credit_rate = go.Figure(go.Bar(
            x=revenue_list,
            y=customer_name_list,
            text=revenue_list,
            marker={"color": colors},
            orientation='h',
            name="",
            textposition='auto'
        ))

        fig_credit_rate.update_xaxes(range=[ave_rate_min_value, ave_max_value])
        fig_credit_rate.update_layout({
            'margin': dict(l=5, r=5, t=5, b=5),
            # "title": "Средневзвешенная ставка",
        })
        fig_credit_rate.update_traces(
            # texttemplate='%{text:.2s}'
            texttemplate='%{x:.1f} млн.руб',
            hovertemplate='%{x:.1f} млн.руб'
        )
        # fig_credit_rate.add_annotation(
        #                    # text="1",
        #                    showarrow=False,
        #                    # yshift=10
        # )
        message = ""
        graph_output = dcc.Graph(id="credit_av_rate_graph", config={'displayModeBar': False}, figure=fig_credit_rate)
        # получаем первую дату в выборке
        df.sort_values(['date'], inplace=True)
        first_date = df.iloc[0, df.columns.get_loc("date")]
        first_date = today
        last_date = df.iloc[-1, df.columns.get_loc("date")]

        # check = str(ave_rate_list) + str(creditor_list)
        output =html.Div(
            children=[
                # credit_datatable,
                graph_output

            ]
        )


    return graph_output, first_date, last_date, check