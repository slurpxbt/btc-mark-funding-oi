# btc-mark-funding-oi
Script that pulls btc and eth mark price, funding and oi data from bitmex, bybit, binance amd okex for perpetual swap contract

<h2>How to use the script</h2>

<p>pip install packages that are missing from your environment</p>
<p>few packages that need to be installed are already listed in <b>oi_mark_fundig.py</b> file, if any other are missing install them</p>
<p>In <b>oi_mark_fundig.py</b> change <b>data_file_path</b> variable to your own folder path in rows <b>42</b> and <b>174</b>, this same path also need to be changed in <b>GUI-newV2.py</b> in rows <b>109</b> and <b>127</b></p>
<p>When you install everything and change the file path, put empty files from <b>empty data storage files</b> folder into <b>data storage</b> folder and replace them</p>
<p>When you have empty files in <b>data storage</b> folder run <b>GUI-newV2.py</b> and click start. Script will collect data every 15 minutes and you can see data by clicking on BTC or ETH button in GUI, you can also change time interval in <b>GUI-newV2.py</b> file in row 22 -> replace 15 with your desired interval</p>

<b>NEW [26.12.2020] : DISCORD INTEGRATION</b>
<p><b>oi_mark_funding_discord.py</b> and <b>collect_data.py</b> script files are needed in the same folder in order for this to work</p>
<p>Also you need to replace webhook url at the start of <b>oi_mark_funding_discord.py</b> file (line <b>37</b>) and set the time you want to start the script in the <b>collect_data.py</b> file (line <b>8</b>)</p>
<p>binance_f and okex folders are also needed in the same folder as script files</>

<b>NOTE</b>
<p>GUI is not yet finished and it's size could be odd on screens that are not in 4k resolution</p>
<p>To avoid this GUI problem you can create your own script with infinite while loop that calls <b>get_and_store_btc_data()</b> and <b>get_and_store_eth_data()</b> functions from  <b>oi_mark_fundig.py</b> on your desired interval, data will be then displayed in console<p>
  
 
