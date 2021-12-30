import requests

sol_endpoint = 'https://ssc-dao.genesysgo.net'

res = requests.post(sol_endpoint, headers={'Content-Type': 'application/json'}, json={
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getEpochSchedule",
})

payload = res.json()
print(payload)
print()

res = requests.post(sol_endpoint, headers={'Content-Type': 'application/json'}, json={
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBlockHeight",
})

payload = res.json()
block_height = payload.get('result')
print(block_height)
print()

res = requests.post(sol_endpoint, headers={'Content-Type': 'application/json'}, json={
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBlocksWithLimit",
    "params": [432000*256, 1]
})

payload = res.json()
print(payload)
print()

res = requests.post(sol_endpoint, headers={'Content-Type': 'application/json'}, json={
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBlock",
    "params": [432000*256]
})

payload = res.json()
# rewards = payload.get('result').get('rewards')

file = open('sol.json', 'w')
file.write(json.dumps(payload))
file.close()
print()