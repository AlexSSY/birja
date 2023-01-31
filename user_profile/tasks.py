import requests
from celery import shared_task


@shared_task
def get_p2p():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }

    data = {
        "asset": "USDT",
        "countries": [],
        "fiat": "UAH",
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "proMerchantAds": False,
        "rows": 10,
        "tradeType": "BUY"
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()


print(get_p2p())