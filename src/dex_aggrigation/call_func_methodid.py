import requests
import web3.types
from web3 import types as type
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_abi import encode
from flashbots import flashbots



w3 = Web3(Web3.HTTPProvider('https://go.getblock.io/047b88b3a0804ed9a12b02214022ebd6'))
# w3 = Web3(Web3.HTTPProvider("https://go.getblock.io/9e9154f93e4440968bbfc4c31a1af414"))
priv_key = "0x5c9c7029dab6e679a3ab00fa683bf1f0b9e34940e48f521919c194937ade4c36"
account: LocalAccount = Account.from_key(priv_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

privet_key_signuter = "0x5c9c77777777777777777778683bf1f0b9e3494096421ab63fc194937ade4c36"
signer: LocalAccount = Account.from_key(priv_key)


class MetaWETH(object):
    address_withdrawal: web3.types.ChecksumAddress = "0x00000000000000000000000000000000000000000"
    address: type.ChecksumAddress = w3.to_checksum_address("0x0000000000000000000000000000000000000000")

    def __init__(self, _address, addr_w=None):
        self.address = _address
        if addr_w:
            self.address_withdrawal = addr_w

    @classmethod
    def nonce(cls):
        nonce = w3.eth.get_transaction_count(account.address)
        return nonce

    @staticmethod
    def gas_price():
        res = requests.get('https://api.blocknative.com/gasprices/blockprices')
        response = res.json()
        a = response["blockPrices"][0]["estimatedPrices"][4]
        if a and a['confidence'] == 70:
            max_priority_gas = a['maxPriorityFeePerGas']
            max_per_gas = a['maxFeePerGas']
            return max_priority_gas, max_per_gas
        else:
            return None

    @classmethod
    def transact(cls, tx_input, withdraw=False, payable_value=False):
        payable_val = 0
        if payable_value:
            payable_val = payable_value
        gas_price = MetaWETH.gas_price()
        trx = {
            'chainId': 1,
            'type': 2,
            'from': account.address,
            'to': cls.address if not withdraw else cls.address_withdrawal,
            'nonce': cls.nonce(),
            'value': payable_val,
            'maxPriorityFeePerGas': w3.to_wei(gas_price[0], 'gwei'),
            'maxFeePerGas': w3.to_wei(gas_price[1], 'gwei'),
            'data': tx_input
        }

        gas = w3.eth.estimate_gas(trx)

        trx = w3.eth.send_transaction({
            'from': account.address,
            'to': cls.address if not withdraw else cls.address_withdrawal,
            'nonce': cls.nonce(),
            'value': 0,
            "gas": gas,
            'maxPriorityFeePerGas': w3.to_wei(gas_price[0], 'gwei'),
            'maxFeePerGas': w3.to_wei(gas_price[1], 'gwei'),
            'data': tx_input
        })
        tx = w3.eth.get_transaction(trx)
        return tx

    def flash_bots(self, trx):
        trx_signature = signer.sign_transaction(trx)
        bundle = [
            {"signed_transaction": trx_signature.rawTransaction},
            {"signer": signer, "transaction": trx},
        ]
        while True:
            block = w3.eth.block_number
            try:
                w3.flashbots.simulate(bundle, block)
            except Exception as e:
                return None


class StETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xae7ab96520de3a18e5e111b5eaab095312d7fe84"),
                         w3.to_checksum_address("0xB9D7934878B5FB9610B3fE8A5e441e8fad7E293f"))

        # mint:"0xa1903eab", burn:"3194528a"

    def mint(self, _referral: type.ChecksumAddress):
        tx_input = "0xa1903eab" + (
            encode(['(address)'], [(_referral,)])).hex()
        self.transact(tx_input=tx_input, withdraw=False)

    def burn(self, amount):
        pass
        tx_input = "0x3194528a" + (encode(['(uint256)'], [(amount,)])).hex()
        addr = self.address_withdrawal
        self.transact(tx_input, True)


class RocketETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xae78736cd615f374d3085123a210448e74fc6393"))

    # mint:"0x94bf804d",burn:"0x42966c68"
    def mint(self, _ethAmount: int, address_to: type.ChecksumAddress):
        tx_input = "0x94bf804d" + (encode(['(uint256,address)'], [(_ethAmount, address_to)])).hex()
        self.transact(tx_input=tx_input)

    def burn(self, reth_amount: int):
        tx_input = "0x42966c68" + (encode(['(uint256)'], [(reth_amount,)])).hex()
        self.transact(tx_input=tx_input)


class MantleStakedEther(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xd5F7838F5C461fefF7FE49ea5ebaF7728bB0ADfa"))

    # mint:"0x40c10f19", burn:"0x42966c68"

    def mint(self, staker: type.ChecksumAddress, amount: int):
        tx_input = "0x40c10f19" + (encode(['(address,uint256)'], [(staker, amount)])).hex()
        self.transact(tx_input=tx_input)

    def burn(self, amount: int):
        tx_input = "0x42966c68" + (encode(['(uint256)'], [(amount,)])).hex()
        self.transact(tx_input=tx_input)


class FraxETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0x5e8422345238f34275888049021821e8e08caa1f"))

    # mint:"0x6a257ebc", burn:"0x42966c68"

    def mint(self, m_address: type.ChecksumAddress, m_amount: int):
        tx_input = "0x6a257ebc" + (encode(['(address,uint256)'], [(m_address, m_amount)])).hex()
        self.transact(tx_input=tx_input)

    def burn(self, amount: int):
        tx_input = "0x42966c68" + (encode(['(uint256)'], [(amount,)])).hex()
        self.transact(tx_input=tx_input)


class StakedFraxEther(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xac3e018457b222d93114458476f3e3416abbe38f"))

    # mint:"0x6e553f65", burn:"0xb460af94"

    def mint(self, assets: int, receiver: type.ChecksumAddress):
        tx_input = "0x6e553f65" + (encode(['(uint256,address)'], [(assets, receiver)])).hex()
        self.transact(tx_input=tx_input)

    def burn(self, assets: int, receiver: type.ChecksumAddress, owner: type.ChecksumAddress):
        tx_input = "0xb460af94" + (encode(['(uint256,address,address)'], [(assets, receiver, owner)])).hex()
        self.transact(tx_input=tx_input)


class CoinbaseWrappedStakedETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xbe9895146f7af43049ca1c1ae358b0541ea49704"))

    # mint:"0x40c10f19",burn:"0x42966c68"

    def mint(self, _to: type.ChecksumAddress, _amount: int):
        tx_input = "0x40c10f19" + (encode(['(address,uint256)'], [(_to, _amount)])).hex()
        self.transact(tx_input=tx_input)

    def burn(self, _amount: int):
        tx_input = "0x42966c68" + (encode(['(uint256)'], [(_amount,)])).hex()
        self.transact(tx_input=tx_input)


class AnkrStakedETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xe95a203b1a91a908f9b9ce46459d101078c2c3cb"))

    # mint: "0x40c10f19", burn: "0x9dc29fac"

    def mint(self, account: type.ChecksumAddress, amount: int):
        tx_input = "0x40c10f19" + (encode(['(address,uint256)'], [(account, amount)])).hex()
        self.transact(tx_input=tx_input)

    def burn(self, account: type.ChecksumAddress, amount: int):
        tx_input = "0x9dc29fac" + (encode(['(address,uint256)'], [(account, amount)])).hex()
        self.transact(tx_input=tx_input)


class WrappedBeaconETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xa2E3356610840701BDf5611a53974510Ae27E2e1"))

    # mint: "0x40c10f19",burn: "0xa0907283"

    def mint(self, _to: type.ChecksumAddress, _amount: int):
        tx_input = "0x40c10f19" + (encode(['(address,uint256)'], [(account, _amount)])).hex()
        self.transact(tx_input=tx_input)

    def burn(self, wbethAmount: int):
        tx_input = "0xa0907283" + (encode(['(uint256)'], [(wbethAmount)])).hex()
        self.transact(tx_input=tx_input)


class sETH2(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xFe2e637202056d30016725477c5da089Ab0A043A"))

    #  mint: "0xa0712d68", burn: "0x9dc29fac"

    def mint(self, amount: int):
        tx_input = "0xa0712d68" + (encode(['(uint256)'], [(amount,)])).hex()

        self.transact(tx_input=tx_input)

    def burn(self, acct: type.ChecksumAddress, amount: int):
        tx_input = "0x9dc29fac" + (encode(['(address,uint256)'], [(acct, amount)])).hex()
        self.transact(tx_input=tx_input, withdraw=False)



class WETH(MetaWETH):
    def __init__(self):
        super().__init__(w3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"))

    #  mint: "0xd0e30db0", burn: "0x2e1a7d4d"

    def mint(self, value):
        tx_input = "0xd0e30db0"
        self.transact(tx_input=tx_input, withdraw=True, payable_value=value)

    def burn(self, wad: int):
        tx_input = "0x2e1a7d4d" + (encode(['(uint256)'], [(wad,)])).hex()
        self.transact(tx_input=tx_input, withdraw=False)

