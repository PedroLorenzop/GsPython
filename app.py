from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import random

app = Dash(__name__)

#Função para gerar valores aleatórios para pH, Temperatura e Turbidez simulando o arduino
def gerar_valores_aleatorios():
    valores = {}
    while len(valores) < 3:
        if len(valores) == 0:
            valores["pH"] = round(random.uniform(7.5, 8.5), 1)  #Valores de pH da água do mar simulando a realidade
        elif len(valores) == 1:
            valores["Temperatura"] = round(random.uniform(10, 30))  #Temperatura em graus Celsius
        elif len(valores) == 2:
            valores["Turbidez"] = round(random.uniform(2, 100))  #Turbidez em NTU (Unidade Nefelométrica de Turbidez), medida usada para medir a turbidez
    return valores

#Dados do gráfico
def criar_dataframe():
    dados_pacifico = gerar_valores_aleatorios()
    dados_atlantico = gerar_valores_aleatorios()
    dados_indico = gerar_valores_aleatorios()
    dados_artico = gerar_valores_aleatorios()
    return pd.DataFrame({
        "Dados": ["pH", "Temperatura", "Turbidez", 
                  "pH", "Temperatura", "Turbidez", 
                  "pH", "Temperatura", "Turbidez", 
                  "pH", "Temperatura", "Turbidez"],
        "Quantidade": [dados_pacifico["pH"], dados_pacifico["Temperatura"], dados_pacifico["Turbidez"],
                       dados_atlantico["pH"], dados_atlantico["Temperatura"], dados_atlantico["Turbidez"],
                       dados_indico["pH"], dados_indico["Temperatura"], dados_indico["Turbidez"],
                       dados_artico["pH"], dados_artico["Temperatura"], dados_artico["Turbidez"]],
        "Oceano": ["Oceano Pacífico", "Oceano Pacífico", "Oceano Pacífico",
                   "Oceano Atlântico", "Oceano Atlântico", "Oceano Atlântico",
                   "Oceano Índico", "Oceano Índico", "Oceano Índico",
                   "Oceano Ártico", "Oceano Ártico", "Oceano Ártico"]
    })

#"Dicionário" para mapear cores
cor_mapa = {
    'Oceano Pacífico': '#49CF8F',  #Verde
    'Oceano Atlântico': '#3744B9',  #Azul escuro
    'Oceano Índico': '#4BC7D8',  #Azul esverdeado
    'Oceano Ártico': '#4B6AD8',  #Azul claro 
}

#Layout do app.py
app.layout = html.Div(
    children=[
        html.Div(id='cabecalho',children=[
        html.Img(src='/assets/image.png', alt='logo dashboard'),
        html.H1(children='Océan Sûr')]),
        html.H2(children='"Mudamos a forma de ver os oceanos"'),
        html.P(children='Esta plataforma serve para ver e analisar como estão as condições do oceano'),
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
            className='dropdown',
        ),
        html.Div(
            className='grafico-container',
            children=[
                dcc.Graph(
                    id='grafico_condicoes_oceanos'
                )
            ]
        ),
        dcc.Interval(
        id='intervalo-atualizacao',
        interval=30*1000,  #Intervalo de 30 segundos, para trocar é so mudar o "30" lembre-se que está em segundos!
        n_intervals=0
        )
    ]
)

#Callback para atualizar o gráfico toda vez que mexer no dropdown
@app.callback(
    Output('grafico_condicoes_oceanos', 'figure'),
    [Input('lista_oceanos', 'value'),
     Input('intervalo-atualizacao', 'n_intervals')]
)
def atualizar_grafico(oceano_selecionado, n_intervals):
    df = criar_dataframe()  #Cria um novo dataframe com os valores atualizados a cada intervalo
    if oceano_selecionado == 'Todos':
        df_filtrado = df
    else:
        df_filtrado = df[df['Oceano'] == oceano_selecionado]
    
    fig = px.bar(df_filtrado, x='Dados', y='Quantidade', color='Oceano', barmode='group',
                 color_discrete_map=cor_mapa)  #Aplica as cores
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
