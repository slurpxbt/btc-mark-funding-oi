###########################

# Author: slurpxbt

###########################
# this script pulls oi,funding and mark price data from bitmex, bybit, Okex, Binance for BTC perpetual swap contracts
# and aggreates data from whole market into files
#TODO: change data_file_path to your own in rows 42 and 174

# ---------------------------
# requirements:
#   pip install bybit
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

# -----------------------------------------------------------




def get_and_store_btc_data():


    data_file_path = "YOUR PATH"

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
    # print outs
    print("-" * 200)
    print(f"{mex_mark}[USD] - {mex_funding}[%] - {mex_oi}[mil USD] => Bitmex")
    print(f"{bybit_mark}[USD] - {bybit_funding}[%] - {bybit_oi}[mil USD] => Bybit")
    print(f"{binance_mark}[USD] - {binance_funding}[%] - {binance_oi}[mil USD] => Binance")
    print(f"{okex_mark}[USD] - {okex_funding}[%] - {okex_oi}[mil USD] => Okex")
    print("-" * 200)


    # data storage

    # all data
    all_swap_data = [mex_mark, mex_funding, mex_oi, bybit_mark, bybit_funding, bybit_oi, binance_mark, binance_funding, binance_oi, okex_mark, okex_funding, okex_oi, time]
    all_swap_data_txt = f"{mex_mark};{mex_funding};{mex_oi};{bybit_mark};{bybit_funding};{bybit_oi};{binance_mark};{binance_funding};{binance_oi};{okex_mark};{okex_funding};{okex_oi};{time}\n"


    with open(f"{data_file_path}/data storage/all_swap_data_storage.txt", "a") as store_swap_data:
        store_swap_data.write(all_swap_data_txt)
        store_swap_data.close()


    # -----------------------------------------------------------

    # avg mark, cum OI, oi weighted funding
    avg_mark = round(np.average([mex_mark, bybit_mark, binance_mark, okex_mark]), 3)    # [USD]
    cum_OI = round(np.sum([mex_oi, bybit_oi, binance_oi, okex_oi]), 3)                  # [mil USD 1000mil => 1bil]
    oi_w_funding = round((mex_oi*mex_funding + bybit_oi*bybit_funding + binance_oi*binance_funding + okex_oi*okex_funding)/(mex_oi + bybit_oi + binance_oi + okex_oi), 3)   # [%] => (-) bears are paying, (+) bulls are paying

    avgMark_cumOI_oiWfunding = [avg_mark, cum_OI, oi_w_funding, time]
    avgMark_cumOI_oiWfunding_txt = f"{avg_mark};{cum_OI};{oi_w_funding};{time}\n"   # [USD] - [mil USD] - [%]

    with open(f"{data_file_path}/data storage/avgMark_cumOI_oiWfunding_storage.txt", "a") as store_avgM_cumOi_oiWfund:
        store_avgM_cumOi_oiWfund.write(avgMark_cumOI_oiWfunding_txt)
        store_avgM_cumOi_oiWfund.close()


    # -----------------------------------------------------------


    # mark prices
    mark_prices = [mex_mark, bybit_mark, binance_mark, okex_mark, time]
    mark_prices_txt = f"{mex_mark};{bybit_mark};{binance_mark};{okex_mark};{time}\n"    # [USD]

    with  open(f"{data_file_path}/data storage/mark_prices_storage.txt", "a") as store_mark_prices:
        store_mark_prices.write(mark_prices_txt)
        store_mark_prices.close()


    # -----------------------------------------------------------

    # fundings
    fundings = [mex_funding, bybit_funding, binance_funding, okex_funding, time]
    fundings_txt = f"{mex_funding};{bybit_funding};{binance_funding};{okex_funding};{time}\n"   # [%]

    with open(f"{data_file_path}/data storage/fundings_storage.txt", "a") as store_fundings:
        store_fundings.write(fundings_txt)
        store_fundings.close()


    # -----------------------------------------------------------

    # open interests
    open_interests = [mex_oi, bybit_oi, binance_oi, okex_oi, time]
    open_interests_txt = f"{mex_oi};{bybit_oi};{binance_oi};{okex_oi};{time}\n"     # [mil USD]

    with open(f"{data_file_path}/data storage/open_interests_storage.txt", "a") as store_open_interests:
        store_open_interests.write(open_interests_txt)
        store_open_interests.close()



    # -----------------------------------------------------------



def get_and_store_eth_data():


    data_file_path = "YOUR PATH"

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
    # print outs
    print("-" * 200)
    print(f"{mex_mark}[USD] - {mex_funding}[%] - {mex_oi}[mil USD] => Bitmex")
    print(f"{bybit_mark}[USD] - {bybit_funding}[%] - {bybit_oi}[mil USD] => Bybit")
    print(f"{binance_mark}[USD] - {binance_funding}[%] - {binance_oi}[mil USD] => Binance")
    print(f"{okex_mark}[USD] - {okex_funding}[%] - {okex_oi}[mil USD] => Okex")
    print("-" * 200)


    # data storage

    # all data
    all_swap_data = [mex_mark, mex_funding, mex_oi, bybit_mark, bybit_funding, bybit_oi, binance_mark, binance_funding, binance_oi, okex_mark, okex_funding, okex_oi, time]
    all_swap_data_txt = f"{mex_mark};{mex_funding};{mex_oi};{bybit_mark};{bybit_funding};{bybit_oi};{binance_mark};{binance_funding};{binance_oi};{okex_mark};{okex_funding};{okex_oi};{time}\n"


    with open(f"{data_file_path}/data storage/all_swap_data_storage_eth.txt", "a") as store_swap_data:
        store_swap_data.write(all_swap_data_txt)
        store_swap_data.close()


    # -----------------------------------------------------------

    # avg mark, cum OI, oi weighted funding
    avg_mark = round(np.average([mex_mark, bybit_mark, binance_mark, okex_mark]), 3)    # [USD]
    cum_OI = round(np.sum([mex_oi, bybit_oi, binance_oi, okex_oi]), 3)                  # [mil USD 1000mil => 1bil]
    oi_w_funding = round((mex_oi*mex_funding + bybit_oi*bybit_funding + binance_oi*binance_funding + okex_oi*okex_funding)/(mex_oi + bybit_oi + binance_oi + okex_oi), 3)   # [%] => (-) bears are paying, (+) bulls are paying

    avgMark_cumOI_oiWfunding = [avg_mark, cum_OI, oi_w_funding, time]
    avgMark_cumOI_oiWfunding_txt = f"{avg_mark};{cum_OI};{oi_w_funding};{time}\n"   # [USD] - [mil USD] - [%]

    with open(f"{data_file_path}/data storage/avgMark_cumOI_oiWfunding_storage_eth.txt", "a") as store_avgM_cumOi_oiWfund:
        store_avgM_cumOi_oiWfund.write(avgMark_cumOI_oiWfunding_txt)
        store_avgM_cumOi_oiWfund.close()


    # -----------------------------------------------------------


    # mark prices
    mark_prices = [mex_mark, bybit_mark, binance_mark, okex_mark, time]
    mark_prices_txt = f"{mex_mark};{bybit_mark};{binance_mark};{okex_mark};{time}\n"    # [USD]

    with  open(f"{data_file_path}/data storage/mark_prices_storage_eth.txt", "a") as store_mark_prices:
        store_mark_prices.write(mark_prices_txt)
        store_mark_prices.close()


    # -----------------------------------------------------------

    # fundings
    fundings = [mex_funding, bybit_funding, binance_funding, okex_funding, time]
    fundings_txt = f"{mex_funding};{bybit_funding};{binance_funding};{okex_funding};{time}\n"   # [%]

    with open(f"{data_file_path}/data storage/fundings_storage_eth.txt", "a") as store_fundings:
        store_fundings.write(fundings_txt)
        store_fundings.close()


    # -----------------------------------------------------------

    # open interests
    open_interests = [mex_oi, bybit_oi, binance_oi, okex_oi, time]
    open_interests_txt = f"{mex_oi};{bybit_oi};{binance_oi};{okex_oi};{time}\n"     # [mil USD]

    with open(f"{data_file_path}/data storage/open_interests_storage_eth.txt", "a") as store_open_interests:
        store_open_interests.write(open_interests_txt)
        store_open_interests.close()








