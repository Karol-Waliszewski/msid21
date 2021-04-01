import requests
from threading import Timer
from enum import Enum

# Api
BITBAY_API = "https://bitbay.net/API/Public/"
BITSTAMP_API = "https://www.bitstamp.net/api/v2/"
APIS = Enum('API', 'BITBAY BITSTAMP')

# Base variables
BASE_INTERVAL = 10
BASE_LIMIT = 20
BASE_CURRENCY = "USD"

# Tickers
CRYPTOCURRENCIES = ["BTC", "ETH", "LTC"]


def setInterval(func, interval):
    func()

    def func_wrapper():
        setInterval(func, interval)

    Timer(interval, func_wrapper).start()


def requestAPI(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.reason)
        return None


def getOrders(api, cryptocurrency, currency, limit=BASE_LIMIT):
    if api == APIS.BITBAY:
        url = f'{BITBAY_API}{cryptocurrency.upper()}{currency.upper()}/orderbook.json'
        orders = requestAPI(url)
        if orders != None:
            return {'bids': orders['bids'][:limit], 'asks': orders['asks'][:limit]}

    elif api == APIS.BITSTAMP:
        url = f'{BITSTAMP_API}order_book/{cryptocurrency.lower()}{currency.lower()}'
        orders = requestAPI(url)
        if orders != None:
            return {'bids': list(map(lambda el: [float(el[0]), float(el[1])], orders['bids'][:limit])), 'asks': list(map(lambda el: [float(el[0]), float(el[1])], orders['asks'][:limit]))}

    return None


def calculateDifference(minimalArray, maximalArray):
    minimalValue, maximalValue = 1, 1
    if len(minimalArray) > 0:
        minimalValue = min(minimalArray)[0]
    if len(maximalArray) > 0:
        maximalValue = max(maximalArray)[0]

    difference = (minimalValue - maximalValue) / maximalValue * 100
    return difference


def calculateDifference(arr1, arr2, comparison="min/max"):
    val1, val2 = 1, 1

    # Calculation is based on comparison method
    if comparison == "min/max":
        if len(arr1) > 0:
            val1 = min(arr1)[0]
        if len(arr2) > 0:
            val2 = max(arr2)[0]

    elif comparison == "max/min":
        if len(arr1) > 0:
            val1 = max(arr1)[0]
        if len(arr2) > 0:
            val2 = min(arr2)[0]

    elif comparison == "min/min":
        if len(arr1) > 0:
            val1 = min(arr1)[0]
        if len(arr2) > 0:
            val2 = min(arr2)[0]

    elif comparison == "max/max":
        if len(arr1) > 0:
            val1 = max(arr1)[0]
        if len(arr2) > 0:
            val2 = max(arr2)[0]

    else:
        raise ValueError("Wrong comparison type")

    difference = (val1 - val2) / val2 * 100
    return difference


def printDifference(profit, ticker, note):
    if note:
        print(f'Difference on {ticker}[{note}]: {profit:.4f}%')
    else:
        print(f'Difference on {ticker}: {profit:.4f}%')


def ex1a():
    for crypto in CRYPTOCURRENCIES:
        bitbayOrders = getOrders(APIS.BITBAY, crypto, BASE_CURRENCY, 5)
        bitstampOrders = getOrders(APIS.BITSTAMP, crypto, BASE_CURRENCY, 5)
        if bitbayOrders and bitstampOrders:
            bitbayBuys = bitbayOrders['asks']
            bitstampBuys = bitstampOrders['asks']
            difference = calculateDifference(bitbayBuys, bitstampBuys, "min/min")
            printDifference(difference, crypto, "BITBAY buy vs BITSTAMP buy")


def ex1b():
    for crypto in CRYPTOCURRENCIES:
        bitbayOrders = getOrders(APIS.BITBAY, crypto, BASE_CURRENCY, 5)
        bitstampOrders = getOrders(APIS.BITSTAMP, crypto, BASE_CURRENCY, 5)
        if bitbayOrders and bitstampOrders:
            bitbaySells = bitbayOrders['bids']
            bitstampSells = bitstampOrders['bids']
            difference = calculateDifference(bitbaySells, bitstampSells, "max/max")
            printDifference(difference, crypto, "BITBAY sell vs BITSTAMP sell")


def main():
    setInterval(ex1a, BASE_INTERVAL)
    setInterval(ex1b, BASE_INTERVAL)


if __name__ == "__main__":
    main()
