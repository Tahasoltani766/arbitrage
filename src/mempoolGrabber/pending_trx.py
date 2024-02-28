import functools
import queue
import random
import multiprocessing as mp
import threading

from hexbytes import HexBytes
from web3.exceptions import TransactionNotFound
from multiprocessing import Queue, Process

from src.last_block_tx_simulatore.block_transactions import filter_transaction
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
    try:

        Thread(target=idk_starter, args=(hash_trx, tx_data_queue)).start()
    except TransactionNotFound:
        return None


q = queue.Queue()


def worker(data, blc_num):
    while True:
        thread = RespPostRust(data, blc_num)
        thread.start()
        thread.join()
        resp = thread.resp
        hash = thread.hash
        return hash, resp



q.join()


class RespPostRust(Thread):
    def __init__(self, data, blck_num):
        super().__init__()
        self.hash = None
        self.resp = None
        self.data = data
        self.blck_unm = blck_num


    def run(self):
        self.resp, self.hash = resp_post_rust(self.data, self.blck_unm)


def printer(tx_data_queue, block_number_queue: Queue):
    blc_num = block_number_queue.get()
    while True:
        if not block_number_queue.empty():
            blc_num = block_number_queue.get()
        data = tx_data_queue.get()
        inp = data['input']
        if inp != zero_input_tx:
            # thread = RespPostRust(data, blc_num)
            # thread.start()
            # thread.join()
            # resp = thread.resp
            # hash = thread.hash
            hash, resp = threading.Thread(target=worker,args=).start()
            print(resp, hash)
            if hash and resp:
                filter_transaction(resp, hash)
            # resp, hash = Thread(target=resp_post_rust, args=(data, blc_num)).start()
            # print(resp, hash)



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
