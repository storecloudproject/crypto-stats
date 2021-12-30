import requests
import pandas as pd
import csv
import datetime

avg_gas_prices = pd.read_csv('./data/avax/export-AvgGasPrice.csv', index_col=0)
gas_used = pd.read_csv('./data/avax/export-GasUsed.csv', index_col=0)
block_rewards = pd.read_csv(
    './data/avax/export-BlockCountRewards.csv', index_col=0)
fee_burn = pd.read_csv('./data/avax/export-DailyBurnt.csv', index_col=0)

super_frame = avg_gas_prices.assign(
    rewards=gas_used.Value, block_rewards=block_rewards.Value, fee_burn=fee_burn.BurntFees)

super_frame.columns = [
    'unix_time', 'avg_gas_price_wei', 'gas_used', 'block_rewards_avax', 'fee_burn']

block_reward_sum = 0
block_reward_sum_usd = 0
fee_sum = 0
fee_sum_usd = 0
fee_burn_sum = 0
fee_burn_usd = 0

WEI_TO_AVAX = 1000000000000000000


for i, row in super_frame.tail(30).iterrows():
    date = datetime.datetime.fromtimestamp(
        row['unix_time']).strftime('%d-%m-%Y')

    avax_price_res = requests.get(
        'https://api.coingecko.com/api/v3/coins/avalanche-2/history?date={}'.format(date))

    res_data = avax_price_res.json()
    daily_price = res_data.get('market_data').get('current_price').get('usd')

    block_reward = float(row['block_rewards_avax'])
    block_reward_sum += block_reward
    block_reward_sum_usd += block_reward * float(daily_price)

    avg_gas_price_wei = float(row['avg_gas_price_wei'])
    gas_used = float(row['gas_used'])
    gas_paid_avax = avg_gas_price_wei * gas_used / WEI_TO_AVAX

    fee_sum += gas_paid_avax
    fee_sum_usd += gas_paid_avax * daily_price


# get fee burn data
fee_burn_data = csv.DictReader(open('./data/avax/export-DailyBurnt.csv'))
fee_burn_dict = [d for d in fee_burn_data]
last_30_days_fee_burn = fee_burn_dict[-30:]

for day in last_30_days_fee_burn:
    fee_burn = float(day.get('BurntFees'))
    fee_burn_sum += float(fee_burn)

    date = day.get('Date(UTC)').split('/')
    date = '-'.join([date[1], date[0], date[2]])

    avax_price_res = requests.get(
        'https://api.coingecko.com/api/v3/coins/avalanche-2/history?date={}'.format(date))
    res_data = avax_price_res.json()
    daily_price = res_data.get('market_data').get('current_price').get('usd')

    fee_burn_usd += daily_price * fee_burn


print('30 day total block reward sum (AVAX): {}'.format(block_reward_sum))
print('30 day average block reward (AVAX): {}'.format(block_reward_sum/30))

print()

print('30 day total block rewards (USD): ${}'.format(block_reward_sum_usd))
print('30 day average block rewards (USD): ${}'.format(block_reward_sum_usd/30))

print()

print('30 day total fees (AVAX): {}'.format(fee_sum))
print('30 day average fees (AVAX): {}'.format(fee_sum/30))

print()

print('30 day total fees (USD): ${}'.format(fee_sum_usd))
print('30 day average fees (USD): ${}'.format(fee_sum_usd/30))

print()

print('30 day total burn (AVAX): {}'.format(fee_burn_sum))
print('30 day average burn (AVAX): {}'.format(fee_burn_sum/30))

print()

print('30 day total burn (USD): ${}'.format(fee_burn_usd))
print('30 day average burn (USD): ${}'.format(fee_burn_sum/30))
