from dash import dcc
import plotly.graph_objects as go
from dash import dash_table
import datetime
def top_independent_customers_barchart_v2_div_func(df_2, data_input, top_independent_customers_year_select):
    if data_input == '1с_api':
        df = df_2
        df['payment_amount'] = df['payment_amount'].astype('float')
        # фильтр по году
        year_full_list = list(df['year'].unique())
        year_filter = year_full_list
        if top_independent_customers_year_select:
            if 'list' in str(type(top_independent_customers_year_select)):
                year_filter = top_independent_customers_year_select
            else:
                year_filter = list(top_independent_customers_year_select)
        year_filter_int_list = []
        for year in year_filter:
            year = int(year)
            year_filter_int_list.append(year)

        # режем выборку по году
        df = df.loc[df['year'].isin(year_filter_int_list)]


        # удаляем ненужные статусы
        full_agreement_status_list = list(df['current_agreement_status'].unique())
        # оставляем только нужные статусы договоров
        updated_full_agreement_status_list = []
        for agreement_status in full_agreement_status_list:
            if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                updated_full_agreement_status_list.append(agreement_status)


        updated_current_agreement_status_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

        updated_status_df = updated_current_agreement_status_status_df

        updated_status_df = updated_status_df.copy()
        # Заполняем колонку company_group
        updated_status_df['company_group'].fillna('not_data', inplace=True)
        # updated_status_df['company_group'] = updated_status_df['company_group'].str.replace(r'^\s*$', 'not_data')
        updated_status_df['company_group'] = updated_status_df['company_group'].replace('', 'not_data')


        # datatable = dash_table.DataTable(data=df_fig.to_dict('records'),)

        # оставляем строки, в которых нет группы компаний
        df_fig = updated_status_df.loc[updated_status_df['company_group'].isin(['not_data'])]

        # определяем даты выборки
        start_date = df_fig.iloc[0]['date']
        # finish_date = df.iloc[-1]['date']
        # start_date = datetime.datetime(start_year, 1, 1)
        start_month_first_date_str = start_date.strftime("%d.%m.%Y")
        finish_year = updated_status_df['year'].max()
        finish_date = df_fig.iloc[-1]['date']
        # finish_date = datetime.datetime(finish_year, 12, 31)
        finish_month_first_date_str = finish_date.strftime("%d.%m.%Y")
        period_text = f"Период: с {start_month_first_date_str} по {finish_month_first_date_str}"



        df_customer_name = df_fig.groupby(['customer_name'], as_index=False).agg(
            {'payment_amount': 'sum'})



        df_customer_name.sort_values(["payment_amount"], ascending=False, inplace=True)


        df_customer_name = df_customer_name.head(20)
        df_fig = df_customer_name.sort_values(["payment_amount"], ascending=True)


        payment_amount_list = list(df_fig['payment_amount']/1000000000)
        customer_name_list = list(df_fig['customer_name'])
        payment_amount_max_value = max(payment_amount_list) * 1.5
        payment_amount_min_value = min(payment_amount_list) - min(payment_amount_list) * 0.3

        fig = go.Figure(go.Bar(
            x=payment_amount_list,
            y=customer_name_list,
            text=payment_amount_list,
            marker={"color": '#b27aa1'},
            orientation='h',
            name="",
            textposition='outside'
        ))
        fig.update_xaxes(range=[payment_amount_min_value, payment_amount_max_value])
        fig.update_layout({
            'margin': dict(l=5, r=5, t=5, b=5),
            # "title": "Средневзвешенная ставка",
        })

        fig.update_traces(
            texttemplate='%{text:.3f} млрд. руб',
            hovertemplate='%{y}: %{text:.3f} млрд. руб',
            textfont_size=14
        )


        output_div = dcc.Graph(config={'displayModeBar': False}, figure=fig)


        # output_df = df_test
        # data = output_df.to_dict('records')
        #
        # top_independent_customers_barchart_v2_div_func_output_table_ = dash_table.DataTable(
        #     data=data,
        # page_action="native",)

        top_independent_customers_barchart_v2_div_func_output_table_ = ""

        # output_div = '13'
        # period_text = datatable
        return output_div, period_text