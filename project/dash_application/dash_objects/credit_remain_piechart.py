import pandas as pd
import plotly.graph_objects as go
import datetime
import dash_application.dash_objects.initial_values as initial_values

def credit_remain_piechart_func(df):
    df = df.loc[df['date'] >= datetime.datetime.now()]
    # Получаем список банков - кредиторов
    credit_banks_df = df.loc[df['agreement_code'] == 'Кредиты']
    fig = go.Figure()
    # Если данных в df нет, то отдаем сообщение, что данных нет
    if len(credit_banks_df) == 0:
        fig.update_xaxes(
            {'visible': False}
        )
        fig.update_yaxes(
            {'visible': False}
        )
        fig.add_annotation(
            # x=2, y=5,
            text="Нет данных для построения графика",
            showarrow=False,
            # xref = "paper",
            # yref =  "paper",

        )
        return fig

    credit_bank_list = list(credit_banks_df['creditor'].unique())

    # Получаем список значений с суммами кредитов
    bank_credit_value_list = []
    df_graph_list = []
    for bank in credit_bank_list:
        temp_dict = {}
        bank_filtered_df = credit_banks_df.loc[credit_banks_df['creditor'] == bank]
        total_bank_credit_value = bank_filtered_df['amount'].sum()
        temp_dict['bank'] = bank
        temp_dict['amount'] = total_bank_credit_value
        bank_credit_value_list.append(total_bank_credit_value)
        df_graph_list.append(temp_dict)
    df_graph = pd.DataFrame(df_graph_list)
    df_graph['amount'] = df_graph['amount'] / 1000000000
    df_graph['amount'] = df_graph['amount'].round(decimals=3)
    df_graph.sort_values(by=['amount'], ascending=True, inplace=True)

    labels = df_graph['bank']
    values = df_graph['amount']
    colors = ['#B99B6B', '#698269', '#183A1D', '#F0A04B', '#E1EEDD', "#b27aa1", "#E8E8E8","#b3e5ca", "#FFC000", "#E8E8E8", "#909090", "#32935F"]
    colors = ["#b27aa1", "#E8E8E8", "#b3e5ca", "#FFC000", "#E8E8E8", "#909090", "#32935F"]
    # colors_dict = initial_values.colors_dict
    #
    # myKeys = list(colors_dict.keys())
    # myKeys.sort(reverse=False)
    # sorted_dict = {i: colors_dict[i] for i in myKeys}
    #
    # colors = list(sorted_dict.values())
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent'
    )])
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.2,
        xanchor="right",
        x=1
    ))
    fig.update_traces(
        marker=dict(colors=colors),
        textposition='auto',
        # texttemplate='%{value} млрд.руб',
        # hovertemplate='%{y}: %{text} млрд.руб'

    )

    return fig