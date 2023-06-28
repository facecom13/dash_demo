import datetime
from dash import html
import dash_bootstrap_components as dbc
def treemap_period_text_func(df):
    # Получение первой даты в выборке
    df = df.copy()
    df.sort_values(['date'], inplace=True, ignore_index=True)
    first_date = df.iloc[0, df.columns.get_loc("date")]
    first_date_text = first_date.strftime('%d.%m.%Y')
    last_date = df.iloc[-1, df.columns.get_loc("date")]
    last_date_text = last_date.strftime('%d.%m.%Y')

    today = datetime.datetime.now()
    today_text = today.strftime("%d.%m.%Y")
    # credit_grapf_period_text = dbc.FormText(
    #     f"Границы отчета: с {today_text} по {last_date_text}",
    #     color="secondary",
    # ),

    block = html.Div(style={
        "display": "inline-block",
        # "width": "20%"
    },
        children=[
            html.Div(html.P('Период:'), style={"display": "inline-block", 'fontWeight': 'bold', 'fontSize': '20px'}),
            html.Div(html.P(f'с {today_text} по {last_date_text}'),
                     style={"display": "inline-block", 'fontWeight': 'bold', 'fontSize': '20px', 'color': '#FFC000',
                            'marginLeft': '7px'})
        ]
    )
    credit_grapf_period_text = block

    return credit_grapf_period_text