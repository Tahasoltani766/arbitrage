import functools
import random
import multiprocessing as mp
from hexbytes import HexBytes
from web3.exceptions import TransactionNotFound
from multiprocessing import Queue, Process
from src.mempoolGrabber.resp_post import resp_post_rust
from src.mempoolGrabber.web3_instances import node_getblock
import time
import asyncio
from web3 import AsyncWeb3, WebsocketProviderV2
from threading import Thread

zero_input_tx = HexBytes('0x')


async def ws_v2_subscription_example(new_pending_queue, block_number_queue):
    async with AsyncWeb3.persistent_websocket(
            WebsocketProviderV2(node_getblock)
    ) as w3:
        pend_id = await w3.eth.subscribe("newPendingTransactions")
        head_id = await w3.eth.subscribe("newHeads")
        async for response in w3.ws.process_subscriptions():
            if response['subscription'] == pend_id:
                tx_hash = response['result']
                new_pending_queue.put(tx_hash)
            elif response['subscription'] == head_id:
                blc_num = response['result']['number']
                block_number_queue.put(int(blc_num, 16))


"""{'subscription': '0xd9c09f81cfe4e0935e63dcca3dc5b315', 'result': AttributeDict({'parentHash': '0x0124addee3dff8e6778de180681e67bd33edce40464f1efd1a33dd15a080c50e', 'sha3Uncles': '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347', 'miner': '0x4838b106fce9647bdf1e7877bf73ce8b0bad5f97', 'stateRoot': '0x8ef2d7abb98bbad0820feec988f5fc2fbecc3d6ec0335e1f17862a027cc285e5', 'transactionsRoot': '0x8258b5afd57885cd4d069c7c97fdc979532f6b69ecc0a3b348dc0c45080c76d9', 'receiptsRoot': '0xd16de567594851347caf2c03ea2398330536a107f8ebdb001486c9f73dd8ab64', 'logsBloom': '0x07a429a0f08b111156188886a8fb99a3909acf41bc234180c5dd011956a0116a864c8f3ccd022028e7ea97029f489503abc8b407fe207a288074eae055bbbb697237cd5ecc488badc8025b5ee3888ebce002d0e554611ba073e3cd07e86ffaa44e09808f7a05826510aac0d006466f6fab5b613148bc06e41360c1b428085d892352f7dcb547196a92e5f0443304d336042002ffe9b8343a19a7cb486ab6240bbb201ac799c2a4200aff52d21ca48eaa10ff160903be8e87ac98b8260680837c73288a921fa18cd368d19bb39d3ff0bca0fdf802520e19d709515a231b40f7a246f1f2e8866460184b078080efe132052ca978a34af028e291533ca290047843', 'difficulty': '0x0', 'number': '0x126aa77', 'gasLimit': '0x1c9c380', 'gasUsed': '0xd48575', 'timestamp': '0x65dc6b63', 'extraData': '0x546974616e2028746974616e6275696c6465722e78797a29', 'mixHash': '0xb4df8889497abd333b176c734d0c8ad6967a0c47aa598923a5fd14d5c6e14609', 'nonce': '0x0000000000000000', 'baseFeePerGas': '0x67b3de622', 'withdrawalsRoot': '0x54b06683ce304c32c55395ba08035b21eeabcbf1e1050460e6e0a9df63c047dd', 'blobGasUsed': None, 'excessBlobGas': None, 'parentBeaconBlockRoot': None, 'hash': '0x362ada825254a3b49fae8ef0b1551bf74623d1d3bbf7e18230d11efcbff13430'})}
"""


async def idk(hash_trx, tx_data_queue):
    async with AsyncWeb3.persistent_websocket(
            WebsocketProviderV2(node_getblock)
    ) as w3:
        tx_data = await w3.eth.get_transaction(hash_trx)
        tx_data_queue.put(tx_data)


def idk_starter(hash_trx, tx_data_queue):
    while True:
        try:
            asyncio.run(idk(hash_trx, tx_data_queue))
            break
        except KeyboardInterrupt:
            break
        except TransactionNotFound:
            break
        except:
            time.sleep(random.random())


async def get_trx_by_hash(hash_trx, tx_data_queue):
    # async with AsyncWeb3.persistent_websocket(
    #         WebsocketProviderV2(node_getblock)
    # ) as w3:
    #     while True:
    try:

        Thread(target=idk_starter, args=(hash_trx, tx_data_queue)).start()
    except TransactionNotFound:
        return None


def printer(tx_data_queue, block_number_queue: Queue):
    blc_num = block_number_queue.get()
    while True:
        if not block_number_queue.empty():
            blc_num = block_number_queue.get()
        data = tx_data_queue.get()
        inp = data['input']
        if inp != zero_input_tx:
            Thread(target=resp_post_rust, args=(data,blc_num)).start()
            # pool.map(functools.partial(resp_post_rust, bl_num=blc_num), [data])


def start_pending_transactions(new_pending_queue, block_number_queue):
    try:
        asyncio.run(ws_v2_subscription_example(new_pending_queue, block_number_queue))
    except KeyboardInterrupt:
        pass


def start_get_tx(new_pending_queue, tx_data_queue):
    while True:
        try:
            hash_trx = new_pending_queue.get()
            asyncio.run(get_trx_by_hash(hash_trx, tx_data_queue))
        except KeyboardInterrupt:
            pass


def main_pend_trx():
    new_pending_queue = Queue()
    tx_data_queue = Queue()
    block_number_queue = Queue()

    p1 = Process(target=start_pending_transactions, args=(new_pending_queue, block_number_queue))
    p2 = Process(target=printer, args=(tx_data_queue, block_number_queue))
    p3 = Process(target=start_get_tx, args=(new_pending_queue, tx_data_queue))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

#
# if __name__ == '__main__':
#     mp.freeze_support()
#     main_pend_trx()
