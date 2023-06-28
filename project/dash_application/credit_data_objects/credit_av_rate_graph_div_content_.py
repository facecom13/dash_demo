import datetime
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
from dash import dash_table

def credit_av_rate_graph_div_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):
    check = ""
    graph_output = ""
    first_date = ''
    last_date = ''
    df['year'] = df['year'].astype(float)
    df['year'] = df['year'].astype('int')
    # режем df по фильтрам

    # фильтр по кредитору ###########################################################################
    creditor_full_list = list(df['creditor'].unique())
    creditor_filter = creditor_full_list
    if creditor_select:
        if 'list' in str(type(creditor_select)):
            creditor_filter = creditor_select
        else:
            creditor_filter = list(creditor_select)

    # режем выборку по кредитору
    df = df.loc[df['creditor'].isin(creditor_filter)]

    #####################################################################################################

    # фильтр по credit_contract ##########################################################################
    credit_contract_full_list = list(df['credit_contract'].unique())
    credit_contract_filter = credit_contract_full_list
    if credit_contract_select:
        if 'list' in str(type(credit_contract_select)):
            credit_contract_filter = credit_contract_select
        else:
            credit_contract_filter = list(credit_contract_select)

    # режем выборку по credit_contract
    df = df.loc[df['credit_contract'].isin(credit_contract_filter)]
    #####################################################################################################

    # фильтр по годам ###########################################################################
    year_full_list = list(df['year'].unique())
    year_filter = year_full_list
    if credit_year_select:
        if 'list' in str(type(credit_year_select)):
            year_filter = credit_year_select
        else:
            year_filter = [credit_year_select]

    year_filter_int_list = []
    for year in year_filter:
        year = int(year)
        if year >= int(datetime.datetime.now().year):
            year_filter_int_list.append(year)

    # режем выборку по годам
    df = df.loc[df['year'].isin(year_filter_int_list)]
    #####################################################################################################

    # фильтр по кварталам ###########################################################################
    quarter_full_list = list(df['quarter'].unique())
    quarter_filter = quarter_full_list
    if credit_tab_quarter_select:
        if 'list' in str(type(credit_tab_quarter_select)):
            quarter_filter = credit_tab_quarter_select
        else:
            quarter_filter = [credit_tab_quarter_select]

    quarter_filter_int_list = []
    for quarter in quarter_filter:
        quarter = int(quarter)
        quarter_filter_int_list.append(quarter)

    # режем выборку по кварталам
    df = df.loc[df['quarter'].isin(quarter_filter_int_list)]
    #####################################################################################################

    # фильтр по месяцам ###########################################################################
    month_full_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    month_filter = month_full_list
    if credit_tab_month_select:
        if 'list' in str(type(credit_tab_month_select)):
            month_filter = credit_tab_month_select
        else:
            month_filter = [credit_tab_month_select]

    month_filter_int_list = []
    for month in month_filter:
        month = int(month)
        month_filter_int_list.append(month)

    df['date_2'] = pd.to_datetime(df['date'])
    if "int" in str(df['date'].dtype):
        df['date_2'] = pd.to_datetime(df['date'], unit='ms')
    df['month'] = df['date_2'].dt.month
    # режем выборку по месяцам
    df = df.loc[df['month'].isin(month_filter_int_list)]
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



        df = df.loc[:, ['date', 'creditor', 'credit_tranch_date', 'credit_annual_rate', 'credit_amount', 'agreement_code', 'amount']]
        # список траншей в работе
        df['tranch_ids'] = df['credit_tranch_date'].astype(str) + "_" + df['creditor'].astype(str)

        creditor_list = list(df['creditor'].unique())
        # колонка с размером годовой суммы процентов
        df = df.copy()
        df['credit_percent_annual_amount'] = df['credit_annual_rate'] / 100 * df['credit_amount']



        # сумма процентов
        percent_sum = df['credit_percent_annual_amount'].sum()
        credit_sum = df['credit_amount'].sum()
        percent_value = percent_sum/credit_sum


        # data = df.to_dict('records')
        # credit_datatable = dash_table.DataTable(
        #
        #     data=data,)


        x_credit_rate = []
        y_credit_rate = []
        result_list = []
        total_credit_amount = df['credit_amount'].sum()
        total_percent_amount = df['credit_percent_annual_amount'].sum()

        for creditor in creditor_list:

            # получаем выборку по банку
            creditor_temp_df = df.loc[df['creditor'] == creditor]

            # стоимость остатка от кредитов
            creditor_temp_df = creditor_temp_df.loc[creditor_temp_df['agreement_code']=='Кредиты']

            # получаем список размера ставок, попавших в выборку
            creditor_rates_list = list(creditor_temp_df['credit_annual_rate'].unique())

            for rate in creditor_rates_list:
                temp_dict = {}
                temp_dict['creditor'] = creditor
                temp_dict['rate'] = rate

                creditor_rate_temp_df = creditor_temp_df.loc[creditor_temp_df['credit_annual_rate']==rate]

                credit_remainings = creditor_rate_temp_df['amount'].sum()
                """ credit_remainings - сумма всего что есть в поле amount в будущем """

                creditor_rate_temp_df = creditor_rate_temp_df.copy()
                creditor_rate_temp_df['percent_amount'] = creditor_rate_temp_df['amount']*rate/100
                percent_amount = creditor_rate_temp_df['percent_amount'].sum()

                temp_dict['credit_remainings'] = credit_remainings
                temp_dict['percent_amount'] = percent_amount
                result_list.append(temp_dict)

        ave_rate_df = pd.DataFrame(result_list)


        # итерируемся по полученной извлекая данные по банкам
        list_of_creditors = list(ave_rate_df['creditor'].unique())

        result_list_temp = []
        for creditor in list_of_creditors:
            temp_dict = {}
            temp_creditor_df = ave_rate_df.loc[ave_rate_df['creditor']==creditor]
            payment_sum = temp_creditor_df['credit_remainings'].sum()
            percent_amount = temp_creditor_df['percent_amount'].sum()
            creditor_rate = percent_amount/payment_sum
            temp_dict['creditor'] = creditor
            temp_dict['credit_remainings'] = payment_sum
            temp_dict['percent_amount'] = percent_amount
            temp_dict['creditor_weight_rate'] = creditor_rate
            result_list_temp.append(temp_dict)

        ave_rate_df = pd.DataFrame(result_list_temp)

        data = ave_rate_df.to_dict('records')
        credit_datatable = dash_table.DataTable(data=data, )




        # получаем количество банков
        qty_of_creditors = len(list(ave_rate_df['creditor']))
        ave_rate_list = []
        ave_rate_list_graph = []
        colors = []
        if qty_of_creditors>1:
            # определяем ставку по портфелю
            total_weight_rate = total_percent_amount / total_credit_amount

            ave_rate_df.sort_values(by=['creditor_weight_rate'], inplace=True)
            df1 = pd.DataFrame([{"creditor": "По портфелю", "creditor_weight_rate": total_weight_rate}])
            common_df = pd.concat([ave_rate_df, df1])

            # data = common_df.to_dict('records')
            # credit_datatable = dash_table.DataTable(
            #     data=data,)


            # common_df['creditor_weight_rate'] = common_df['creditor_weight_rate'].round(decimals=3)

            ave_rate_list = list(common_df['creditor_weight_rate'] * 100)
            ave_rate_list_graph = []
            for ave_value in ave_rate_list:
                value = "{:.4f}".format(ave_value)
                ave_rate_list_graph.append(value)
            creditor_list = list(common_df['creditor'])

            total_ave_rate_index = 0
            i = 0
            for creditor in creditor_list:
                if creditor == "По портфелю":
                    total_ave_rate_index = i
                i = i + 1
            colors = ['#32935F', ] * len(creditor_list)
            colors[total_ave_rate_index] = '#FFC000'
            ave_max_value = max(ave_rate_list) * 1.02
            ave_rate_min_value = min(ave_rate_list) - min(ave_rate_list) * 0.06
        else:
            # ave_rate_df['creditor_weight_rate'] = ave_rate_df['creditor_weight_rate'].round(decimals=3)
            ave_rate_list = list(ave_rate_df['creditor_weight_rate'] * 100)
            ave_rate_list_graph = []
            for ave_value in ave_rate_list:
                value = "{:.4f}".format(ave_value)
                ave_rate_list_graph.append(value)
            creditor_list = list(ave_rate_df['creditor'])
            colors = ['#32935F', ] * len(creditor_list)
            ave_max_value = max(ave_rate_list) * 1.02
            ave_rate_min_value = min(ave_rate_list) - min(ave_rate_list) * 0.06

        fig_credit_rate = go.Figure(go.Bar(
            x=ave_rate_list,
            y=creditor_list,
            text=ave_rate_list_graph,
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
            texttemplate='%{x:.2f}%',
            hovertemplate='%{x:.2f}%'
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

        check = str(ave_rate_list) + str(creditor_list)
        output =html.Div(
            children=[
                credit_datatable,
                graph_output

            ]
        )


    return graph_output, first_date, last_date, check