import os
import requests

infura_project_secret = os.getenv('INFURA_SECRET')
infura_project_id = 'ef2c03f74f0345f79fb39036828dd707'
infura_endpoint = 'https://mainnet.infura.io/v3/{}'.format(infura_project_id)

body = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
headers = {'user': infura_project_secret}

res = requests.post(infura_endpoint, json=body, headers=headers)
res_json = res.json()
print('latest block:', int(res_json.get('result'), 0))
