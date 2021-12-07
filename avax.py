import requests
import pandas as pd
import csv
import datetime

avg_gas_prices = pd.read_csv('./avax/AvgGasPrice.csv', index_col=0)
gas_used = pd.read_csv('./avax/GasUsed.csv', index_col=0)
block_rewards = pd.read_csv('./avax/BlockCountRewards.csv', index_col=0)

super_frame = avg_gas_prices.assign(
    rewards=gas_used.Value).assign(block_rewards=block_rewards.Value)

super_frame.columns = [
    'unix_time', 'avg_gas_price_wei', 'gas_used', 'block_rewards_avax']


block_reward_sum = 0
block_reward_sum_usd = 0
fee_sum = 0
fee_sum_usd = 0
WEI_TO_AVAX = 1000000000000000000


for i, row in super_frame.tail(30).iterrows():
    date = datetime.datetime.fromtimestamp(
        row['unix_time']).strftime('%d-%m-%Y')

    avax_price_res = requests.get(
        'https://api.coingecko.com/api/v3/coins/avalanche-2/history?date={}'.format(date))

    res_data = avax_price_res.json()
    daily_price = res_data.get('market_data').get(
        'current_price').get('usd')

    block_reward = float(row['block_rewards_avax'])
    block_reward_sum += block_reward
    block_reward_sum_usd += block_reward * float(daily_price)

    avg_gas_price_wei = float(row['avg_gas_price_wei'])
    gas_used = float(row['gas_used'])
    gas_paid_avax = avg_gas_price_wei * gas_used / WEI_TO_AVAX

    fee_sum += gas_paid_avax
    fee_sum_usd += gas_paid_avax * daily_price

print('30 day total block reward sum (AVAX): {}'.format(block_reward_sum))
print('30 day average block reward (AVAX): {}'.format(block_reward_sum/30))

print()

print('30 day total block rewarsd (USD): ${}'.format(block_reward_sum_usd))
print('30 day average block rewards (USD): ${}'.format(block_reward_sum_usd/30))

print()

print('30 day total fees (AVAX): {}'.format(fee_sum))
print('30 day average fees (AVAX): {}'.format(fee_sum/30))

print()

print('30 day total fees (USD): ${}'.format(fee_sum_usd))
print('30 day average fees (USD): ${}'.format(fee_sum_usd/30))
