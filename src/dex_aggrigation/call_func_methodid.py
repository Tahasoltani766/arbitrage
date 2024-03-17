import web3.types
from web3 import types as type
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3, EthereumTesterProvider
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_abi import encode

w3 = Web3(Web3.HTTPProvider('https://go.getblock.io/047b88b3a0804ed9a12b02214022ebd6'))
# w3 = Web3(Web3.HTTPProvider("https://go.getblock.io/9e9154f93e4440968bbfc4c31a1af414"))
priv_key = "0x5c9c7029dab6e679a3ab00fa683bf1f0b9e34940e48f521919c194937ade4c36"
account: LocalAccount = Account.from_key(priv_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))


# contract = w3.eth.contract(address=W3.to_checksum_address("0x"))
# identity_func = contract.get_function_by_signature('identity(uint256,bool)')
# identity_func(1, True).call()

class MetaWETH(object):
    def __init__(self, _address, _sig_mint, _burn):
        self.address = _address
        self.sig_mint = _sig_mint
        self.sig_burn = _burn
        self.contract = w3.eth.contract(address=self.address)

    @classmethod
    def nonce(cls):
        nonce = w3.eth.get_transaction_count(account.address)
        return nonce

    def mint(self, *args, **kwargs):
        mint_func = self.contract.get_function_by_selector(self.sig_mint)
        mint_func(*args[0]).call()

    def burn(self, *args, **kwargs):
        burn_func = self.contract.get_function_by_selector(self.sig_burn)
        burn_func(*args[0]).call()


class StETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xae7ab96520de3a18e5e111b5eaab095312d7fe84"), "aa0b7db7", ":3194528a")
        self.address_withdrawal = w3.to_checksum_address("0xB9D7934878B5FB9610B3fE8A5e441e8fad7E293f")
        self.contract_withdrawal = w3.eth.contract(address=self.address_withdrawal)

    def mint(self, _maxDepositsCount: int, _stakingModuleId: int, _depositCalldata: bytes):
        tx_input = "0xaa0b7db7" + (
            encode(['uint256', 'uint256', 'bytes'], [_maxDepositsCount, _stakingModuleId, _depositCalldata])).hex()
        # super().mint((_maxDepositsCount, _stakingModuleId, _depositCalldata))

    def burn(self, *args, **kwargs):
        burn_func = self.contract_withdrawal.get_function_by_identifier("3194528a")
        burn_func(*args[0]).call()


class RocketETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xae78736cd615f374d3085123a210448e74fc6393"), "0x49123dc2",
                         "0x42966c68")

    def mint(self, _ethAmount: int, address_to: str):
        tx_input = "0x49123dc2" + (encode(['(uint256,address)'], [(_ethAmount, address_to)])).hex()
        # super().mint(_ethAmount, address_to)

    def burn(self, reth_amount):
        tx_input = "0x42966c68" + (encode(['uint256'], [reth_amount])).hex()
        # super().burn(reth_amount)


class MantleStakedEther(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xd5F7838F5C461fefF7FE49ea5ebaF7728bB0ADfa"), "49123dc2", "42966c68")

    def mint(self, staker: str, amount: int):
        tx_input = "0x49123dc2" + (encode(['(address,uint256)'], [(staker, amount)])).hex()
        print(tx_input)
        # super().mint(staker, amount)

    def burn(self, amount: int):
        tx_input = "0x42966c68" + (encode(['uint256'], [amount])).hex()
        print(tx_input)
        # super().burn(amount)


class FraxETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0x5e8422345238f34275888049021821e8e08caa1f"), "49123dc2", "42966c68")

    def mint(self, m_address: str, m_amount: int):
        tx_input = "0x49123dc2" + (encode(['(address,uint256)'], [(m_address, m_amount)])).hex()
        # super().mint(m_address, m_amount)

    def burn(self, amount: int):
        tx_input = "0x42966c68" + (encode(['uint256'], [amount])).hex()
        # super().burn(amount)


class StakedFraxEther(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xac3e018457b222d93114458476f3e3416abbe38f"), "6e553f65", "b460af94")

    def mint(self, assets: int, receiver: str):
        tx_input = "0x6e553f65" + (encode(['(uint256,address)'], [(assets, receiver)])).hex()
        # super().mint(assets, receiver)

    def burn(self, assets: int, receiver: type.ChecksumAddress, owner: type.ChecksumAddress):
        tx_input = "0x6e553f65" + (encode(['(uint256,address,address)'], [(assets, receiver, owner)])).hex()
        # super().burn(assets, receiver, owner)




class CoinbaseWrappedStakedETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xbe9895146f7af43049ca1c1ae358b0541ea49704"), "0x40c10f19",
                         "0x42966c68")

    def mint(self, _to: type.ChecksumAddress, _amount: int):
        tx_input = "0x40c10f19" + (encode(['(address,uint256)'], [(_to, _amount)])).hex()
        # super().mint(_to, _amount)

    def burn(self, _amount: float):
        tx_input = "0x42966c68" + (encode(['(uint256)'], [(_amount)])).hex()
        super().burn(_amount)


class AnkrStakedETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xe95a203b1a91a908f9b9ce46459d101078c2c3cb"), "49123dc2", "9dc29fac")

    def mint(self, account: str, amount: int):
        tx_input = "0x49123dc2" + (encode(['(address,uint256)'], [(account, amount)])).hex()
        # super().mint(account, amount)

    def burn(self, account: str, amount: int):
        tx_input = "0x9dc29fac" + (encode(['(address,uint256)'], [(account, amount)])).hex()
        # super().burn(account, amount)


class WrappedBeaconETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xa2E3356610840701BDf5611a53974510Ae27E2e1"), "49123dc2", "42966c68")

    def mint(self, _to: str, _amount: int):
        tx_input = "0x49123dc2" + (encode(['(address,uint256)'], [(account, _amount)])).hex()
        # super().mint(_to, _amount)

    def burn(self, wbethAmount: int):
        tx_input = "0x42966c68" + (encode(['(uint256)'], [(wbethAmount)])).hex()
        # super().burn(wbethAmount)


class sETH2(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xFe2e637202056d30016725477c5da089Ab0A043A"), "a0712d68", "9dc29fac")

    def mint(self, amount: int):
        tx_input = "0xa0712d68" + (encode(['(uint256)'], [(amount)])).hex()
        # super().mint(amount)

    def burn(self, account: str, amount: float):
        tx_input = "0x9dc29fac" + (encode(['(address,uint256)'], [(account, amount)])).hex()
        # super().burn(account, amount)
