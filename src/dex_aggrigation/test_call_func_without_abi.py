# from Crypto.Hash import keccak
# k = keccak.new(digest_bits=256)
# id = k.update(b'withdrawWithdrawals(uint256)').hexdigest()
# method_id = id[:8]
# print(id)
# print(method_id)
# #mint(address,uint256)
from pprint import pprint

import requests

# x = {"system": "ethereum", "network": "main", "unit": "gwei", "maxPrice": 32, "currentBlockNumber": 19453572,
#      "msSinceLastBlock": 1835, "blockPrices": [
#         {"blockNumber": 19453573, "estimatedTransactionCount": 44, "baseFeePerGas": 25.884011441,
#          "blobBaseFeePerGas": 1e-9,
#          "estimatedPrices": [{"confidence": 99, "price": 25, "maxPriorityFeePerGas": 0.1, "maxFeePerGas": 31.67},
#                              {"confidence": 95, "price": 25, "maxPriorityFeePerGas": 0.09, "maxFeePerGas": 31.66},
#                              {"confidence": 90, "price": 25, "maxPriorityFeePerGas": 0.09, "maxFeePerGas": 31.66},
#                              {"confidence": 80, "price": 25, "maxPriorityFeePerGas": 0.08, "maxFeePerGas": 31.65},
#                              {"confidence": 70, "price": 25, "maxPriorityFeePerGas": 0.07, "maxFeePerGas": 31.64}]}]}

res = requests.get('https://api.blocknative.com/gasprices/blockprices')
response = res.json()
a = response["blockPrices"][0]["estimatedPrices"][4]
if a and a['confidence'] == 70:
    max_priority_gas = a['maxPriorityFeePerGas']
    max_per_gas = a['maxFeePerGas']
    print(max_priority_gas, max_per_gas)
else:
    print(None)