from functools import cache
from web3_instances import w3, abi2, abi3, abi_erc20
from web3.exceptions import ContractLogicError
from mongo_handler import *


def get_data_pool_mongo():
    loaded_data = pool_coloction.find({})
    for data in loaded_data:
        yield data


def get_pool_address():
    data = get_data_pool_mongo()
    list_tokens = []
    while 1:
        try:
            datum = next(data)
            _id = datum['_id']
            _balance = datum['Balance']
            block_number = datum['BlockNumber']
        except StopIteration:
            break
        t0, t1 = gen_handler(datum['Type Pool'], datum['Pool'])
        if t1 == t0 == 0:
            pass
        else:
            list_tokens.append((t0, t1))
            b0, b1 = get_balance0f_before(t0, t1, datum['Pool'], block_number)
            if str(b0) == _balance or str(b1) == _balance:
                pool_coloction.delete_one(datum)
            else:
                m_query = {"_id": _id}
                new_q = {'$set': {"Balance Token0 before": str(b0), "Balance Token1 before": str(b1),
                                  "Token0": str(t0),
                                  "Token1": str(t1)
                                  }}
                pool_coloction.update_one(m_query, new_q)
    return list_tokens


@cache
def gen_handler(datum_type_pool, adr_pl):
    if datum_type_pool == 'v3':
        t0, t1 = v2_contract(adr_pl)
    elif datum_type_pool == 'v2':
        t0, t1 = v3_contract(adr_pl)
    else:
        return 0, 0
    return t0, t1


@cache
def v2_contract(adr_pl):
    try:
        contract = w3.eth.contract(address=adr_pl, abi=abi2)
        token0 = contract.functions.token0().call()
        token1 = contract.functions.token1().call()
        return token0, token1
    except ContractLogicError:
        return 0, 0


@cache
def v3_contract(adr_pl):
    try:
        contract = w3.eth.contract(address=adr_pl, abi=abi3)
        token0 = contract.functions.token0().call()
        token1 = contract.functions.token1().call()
        return token0, token1
    except ContractLogicError:
        return 0, 0


def get_balance0f_before(token0, token1, adr_pl, block_num):
    contract_token1 = w3.eth.contract(address=token1, abi=abi_erc20)
    blnc_tk1 = contract_token1.functions.balanceOf(adr_pl).call(
        block_identifier=int(block_num))

    contract_token0 = w3.eth.contract(address=token0, abi=abi_erc20)
    blnc_tk0 = contract_token0.functions.balanceOf(adr_pl).call(
        block_identifier=int(block_num))

    return blnc_tk0, blnc_tk1
