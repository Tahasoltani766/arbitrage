import threading
from web3 import Web3
from functools import cache, partial
import multiprocessing as mp
from src.dexAggrigation.web3_instances import w3, pair, dexs, get_dexs
from src.dexAggrigation.constant import *
from src.dexAggrigation.wrappers import oneinch_weth_wrrper
import requests

token1 = Web3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
token0 = Web3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")


def get_tokens(tk0, tk1):
    pool = mp.Pool(4)
    dex_list = [sushi_swap, one_inch, uni_v2, uni_v3]
    pool.map(partial(worker, t0=tk0, t1=tk1), dex_list)


def worker(func, t0, t1):
    func(t0, t1)


def pair_handler(tk0, tk1):
    for dex in dexs:
        get_dexs(dex, tk0, tk1)


@cache
def sushi_swap(tk0, tk1):
    t0, t1, get_pair = pair(adr_sushi_factory, abi_sushiswap, 'getPair', tk0, tk1)
    get_balanceof_pool(t0, t1, get_pair)


@oneinch_weth_wrrper
@cache
def one_inch(tk0, tk1):
    t0, t1, get_pair = pair(adr_oneinch_factory, abi_oneinch, 'pools', tk0, tk1)
    get_balanceof_pool(t0, t1, get_pair)


@cache
def uni_v2(tk0, tk1):
    t0, t1, get_pair = pair(adr_univ2_factory, abi_univ2, 'getPair', tk0, tk1)
    get_balanceof_pool(t0, t1, get_pair)


# GET BALANCE OF POOLS
def get_balanceof_pool(token0, token1, adr_pl):
    if adr_pl != "0x0000000000000000000000000000000000000000":
        contract_token0 = w3.eth.contract(address=token0, abi=abi_erc20)
        contract_token1 = w3.eth.contract(address=token1, abi=abi_erc20)

        if token0 == "0x0000000000000000000000000000000000000000":
            blnc_tk0 = w3.eth.get_balance(adr_pl)
        else:
            blnc_tk0 = contract_token0.functions.balanceOf(adr_pl).call()
        if token1 == "0x0000000000000000000000000000000000000000":
            blnc_tk1 = w3.eth.get_balance(adr_pl)
        else:
            blnc_tk1 = contract_token1.functions.balanceOf(adr_pl).call()
        print('balance token 0:', blnc_tk0, 'balance token 1:', blnc_tk1, 'address pool:', adr_pl)
    else:
        print("none")


@cache
def uni_v3(tk0, tk1):
    list_percent = [100, 500, 1000, 3000, 10000]
    l_pool = []
    for percent in list_percent:
        contract = w3.eth.contract(address=Web3.to_checksum_address(adr_univ3_factory), abi=abi_univ3)
        get_pair = contract.functions.getPool(tk0, tk1, percent).call()
        if get_pair == "0x0000000000000000000000000000000000000000":
            print('v3\n none')
            l_pool.append({'pair': None, "b0": None, "b1": None})
        else:
            get_balance_v3(get_pair)
            print("v3")
            l_pool.append({'pair': None, "b0": None, "b1": None})


def get_balance_v3(adr_pl):
    contract = w3.eth.contract(address=Web3.to_checksum_address(adr_pl), abi=abi_v3)
    slot0 = contract.functions.slot0().call()
    liquidity = contract.functions.liquidity().call()
    sqrtp = slot0[0]
    tick = slot0[1]
    print("sqrpt:", sqrtp, "liquidity:", liquidity, "tick:", tick)


def zero_ex(tk0, tk1, sell_amount):
    zer_ex_api = f"https://api.0x.org/swap/v1/price?sellToken={tk0}&buyToken={tk1}&sellAmount={sell_amount}"
    header = {"content-type": "application/json",
              '0x-api-key': 'b59f93cd-8b0f-4b28-9ae8-3d10bcab7490'}
    response = requests.get(zer_ex_api, headers=header)
    response_json = response.json()
    print(response_json)
