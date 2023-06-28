import datetime
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import dash_application.dash_objects.initial_values as initial_values
import dash_application_retail.colors as colors_file

def marketing_cost_div_func(df, retail_customer_select):
    output = 'credit_treemap_div_content'
    df['year'] = df['year'].astype(float)
    df['year'] = df['year'].astype('int')
    # режем df по фильтрам

    # фильтр по кредитору ###########################################################################
    # creditor_full_list = list(df['creditor'].unique())
    # creditor_filter = creditor_full_list
    # if creditor_select:
    #     if 'list' in str(type(creditor_select)):
    #         creditor_filter = creditor_select
    #     else:
    #         creditor_filter = list(creditor_select)
    #
    # # режем выборку по кредитору
    # df = df.loc[df['creditor'].isin(creditor_filter)]

    #####################################################################################################

    # фильтр по credit_contract ##########################################################################
    # credit_contract_full_list = list(df['credit_contract'].unique())
    # credit_contract_filter = credit_contract_full_list
    # if credit_contract_select:
    #     if 'list' in str(type(credit_contract_select)):
    #         credit_contract_filter = credit_contract_select
    #     else:
    #         credit_contract_filter = list(credit_contract_select)
    #
    # # режем выборку по credit_contract
    # df = df.loc[df['credit_contract'].isin(credit_contract_filter)]
    #####################################################################################################

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


    df_origin = df
    today = datetime.datetime.now()

    try:
        df = df.loc[df['date'] >= datetime.datetime(2023,1,1)]
    except:
        df = df.loc[df['date'] >= datetime.datetime(2023,1,1).date()]

    try:
        df = df.loc[df['date'] <= today]
    except:
        df = df.loc[df['date'] >= today.date()]

    df.sort_values(by="date", inplace=True)
    df_groupped = df.groupby(['month_first_date'], as_index=False).agg(
        {'amount': 'sum'})

    fig = go.Figure()
    # получаем список видов
    # credit_type_select_list = list(df_groupped['agreement_code'].unique())
    # colors = ["#FFC000", "#32935F"]
    # i = 0
    #
    # for credit_type in credit_type_select_list:
    #     temp_credit_df = df_groupped.loc[df_groupped['agreement_code'] == credit_type]
    #     temp_credit_df = temp_credit_df.copy()
    #     temp_credit_df['amount'] = temp_credit_df['amount'] / 1000000000
    #     temp_credit_df['amount'] = temp_credit_df['amount'].round(decimals=3)
    #     # print(temp_credit_df)
    #     x_credit = list(temp_credit_df['month_first_date'])
    #     # print("x_credit: ", x_credit)
    #     y_credit = list(temp_credit_df['amount'])
    #     fig_credit_type.add_trace(go.Bar(
    #         x=x_credit,
    #         y=y_credit,
    #         name=credit_type,
    #         marker=dict(color=colors[i]),
    #         hovertemplate='%{x}: %{y} млрд.руб<extra></extra>',
    #     ))
    #     i = i + 1

    first_main_color = colors_file.colors_dict[0]
    second_main_color = colors_file.colors_dict[2]


    x_past = df_groupped['month_first_date']
    y_past = df_groupped['amount'] / 1000000
    fig.add_trace(go.Bar(
                x=x_past,
                y=y_past,
                name='Факт',
                marker=dict(color=first_main_color),
                hovertemplate='%{x}: %{y}<br>млн.р<extra></extra>',
                textposition='outside'
            ))



    try:
        df_future = df_origin.loc[df_origin['date'] >= datetime.datetime.now()]
    except:
        df_future = df_origin.loc[df_origin['date'] >= datetime.datetime.now().date()]

    try:
        df_future = df_future.loc[df_future['date'] <= datetime.datetime(2024,1,1)]
    except:
        df_future = df_future.loc[df_future['date'] <= datetime.datetime(2024,1,1).date()]


    df_future.sort_values(by="date", inplace=True)
    df_groupped_future = df_future.groupby(['month_first_date'], as_index=False).agg(
        {'amount': 'sum'})

    x_future = df_groupped_future['month_first_date']
    y_future = df_groupped_future['amount'] / 1000000

    max_value = max(list(y_future)) * 1.2
    fig.add_trace(go.Bar(
        x=x_future,
        y=y_future,
        name='Запланировано',
        marker=dict(color=second_main_color),
        hovertemplate='%{x}: %{y}<br>млн.р<extra></extra>',
        textposition='outside'
    ))


    # добавление вертикальных линий в первый день года

    # date_finish = df['date'].max()
    # first_year_date_start = datetime.datetime(2023, 1, 1)
    # temp_date = first_year_date_start
    # while temp_date < date_finish:
    #     fig.add_vline(
    #         x=temp_date,
    #         # line_width=3,
    #         # line_dash="dash",
    #         line_color="grey")
    #     temp_date = temp_date + datetime.timedelta(days=365.25)

    fig.update_layout({
        # 'barmode': 'stack',
        'xaxis_tickangle': -90,
        'margin': dict(l=2, r=18, t=5, b=5),

        # "title": "Погашение кредитного портфеля",
        'legend': {
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1.08,
        }
    })
    # fig_credit_type.update_layout(legend=dict(
    #     orientation="h",
    #     yanchor="bottom",
    #     y=1.02,
    #     xanchor="right",
    #     x=1

    fig.update_yaxes(range=[0, max_value])

    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%y",
        rangeslider_visible=True
    )

    fig.update_traces(
        texttemplate='%{y:.1f}<br>млн.р',
        hovertemplate='<extra></extra>%{x}:<br>%{y:.1f} млн.р',
        textfont_size=14
    )



    # получаем первую дату в выборке
    first_date = df.iloc[0, df.columns.get_loc("date")]
    # first_date = today
    last_date = df.iloc[-1, df.columns.get_loc("date")]

    fig_obj = dcc.Graph(figure=fig, config={'displayModeBar': False})
    return fig_obj, first_date, last_date