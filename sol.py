import json
import requests

last_30_days = []

with open('sol.json', 'r') as f:
    data = json.load(f)
    tx_data = data.get('solana').get('transactions')
    last_30_days = tx_data[-30:]

tx_sum_sol = 0
tx_sum_usd = 0
for day in last_30_days:
    daily_fee_sol = day.get('transactionFee')
    tx_sum_sol += daily_fee_sol

    date_string = day.get('date').get('date').split('-')
    date_string.reverse()
    date_string = '-'.join(date_string)

    print(date_string)

    sol_price_res = requests.get(
        'https://api.coingecko.com/api/v3/coins/solana/history?date={}'.format(date_string))

    res_data = sol_price_res.json()
    daily_price = res_data.get('market_data').get('current_price').get('usd')

    tx_sum_usd += daily_price*tx_sum_sol


print('30 day total tx sum (SOL): {}'.format(tx_sum_sol))
print('30 day average (SOL): {}'.format(tx_sum_sol/30))

print()

print('30 day total tx sum (USD): ${}'.format(tx_sum_usd))
print('30 day average (USD): ${}'.format(tx_sum_usd/30))


exit()

sol_endpoint = 'https://ssc-dao.genesysgo.net'

res = requests.post(sol_endpoint, headers={'Content-Type': 'application/json'}, json={
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getAccountInfo",
    "params": [
        "9aiGb2qTGB7xxrEWRrHtzgzBYTfq4y51hQGHrYxxJWna",
        {
            "encoding": "base58"
        }
    ]
})

payload = res.json()
print(payload)