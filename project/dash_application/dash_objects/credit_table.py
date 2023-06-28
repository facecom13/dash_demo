import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
from dash.dash_table.Format import Format, Group
import dash_application.functions.mapping as mapping

def credit_table_func(df):
    # Фильтруем таблицу по кредитам
    df_filtered_credits = df.loc[df['agreement_code']=='Кредиты']
    df_temp = df_filtered_credits
    df_temp = df_temp.copy()
    # df.sort_values(by="date", inplace=True)
    df_temp['year'] = df_temp['date'].dt.year
    df_temp['month'] = df_temp['date'].dt.month
    df_temp['month_name'] = df_temp['date'].dt.month_name()
    df_temp['month_name_year'] = df_temp['month_name'].astype(str) + "_" + df['year'].astype(str)

    df_temp['id'] = df_temp['creditor'] + "_" + df_temp['month_name'].astype(str) + "_" + df_temp['year'].astype(str)
    df_temp_groupped = df_temp.groupby(['id', 'creditor', 'month_name_year', 'month', 'year'], as_index=False).agg(
        {'amount': 'sum'})
    df_temp_groupped.sort_values(["year", "month"], inplace=True)
    df_temp_groupped.rename({
        'amount': 'credit_amount',
        'creditor': 'creditor_credit',
        'month': 'month_credit',
        'year': 'year_credit'

    }, axis=1, inplace=True)
    df_credits = df_temp_groupped


    # Фильтруем таблицу по процентам
    df_filtered_percent = df.loc[df['agreement_code'] == 'Проценты']
    df_temp_percent = df_filtered_percent
    df_temp_percent = df_temp_percent.copy()

    df_temp_percent['year'] = df_temp_percent['date'].dt.year
    df_temp_percent['month'] = df_temp_percent['date'].dt.month
    df_temp_percent['month_name'] = df_temp_percent['date'].dt.month_name()
    df_temp_percent['month_name_year'] = df_temp_percent['month_name'].astype(str) + "_" + df_temp_percent['year'].astype(str)

    df_temp_percent['id'] = df_temp_percent['creditor'] + "_" + df_temp_percent['month_name'].astype(str) + "_" + df_temp_percent['year'].astype(str)
    df_temp_percent_groupped = df_temp_percent.groupby(['id', 'creditor', 'month_name_year', 'month', 'year'], as_index=False).agg(
        {'amount': 'sum'})

    df_temp_percent_groupped.rename({
        'amount': 'percent_amount',
        'creditor': 'creditor_percent',
        'month': "month_percent",
        'year': 'year_percent'

    }, axis=1, inplace=True)
    df_percents = df_temp_percent_groupped.loc[:, ['id', 'creditor_percent', 'percent_amount', 'month_percent', 'year_percent']]

    joined_df = pd.merge(df_credits, df_percents, how='outer', on='id')


    joined_df['creditor_credit'].fillna("no_data", inplace=True)
    joined_df['creditor_percent'].fillna("no_data", inplace=True)
    joined_df['credit_amount'].fillna(0, inplace=True)
    joined_df['percent_amount'].fillna(0, inplace=True)
    joined_df['month_credit'].fillna(0, inplace=True)
    joined_df['year_credit'].fillna(0, inplace=True)
    joined_df['month_percent'].fillna(0, inplace=True)
    joined_df['year_percent'].fillna(0, inplace=True)

    joined_df['creditor'] = ""
    joined_df['month'] = 0
    joined_df['year'] = 0
    for row in joined_df.itertuples():
        creditor_credit = getattr(row, 'creditor_credit')
        creditor_percent = getattr(row, 'creditor_percent')
        month_credit = getattr(row, 'month_credit')
        year_credit = getattr(row, 'year_credit')
        month_percent = getattr(row, 'month_percent')
        year_percent = getattr(row, 'year_percent')

        table_index = getattr(row, 'Index')
        if creditor_credit != 'no_data':
            joined_df.iloc[table_index, joined_df.columns.get_loc('creditor')] = creditor_credit
        if creditor_percent != 'no_data':
            joined_df.iloc[table_index, joined_df.columns.get_loc('creditor')] = creditor_percent
        if month_credit != 0:
            joined_df.iloc[table_index, joined_df.columns.get_loc('month')] = month_credit
        if year_credit != 0:
            joined_df.iloc[table_index, joined_df.columns.get_loc('year')] = year_credit
        if month_percent != 0:
            joined_df.iloc[table_index, joined_df.columns.get_loc('month')] = month_percent
        if year_percent != 0:
            joined_df.iloc[table_index, joined_df.columns.get_loc('year')] = year_percent

    joined_df['total'] = joined_df['credit_amount'] + joined_df['percent_amount']

    ####################### ОКРУГЛЕНИЕ ЗНАЧЕНИЙ #################
    joined_df['credit_amount'] = joined_df['credit_amount'] / 1000000000
    joined_df['credit_amount'] = joined_df['credit_amount'].round(3)
    joined_df['percent_amount'] = joined_df['percent_amount'] / 1000000000
    joined_df['percent_amount'] = joined_df['percent_amount'].round(3)
    joined_df['total'] = joined_df['total'] / 1000000000
    joined_df['total'] = joined_df['total'].round(3)

    joined_df.sort_values(['year', 'month', 'total'], ascending=[True,True,False], inplace=True, ignore_index=True)
    ##############################################################

    mapping_month = mapping.month_mapping()
    joined_df['month_name_rus'] = joined_df['month'].map(mapping_month)
    joined_df['month_name_rus'] = joined_df['month_name_rus'] + " " + joined_df['year'].astype(str)
    joined_df = joined_df.loc[joined_df['year']>=2023]
    # joined_df.to_csv('joined_df.csv')


    low_total_row_df_list = [{'creditor': 'Всего',
                              'credit_amount': joined_df['credit_amount'].sum(),
                              'percent_amount':joined_df['percent_amount'].sum(),
                              'total': joined_df['total'].sum()},
                             ]
    low_total_row_df = pd.DataFrame(low_total_row_df_list)
    final_df = pd.concat([joined_df, low_total_row_df], ignore_index=True)


    # columns = [{"name": i, "id": i, } for i in (df_groupped.columns)]
    columns = [
        dict(id='month_name_rus', name='Период'),
        dict(id='creditor', name='Кредитор'),
        dict(id='percent_amount', name='Проценты, млрд. руб', type='numeric', format=Format(group_delimiter=" ", decimal_delimiter=",").group(True)),
        dict(id='credit_amount', name='Кредиты, млрд. руб', type='numeric', format=Format(group_delimiter=" ", decimal_delimiter=",").group(True)),
        dict(id='total', name='Всего, млрд. руб', type='numeric', format=Format(group_delimiter=" ", decimal_delimiter=",").group(True))
               ]
    # print(joined_df)

    data = joined_df.to_dict('records')

    table_data_len = len(joined_df.index)-1
    credit_datatable = dash_table.DataTable(

        data = data,
        columns=columns,
        sort_action="native",
        page_size=10,
        style_cell={'textAlign': 'left',
                    # 'padding-left': '30px',
                    'font-family': 'sans-serif',
                    "font-size": "small"
                    },
        style_header={
            'fontWeight': 'bold',
            'textAlign': 'center',
            'whiteSpace': 'normal',
            # 'paddingLeft': '10px'
        },
        # sort_action="native",
        # style_as_list_view=True,
        style_data_conditional=[
            {
                "if": {"state": "selected"},
                "backgroundColor": "inherit !important",
                "border": "inherit !important",
            },
            {
                'if': {
                    'column_id': 'total',
                    },
                "fontWeight": "bold",
            }

            # {
            #     'if': {
            #         'row_index': table_data_len,  # number | 'odd' | 'even'
            #     },
            #     'color': 'black',
            #     "fontWeight": "bold",
            # },
        ]
    )
    return credit_datatable