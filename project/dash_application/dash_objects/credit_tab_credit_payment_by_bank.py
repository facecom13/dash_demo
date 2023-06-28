import datetime

import plotly.graph_objects as go

def credit_tab_credit_payment_by_bank_func(df, bank):
    df = df.loc[df['date']>=datetime.datetime.now()]
    df = df.loc[df['creditor']==bank]
    df = df.loc[df['agreement_code'] == "Кредиты"]
    df_groupped = df.groupby(['year'], as_index=False).agg(
        {'amount': 'sum'})
    df_groupped.sort_values(by="year", inplace=True)

    fig = go.Figure(go.Bar(
        x=df_groupped['year'],
        y=df_groupped['amount']/1000000000,
        text=df_groupped['amount']/1000000000,
        marker=dict(color="#FFC000")
        ))

    fig.update_layout({
        'margin': dict(l=5, r=5, t=45, b=5),
        "bargap": 0.30,
        # 'barmode': 'stack',
        "title": f"Погашение кредитного портфеля {bank}",
        # 'legend': {
        #     'orientation': "h",
        #     'yanchor': "bottom",
        #     'y': 1.08,
        # }
    })
    fig.update_xaxes(
        # dtick="M1",
        # tickformat="%y",
        # rangeslider_visible=True
    )
    fig.update_traces(
        texttemplate='%{text:.3f} млрд.руб',
        hovertemplate='<extra></extra>%{x}:<br>%{text:.3f} млрд.руб',
    )
    return fig