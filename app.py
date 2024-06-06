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
            valores["Temperatura"] = round(random.uniform(10, 23))  #Temperatura em graus Celsius 
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

df = criar_dataframe()

#Criando layout do gráfico
fig = px.bar(df, x="Dados", y="Quantidade", color="Oceano", barmode="group")

opcoes = list(df['Oceano'].unique())
opcoes.append('Todos os Oceanos')

app.layout = html.Div(children=[
    html.H1(children='Océan Sûr'),
    html.H2(children=' "Mudamos a forma de ver o oceano" '),
    html.P(children='''
        Esta plataforma serve para ver e analisar como estão as condições do oceano
    '''),
    html.Div(id='texto'),
    dcc.Dropdown(opcoes, value='Todos os Oceanos', id='lista_oceanos'),  #Gera o campo de escolha
    dcc.Graph(
        id='grafico_dados_oceanos',
        figure=fig
    ),
    dcc.Interval(
        id='intervalo',
        interval=30*1000,  #Atualiza a cada 30 segundos (30000 milissegundos)
        n_intervals=0
    )
])

@app.callback(
    #Quem vai ser modificado
    Output('grafico_dados_oceanos', 'figure'),
    #Responsável por selecionar o valor e pelo intervalo de tempo
    [Input('lista_oceanos', 'value'), Input('intervalo', 'n_intervals')]
)
def atualiza_output(value, n):
    df = criar_dataframe()  #Atualiza os dados
    if value == 'Todos os Oceanos':
        fig = px.bar(df, x="Dados", y="Quantidade", color="Oceano", barmode="group")
    else:
        tabela_filtrada = df.loc[df['Oceano'] == value, :]
        fig = px.bar(tabela_filtrada, x="Dados", y="Quantidade", color="Oceano", barmode="group")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
