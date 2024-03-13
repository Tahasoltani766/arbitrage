from web3 import Web3
from src.dex_aggrigation.constant import *

rpc_url = 'https://go.getblock.io/9e9154f93e4440968bbfc4c31a1af414'
w3 = Web3(Web3.HTTPProvider(rpc_url))
node_getblock = f"wss://black-restless-brook.quiknode.pro/8e81354a00253b0de72c86b4561b50d5cd212216"

dexs = [{'dex': 'sushi_swap', "factory addr": adr_sushi_factory, "abi": abi_sushiswap, "function pool": "getPair"},
        {'dex': 'one_inch', "factory addr": adr_oneinch_factory, "abi": abi_oneinch, "function pool": "pools"},
        {'dex': 'uni_swapv2', "factory addr": adr_univ2_factory, "abi": abi_univ2, "function pool": "getPair"},
        {'dex': 'uni_swapv3', "factory addr": adr_univ3_factory, "abi": abi_univ3, "function pool": "getPair",
         "fee": True}
        ]

token1 = Web3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
token0 = Web3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")


# def get_dexs(tk0, tk1, dex: dict):
#     list_percent = [100, 500, 1000, 3000, 10000]
#     contract = w3.eth.contract(address=Web3.to_checksum_address((dex['factory addr'])), abi=dex['abi'])
#     if "fee" in dex.keys():
#         for fee in list_percent:
#             get_pair = contract.functions.getPool(tk0, tk1, fee).call()
#             return tk0, tk1, get_pair
#     else:
#         print(type(dex['function pool']))
#         # noinspection PyCallingNonCallable
#         get_pair = contract.functions[dex['function pool']](tk0, tk1).call()
#         return tk0, tk1, get_pair
#
#
# get_dexs(token0, token1, dexs[0])
