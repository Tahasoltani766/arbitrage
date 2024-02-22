import random
from pprint import pprint
from web3.exceptions import TransactionNotFound
from multiprocessing import Queue, Process
from src.mempoolGrabber.web3_instances import node_getblock
import time
import asyncio
from web3 import AsyncWeb3, WebsocketProviderV2
from threading import Thread


async def ws_v2_subscription_example(new_pending_queue):
    async with AsyncWeb3.persistent_websocket(
            WebsocketProviderV2(node_getblock)
    ) as w3:
        await w3.eth.subscribe("newPendingTransactions")
        async for response in w3.ws.process_subscriptions():
            tx_hash = response['result']
            new_pending_queue.put(tx_hash)


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


async def get_trx_by_hash(new_pending_queue, tx_data_queue):
    async with AsyncWeb3.persistent_websocket(
            WebsocketProviderV2(node_getblock)
    ) as w3:
        while True:
            try:
                hash_trx = new_pending_queue.get()
                Thread(target=idk_starter, args=(hash_trx, tx_data_queue)).start()
            except TransactionNotFound:
                return None


def printer(tx_data_queue):
    while True:
        data = tx_data_queue.get()
        pprint(data)


def start_pending_transactions(new_pending_queue):
    try:
        asyncio.run(ws_v2_subscription_example(new_pending_queue))
    except KeyboardInterrupt:
        pass


def start_get_tx(new_pending_queue, tx_data_queue):
    try:
        asyncio.run(get_trx_by_hash(new_pending_queue, tx_data_queue))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    new_pending_queue = Queue()
    tx_data_queue = Queue()

    p1 = Process(target=start_pending_transactions, args=(new_pending_queue,))
    p2 = Process(target=printer, args=(tx_data_queue,))
    p3 = Process(target=start_get_tx, args=(new_pending_queue, tx_data_queue))

    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
