import plotly.graph_objects as go

def graph(df):
    df = df.loc[df['year']>=2023]
    df = df.copy()
    df.sort_values(by="year", inplace=True)
    df['year'] = df['year_dt'].dt.year
    df_groupped = df.groupby(['year_dt','year', 'agreement_code'], as_index=False).agg(
        {'amount': 'sum'})


    df_totals = df.groupby(['year'], as_index=False).agg({'amount': 'sum'})
    df_totals['amount'] = df_totals['amount'] / 1000000000
    df_totals['amount'] = df_totals['amount'].round(decimals=3)
    df_totals['total_label'] = df_totals['amount'] * 1

    labels = list(df_totals['amount'])
    labels_total = list(df_totals['total_label'])
    year_x = list(df_totals['year'])

    fig_credit_type = go.Figure()
    # получаем список видов
    credit_type_select_list = list(df_groupped['agreement_code'].unique())
    colors = ["#FFC000", "#32935F"]
    i = 0

    for credit_type in credit_type_select_list:
        temp_credit_df = df_groupped.loc[df_groupped['agreement_code'] == credit_type]
        temp_credit_df = temp_credit_df.copy()
        # temp_credit_df['year'] = temp_credit_df['year_dt'].dt.year
        temp_credit_df = temp_credit_df.copy()
        temp_credit_df['amount'] = temp_credit_df['amount'] / 1000000000
        temp_credit_df['amount'] = temp_credit_df['amount'].round(decimals=3)

        x_credit = list(temp_credit_df['year'])
        y_credit = list(temp_credit_df['amount'])
        fig_credit_type.add_trace(go.Bar(
            x=x_credit,
            y=y_credit,
            name=credit_type,
            # text = y_credit,
            marker=dict(color=colors[i])
        ))
        i=i+1
    fig_credit_type.add_trace(go.Scatter(
        x=year_x,
        y=labels_total,
        text=labels,
        mode='text',
        textposition='top center',
        textfont=dict(
            size=18,
        ),
        showlegend=False
    ))
    fig_credit_type.update_layout({
        'barmode': 'stack',
        'margin': dict(l=5, r=5, t=5, b=5),
        # "title": "Погашение кредитного портфеля",
        'legend': {
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1.08,
        }
    })
    fig_credit_type.update_xaxes(
        # dtick="%Y",
        # tickformat="%Y",
        # rangeslider_visible=True
        type = 'category'
    )
    # fig_credit_type.update_traces(
    #     texttemplate='%{text:.3f} млрд.руб',
    #     hovertemplate='<extra></extra>%{x}:<br>%{text:.3f} млрд.руб',
    # )


    return fig_credit_type