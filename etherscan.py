import os
import time
import datetime
import requests

ETHERSCAN_TOKEN = os.getenv('ETHERSCAN_TOKEN')

# get latest block number

latest_block = 'https://api.etherscan.io/api?module={}&action={}&timestamp={}&closest={}&apikey={}'.format(
    'block', 'getblocknobytime', str(int(time.time())), 'before', ETHERSCAN_TOKEN)

res = requests.get(latest_block)
res_json = res.json()
latest_block_num = res_json.get('result')
print('latest block number:', latest_block_num)

# get daily fees for range

dt = datetime.datetime.now()
print(dt.strftime('%d-%m-%Y'))

etherscan_endpoint = 'https://api.etherscan.io/api?module={}&action={}&startdate={}&enddate={}&sort={}&apikey={}'.format(
    'stats', 'dailytxnfee', dt.strftime('%Y-%m-%d'), dt.strftime('%Y-%m-%d'), 'asc', ETHERSCAN_TOKEN)

res = requests.get(etherscan_endpoint)
res_json = res.json()
print(res_json)
