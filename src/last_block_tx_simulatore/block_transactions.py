import json
import re
from functools import cache
import multiprocessing as mp
import requests
from src.wrappers import w3 as web3_instance
from src.last_block_tx_simulatore.constant import *
from src.last_block_tx_simulatore.filter_address_pool import get_data
from hexbytes import HexBytes


class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


zero_input_tx = HexBytes('0x')


# def get_hash_txs(w3=web3_instance()):
#     tx_hash_list = []
#     if w3.is_connected():
#         block = w3.eth.get_block('latest')
#         if block:
#             tx_hash_list = block['last_block_tx_simulatore']
#             pool = mp.Pool(mp.cpu_count() - 2)
#             pool.map(get_tx_data, tx_hash_list)
#     return tx_hash_list
#
#
# @cache
# def get_tx_data(tx_hash, w3=web3_instance()):
#     trx = w3.eth.get_transaction(tx_hash)
#     inp = trx['input']
#     if inp != zero_input_tx:
#         resp_post_rust(trx)


# def get_tx_attr(tx, key):
#     if key == "blockNumber":
#         return tx[0]
#     elif key == "from":
#         return tx[1]
#     elif key == "gas":
#         return tx[2]
#     elif key == "hash":
#         return tx[3]
#     elif key == "input":
#         return tx[4]
#     elif key == "to":
#         return tx[5]
#     elif key == "value":
#         return tx[6]
#     return None

def resp_post_rust(trx, bl_num: int | None = None):
    if not bl_num:
        tx = {
            "chainId": 1,
            "from": str(trx['from']),
            "to": trx['to'],
            "data": trx['input'].hex(),
            "gasLimit": trx['gas'],
            "value": str(trx['value']),
            "blockNumber": int(trx['blockNumber']) - 1,
            "formatTrace": True
        }
    else:
        tx = {
            "chainId": 1,
            "from": trx['from'],
            "to": trx['to'],
            "data": trx['input'].hex(),
            "gasLimit": trx['gas'],
            "value": str(trx['value']),
            "blockNumber": bl_num,
            "formatTrace": True
        }

    resp = requests.post("http://localhost:8080/api/v1/simulate", data=json.dumps(tx))
    if 'formattedTrace' in resp.json().keys():
        return resp.json(), trx['hash']
    return None,None


def filter_transaction(transaction, _hash):
    address_dexs = [swap_router01, uniswap_router2, zerox, oneinch, sushiswap, universal_router, swap_router02]
    cleaned_formatrace = re.sub(combined_regex, '', transaction['formattedTrace'])
    n = True
    list_data = []
    try:
        if "trace" in transaction.keys():
            for i in transaction['trace']:
                for item in i.values():
                    if item in address_dexs:
                        _data = {
                            'Dex': f"{item}",
                            'Trace': f"{transaction['trace']}",
                            'formattedTrace': f"{cleaned_formatrace}",
                            'hash': f"{_hash.hex()}",
                            'blockNumber': f"{transaction['blockNumber']}"
                        }
                        list_data.append(_data)
                        n = False
                if not n:
                    break
            get_data(list_data)
    except Exception as e:
        pass


def main():
    mp.freeze_support()

# print(get_hash_txs())
