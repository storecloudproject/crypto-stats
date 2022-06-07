import os
import json
import datetime
import requests
import csv

ETHERSCAN_TOKEN = os.getenv('ETHERSCAN_TOKEN')

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 6, 1)
time_diff = end_date-start_date
time_diff_days = time_diff.days


def call_etherscan(action):
    res = requests.get('https://api.etherscan.io/api?module={}&action={}&startdate={}&enddate={}&sort={}&apikey={}'.format(
        'stats', action, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), 'asc', ETHERSCAN_TOKEN))
    response = res.json()
    return response.get('result')


print('start date: {}, end date: {}. {} days'.format(
    start_date, end_date, time_diff_days))
print()

tx_count = 0

daily_txs_list = call_etherscan('dailytx')
for day in daily_txs_list:
    tx_count += int(day.get('transactionCount'))

print('total txs: {:,}'.format(tx_count))
print()

fee_sum = 0

daily_fees_list = call_etherscan('dailytxnfee')
for day in daily_fees_list:
    fee_sum += float(day.get('transactionFee_Eth'))

print('total fees paid to miners (ETH): {:,}'.format(fee_sum))
print('daily avg fees paid to miners (ETH): {:,}'.format(
    fee_sum/time_diff_days))

daily_fees_and_tx_counts = []
for tx_count, fee_total in zip(daily_txs_list, daily_fees_list):
    daily_fees_and_tx_counts.append({
        'utc_date': tx_count.get('UTCDate'),
        'tx_count': tx_count.get('transactionCount'),
        'tx_fees_paid_to_miners_eth': float(fee_total.get('transactionFee_Eth')),
    })

fee_sum_usd = 0
daily_prices_list = call_etherscan('ethdailyprice')

for i in range(len(daily_prices_list)):
    eth_price = float(daily_prices_list[i].get('value'))
    total_fees_eth = float(daily_fees_list[i].get('transactionFee_Eth'))
    fee_sum_usd += eth_price * total_fees_eth

print()
print('total fees paid to miners (USD): ${:,}'.format(fee_sum_usd))
print('average daily fees paid to miners (USD): ${:,}'.format(
    fee_sum_usd/time_diff_days))

block_reward_sum_usd = 0
daily_block_rewards = call_etherscan('dailyblockrewards')

for i in range(time_diff_days):
    eth_price = float(daily_prices_list[i].get('value'))
    block_rewards_eth = float(daily_block_rewards[i].get('blockRewards_Eth'))
    block_reward_sum_usd += eth_price * block_rewards_eth

print()
print('total block rewards paid to miners (USD): ${:,}'.format(
    block_reward_sum_usd))
print('daily average block rewards paid to miners (USD): ${:,}'.format(
    block_reward_sum_usd/time_diff_days))

print()
print('total miner income (USD): ${:,}'.format(
    block_reward_sum_usd+fee_sum_usd))
print('daily average miner income (USD): ${:,}'.format(
    (block_reward_sum_usd+fee_sum_usd)/time_diff_days))

# get fee burn data
fee_burn_data = csv.DictReader(open('./data/eth/export-DailyEthBurnt.csv'))
fee_burn_dict = [d for d in fee_burn_data]

fee_burn_sum = 0
fee_burn_usd = 0
fee_paid_sum_usd = 0

start_index = -1
end_index = -1

for index, day_object in enumerate(fee_burn_dict):
    if day_object.get('Date(UTC)') == start_date.strftime('%m/%d/%Y'):
        start_index = index
    elif day_object.get('Date(UTC)') == end_date.strftime('%m/%d/%Y'):
        end_index = index

last_n_days_fee_burn = fee_burn_dict[start_index:end_index+1]


for day_burn, day_fees_txs, day_price in zip(last_n_days_fee_burn, daily_fees_and_tx_counts, daily_prices_list):
    fee_burn_eth = float(day_burn.get('BurntFees'))
    fee_burn_sum += float(fee_burn_eth)

    daily_price = float(day_price.get('value'))

    day_fees_eth = float(day_fees_txs.get('tx_fees_paid_to_miners_eth'))
    tx_fee_usd = daily_price * day_fees_eth
    day_fees_txs['tx_fees_paid_to_miners_usd'] = tx_fee_usd
    day_fees_txs['avg_tx_fee_paid_to_miners_usd'] = tx_fee_usd / \
        day_fees_txs['tx_count']

    fees_paid_by_users = (fee_burn_eth + day_fees_eth) * daily_price
    day_fees_txs['tx_fees_paid_by_users_usd'] = fees_paid_by_users
    day_fees_txs['avg_fees_paid_by_users_usd'] = fees_paid_by_users / \
        day_fees_txs['tx_count']

    fee_paid_sum_usd += fees_paid_by_users

    fee_burn_usd += daily_price * float(fee_burn_eth)

file = open('data/eth/eth.json', 'w')
file.write(json.dumps(daily_fees_and_tx_counts))
file.close()

print()
print('total fee burn (USD): ${:,}'.format(fee_burn_usd))
print('daily average fee burn (USD): ${:,}'.format(
    (fee_burn_usd)/time_diff_days))

print()
print('total fee burn (ETH): {:,}'.format(fee_burn_sum))
print('daily average fee burn (ETH): {:,}'.format(
    (fee_burn_sum)/time_diff_days))

print()
print('total fees paid by users (ETH): {:,}'.format(fee_burn_sum+fee_sum))
print('total fees paid by users (USD): ${:,}'.format(fee_paid_sum_usd))
