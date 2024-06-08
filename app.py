from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import random

app = Dash(__name__)

def gerar_valores_praias():
    valores = {}
    while len(valores) < 3:
        if len(valores) == 0:
            valores["pH"] = round(random.uniform(7.0, 8.0), 1)  # Exemplo de valores de pH para praias
        elif len(valores) == 1:
            valores["Temperatura"] = round(random.uniform(20, 35))  # Exemplo de temperatura em graus Celsius para praias
        elif len(valores) == 2:
            valores["Turbidez"] = round(random.uniform(5, 50))  # Exemplo de turbidez para praias
    return valores

def gerar_valores_aleatorios():
    valores = {}
    while len(valores) < 3:
        if len(valores) == 0:
            valores["pH"] = round(random.uniform(7.5, 8.5), 1)  # Valores de pH da água do mar simulando a realidade
        elif len(valores) == 1:
            valores["Temperatura"] = round(random.uniform(10, 30))  # Temperatura em graus Celsius
        elif len(valores) == 2:
            valores["Turbidez"] = round(random.uniform(2, 100))  # Turbidez em NTU (Unidade Nefelométrica de Turbidez)
    return valores

def criar_dataframe():
    dados_oceanos = {
        "Dados": [],
        "Quantidade": [],
        "Oceano": []
    }
    
    # Dados para oceanos
    for oceano in ["Oceano Pacífico", "Oceano Atlântico", "Oceano Índico", "Oceano Ártico"]:
        valores = gerar_valores_aleatorios()
        dados_oceanos["Dados"].extend(["pH", "Temperatura", "Turbidez"])
        dados_oceanos["Quantidade"].extend([valores["pH"], valores["Temperatura"], valores["Turbidez"]])
        dados_oceanos["Oceano"].extend([oceano] * 3)
    
    # Dados para praias
    praias = ["Guarujá", "Praia Grande", "Santos", "Bertioga"]
    for praia in praias:
        valores = gerar_valores_praias()
        dados_oceanos["Dados"].extend(["pH", "Temperatura", "Turbidez"])
        dados_oceanos["Quantidade"].extend([valores["pH"], valores["Temperatura"], valores["Turbidez"]])
        dados_oceanos["Oceano"].extend([praia] * 3)
    
    return pd.DataFrame(dados_oceanos)

cor_mapa = {
    'Oceano Pacífico': '#49CF8F',  # Verde
    'Oceano Atlântico': '#3744B9',  # Azul escuro
    'Oceano Índico': '#4BC7D8',  # Azul esverdeado
    'Oceano Ártico': '#4B6AD8',  # Azul claro 
}

cor_praia = {
    'Guarujá': '#E00043',  # Rosa
    'Praia Grande': '#FFA63D',  # Amarelo "apagado" 
    'Santos': '#F43636',  # Vermelho
    'Bertioga': '#D9B600', # Amarelo mais "vibrante"
}

app.layout = html.Div(
    children=[
        html.Div(id='cabecalho', children=[
            html.Img(src='/assets/image.png', alt='logo dashboard'),
            html.H1(children='Océan Sûr')
        ]),
        html.H2(children='"Mudamos a forma de ver os oceanos"'),
        html.P(children='Esta plataforma serve para ver e analisar como estão as condições do oceano'),
        dcc.Tabs(id='tabs', value='tab-oceanos', children=[
            dcc.Tab(id = 'troca_secao', label='Oceanos', value='tab-oceanos', children=[
                dcc.Dropdown(
                    id='lista_oceanos',
                    options=[
                        {'label': 'Todos os Oceanos', 'value': 'Todos'},
                        {'label': 'Oceano Pacífico', 'value': 'Oceano Pacífico'},
                        {'label': 'Oceano Atlântico', 'value': 'Oceano Atlântico'},
                        {'label': 'Oceano Índico', 'value': 'Oceano Índico'},
                        {'label': 'Oceano Ártico', 'value': 'Oceano Ártico'}
                    ],
                    value='Todos',
                ),
                html.Div(
                    className='grafico-container',
                    children=[
                        dcc.Graph(
                            id='grafico_condicoes_oceanos'
                        )
                    ]
                ),
            ]),
            dcc.Tab(id = 'troca_secao',label='Praias', value='tab-praias', children=[
                dcc.Dropdown(
                    id='lista_praias',
                    options=[
                        {'label': 'Todas as Praias', 'value': 'Todas'},
                        {'label': 'Guarujá', 'value': 'Guarujá'},
                        {'label': 'Praia Grande', 'value': 'Praia Grande'},
                        {'label': 'Santos', 'value': 'Santos'},
                        {'label': 'Bertioga', 'value': 'Bertioga'}
                    ],
                    value='Todas',
                ),
                html.Div(
                    className='grafico-container',
                    children=[
                        dcc.Graph(
                            id='grafico_condicoes_praias'
                        )
                    ]
                ),
            ]),
        ]),
        dcc.Interval(
            id='intervalo-atualizacao',
            interval=30*1000,  # Intervalo de 30 segundos
            n_intervals=0
        )
    ]
)

@app.callback(
    Output('grafico_condicoes_oceanos', 'figure'),
    [Input('lista_oceanos', 'value'),
     Input('intervalo-atualizacao', 'n_intervals')]
)
def atualizar_grafico_oceanos(oceano_selecionado, n_intervals):
    df = criar_dataframe()  # Criar DataFrame com os valores atualizados
    if oceano_selecionado == 'Todos':
        df_filtrado = df[df['Oceano'].isin(['Oceano Pacífico', 'Oceano Atlântico', 'Oceano Índico', 'Oceano Ártico'])]
    else:
        df_filtrado = df[df['Oceano'] == oceano_selecionado]
    
    fig = px.bar(df_filtrado, x='Dados', y='Quantidade', color='Oceano', barmode='group', color_discrete_map=cor_mapa)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

@app.callback(
    Output('grafico_condicoes_praias', 'figure'),
    [Input('lista_praias', 'value'),
     Input('intervalo-atualizacao', 'n_intervals')]
)
def atualizar_grafico_praias(praia_selecionada, n_intervals):
    df = criar_dataframe()  # Criar DataFrame com os valores atualizados
    if praia_selecionada == 'Todas':
        df_filtrado = df[df['Oceano'].isin(['Guarujá', 'Praia Grande', 'Santos', 'Bertioga'])]
    else:
        df_filtrado = df[df['Oceano'] == praia_selecionada]
    
    fig = px.bar(df_filtrado, x='Dados', y='Quantidade', color='Oceano', barmode='group', color_discrete_map=cor_praia)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)