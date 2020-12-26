import oi_mark_funding_discord as exchange_data
import pause
from datetime import datetime
import time

# you need to change variable ura to time you wish script starts working
# format for date datetime(year, month, day, hour, minute, second)
ura = datetime(2020,12,26,8,0,0)    
pause.until(ura)

i = 0
min15 = 60 * 15

while True:

    start_time = time.time()   # timestap

    i = i + 1
    print(f"getting data #{i}")

    exchange_data.get_and_store_btc_data() 
    exchange_data.get_and_store_eth_data()

    exe_time = time.time() - start_time             # calculates script execution time
    print(f"script execution time was: {exe_time}s")
    time.sleep(min15 - exe_time)                    # subtracts script execution time from time interval so we don't get data request delays

    print("----------------------------NEW OI DATA-------------------------------")




