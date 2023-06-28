from dash import html
import dash_bootstrap_components as dbc
def credit_grapf_period_text_func(credit_grapf_text_first_date, credit_grapf_text_last_date):
    first_date_text = credit_grapf_text_first_date.strftime('%d.%m.%Y')
    last_date_text = credit_grapf_text_last_date.strftime('%d.%m.%Y')

    block = html.Div(style={
        "display": "inline-block",
        # "width": "20%"
    },
        children=[
            html.Div(html.P('Период:'), style={"display": "inline-block", 'fontWeight': 'bold', 'fontSize': '20px'}),
            html.Div(html.P(f'с {first_date_text} по {last_date_text}'),
                     style={"display": "inline-block", 'fontWeight': 'bold', 'fontSize': '20px',
                            # 'color': '#FFC000',
                            'color': '#32935F',
                            'marginLeft': '7px'})
        ]
    )
    credit_grapf_period_text = block

    return credit_grapf_period_text