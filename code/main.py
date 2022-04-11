import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines

# Variáveis padrão para realizar a consulta a API
api_key = '############'
function = 'TIME_SERIES_DAILY'
output_size = 'full'

def get_cotations_data(symbol):
    # Monta a URL da requisição
    url = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' + \
        symbol + '&outputsize=' + output_size + '&apikey=' + api_key

    # Realiza a requisição
    r = requests.get(url)
    data = r.json()

    # Cria o dataframe já invertendo índices e colunas
    df = pd.DataFrame.from_dict(data['Time Series (Daily)']).transpose()

    # Inverte a ordem do dataframe (data mais antiga primero)
    df = df.iloc[::-1]

    # Converte o índice do dataframe de string para o objeto de data do Pandas
    df = df.set_index(pd.to_datetime(df.index, format='%Y-%m-%d'))

    return df

def get_intraday_variation(previous_value, close_value):
    # Variação de um dia para o outro = (valor de fechamento atual / valor de fechamento anterior - 1) * 100
    variation = (close_value / previous_value - 1) * 100

    return variation

def plot_graph(title, legend, days, closes, markers):
    # Plota o gráfica relacionando datas e fechamentos, inserindo os marcadores
    plt.plot(days, closes, markevery=markers, marker="o",
        markerfacecolor='red', markersize=8)
        
    # Define tamanhos de títulos e rotações de labels
    plt.title(title, size=18, pad=24)
    plt.xticks(rotation=90)

    # Remove a margem dos lados e adiciona o grid horizontal
    plt.grid(axis='y')
    plt.margins(x=0)

    # Adiciona label de performance ao gráfico
    plt.ylabel("Performance", labelpad=15)

    # Converte datas para anos
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Cria a legenda do gráfico
    red_square = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
        markersize=10, label=legend)         
    plt.legend(handles=[red_square])

    # Mostra o resultado na tela
    plt.show()

def build_title(symbol, df):
    # Busca o menor e maior ano de dados obtidos
    min_date = df.index[0].year
    max_date = df.index[-1].year

    # Monta a string de título
    title = symbol + " " + "stock performance" + " " + "(" + str(min_date) + " - " + str(max_date) + ")"

    return title

def build_legend(operator, reference):
    # Cria um dicionário para traduzir o operador passado
    operator_dict = {
        "=": "=",
        "+": ">",
        "-": "<",
    }

    # Monta a string de legenda
    legend = "Variation" + " " + operator_dict[operator] + " " + str(reference)

    return legend

def test_variation(operator, reference, variation):
    # Identifica qual o operador passado e realiza o determinado teste
    if operator == "=":
        # Testa se são iguais
        return reference == variation
    elif operator == "+":
        # Testa se a variação é maior que a referência
        return reference < variation
    elif operator == "-":
        # Testa se a variação é menor que a referência
        return reference > variation
    else:
        # Trata erro caso o operador não seja reconhecido
        return False

def get_arguments():
    # Recebe os argumentos do vetor de argumentos passado
    symbol = sys.argv[1]
    operator = sys.argv[2]
    reference = float(sys.argv[3])

    # Retorna os parâmetros
    return symbol, operator, reference

def main():
    # Recebe os argumentos passados
    symbol, operator, reference = get_arguments()

    # Recebe o datafram com os dados das cotações
    df = get_cotations_data(symbol)

    # Recebe o valor de fechamento da menor data
    previous_value = float(df.tail(1)['4. close'])

    # Cria os vetores auxiliares
    closes = []
    days = []
    markers = []

    # Itera por todos os dias disponíveis, pulando o menor deles
    for index, row in df.iloc[1:].iterrows():
        # Recebe o valor de fechamento do dia atual
        close_value = float(row['4. close'])

        # Recebe a variação atual do preço do ativo, baseado no fechamento anterior e atual
        variation = get_intraday_variation(previous_value, close_value)

        # Trata todos os tipos de operando passados
        if test_variation(operator, reference, variation):
            # Caso a variação tenha passado no teste, salva ela no vetor auxiliar
            markers.append(index)

        # Salva o fechamento e dia atuais para plotas no gráfico
        closes.append(close_value)
        days.append(index)

        # Prepara o valor anterior de fechamento como o valor atual para a próxima iteração
        previous_value = close_value

    # Converte os dias salvos para marcação em índices do vetor de dias
    markers = [days.index(day) for day in markers]

    # Monta o título e legenda do gráfico
    title = build_title(symbol, df)
    legend = build_legend(operator, reference)

    # Plota o resultado final
    plot_graph(title, legend, days, closes, markers)


if __name__ == "__main__":
    main()
