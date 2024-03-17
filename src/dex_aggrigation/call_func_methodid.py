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


class MetaWETH(object):
    def __init__(self, _address, _sig_mint, _burn):
        self.address = _address
        # self.sig_mint = _sig_mint
        # self.sig_burn = _burn
        # self.contract = w3.eth.contract(address=self.address)

    @classmethod
    def nonce(cls):
        nonce = w3.eth.get_transaction_count(account.address)
        return nonce

    def transact(self, tx_input):
        trx = {
            'from': account.address,
            'to': self.address,
            'nonce': self.nonce,
            'value': None,
            'input': tx_input,
            'gas': 100000,
            'gasPrice': w3
        }
    # def mint(self, *args, **kwargs):
    #     mint_func = self.contract.get_function_by_selector(self.sig_mint)
    #     mint_func(*args[0]).call()
    #
    # def burn(self, *args, **kwargs):
    #     burn_func = self.contract.get_function_by_selector(self.sig_burn)
    #     burn_func(*args[0]).call()


class StETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xae7ab96520de3a18e5e111b5eaab095312d7fe84"), "0xaa0b7db7",
                         ":3194528a")
        self.address_withdrawal = w3.to_checksum_address("0xB9D7934878B5FB9610B3fE8A5e441e8fad7E293f")
        self.contract_withdrawal = w3.eth.contract(address=self.address_withdrawal)

    def mint(self, maxDepositsCount: int, stakingModuleId: int, depositCalldata: bytes):
        tx_input = "0xaa0b7db7" + (
            encode(['(uint256,uint256,bytes)'], [maxDepositsCount, stakingModuleId, depositCalldata])).hex()
        super().transact(tx_input)

    def burn(self, amount):
        pass
        # tx_input = "0x3194528a" + (encode(['uint256'], [amount])).hex()
        # burn_func = self.contract_withdrawal.get_function_by_identifier("3194528a")
        # burn_func(*args[0]).call()


class RocketETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xae78736cd615f374d3085123a210448e74fc6393"), "0x94bf804d",
                         "0x42966c68")

    def mint(self, _ethAmount: int, address_to: type.ChecksumAddress):
        tx_input = "0x94bf804d" + (encode(['(uint256,address)'], [(_ethAmount, address_to)])).hex()
        super().transact(tx_input)

    def burn(self, reth_amount: int):
        tx_input = "0x42966c68" + (encode(['uint256'], [reth_amount])).hex()
        super().transact(tx_input)


class MantleStakedEther(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xd5F7838F5C461fefF7FE49ea5ebaF7728bB0ADfa"), "0x40c10f19", "0x42966c68")

    def mint(self, staker: type.ChecksumAddress, amount: int):
        tx_input = "0x40c10f19" + (encode(['(address,uint256)'], [(staker, amount)])).hex()
        super().transact(tx_input)

    def burn(self, amount: int):
        tx_input = "0x42966c68" + (encode(['uint256'], [amount])).hex()
        super().transact(tx_input)


class FraxETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0x5e8422345238f34275888049021821e8e08caa1f"), "0x6a257ebc", "0x42966c68")

    def mint(self, m_address: type.ChecksumAddress, m_amount: int):
        tx_input = "0x6a257ebc" + (encode(['(address,uint256)'], [(m_address, m_amount)])).hex()
        super().transact(tx_input)

    def burn(self, amount: int):
        tx_input = "0x42966c68" + (encode(['uint256'], [amount])).hex()
        super().transact(tx_input)


class StakedFraxEther(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xac3e018457b222d93114458476f3e3416abbe38f"), "0x6e553f65", "0xb460af94")

    def mint(self, assets: int, receiver: type.ChecksumAddress):
        tx_input = "0x6e553f65" + (encode(['(uint256,address)'], [(assets, receiver)])).hex()
        super().transact(tx_input)

    def burn(self, assets: int, receiver: type.ChecksumAddress, owner: type.ChecksumAddress):
        tx_input = "0xb460af94" + (encode(['(uint256,address,address)'], [(assets, receiver, owner)])).hex()
        super().transact(tx_input)


class CoinbaseWrappedStakedETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xbe9895146f7af43049ca1c1ae358b0541ea49704"), "0x40c10f19",
                         "0x42966c68")

    def mint(self, _to: type.ChecksumAddress, _amount: int):
        tx_input = "0x40c10f19" + (encode(['(address,uint256)'], [(_to, _amount)])).hex()
        super().transact(tx_input)

    def burn(self, _amount: int):
        tx_input = "0x42966c68" + (encode(['(uint256)'], [(_amount)])).hex()
        super().transact(tx_input)


class AnkrStakedETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xe95a203b1a91a908f9b9ce46459d101078c2c3cb"), "0x40c10f19", "0x9dc29fac")

    def mint(self, account: type.ChecksumAddress, amount: int):
        tx_input = "0x40c10f19" + (encode(['(address,uint256)'], [(account, amount)])).hex()
        super().transact(tx_input)

    def burn(self, account: type.ChecksumAddress, amount: int):
        tx_input = "0x9dc29fac" + (encode(['(address,uint256)'], [(account, amount)])).hex()
        super().transact(tx_input)


class WrappedBeaconETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xa2E3356610840701BDf5611a53974510Ae27E2e1"), "0x40c10f19", "0xa0907283")

    def mint(self, _to: type.ChecksumAddress, _amount: int):
        tx_input = "0x40c10f19" + (encode(['(address,uint256)'], [(account, _amount)])).hex()
        super().transact(tx_input)

    def burn(self, wbethAmount: int):
        tx_input = "0xa0907283" + (encode(['(uint256)'], [(wbethAmount)])).hex()
        super().transact(tx_input)


class sETH2(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xFe2e637202056d30016725477c5da089Ab0A043A"), "0xa0712d68", "0x9dc29fac")

    def mint(self, amount: int):
        tx_input = "0xa0712d68" + (encode(['(uint256)'], [(amount)])).hex()
        super().transact(tx_input)

    def burn(self, account: type.ChecksumAddress, amount: float):
        tx_input = "0x9dc29fac" + (encode(['(address,uint256)'], [(account, amount)])).hex()
        super().transact(tx_input)
