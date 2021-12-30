import os
import time
import datetime
import requests
import csv

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

print()
print('total 30 day miner income (USD): ${}'.format(
    block_reward_sum_usd+fee_sum_usd))
print('30 day average miner income (USD): ${}'.format(
    (block_reward_sum_usd+fee_sum_usd)/30))

# get fee burn data
fee_burn_data = csv.DictReader(open('./data/eth/export-DailyEthBurnt.csv'))
fee_burn_dict = [d for d in fee_burn_data]
last_30_days_fee_burn = fee_burn_dict[-30:]

fee_burn_sum = 0
fee_burn_usd = 0

for day in last_30_days_fee_burn:
    fee_burn_eth = float(day.get('BurntFees'))
    fee_burn_sum += float(fee_burn_eth)

    date = day.get('Date(UTC)').split('/')
    date = '-'.join([date[1], date[0], date[2]])

    eth_price_res = requests.get(
        'https://api.coingecko.com/api/v3/coins/ethereum/history?date={}'.format(date))
    res_data = eth_price_res.json()
    daily_price = res_data.get('market_data').get('current_price').get('usd')

    fee_burn_usd += daily_price * fee_burn_eth

print()
print('total 30 day fee burn (USD): ${}'.format(fee_burn_usd))
print('30 day average fee burn (USD): ${}'.format((fee_burn_usd)/30))

print()
print('total 30 day fee burn (ETH): {}'.format(fee_burn_sum))
print('30 day average fee burn (ETH): {}'.format((fee_burn_sum)/30))
