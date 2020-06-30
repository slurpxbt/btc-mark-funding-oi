# this script pulls oi,funding and mark price data from bitmex, bybit, Okex, Binance for BTC perpetual swap contracts

# ---------------------------
# requirements:
#   pip install bybit
#   pip install bitmex-ws
# if any other package is missing just pip install it 
# ---------------------------



# imports --------------------------------------------------
# bitmex imports
from bitmex_websocket import BitMEXWebsocket
import datetime

# bybit imports
import bybit

# binance imports
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *

# okex imports
from okex import swap_api as swap
from okex import futures_api as future
import json

# -----------------------------------------------------------





# get data from bitmex
ws_btc = BitMEXWebsocket(endpoint="https://www.bitmex.com", symbol="XBTUSD", api_key=None, api_secret=None)

data_btc = ws_btc.get_instrument()

mex_oi = data_btc["openInterest"]
mex_mark = data_btc["markPrice"]
mex_funding = data_btc["fundingRate"]
# -----------------------------------------------------------

# get data from bybit 
client = bybit.bybit(test=False, api_key="", api_secret="")

info = client.Market.Market_symbolInfo(symbol="BTCUSD").result()
info_dict = info[0]["result"][0]

bybit_mark = float(info_dict["mark_price"])
bybit_oi = int(info_dict["open_interest"])
bybit_funding = float(info_dict["funding_rate"])
# -----------------------------------------------------------

# get data from binance
request_client = RequestClient(api_key="None", secret_key="None", url="https://fapi.binance.com")

binance_oi = request_client.get_open_interest(symbol="BTCUSDT")
binance_mark = request_client.get_mark_price(symbol="BTCUSDT")
# -----------------------------------------------------------

# get data from okex
api_key = ""
secret_key = ""
passphrase = ""
swap_contract = "BTC-USD-SWAP"

swapAPI = swap.SwapAPI(api_key, secret_key, passphrase)
mark_price_api = swapAPI.get_mark_price(swap_contract)
okex_mark = float(mark_price_api["mark_price"])

funding_api = swapAPI.get_funding_time(swap_contract)
okex_funding = float(funding_api["funding_rate"])

oi = swapAPI.get_holds(swap_contract)
okex_oi = int(oi["amount"])
# -----------------------------------------------------------


# -----------------------------------------------------------
# print outs
print("-" * 200)
print(f"{round(mex_mark, 1)}[USD] - {round(mex_funding * 100, 3)}[%] - {round((mex_oi / (10 ** 6)), 3)}[mil] => Bitmex")
print(f"{round(bybit_mark,1)}[USD] - {round(bybit_funding * 100, 3)}[%] - {round((bybit_oi / (10 ** 6)), 3)}[mil] => Bybit")
print(f"{round(binance_mark.markPrice,1)}[USD] - {round(binance_mark.lastFundingRate * 100, 3)}[%] - {round((binance_oi.openInterest * binance_mark.markPrice / 10**6), 3)}[mil] => Binance")
print(f"{round(okex_mark,1)}[USD] - {round(okex_funding * 100, 3)}[%] - {round((okex_oi * 100 / (10 ** 6)), 3)}[mil] => Okex")
print("-" * 200)










