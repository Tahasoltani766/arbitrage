from src.dexAggrigation.web3_instances import *


def oneinch_weth_wrrper(func):
    def wrraper(*args, **kwargs):
        weth_adrrs = Web3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
        a = []
        for addr in args:
            if addr == weth_adrrs:
                a.append("0x0000000000000000000000000000000000000000")
            else:
                a.append(addr)
        res = func(a[0], a[1], **kwargs)
        return res

    return wrraper
