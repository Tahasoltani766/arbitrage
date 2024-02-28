import web3.eth
from web3 import  Web3 as ww
dexs = [{'dex':'sushi',"factory addr":"0x123","abi":"abi abiabi","function pool":"getpait"},{'dex':'kushi',"factory addr":"0x1238956","abi":"abi","function pool":"get"}]

def a(dex:dict):
    contr = web3.eth.contract(address=ww.to_checksum_address(dex['dex'],abi=dex['abi']))


for i in dexs:
    a(i)
