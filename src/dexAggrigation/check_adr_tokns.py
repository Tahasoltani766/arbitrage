from src.dexAggrigation.web3_instances import *
from src.dexAggrigation.constant import *
from src.dexAggrigation.wrappers import oneinch_weth_wrrper

token1 = Web3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
token0 = Web3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")


def sushi_swap(tk0, tk1):
    contract = w3.eth.contract(address=Web3.to_checksum_address(adr_sushi_factory), abi=abi_sushiswap)
    get_pair = contract.functions.getPair(tk0, tk1).call()
    print(get_pair)


@oneinch_weth_wrrper
def one_inch(tk0, tk1):
    contract = w3.eth.contract(address=Web3.to_checksum_address(adr_oneinch_factory), abi=abi_oneinch)
    get_pair = contract.functions.pools(tk0, tk1).call()
    print(get_pair)


def uni_v2(tk0, tk1):
    contract = w3.eth.contract(address=Web3.to_checksum_address(adr_univ2_factory), abi=abi_univ2)
    get_pair = contract.functions.getPair(tk0, tk1).call()
    print(get_pair)


def uni_v3(tk0, tk1):
    list_percent = [100, 500, 1000, 3000, 10000]
    for percent in list_percent:
        contract = w3.eth.contract(address=Web3.to_checksum_address(adr_univ3_factory), abi=abi_univ3)
        get_pair = contract.functions.getPool(tk0, tk1, percent).call()
        if get_pair == "0x0000000000000000000000000000000000000000":
            pass
        else:
            print(get_pair, percent)


uni_v3(token0, token1)
