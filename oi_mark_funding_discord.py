# this script pulls oi,funding and mark price data from bitmex, bybit, Okex, Binance for BTC perpetual swap contracts
# and aggreates data from whole market into files
#TODO: change data_file_path to your own in rows 42 and 174
# ---------------------------
# requirements:
#   pip install bybit
#   pip install bitmex-ws
#   pip install APScheduler
#   pip install bitmex
# if any other package is missing just pip install it 
# ---------------------------



# imports --------------------------------------------------
import numpy as np

# bitmex imports
import bitmex
import datetime

# bybit imports
import bybit

# binance imports
from binance_f import RequestClient

# okex imports
from okex import swap_api as swap
from okex import futures_api as future
import json
from dhooks import Webhook

# -----------------------------------------------------------


hook = Webhook("YOUR DISCORD WEBHOOK URL")

def get_and_store_btc_data():
    """
        This script pulls OI, funding and mark price from bitmex, bybit, binance and okex
    """

    client = bitmex.bitmex(test=False)
    instrument_data = client.Instrument.Instrument_get(symbol='XBTUSD').result()

    mex_mark = round(instrument_data[0][0]["markPrice"], 1)                      # [USD]
    mex_oi = round(instrument_data[0][0]["openInterest"] / 10 ** 6, 3)           # [mil USD]
    mex_funding = round(instrument_data[0][0]["fundingRate"] * 100, 3)           # [%]
    # -----------------------------------------------------------

    # get data from bybit 
    client = bybit.bybit(test=False, api_key="", api_secret="")

    info = client.Market.Market_symbolInfo(symbol="BTCUSD").result()
    info_dict = info[0]["result"][0]

    bybit_mark = round(float(info_dict["mark_price"]), 1)               # [USD]
    bybit_oi = round(int(info_dict["open_interest"]) / 10 ** 6, 3)      # [mil USD]
    bybit_funding = round(float(info_dict["funding_rate"]) * 100, 3)    # [%]
    # -----------------------------------------------------------

    # get data from binance
    request_client = RequestClient(api_key="None", secret_key="None", url="https://fapi.binance.com")

    binance_oi_api = request_client.get_open_interest(symbol="BTCUSDT")
    binance_mark_api = request_client.get_mark_price(symbol="BTCUSDT")

    binance_mark = round(binance_mark_api.markPrice , 1)                            # [USD]
    binance_funding = round(binance_mark_api.lastFundingRate * 100, 3)              # [mil USD]
    binance_oi = round(binance_oi_api.openInterest * binance_mark / 10 ** 6, 3)     # [%]
    # -----------------------------------------------------------   

    # get data from okex
    api_key = ""
    secret_key = ""
    passphrase = ""
    swap_contract = "BTC-USD-SWAP"

    swapAPI = swap.SwapAPI(api_key, secret_key, passphrase)
    mark_price_api = swapAPI.get_mark_price(swap_contract)
    okex_mark = round(float(mark_price_api["mark_price"]), 1)               # [USD]

    funding_api = swapAPI.get_funding_time(swap_contract)
    okex_funding = round(float(funding_api["funding_rate"]) * 100, 3)       # [%]

    oi = swapAPI.get_holds(swap_contract)
    okex_oi = round(int(oi["amount"]) * 100 / 10 ** 6, 3)                   # [mil USD]
    # -----------------------------------------------------------

    # time 
    time = datetime.datetime.now().strftime("%Y-%d-%m %H:%M") # year-day-month hours-minutes-seconds


    # -----------------------------------------------------------

    # avg mark, cum OI, oi weighted funding
    avg_mark = round(np.average([mex_mark, bybit_mark, binance_mark, okex_mark]), 2)    # [USD]
    cum_OI = round(np.sum([mex_oi, bybit_oi, binance_oi, okex_oi]), 3)                  # [mil USD 1000mil => 1bil]
    oi_w_funding = round((mex_oi*mex_funding + bybit_oi*bybit_funding + binance_oi*binance_funding + okex_oi*okex_funding)/(mex_oi + bybit_oi + binance_oi + okex_oi), 3)   # [%] => (-) bears are paying, (+) bulls are paying


    dis_msg = f"```BTC: mark price: {avg_mark} $ || cum OI: {cum_OI} mil USD || OI w funding {oi_w_funding} %```"
    hook.send(dis_msg)
    # -----------------------------------------------------------



def get_and_store_eth_data():


    #data_btc = ws_btc.get_instrument()
    client = bitmex.bitmex(test=False)
    instrument_data = client.Instrument.Instrument_get(symbol='ETHUSD').result()

    mex_mark = round(instrument_data[0][0]["markPrice"], 1)                      # [USD]
    mex_oi = round(instrument_data[0][0]["openInterest"] / 10 ** 6, 3)           # [mil USD]
    mex_funding = round(instrument_data[0][0]["fundingRate"] * 100, 3)           # [%]
    # -----------------------------------------------------------

    # get data from bybit 
    client = bybit.bybit(test=False, api_key="", api_secret="")

    info = client.Market.Market_symbolInfo(symbol="ETHUSD").result()
    info_dict = info[0]["result"][0]

    bybit_mark = round(float(info_dict["mark_price"]), 1)               # [USD]
    bybit_oi = round(int(info_dict["open_interest"]) / 10 ** 6, 3)      # [mil USD]
    bybit_funding = round(float(info_dict["funding_rate"]) * 100, 3)    # [%]
    # -----------------------------------------------------------

    # get data from binance
    request_client = RequestClient(api_key="None", secret_key="None", url="https://fapi.binance.com")

    binance_oi_api = request_client.get_open_interest(symbol="ETHUSDT")
    binance_mark_api = request_client.get_mark_price(symbol="ETHUSDT")

    binance_mark = round(binance_mark_api.markPrice , 1)                            # [USD]
    binance_funding = round(binance_mark_api.lastFundingRate * 100, 3)              # [mil USD]
    binance_oi = round(binance_oi_api.openInterest * binance_mark / 10 ** 6, 3)     # [%]
    # -----------------------------------------------------------   

    # get data from okex
    api_key = ""
    secret_key = ""
    passphrase = ""
    swap_contract = "ETH-USD-SWAP"

    swapAPI = swap.SwapAPI(api_key, secret_key, passphrase)
    mark_price_api = swapAPI.get_mark_price(swap_contract)
    okex_mark = round(float(mark_price_api["mark_price"]), 1)               # [USD]

    funding_api = swapAPI.get_funding_time(swap_contract)
    okex_funding = round(float(funding_api["funding_rate"]) * 100, 3)       # [%]

    oi = swapAPI.get_holds(swap_contract)
    okex_oi = round(int(oi["amount"]) * 10 / 10 ** 6, 3)                   # [mil USD]
    # -----------------------------------------------------------

    # time 
    time = datetime.datetime.now().strftime("%Y-%d-%m %H:%M") # year-day-month hours-minutes-seconds


    # -----------------------------------------------------------

    # avg mark, cum OI, oi weighted funding
    avg_mark = round(np.average([mex_mark, bybit_mark, binance_mark, okex_mark]), 3)    # [USD]
    cum_OI = round(np.sum([mex_oi, bybit_oi, binance_oi, okex_oi]), 3)                  # [mil USD 1000mil => 1bil]
    oi_w_funding = round((mex_oi*mex_funding + bybit_oi*bybit_funding + binance_oi*binance_funding + okex_oi*okex_funding)/(mex_oi + bybit_oi + binance_oi + okex_oi), 3)   # [%] => (-) bears are paying, (+) bulls are paying

    
    dis_msg = f"```ETH: mark price: {avg_mark} $ || cum OI: {cum_OI} mil USD || OI w funding {oi_w_funding} %```"
    hook.send(dis_msg)

  
  








