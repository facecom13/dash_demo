from dash import html, dcc
import dash_bootstrap_components as dbc

def theme_selector():
    theme_selector = html.Div(style={
        'marginTop': '15px'
    },
        children=[
            dbc.Row(
                dbc.Col(width=2,
                    children=[
                        dcc.Dropdown(
                            options={'cerulean': 'cerulean', 'darkly':'darkly'},
                            multi=False,
                            placeholder="Тема...",
                            id='theme_select',
                            # optionHeight=50,
                        ),

                    ]
                )
            )
        ]
    )
    return theme_selector