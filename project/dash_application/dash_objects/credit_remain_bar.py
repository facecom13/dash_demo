import datetime

import pandas as pd
import plotly.graph_objects as go

def credit_remain_bar_graph_func(df):
    df = df.loc[df['date']>=datetime.datetime.now()]
    # Получаем список банков - кредиторов
    credit_banks_df = df.loc[df['agreement_code']=='Кредиты']
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
        bank_filtered_df = credit_banks_df.loc[credit_banks_df['creditor']==bank]
        total_bank_credit_value = bank_filtered_df['amount'].sum()
        temp_dict['bank'] = bank
        temp_dict['amount'] = total_bank_credit_value
        bank_credit_value_list.append(total_bank_credit_value)
        df_graph_list.append(temp_dict)
    df_graph = pd.DataFrame(df_graph_list)
    df_graph['amount'] = df_graph['amount'] / 1000000000
    df_graph['amount'] = df_graph['amount'].round(decimals=3)
    df_graph.sort_values(by=['amount'], ascending=True, inplace=True)


    # print(credit_banks_df)
    fig = go.Figure(go.Bar(
        x=df_graph['amount'],
        y=df_graph['bank'],
        text=df_graph['amount'],
        name="",
        marker=dict(color='#32935F'),
        orientation='h'))
    annotation_text = "Кликнуть на столбик для перехода <br>в график выплаты по годам"
    fig.add_annotation(
        # x=2,
        y=1.2,
        text=annotation_text,
        align="left",
        showarrow=False,
        xref="paper",
        yref="paper",
        # bordercolor="#c7c7c7",
        # borderwidth=2,
        # borderpad=4,
        bgcolor="white",
        # opacity=0.8

    )
    fig.update_traces(
        # texttemplate='%{text:.2s}'
        texttemplate='%{text} млрд.руб',
        hovertemplate = '%{y}: %{text} млрд.руб'
    )
    return fig