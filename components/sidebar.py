import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app


from globals import *
from globals import cat_despesa, cat_receita, df_cat_receita, df_cat_despesa, df_despesa, df_receita


from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd
from components import sidebar, dashboards, extratos


# ========= Layout ========= #
layout = dbc.Col([
    html.H1("MoneyHub", className="text-primary"),
    html.P("By Otavio", className="text-info"),
    html.Hr(),

    # perfil -----------------------------
    dbc.Button(id='botao_avatar',
               children=[html.Img(src='/assets/img_hom.png', id='avatar_change', alt='Avatar', className='perfil_avatar')
                         ], style={'background-color': 'transparent', 'bordercolor': 'transparent'}),

    # seção despesa receita -----------------------------
    dbc.Row([
        dbc.Col([
            dbc.Button(color='success', id='open-novo-receita',
                children=['+ Receita'])
        ], width=6),

        dbc.Col([
            dbc.Button(color='danger', id='open-novo-despesa',
                children=['- Despesa'])
        ], width=6)
    ]),

    # MODAL RECEITA  ===========================================================
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar Receita')),
        dbc.ModalBody([
            dbc.Row([
                    dbc.Col([
                        dbc.Label('Descrição: '),
                        dbc.Input(
                            placeholder="Ex: Dividendos, herança, salário, etc.", id='txt-receita'),
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Valor: "),
                        dbc.Input(placeholder="$100,00",
                                  id='valor-receita', value="")
                    ], width=6)
                    ]),

            dbc.Row([
                    dbc.Col([
                        dbc.Label("Data: "),
                        dcc.DatePickerSingle(id='date-receita',
                            min_date_allowed=date(2020, 1, 1),
                            max_date_allowed=date(2030, 12, 31),
                            date=datetime.today(),
                            style={"width": "100%"}
                        ),
                    ], width=4),

                    dbc.Col([
                        dbc.Label("Opções Extras"),
                        dbc.Checklist(
                            options=[{'label': 'Foi recebida', 'value': 1},
                                     {'label': 'Receita Recorrente', 'value': 2}],
                            value=[1],
                            id="switches-input-receita",
                            switch=True),
                    ], width=4),

                    dbc.Col([
                        html.Label("Categoria da receita"),
                        dbc.Select(
                            id='select-receita', 
                            options=[{'Label': i, 'value': i} for i in cat_receita], 
                            value=[])
                    ], width=4)
                    ], style={'margin-top': '25px'}),

            # Categoria de receita
            dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend("Adicionar categoria", style={
                                                'color': 'green'}),
                                    dbc.Input(
                                        type="text", placeholder="Nova categoria...", id="input-add-receita", value=""),
                                    html.Br(),
                                    dbc.Button("Adicionar", className="btn btn-success",
                                               id="add-category-receita", style={"margin-top": '20px'}),
                                    html.Br(),
                                    html.Div(
                                        id="category-div-add-receita", style={}),
                                ], width=6),
                                dbc.Col([
                                    html.Legend('Excluir categorias',
                                                style={'color': 'red'}),
                                    dbc.Checklist(
                                        id='checklist-selected-style-receita',
                                        options=[],
                                        value=[],
                                        label_checked_style={'color': 'red'},
                                        input_checked_style={
                                            'background-color': 'blue', 'border-color': 'orange'},
                                    ),
                                    dbc.Button(
                                        'Remove', color='warning', id='remove-category-receita', style={'margin-top': '20px'}),
                                ], width=6)
                            ])
                        ], title='Adicionar/Remover categorias')
                    ], flush=True, start_collapsed=True, id='accordion-receita'),

                    html.Div(id='id_teste_receita', style={
                             'padding-top': '20px'}),
                    dbc.ModalFooter([
                        dbc.Button("Adicionar nova receita",
                                   id='salvar_receita', color='success'),
                        dbc.Popover(dbc.PopoverBody(
                            "Receita salva!"), target='salvar_receita', placement="left", trigger="click"),

                    ])
                    ], style={'margin-top': '25px'})
        ])
    ], style={"background-color": "rgba(17, 140, 79, 0.05"},
        id="modal-novo-receita",
        size="lg",
        is_open=False,
        centered=True,
        backdrop=True),

    # MODAL DESPESA ===========================================================
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar Despesa')),
        dbc.ModalBody([
            dbc.Row([
                    dbc.Col([
                        dbc.Label('Descrição: '),
                        dbc.Input(
                            placeholder="Ex: Gastos, comida, abastecimento, etc.", id='txt-despesa'),
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Valor: "),
                        dbc.Input(placeholder="$100,00",
                                  id='valor-despesa', value="")
                    ], width=6)
                    ]),

            dbc.Row([
                    dbc.Col([
                        dbc.Label("Data: "),
                        dcc.DatePickerSingle(id='date-despesa',
                            min_date_allowed=date(2020, 1, 1),
                            max_date_allowed=date(2030, 12, 31),
                            date=datetime.today(),
                            style={"width": "100%"}
                        ),
                    ], width=4),

                    dbc.Col([
                        dbc.Label("Extras"),
                        dbc.Checklist(
                            options=[],
                            value=[],
                            id='switches-input-despesa',
                            switch=True
                        )
                    ], width=4),

                    dbc.Col([
                        html.Label("Categoria da despesa"),
                        dbc.Select(id='select-despesa', options=[], value=[])
                    ], width=4)
                    ], style={'margin-top': '25px'}),

            # Categoria de despesa
            dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend("Adicionar categoria", style={
                                                'color': 'green'}),
                                    dbc.Input(
                                        type="text", placeholder="Nova categoria...", id="input-add-despesa", value=""),
                                    html.Br(),
                                    dbc.Button("Adicionar", className="btn btn-success",
                                               id="add-category-despesa", style={"margin-top": '20px'}),
                                    html.Br(),
                                    html.Div(
                                        id="category-div-add-despesa", style={}),
                                ], width=6),
                                dbc.Col([
                                    html.Legend('Excluir categorias',
                                                style={'color': 'red'}),
                                    dbc.Checklist(
                                        id='checklist-selected-style-despesa',
                                        options=[],
                                        value=[],
                                        label_checked_style={'color': 'red'},
                                        input_checked_style={
                                            'background-color': 'blue', 'border-color': 'orange'},
                                    ),
                                    dbc.Button(
                                        'Remove', color='warning', id='remove-category-despesa', style={'margin-top': '20px'}),
                                ], width=6)
                            ])
                        ], title='Adicionar/Remover categorias')
                    ], flush=True, start_collapsed=True, id='accordion-despesa'),

                    html.Div(id='id_teste_despesa', style={
                             'padding-top': '20px'}),
                    dbc.ModalFooter([
                        dbc.Button("Adicionar nova despesa",
                                   id='salvar_despesa', color='success'),
                        dbc.Popover(dbc.PopoverBody(
                            "Despesa salva!"), target='salvar_despesa', placement="left", trigger="click"),

                    ])
                    ], style={'margin-top': '25px'})
        ])
    ], style={"background-color": "rgba(17, 140, 79, 0.05"},
        id="modal-novo-despesa",
        size="lg",
        is_open=False,
        centered=True,
        backdrop=True),

    # Navegar entre páginas -----------------------------
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink("Dashbaord", href='/dashboards', active='extract'),
            dbc.NavLink("Extratos", href='/extratos', active='extract'),
        ], vertical=True, pills=True, id='nav-buttons', style={"margin-bottom": "50px"}),
], id='sidebar_completa')

# =========  Callbacks  =========== #

# Pop-up receita


@app.callback(
    Output('modal-novo-receita', 'is_open'),
    Input('open-novo-receita', 'n_clicks'),
    State('modal-novo-receita', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Pop-up despesa


@app.callback(
    Output('modal-novo-despesa', 'is_open'),
    Input('open-novo-despesa', 'n_clicks'),
    State('modal-novo-despesa', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
