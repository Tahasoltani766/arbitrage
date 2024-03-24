import secrets
from uuid import uuid4
from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from flashbots import flashbot
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound
from web3.types import TxParams

# change this to `False` if you want to use mainnet
USE_SEPOLIA = True
CHAIN_ID = 111555111 if USE_SEPOLIA else 1




def random_account() -> LocalAccount:
    key = "0x" + secrets.token_hex(32)
    return Account.from_key(key)


def main() -> None:
    sender: LocalAccount = Account.from_key("0x5c9c7029dab6e679a3ab00fa683bf1f0b9e34940e48f521919c194937ade4c36")
    receiverAddress = Web3.to_checksum_address(random_account().address)

    signer: LocalAccount = Account.from_key("0x5c9c77777777777777777778683bf1f0b9e3494096421ab63fc194937ade4c36")

    w3 = Web3(HTTPProvider('https://go.getblock.io/047b88b3a0804ed9a12b02214022ebd6'))
    flashbot(w3, signer,"https://relay-sepolia.flashbots.net")

    # if USE_SEPOLIA:
    #     flashbot(w3, signer, "https://relay-sepolia.flashbots.net")
    # else:
    #     flashbot(w3, signer)

    print(f"Sender address: {sender.address}")
    print(f"Receiver address: {receiverAddress}")
    print(
        f"Sender account balance: {Web3.from_wei(w3.eth.get_balance(sender.address), 'ether')} ETH"
    )
    print(
        f"Receiver account balance: {Web3.from_wei(w3.eth.get_balance(receiverAddress), 'ether')} ETH"
    )

    # bundle two EIP-1559 (type 2) transactions, pre-sign one of them
    # NOTE: chainId is necessary for all EIP-1559 txns
    # NOTE: nonce is required for signed txns

    nonce = w3.eth.get_transaction_count(sender.address)
    tx1: TxParams = {
        "to": receiverAddress,
        "value": Web3.to_wei(0.001, "ether"),
        "gas": 21000,
        "gasPrice": Web3.to_wei(200, "gwei"),
        # "maxPriorityFeePerGas": Web3.to_wei(50, "gwei"),
        "nonce": nonce,
        "chainId": CHAIN_ID,
        # "type": 2,
    }
    print(tx1)
    tx1_signed = sender.sign_transaction(tx1)

    tx2: TxParams = {
        "to": receiverAddress,
        "value": Web3.to_wei(0.001, "ether"),
        "gas": 21000,
        "maxFeePerGas": Web3.to_wei(200, "gwei"),
        "maxPriorityFeePerGas": Web3.to_wei(50, "gwei"),
        "nonce": nonce + 1,
        "chainId": CHAIN_ID,
        "type": 2,
    }

    bundle = [{"signed_transaction": tx1_signed.rawTransaction}]

    # keep trying to send bundle until it gets mined
    while True:
        block = w3.eth.block_number
        print(f"Simulating on block {block}")
        # simulate bundle on current block
        try:
            w3.flashbots.simulate_bundle(bundle, block)
            print("Simulation successful.")
        except Exception as e:
            print("Simulation error", e)
            return

        # send bundle targeting next block
        print(f"Sending bundle targeting block {block+1}")
        replacement_uuid = str(uuid4())
        print(f"replacementUuid {replacement_uuid}")
        send_result = w3.flashbots.send_bundle(
            bundle,
            target_block_number=block + 1,
            opts={"replacementUuid": replacement_uuid},
        )
        print("bundleHash", w3.to_hex(send_result.bundle_hash()))

        stats_v1 = w3.flashbots.get_bundle_stats(
            w3.to_hex(send_result.bundle_hash()), block
        )
        print("bundleStats v1", stats_v1)

        stats_v2 = w3.flashbots.get_bundle_stats_v2(
            w3.to_hex(send_result.bundle_hash()), block
        )
        print("bundleStats v2", stats_v2)

        send_result.wait()
        try:
            receipts = send_result.receipts()
            print(f"\nBundle was mined in block {receipts[0].blockNumber}\a")
            break
        except TransactionNotFound:
            print(f"Bundle not found in block {block+1}")
            # essentially a no-op but it shows that the function works
            cancel_res = w3.flashbots.cancel_bundles(replacement_uuid)
            print(f"canceled {cancel_res}")

    print(
        f"Sender account balance: {Web3.from_wei(w3.eth.get_balance(sender.address), 'ether')} ETH"
    )
    print(
        f"Receiver account balance: {Web3.from_wei(w3.eth.get_balance(receiverAddress), 'ether')} ETH"
    )


if __name__ == "__main__":
    main()