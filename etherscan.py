import os
import time
import datetime
import requests

ETHERSCAN_TOKEN = os.getenv('ETHERSCAN_TOKEN')

latest_block = 'https://api.etherscan.io/api?module={}&action={}&timestamp={}&closest={}&apikey={}'.format(
    'block', 'getblocknobytime', str(int(time.time())), 'before', ETHERSCAN_TOKEN)

dt = datetime.datetime.now()
dt_30_days_ago = dt - datetime.timedelta(days=30)

etherscan_endpoint = 'https://api.etherscan.io/api?module={}&action={}&startdate={}&enddate={}&sort={}&apikey={}'.format(
    'stats', 'dailytxnfee', dt_30_days_ago.strftime('%Y-%m-%d'), dt.strftime('%Y-%m-%d'), 'asc', ETHERSCAN_TOKEN)

res = requests.get(etherscan_endpoint)
daily_fees = res.json()
daily_fees_list = daily_fees.get('result')
fee_sum = 0

for day in daily_fees_list:
    fee_sum += float(day.get('transactionFee_Eth'))

print('30 day total fees paid to miners (ETH)', fee_sum)
print('daily avg fees paid to miners (ETH)', fee_sum/30)

etherscan_endpoint = 'https://api.etherscan.io/api?module={}&action={}&startdate={}&enddate={}&sort={}&apikey={}'.format(
    'stats', 'ethdailyprice', dt_30_days_ago.strftime('%Y-%m-%d'), dt.strftime('%Y-%m-%d'), 'asc', ETHERSCAN_TOKEN)

res = requests.get(etherscan_endpoint)
daily_prices = res.json()

fee_sum_usd = 0
daily_prices_list = daily_prices.get('result')

for i in range(30):
    eth_price = float(daily_prices_list[i].get('value'))
    total_fees_eth = float(daily_fees_list[i].get('transactionFee_Eth'))
    fee_sum_usd += eth_price * total_fees_eth

print()
print('total fees paid to miners (USD): ${}'.format(fee_sum_usd))
print('30 day average fees to miners (USD): ${}'.format(fee_sum_usd/30))

etherscan_endpoint = 'https://api.etherscan.io/api?module={}&action={}&startdate={}&enddate={}&sort={}&apikey={}'.format(
    'stats', 'dailyblockrewards', dt_30_days_ago.strftime('%Y-%m-%d'), dt.strftime('%Y-%m-%d'), 'asc', ETHERSCAN_TOKEN)

res = requests.get(etherscan_endpoint)
daily_block_rewards = res.json()

block_reward_sum_usd = 0
daily_block_rewards = daily_block_rewards.get('result')

for i in range(30):
    eth_price = float(daily_prices_list[i].get('value'))
    block_rewards_eth = float(daily_block_rewards[i].get('blockRewards_Eth'))
    block_reward_sum_usd += eth_price * block_rewards_eth

print()
print('total block rewards paid to miners (USD): ${}'.format(block_reward_sum_usd))
print('30 day average block rewards paid to miners (USD): ${}'.format(
    block_reward_sum_usd/30))

# total miner income3

print()
print('total 30 day miner income (USD): ${}'.format(
    block_reward_sum_usd+fee_sum_usd))
print('30 day average miner income (USD): ${}'.format(
    (block_reward_sum_usd+fee_sum_usd)/30))
