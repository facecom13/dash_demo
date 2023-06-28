import plotly.graph_objects as go
import datetime
import dash_application.dash_objects.initial_values as initial_values

def credit_tab_payment_grapf_month_func(df, credit_grapf_range_slider):
    df = df.copy()

    date_start = initial_values.start_date
    if credit_grapf_range_slider:
        date_start = datetime.datetime.fromtimestamp(credit_grapf_range_slider[0])

    date_finish = initial_values.finish_date
    if credit_grapf_range_slider:
        date_finish = datetime.datetime.fromtimestamp(credit_grapf_range_slider[1])
    try:
        df = df.loc[df['date']>=date_start]
        df = df.loc[df['date'] <= date_finish]
    except:
        pass
    df = df.loc[df['year']>=2023]
    # режем по слайдеру

    df.sort_values(by="date", inplace=True)
    df_groupped = df.groupby(['month_first_date', 'agreement_code'], as_index=False).agg(
        {'amount': 'sum'})
    # df_groupped.to_csv("temp_csv_to_delete.csv")
    fig_credit_type = go.Figure()
    # получаем список видов
    credit_type_select_list = list(df_groupped['agreement_code'].unique())
    colors = ["#FFC000", "#32935F"]
    i=0

    for credit_type in credit_type_select_list:
        temp_credit_df = df_groupped.loc[df_groupped['agreement_code'] == credit_type]
        temp_credit_df = temp_credit_df.copy()
        temp_credit_df['amount'] = temp_credit_df['amount']/1000000000
        temp_credit_df['amount'] = temp_credit_df['amount'].round(decimals =3)
        # print(temp_credit_df)
        x_credit = list(temp_credit_df['month_first_date'])
        # print("x_credit: ", x_credit)
        y_credit = list(temp_credit_df['amount'])
        fig_credit_type.add_trace(go.Bar(
            x=x_credit,
            y=y_credit,
            name=credit_type,
            marker=dict(color=colors[i]),
            hovertemplate='%{x}: %{y} млрд.руб<extra></extra>',
        ))
        i=i+1

    # добавление вертикальных линий в первый день года
    first_year_date_start = datetime.datetime(date_start.year,1,1)
    temp_date = first_year_date_start
    while temp_date < date_finish:
        fig_credit_type.add_vline(
            x=temp_date,
            # line_width=3,
            # line_dash="dash",
            line_color="grey")
        temp_date = temp_date + datetime.timedelta(days=365.25)

    fig_credit_type.update_layout({
        'barmode': 'stack',
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

    fig_credit_type.update_traces(
        # marker=dict(color=colors)
    )

    fig_credit_type.update_xaxes(
        # dtick="M1",
        # tickformat="%b\n%y",
        rangeslider_visible=True
    )
    return fig_credit_type