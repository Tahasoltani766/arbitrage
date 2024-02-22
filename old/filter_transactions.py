import json
import re
import threading
from time import sleep
import requests
from web3_instances import *
import asyncio
from mongo_handler import blockchain_db as db
from constant import *


async def get_hash_transaction():
    th_list = []
    if w3.is_connected():
        block = w3.eth.get_block('latest')
        if block:
            for tx_hash in block['last_block_tx_simulatore']:
                a = threading.Thread(target=get_transaction, args=(tx_hash,))
                sleep(0.5)
                a.start()
                th_list.append(a)
    for t in th_list:
        t.join()


def get_transaction(tx_hash):
    transaction = w3.eth.get_transaction(tx_hash)
    if str(transaction['input']) != "0x":
        a: threading.Thread = threading.Thread(target=tx, args=(transaction,))
        a.start()
        a.join()


def tx(trs):
    trx = {
        "chainId": 1,
        "from": trs['from'],
        "to": trs['to'],
        "data": trs['input'].hex(),
        "gasLimit": trs['gas'],
        "value": str(trs['value']),
        "blockNumber": int(trs['blockNumber'])-1,
        "formatTrace": True
    }
    if trs['input'].hex() != '0x':
        resp = requests.post("http://localhost:8080/api/v1/simulate", data=json.dumps(trx))
        print(resp)
        if 'formattedTrace' in resp.json().keys():
            a: threading.Thread = threading.Thread(target=filter_transaction,
                                                   args=(resp.json(), trs['hash']))
            a.start()
            a.join()


def filter_transaction(transaction, _hash):
    address_dexs = [uniswap_router2, zerox, oneinch, sushiswap, universal_router, swap_router02]
    cleaned_formatrace = re.sub(combined_regex, '', transaction['formattedTrace'])
    n = True
    try:
        if "trace" in transaction.keys():
            for i in transaction['trace']:
                for j in address_dexs:
                    if j in i.values():
                        _data = {
                            'Dex': f"{j}",
                            'Trace': f"{transaction['trace']}",
                            'formattedTrace': f"{cleaned_formatrace}",
                            'hash': f"{_hash.hex()}",
                            'blockNumber': f"{transaction['blockNumber']}"
                        }
                        posts = db.Transactions
                        tras = posts.insert_one(_data)
                        n = False
                if not n:
                    break
    except Exception as e:
        pass


async def main():
    await asyncio.gather(get_hash_transaction())

asyncio.run(main())