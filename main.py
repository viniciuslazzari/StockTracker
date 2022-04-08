import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines

api_key = 'A6XD7GJ7B7UE9JAT'
function = 'TIME_SERIES_DAILY'
output_size = 'full'

def get_cotations_data(symbol):
    url = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' + \
        symbol + '&outputsize=' + output_size + '&apikey=' + api_key
    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame.from_dict(data['Time Series (Daily)']).transpose()

    df = df.iloc[::-1]

    df = df.set_index(pd.to_datetime(df.index, format='%Y-%m-%d'))

    return df

def get_intraday_variation(previous_value, close_value):
    variation = (close_value / previous_value - 1) * 100

    return variation

def plot_graph(title, legend, days, closes, markers):
    plt.plot(days, closes, markevery=markers, marker="o",
             markerfacecolor='red', markersize=8)
    plt.title(title, size=18, pad=24)
    plt.xticks(rotation=90)

    plt.grid(axis='y')
    plt.margins(x=0)

    plt.ylabel("Performance", labelpad=15)

    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    red_square = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=10, label=legend)
                        
    plt.legend(handles=[red_square])

    plt.show()

def build_title(symbol, df):
    min_date = df.index[0].year
    max_date = df.index[-1].year

    title = symbol + " " + "stock performance" + " " + "(" + str(min_date) + " - " + str(max_date) + ")"

    return title

def build_legend(operator, reference):
    operator_dict = {
        "=": "=",
        "+": ">",
        "-": "<",
    }

    legend = "Variation" + " " + operator_dict[operator] + " " + str(reference)

    return legend

def test_variation(operator, reference, variation):
    if operator == "=":
        return reference == variation
    elif operator == "+":
        return reference < variation
    elif operator == "-":
        return reference > variation
    else:
        return False

def get_arguments():
    symbol = sys.argv[1]
    operator = sys.argv[2]
    reference = float(sys.argv[3])

    return symbol, operator, reference

def main():
    symbol, operator, reference = get_arguments()

    df = get_cotations_data(symbol)

    previous_value = float(df.tail(1)['4. close'])

    closes = []
    days = []
    markers = []

    for index, row in df.iloc[1:].iterrows():
        close_value = float(row['4. close'])

        variation = get_intraday_variation(previous_value, close_value)

        if test_variation(operator, reference, variation):
            markers.append(index)

        closes.append(close_value)
        days.append(index)

        previous_value = close_value

    markers = [days.index(day) for day in markers]

    title = build_title(symbol, df)
    legend = build_legend(operator, reference)

    plot_graph(title, legend, days, closes, markers)


if __name__ == "__main__":
    main()
