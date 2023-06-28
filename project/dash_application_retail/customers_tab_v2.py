import dash_bootstrap_components as dbc
import datetime
from dash import html, dcc
import plotly.graph_objs as go



def customers_tab_content():
    mapbox_layout = go.Layout(
        mapbox=dict(
            accesstoken='pk.eyJ1IjoiZXZnZW55emgyMzExIiwiYSI6ImNsZ2tpM2ZzODFmeDAzdXQxOHgzcmp1aWcifQ.2f-1wW_y9wsqWEZJir3xEQ',
            center=dict(
                lat=38.92,
                lon=-77.07
            ),
            zoom=10,
            style='open-street-map'
        )
    )
    data = [go.Scattermapbox(
        lat=['38.92', '38.91', '38.93'],
        lon=['-77.07', '-77.06', '-77.08'],
        mode='markers',
        marker=dict(
            size=14,
            color='rgb(255, 0, 0)'
        ),
        text=['Washington DC', 'Maryland', 'Virginia']
    )]






    tab_customers = html.Div(
        children=[
            html.Div([
                dcc.Graph(
                    id='scatter-mapbox',
                    figure={
                        'data': data,
                        'layout': mapbox_layout
                    }
                )
            ]),

            html.Div([
                html.Label('Marker Color'),
                dcc.Dropdown(
                    id='marker-color',
                    options=[
                        {'label': 'Red', 'value': 'rgb(255, 0, 0)'},
                        {'label': 'Green', 'value': 'rgb(0, 255, 0)'},
                        {'label': 'Blue', 'value': 'rgb(0, 0, 255)'}
                    ],
                    value='rgb(255, 0, 0)'
                )
            ])

        ]
    )






    return tab_customers