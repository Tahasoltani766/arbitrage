import re
from functools import cache
from src.last_block_tx_simulatore.mongo_handler import blockchain_db as db
from eth_typing import ChecksumAddress
from web3 import Web3
from src.last_block_tx_simulatore.uni_pool_math.math_v2 import math_delta_y, math_delta_x
from web3.exceptions import ContractLogicError
from src.last_block_tx_simulatore.uni_pool_math.math_v3 import get_liq_sqrtp, swap_t1_in, swap_t0_in
from src.last_block_tx_simulatore.constant import list_address_router
from src.last_block_tx_simulatore.patterns import *
from src.last_block_tx_simulatore.web3_instances import w3, abi_pool_get_token, abi_balance_erc20
from typing import TypedDict, Literal


class AnalyzeArg(TypedDict):
    type_pool: Literal["v2", "v3"]
    token: ChecksumAddress
    token0: ChecksumAddress
    token1: ChecksumAddress
    blnc_bfr_tk0: int
    blnc_bfr_tk1: int
    balance: int
    block_num: int
    item: ChecksumAddress


@cache
def factory_handler(addr):
    contract = w3.eth.contract(address=addr, abi=abi_pool_get_token)
    return contract.functions.factory().call()


def get_data(loaded_data: list):
    dt_list = []
    for datum in loaded_data:
        formatrace = datum['formattedTrace']
        result_formatrace = re.sub(pt, '', formatrace, flags=re.MULTILINE)
        find_balanceof = re.findall(pattern_balanceof, result_formatrace, flags=re.MULTILINE)
        for balance_of in find_balanceof:
            find_address = re.findall(pattern_address, balance_of, flags=re.MULTILINE)
            try:
                dt_ = pool_version_identifier(find_address[1], datum, balance_of)
                dt_list.append(dt_)
            except:
                pass


def pool_version_identifier(item: str, datum: dict, balance_of: str):
    """
    this func will calculate new balance of a pool after swap (v2,v3)
    :param item:address
    :param datum: loaded data
    :param balance_of: address token and balance of
    :return: dictionary of new balances
    """
    dex = datum['Dex']
    hash_trx = datum['hash']
    token_ = balance_of.split("::")[0][1:]
    block_number = datum['blockNumber']
    balance = int(balance_of[-66:], 0)
    try:
        item_v = ""
        factory = factory_handler(item)
        if factory == "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f":
            item_v = 'v2'

        elif "0x1F98431c8aD98523631AE4a59f267346ea31F984" == factory:
            item_v = 'v3'
        for name, address in zip(["uniswap", "zerox", "oneinch", "sushiswap", "universal_router",
                                  "swap_router02"],
                                 list_address_router):
            if dex == address and item_v:
                dt = {
                    'Type Pool': f'{item_v}',
                    'Pool': f'{item}',
                    'Dex': dex,
                    'Hash': hash_trx,
                    "Token": str(token_),
                    "Balance": str(balance),
                    'BlockNumber': block_number
                }
                t0, t1 = uni_swap_contract(item)
                if t0 and t1:
                    b0, b1 = get_blnc_bfr(t0, t1, item, block_number)
                    arg = AnalyzeArg(type_pool=item_v, token=token_, token0=Web3.to_checksum_address(t0),
                                     token1=Web3.to_checksum_address(t1), blnc_bfr_tk0=b0, blnc_bfr_tk1=b1,
                                     balance=balance, block_num=block_number, item=Web3.to_checksum_address(item))
                    new_price, after_tk0, after_tk1 = analyze(data=arg)
                    dt['balance 0'] = b0
                    dt['balance 1'] = b1
                    dt['newPrice'] = new_price
                    dt['afterToken0'] = after_tk0
                    dt['afterToken1'] = after_tk1
                    posts = db.Transactions
                    tras = posts.insert_one(dt)
                    print(tras)
    except Exception as e:
        pass


@cache
def uni_swap_contract(adr_pl):
    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(adr_pl), abi=abi_pool_get_token)
        token0 = contract.functions.token0().call()
        token1 = contract.functions.token1().call()
        return token0, token1
    except ContractLogicError:
        return None


def get_blnc_bfr(tk0, tk1, adr_pl, block_num):
    contract_token1 = w3.eth.contract(address=Web3.to_checksum_address(tk1), abi=abi_balance_erc20)
    blnc_tk1 = contract_token1.functions.balanceOf(Web3.to_checksum_address(adr_pl)).call(
        block_identifier=int(block_num))

    contract_token0 = w3.eth.contract(address=Web3.to_checksum_address(tk0), abi=abi_balance_erc20)
    blnc_tk0 = contract_token0.functions.balanceOf(Web3.to_checksum_address(adr_pl)).call(
        block_identifier=int(block_num))

    return blnc_tk0, blnc_tk1


def analyze(**kwargs):  # type_pool, token, token0, token1, blnc_bfr_tk0, blnc_bfr_tk1, balance, block_num, item):
    data = kwargs['data']
    token = data['token']
    token0 = data["token0"]
    token1 = data["token1"]
    blnc_bfr_tk0 = data["blnc_bfr_tk0"]
    blnc_bfr_tk1 = data["blnc_bfr_tk1"]
    item = data['item']
    balance = data['balance']
    if data['type_pool'] == 'v2':
        if token == token0:
            delta_tk1 = blnc_bfr_tk0 - balance
            new_price, after_tk0, after_tk1 = math_delta_x(blnc_bfr_tk0, blnc_bfr_tk1, delta_tk1, balance)
            return new_price, after_tk0, after_tk1
        elif token == token1:
            delta_tk0 = blnc_bfr_tk1 - balance
            new_price, after_tk0, after_tk1 = math_delta_y(blnc_bfr_tk0, blnc_bfr_tk1, delta_tk0, balance)
            return new_price, after_tk0, after_tk1
    elif data["type_pool"] == 'v3':
        sqrtp, liq = get_liq_sqrtp(item, data['block_num'])
        if token == token0:
            amount_in = balance - blnc_bfr_tk0
            new_price, after_tk0, after_tk1 = swap_t0_in(liq, sqrtp, amount_in, blnc_bfr_tk0, blnc_bfr_tk1)
            return new_price, after_tk0, after_tk1
        elif token == token1:
            amount_in = balance - blnc_bfr_tk1
            new_price, after_tk0, after_tk1 = swap_t1_in(liq, sqrtp, amount_in, blnc_bfr_tk1, blnc_bfr_tk0)
            return new_price, after_tk0, after_tk1
    return None