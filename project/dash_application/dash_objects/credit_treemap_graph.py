import datetime

import plotly.graph_objects as go

def credit_treemap_graph_func(df):
    today = datetime.datetime.now()
    df = df.loc[df['date']>=today]
    df_groupped = df.groupby(['agreement_code', 'creditor'], as_index=False).agg(
        {'amount': 'sum'})
    labels = ['Выплаты, млрд руб. Доля в общем объеме, %']
    parents = ['']
    values = [0]

    # Получаем список категорий из колонки agreement_code
    agreement_code_list = list(df_groupped['agreement_code'].unique())
    # добавляем эти категории первым уровнем в родительский корень
    for agreement_code_list_item in agreement_code_list:
        labels.append(agreement_code_list_item)
        parents.append('Выплаты, млрд руб. Доля в общем объеме, %')
        values.append(0)
        # получаем выборку по текущему agreement_code
        agreement_code_filtered = df_groupped.loc[df_groupped['agreement_code']==agreement_code_list_item]
        # группируем результат по полю creditor
        agreement_code_groupped_df = agreement_code_filtered.groupby(['creditor'], as_index=False).agg(
        {'amount': 'sum'})
        # итерируемся по полученному df
        for row in agreement_code_groupped_df.itertuples():
            amount = getattr(row, 'amount')
            amount = round(amount/1000000000, 3)
            # добавляем в списки treemap значения
            if agreement_code_list_item == 'Проценты':
                creditor = getattr(row, 'creditor') + " "
            else:
                creditor = getattr(row, 'creditor')
            labels.append(creditor)
            values.append(amount)
            parents.append(agreement_code_list_item)
    # print(labels)
    list_len = len(labels)
    text_font_dict = {}
    # for label in labels:
    #     text_font_dict['color'] =

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        # marker_colorscale='Blues',
        values=values,
        textinfo="label+value+percent parent",
        # '%{y}: %{text:.3f} млрд руб.'
        hoverinfo="label+value+percent parent",
        # hovertemplate='<extra></extra>%{label}<br>%{value:.3f} млрд руб<br>%{percent}%',
        # textfont = {'color':['red', 'blue', 'blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue',]},
        # texttemplate="%{label}: <br>%{percent:.1f} </br> %{value}",
        root={"color": "#f6f8f7"}
    ))


    fig.update_layout(
        margin=dict(t=5, l=5, r=5, b=25),
        treemapcolorway=["#32935F", "#FFC000"],
    )

    return fig