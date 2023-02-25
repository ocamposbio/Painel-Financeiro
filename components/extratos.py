import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from globals import cat_despesa, cat_receita, df_cat_receita, df_cat_despesa, df_despesa, df_receita
from app import app

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        html.Legend('Tabela de Despesas'),
        html.Div(id='tabela-de-despesa', className='dbc')
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph', style={'margin-right': '20px'})
        ], width=9),
        dbc.Col([
            dbc.CardBody([
                html.H4('Despesas'),
                html.Legend("R$ 4400", id="valor-despesa-card",
                            style={'font-size': '60px'}),
                html.H6("Total de Despesas"),
            ], style={'text-align': 'center', 'padding-top': '30px'})
        ], width=3)
    ])

], style={'padding': '10px'})

# =========  Callbacks  =========== #
# Tabela
