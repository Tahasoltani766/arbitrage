from web3 import Web3
from constant import *

rpc_url = 'https://go.getblock.io/9e9154f93e4440968bbfc4c31a1af414'
w3 = Web3(Web3.HTTPProvider(rpc_url))
node_getblock = f"wss://black-restless-brook.quiknode.pro/8e81354a00253b0de72c86b4561b50d5cd212216"

dexs = [{'dex': 'sushi_swap', "factory addr": adr_sushi_factory, "abi": abi_sushiswap, "function pool": "getPair"},
        {'dex': 'one_inch', "factory addr": adr_oneinch_factory, "abi": abi_oneinch, "function pool": "pools"},
        {'dex': 'uni_swapv2', "factory addr": adr_univ2_factory, "abi": abi_univ2, "function pool": "getPair"},
        {'dex': 'uni_swapv3', "factory addr": adr_univ3_factory, "abi": abi_univ3, "function pool": "getPair",
         "fee": True}
        ]


def get_dexs(dex: dict, tk0, tk1):
    list_percent = [100, 500, 1000, 3000, 10000]
    contract = w3.eth.contract(address=Web3.to_checksum_address(dex['factory addr']), abi=dex['abi'])
    if dex['fee'] == True:
        for fee in list_percent:
            get_pair = contract.functions.getPool(tk0, tk1, fee).call()
            return tk0, tk1, get_pair
    elif dex['fee'] == False:
        get_pair = contract.functions.dex['function pool'](tk0, tk1).call()
        return tk0, tk1, get_pair




def pair(adr_factory, abi, func, tk0, tk1):
    contract = w3.eth.contract(address=Web3.to_checksum_address(adr_factory), abi=abi)
    if func == "pools":
        get_pair = contract.functions.pools(tk0, tk1).call()
        return tk0, tk1, get_pair
    elif func == "getPair":
        get_pair = contract.functions.getPair(tk0, tk1).call()
        return tk0, tk1, get_pair
