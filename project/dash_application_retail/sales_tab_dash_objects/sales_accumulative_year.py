import datetime

import plotly.graph_objects as go
import dash_application.dash_objects.initial_values as initial_values
from dash import dcc

def sales_accumulative_year_func(df, sales_tab_product_category_select):
    product_category_options_list = list(df['product_category'].unique())
    product_category_options = {}
    for item in product_category_options_list:
        product_category_options[item] = item




    customer_product_category_full_list = list(df['product_category'].unique())
    product_category_filter = customer_product_category_full_list
    if sales_tab_product_category_select:
        if 'list' in str(type(sales_tab_product_category_select)):
            product_category_filter = sales_tab_product_category_select
        else:
            product_category_filter = list(sales_tab_product_category_select)

    # режем выборку
    df = df.loc[df['product_category'].isin(product_category_filter)]

    date_min = df['date'].min()
    date_max = df['date'].max()

    max_value = df['payment_amount'].sum()

    # ряд с планами продаж
    sales_df = df.groupby(['date'], as_index=False).agg({'plan': 'sum'})

    df = df.loc[df['date']<=datetime.datetime.now()]




    fig = go.Figure()
    colors = list(initial_values.colors_dict.values())

    i = 0
    max_graph_value_ = 0
    for product_category in customer_product_category_full_list:
        temp_product_category_df = df.loc[df['product_category']==product_category]
        temp_product_category_df = temp_product_category_df.copy()
        temp_product_category_df['cum_sales'] = temp_product_category_df['payment_amount'].cumsum()

        max_graph_value = temp_product_category_df['cum_sales'].max()
        max_graph_value_ = max_graph_value_ + max_graph_value

        x_dates = temp_product_category_df['date']
        y_sales = temp_product_category_df['cum_sales']

        fig.add_trace(go.Scatter(
            x=x_dates,
            y=y_sales,
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5, color=colors[i]),
            name = product_category,
            stackgroup='one'
        ))
        i = i+1


    fig.add_trace(go.Scatter(x=sales_df['date'], y=sales_df['plan'], name='План продаж', line={'color': 'gray'}))

    fig.update_layout({
        # 'xaxis_tickangle': -90,
        'margin': dict(l=2, r=18, t=5, b=5),

        # "title": "Погашение кредитного портфеля",
        'legend': {
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1.08,
        }
    })
    fig.update_xaxes(range=[date_min, date_max])
    fig.update_yaxes(range=[0, max_graph_value_*2])

    output = dcc.Graph(figure=fig, config={'displayModeBar': False, 'locale':"ru"})


    return output, product_category_options



