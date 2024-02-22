import time
from web3 import Web3
from functools import cache

# rpc_url = 'https://go.getblock.io/c6deafecae81430da2229597a4effef6'
rpc_url = 'https://eth-mainnet.g.alchemy.com/v2/N1rPfpXLcgfLjyGiaCEmG9VHP8DeYW74'


# def w3_wrapper(func):
#     def wrap(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrap()


# @cache
def w3():
    return Web3(Web3.HTTPProvider(rpc_url))


def web3_wrapper(func):
    def wrap(*args, **kwargs):
        return func(*args, **kwargs, w3=w3())
    return wrap


# def timewraper(func):
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         for i in range(20):
#             result = func(*args, **kwargs)
#         end = time.time()
#         print("Time", abs(start - end)/100)
#         return result
#
#     return wrapper


# rpc_url = 'https://eth-mainnet.g.alchemy.com/v2/N1rPfpXLcgfLjyGiaCEmG9VHP8DeYW74'
# w3 = Web3(Web3.HTTPProvider(rpc_url))


