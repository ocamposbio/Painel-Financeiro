from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import sidebar, dashboards, extratos

from globals import *
from globals import cat_despesa, cat_receita, df_cat_receita, df_cat_despesa, df_despesa, df_receita

# =========  Layout  =========== #
content = html.Div(id="page-content") #Var Content#


#layout principal
app.layout = dbc.Container(children=[ 
    dcc.Store(id='store-receita', data=df_receita.to_dict()),
    dcc.Store(id='store-despesa', data=df_despesa.to_dict()),
    dcc.Store(id='store-cat_receita', data=df_cat_receita.to_dict()),
    dcc.Store(id='store-cat_despesa', data=df_cat_despesa.to_dict()),

    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout

        ], md=2, style={'background-color': 'white', 'height': '1080px'}),
        dbc.Col([
            content
        ], md=10, style={'background-color': 'white', 'height': '1080px'})
    ])


], fluid=True,)

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def render_page(pathname):
    if pathname == ' /' or pathname == '/dashboards':
        return dashboards.layout
    
    if pathname == '/extratos':
        return extratos.layout


if __name__ == '__main__':
    app.run_server(port=8051, debug=True)