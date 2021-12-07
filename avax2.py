import requests

application_id = 'Nf96sS25j3QVRiciVq8Jt6ZBQypMeT52smFyFN3b'
master_key = 'yrtwS3a0oT766B5QwJMPSk8Q6JQbv0UjuH8YDhUN'
dashboard_user = 'H8qbmIGtLu'

moralis_url = 'https://4mt0j0ldyrcs.usemoralis.com:2053/server'
moralis_speedy_url = 'https://speedy-nodes-nyc.moralis.io/4f023a6aa148b1e6a3b48c36/avalanche/mainnet'

avax_res = requests.get(moralis_speedy_url)
print(avax_res.text)
# print(avax_res.json())
