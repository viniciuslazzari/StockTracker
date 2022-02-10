import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

api_key = 'A6XD7GJ7B7UE9JAT'
symbol = 'AMZN'
function = 'TIME_SERIES_DAILY'
outputsize = 'full'


def main():
    url = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' + \
        symbol + '&outputsize=' + outputsize + '&apikey=' + api_key
    r = requests.get(url)
    data = r.json()

    fistDate = list(data['Time Series (Daily)'])[-1]

    previous = float(data['Time Series (Daily)'][fistDate]['4. close'])

    i = 0
    closes = []
    days = []
    markers = []

    for key in reversed(data['Time Series (Daily)'].keys()):
        if i == 0:
            i = i + 1
            continue

        daily = data['Time Series (Daily)'][key]

        close = float(daily['4. close'])

        variation = (close / previous - 1) * 100

        if variation > 10:
            markers.append(key)

        closes.append(close)
        days.append(key)

        previous = close

    markers = [days.index(i) for i in markers]

    plt.plot(days, closes, markevery=markers, marker="o",
             markerfacecolor='red', markersize=8)
    plt.title('Amazon stock price (1999 - 2022)', size=18)
    plt.xticks(rotation=45)

    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    plt.show()


if __name__ == "__main__":
    main()
