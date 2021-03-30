import requests
from time import sleep
from enum import Enum

BITBAY_API = "https://bitbay.net/API/Public/"
BITSTAMP_API = "https://www.bitstamp.net/api/"

APIS = Enum('API', 'BITBAY BITSTAMP')


def setInterval(func, interval):
    func()
    sleep(5)
    setInterval(func, interval)


def requestAPI(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.reason)
        return None


def getOrders(api, cryptocurrency, currency, limit=10):
    if api == APIS.BITBAY:
        url = f'{BITBAY_API}{cryptocurrency}{currency}/orderbook.json'
        orders = requestAPI(url)
        if orders != None:
            return {'bids': orders['bids'][:limit], 'asks': orders['asks'][:limit]}

    elif api == APIS.BITSTAMP:
        url = f'{BITSTAMP_API}order_book/{cryptocurrency}{currency}'
        orders = requestAPI(url)
        if orders != None:
            return {'bids': list(map(lambda el: [float(el[0]), float(el[1])], orders['bids'][:limit])), 'asks': list(map(lambda el: [float(el[0]), float(el[1])], orders['asks'][:limit]))}

    return None


# def findProfit(cryptocurrency, currency, limit=5, average=False):
#     orders = getOrders(cryptocurrency, currency, limit)
#     if orders != None:
#         sellOrders, buyOrders = orders['bids'], orders['asks']
#         buyPrice, sellPrice = 0, 0
#         if average:
#             sumOfBuyPrice = 0
#             sumOfSellPrice = 0
#             length = min(len(buyOrders), len(sellOrders))

#             for index in range(length):
#                 sumOfBuyPrice = sumOfBuyPrice + (buyOrders[index][0])
#                 sumOfSellPrice = sumOfSellPrice + (sellOrders[index][0])

#             buyPrice = sumOfBuyPrice / length
#             sellPrice = sumOfSellPrice / length
#         else:
#             buyPrice = max(buyOrders)[0]
#             sellPrice = min(sellOrders)[0]

#         profit = calculateProfit(sellPrice, buyPrice)
#         if average:
#             print(f'Average profit on: {cryptocurrency} = {profit:.2f}%')
#         else:
#             print(f'Profit on: {cryptocurrency} = {profit:.2f}%')


# def calculateProfit(sellPrice=1, buyPrice=1):
#     return 1 - (sellPrice - buyPrice) / buyPrice * 100


def main():
    print(getOrders(APIS.BITBAY, "BTC", 'USD', 3))
    print(getOrders(APIS.BITSTAMP, "BTC", 'USD', 3))


if __name__ == "__main__":
    main()
