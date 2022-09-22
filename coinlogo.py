import json


import requests
import json

# import symbol

listData = []

# def fetch(num):
#     response_API = requests.get(
#         'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=' + num + '&sparkline=false')
    # data = response_API.text
    # parse_json = json.loads(data)
#     # print(parse_json)
#     return parse_json


# for j in range(1, 3):
#     list = fetch(str(j))
#     for i in range(100):
#         # file.write(str(list[i]["symbol"]) + "\n")
#         listData.append(str(list[i]["image"]))
# # file.close()
# print(listData)

output = []
for i in range(1, 2):
    response_API = requests.get(
            'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=' + str(i) + '&sparkline=false&price_change_percentage=7d')
        # 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=' + str(i) + '&sparkline=false')
    data = response_API.text
    parse_json = json.loads(data)
    output.extend(parse_json)
# for data in output:
    # print(data)
    
print(output[0])
    
# mergeData = {key : value for (key,value) in data[i]}




 
# def coinData(period):
#     output = []
#     for i in range(1, 3):
#         response_API = requests.get(
        # 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=' + str(i) + '&sparkline=false')
            # 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=' + str(i) + '&sparkline=false&price_change_percentage=' + period)
#         data = response_API.text
#         parse_json = json.loads(data)
#         output.extend(parse_json)
#     return parse_json


# print(coinData("24h"))