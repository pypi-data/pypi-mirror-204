from typing import Any

from novalabs.clients.binance import Binance
from novalabs.clients.btcex import BTCEX
from novalabs.clients.bybit import Bybit
from novalabs.clients.huobi import Huobi
from novalabs.clients.kucoin import Kucoin
from novalabs.clients.oanda import Oanda
from novalabs.clients.okx import OKX


def clients(
    exchange: str,
    api_key: str = "",
    api_secret: str = "",
    passphrase: str = "",
) -> Any:
    if exchange == "binance":
        return Binance(
            api_key=api_key, api_secret=api_secret, passphrase=passphrase, limit=1000
        )
    elif exchange == "okx":
        return OKX(
            api_key=api_key, api_secret=api_secret, passphrase=passphrase, limit=100
        )
    elif exchange == "kucoin":
        return Kucoin(
            api_key=api_key, api_secret=api_secret, passphrase=passphrase, limit=1000
        )
    elif exchange == "huobi":
        return Huobi(
            api_key=api_key, api_secret=api_secret, passphrase=passphrase, limit=2000
        )
    elif exchange == "bybit":
        return Bybit(
            api_key=api_key, api_secret=api_secret, passphrase=passphrase, limit=1000
        )
    elif exchange == "oanda":
        return Oanda(
            api_key=api_key, api_secret=api_secret, passphrase=passphrase, limit=1000
        )
    elif exchange == "btcex":
        return BTCEX(
            api_key=api_key, api_secret=api_secret, passphrase=passphrase, limit=1000
        )
