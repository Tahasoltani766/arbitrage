from web3 import Web3
import pandas

w3 = Web3(Web3.HTTPProvider("url"))


# contract = w3.eth.contract(address=W3.to_checksum_address("0x"))
# identity_func = contract.get_function_by_signature('identity(uint256,bool)')
# identity_func(1, True).call()

class MetaWETH(object):
    def __init__(self, _address, _sig_mint, _burn):
        self.address = _address
        self.sig_mint = _sig_mint
        self.sig_burn = _burn
        # self.object_contract = _object_contract
        self.contract = w3.eth.contract(address=self.address)

    def mint(self, *args, **kwargs):
        mint_func = self.contract.get_function_by_identifier(self.sig_mint)
        mint_func(*args[0]).call()

    def burn(self, *args, **kwargs):
        burn_func = self.contract.get_function_by_identifier(self.sig_burn)
        burn_func(*args[0:]).call()


class StETH(MetaWETH):
    def __init__(self, _burn):
        super().__init__("0xae7ab96520de3a18e5e111b5eaab095312d7fe84", "aa0b7db7", _burn)

    def mint(self, _maxDepositsCount: int, _stakingModuleId: int, _depositCalldata: bytes):
        super().mint((_maxDepositsCount, _stakingModuleId, _depositCalldata))


class RocketETH(MetaWETH):
    def __init__(self):
        super().__init__("0xae78736cd615f374d3085123a210448e74fc6393", "d0e30db0", "42966c68")

    def mint(self):
        pass

    def burn(self, reth_amount: int):
        super().burn(reth_amount)


class MantleStakedEther(MetaWETH):
    def __init__(self):
        super().__init__("0xd5F7838F5C461fefF7FE49ea5ebaF7728bB0ADfa", "49123dc2", "42966c68")

    def mint(self, staker: str, amount: int):
        super().mint(staker, amount)

    def burn(self, amount: int):
        super().burn(amount)


class FraxETH(MetaWETH):
    def __init__(self):
        super().__init__("0x5e8422345238f34275888049021821e8e08caa1f", "49123dc2", "42966c68")

    def mint(self, m_address: str, m_amount: int):
        super().mint(m_address, m_amount)

    def burn(self, amount: int):
        super().burn(amount)


class StakedFraxEther(MetaWETH):
    def __init__(self):
        super().__init__("0xac3e018457b222d93114458476f3e3416abbe38f", "6e553f65", "b460af94")

    def mint(self, assets: int, receiver: str):
        super().mint(assets, receiver)

    def burn(self, assets: int, receiver: str, owner: str):
        super().burn(assets, receiver, owner)


class CoinbaseWrappedStakedETH(MetaWETH):
    def __init__(self):
        super().__init__("0xbe9895146f7af43049ca1c1ae358b0541ea49704", "42966c68", "b460af94")

    def mint(self, _to: str, _amount: int):
        super().mint(_to, _amount)

    def burn(self, _amount: int):
        super().burn(_amount)


class AnkrStakedETH(MetaWETH):
    def __init__(self):
        super().__init__("0xe95a203b1a91a908f9b9ce46459d101078c2c3cb", "49123dc2", "9dc29fac")

    def mint(self, account: str, amount: int):
        super().mint(account, amount)

    def burn(self, account: str, amount: int):
        super().burn(account, amount)


class WrappedBeaconETH(MetaWETH):
    def __init__(self):
        super().__init__("0xa2E3356610840701BDf5611a53974510Ae27E2e1", "4b29d210", "42966c68")

    def mint(self, referral: str):
        super().mint(referral)
        # pyable

    def burn(self, wbethAmount: int):
        super().burn(wbethAmount)


class sETH2(MetaWETH):
    def __init__(self):
        super().__init__("0xFe2e637202056d30016725477c5da089Ab0A043A", "a0712d68", "9dc29fac")

    def mint(self, amount: int):
        super().mint(amount)

    def burn(self, account: str, amount: int):
        super().burn(account, amount)
