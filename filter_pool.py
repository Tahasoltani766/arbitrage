import multiprocessing as mp
import re
from functools import cache
from constant import *
from mongo_handler import blockchain_db, trx_collection
from web3_instances import *


@cache
def factory_handler(addr):
    contract = w3.eth.contract(address=addr, abi=abi2)
    return contract.functions.factory().call()


def filter_pool():
    loaded_data = trx_collection.find({})
    for data in list(loaded_data):
        block_number = data['blockNumber']
        hash_transaction = data['hash']
        formatrace = data['formattedTrace']
        pt = r'^\D*\d+\s*\]|\bm\b||←|│|└─|.*\bPermit2\b.*|\(\)|.*\bemit\b.*'
        result_formatrace = re.sub(pt, '', formatrace, flags=re.MULTILINE)
        pattern_balanceof = r'.*\bbalanceOf\b.*\n.*'
        find_balanceof = re.findall(pattern_balanceof, result_formatrace, flags=re.MULTILINE)
        for balance_of in find_balanceof:
            pattern_address = r'\b0x[0-9a-fA-F]{40}\b'
            find_address = re.findall(pattern_address, balance_of, flags=re.MULTILINE)
            for item in find_address:
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
                        if data['Dex'] == address and item_v:
                            d = {
                                'Type Pool': f'{item_v}',
                                'Pool': f'{item}',
                                'Dex': data['Dex'],
                                'Hash': f'{hash_transaction}',
                                "Token": f'{balance_of.split("::")[0][1:]}'
                                , "Balance": f"{int(balance_of[-66:], 0)}",
                                'BlockNumber': f'{block_number}'
                            }
                            posts = blockchain_db.FilterPool
                            tras = posts.insert_one(d)
                            print(tras)
                            break
                except Exception as e:
                    pass


def main():
    procces_filter_pool = mp.Process(target=filter_pool)
    procces_filter_pool.start()
    procces_filter_pool.join()
