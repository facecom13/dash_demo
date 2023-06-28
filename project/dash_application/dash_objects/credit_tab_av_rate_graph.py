import datetime
from dash import dash_table
import pandas as pd
import plotly.graph_objects as go
import dash_application.functions.av_rate_data as av_rate_data
from dash import dcc
def credit_av_rate_graph_func(df):
    df = df.loc[df['date']>=datetime.datetime.now()]

    # выбираем только те банки, по которым у нас с текущей даты есть кредитные обязательства.
    # то есть те, у которых в будущем есть значения или по процентам или по кредитам

    df = df.loc[:, ['date', 'creditor', 'credit_tranch_date', 'credit_annual_rate', 'credit_amount']]
    # список траншей в работе
    df['tranch_ids'] = df['credit_tranch_date'].astype(str) + "_" + df['creditor'].astype(str)

    creditor_list = list(df['creditor'].unique())
    # колонка с размером годовой суммы процентов
    df = df.copy()
    df['credit_percent_annual_amount'] = df['credit_annual_rate']/100*df['credit_amount']

    x_credit_rate = []
    y_credit_rate = []
    result_list = []
    total_credit_amount = 0
    total_percent_amount = 0
    message = ""
    message_df_list = []
    for creditor in creditor_list:
        temp_dict = {}
        # получаем выборку по банку
        creditor_temp_df = df.loc[df['creditor']==creditor]
        # получаем список траншей, попавших в выборку
        tranch_ids_list = list(creditor_temp_df['tranch_ids'].unique())
        bank_credit_amount = 0
        bank_percent_amount = 0
        for tranch in tranch_ids_list:
            message_df_temp = {}
            temp_creditor_tranch_df = creditor_temp_df.loc[creditor_temp_df['tranch_ids']==tranch]
            # получаем значение выданного кредита по данному траншу:
            tranch_credit_amount = temp_creditor_tranch_df.iloc[0, temp_creditor_tranch_df.columns.get_loc("credit_amount")]
            # получаем суммарное значение выданных траншей по банку
            bank_credit_amount = bank_credit_amount + tranch_credit_amount
            # получаем значение годовой суммы процентов, которые надо заплатить по данному траншу
            tranch_percent_volume = temp_creditor_tranch_df.iloc[0, temp_creditor_tranch_df.columns.get_loc("credit_percent_annual_amount")]
            bank_percent_amount = bank_percent_amount + tranch_percent_volume


            message_df_temp['creditor'] = creditor
            message_df_temp['tranch_date'] =  temp_creditor_tranch_df.iloc[0, temp_creditor_tranch_df.columns.get_loc("credit_tranch_date")]
            message_df_temp['tranch_amount'] = tranch_credit_amount
            message_df_temp['tranch_rate'] = temp_creditor_tranch_df.iloc[0, temp_creditor_tranch_df.columns.get_loc("credit_annual_rate")]
            message_df_temp['tranch_annual_percent_volume'] = tranch_percent_volume

            message_df_list.append(message_df_temp)

        # получаем ставку по банку
        total_credit_amount = total_credit_amount + bank_credit_amount
        total_percent_amount = total_percent_amount + bank_percent_amount
        creditor_weight_rate = bank_percent_amount / bank_credit_amount
        x_credit_rate.append(creditor)
        y_credit_rate.append(creditor_weight_rate)
        temp_dict['creditor'] = creditor
        temp_dict['creditor_weight_rate'] = creditor_weight_rate
        result_list.append(temp_dict)

    ############################################# MESSAGE TO DELETE #######
    # message_df = pd.DataFrame(message_df_list)

    av_rate_dict = av_rate_data.data

    message_df = pd.DataFrame.from_dict(av_rate_dict)
    if "int" in str(message_df['tranch_date'].dtype):
        message_df['tranch_date'] = pd.to_datetime(message_df['tranch_date'], unit='ms')

    # message_df.to_csv('message_df.csv')
    # data = message_df.to_dict('records')
    # datatable = dash_table.DataTable(data=data)
    # data_json = message_df.to_json(force_ascii=False)

    # message = datatable

    ave_rate_df = pd.DataFrame(result_list)


    # определяем ставку по портфелю
    total_weight_rate = total_percent_amount/total_credit_amount

    ave_rate_df.sort_values(by=['creditor_weight_rate'], inplace=True)
    df1 = pd.DataFrame([{"creditor": "По портфелю", "creditor_weight_rate": total_weight_rate}])
    common_df = pd.concat([ave_rate_df, df1])

    common_df['creditor_weight_rate'] = common_df['creditor_weight_rate'].round(decimals=3)

    ave_rate_list = list(common_df['creditor_weight_rate']*100)
    ave_rate_list_graph = []
    for ave_value in ave_rate_list:
        value = "{:.4f}".format(ave_value)
        ave_rate_list_graph.append(value)
    creditor_list = list(common_df['creditor'])

    total_ave_rate_index = 0
    i=0
    for creditor in creditor_list:
        if creditor == "По портфелю":
            total_ave_rate_index = i
        i=i+1
    colors = ['#32935F', ] * len(creditor_list)
    colors[total_ave_rate_index] = '#FFC000'
    ave_max_value = max(ave_rate_list)*1.02
    ave_rate_min_value = min(ave_rate_list) - min(ave_rate_list)*0.06
    fig_credit_rate = go.Figure(go.Bar(
        x=ave_rate_list,
        y=creditor_list,
        text=ave_rate_list_graph,
        marker= {"color": colors},
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
    return graph_output, message