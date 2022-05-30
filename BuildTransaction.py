# Description
# -----------------
# functionality for interfacing with our smart contract

# Resources
# -----------------
# Sign a Contract Txn: https://web3py.readthedocs.io/en/stable/web3.eth.account.html#sign-a-contract-transaction
#

from web3 import Web3
from web3.auto import w3
import json
import os

from datetime import datetime
import logging


class MintFactory:

    def __init__(self, contract_address, owner_address, network="mainnet"):
        self.contract_address = contract_address
        self.owner_address = owner_address
        self.w3 = self.set_w3(network)
        self.nft_contract = self.set_contract()
        self.nonce = self.set_nonce()
        self.token = self.set_token_count()

        print(f"Connection status: {self.w3.isConnected()}")
        print(f"Next nonce: {self.nft_contract.functions.balanceOf(self.owner_address).call()}")
        print(f"Next token ID: {self.token}")

    def set_w3(self, network):
        return Web3(Web3.HTTPProvider(f'https://{network}.infura.io/v3/4dd6cccb7c6c4c7a9a01f8b02b1ada03'))

    def set_contract(self):
        with open("contract_abi.json", "r") as f:
            contract_abi = json.load(f)
        return self.w3.eth.contract(address=self.contract_address, abi=contract_abi)

    def set_nonce(self):
        return self.w3.eth.get_transaction_count(self.owner_address, 'pending')

    def set_token_count(self):
        return self.nft_contract.functions.nextID().call() + 1

# mints an NFT
    def mint_nft(self, to_address, uri):
        # get nonce and token id for transaction
        nonce = self.nonce
        self.nonce += 1

        token_id = self.token
        self.token += 1

        mint_txn = self.nft_contract.functions.mint(
            to_address,     # owner of newly minted NFT
            token_id,       # unique identifier for the NFT
            uri,            # hosted link of JSON metadata
        ).buildTransaction({
            'gas': 700000,
            'gasPrice': self.w3.eth.gas_price,
            'from': self.owner_address,
            'nonce': nonce,
            'chainId': 3,
        })

        # sign the transaction
        private_key = os.environ['PK']
        signed_txn = self.w3.eth.account.sign_transaction(mint_txn, private_key=private_key)

        # broadcast the transaction
        bc_txn = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        w3.toHex(w3.keccak(signed_txn.rawTransaction))

        # txhash = signed_txn['hash']
        # tx_status = self.w3.eth.wait_for_transaction_receipt(txhash)['status']
        # if tx_status == 0:
        #     msg = "{} >>>> Failed txn. See tx hash for more: {}".format(datetime.now(), txhash.hex())
        #     print(msg)
        #     logging.info(msg)
        # else:
        #     msg = "{} >>>> Successful txn. Txhash: {}".format(datetime.now(), signed_txn['hash'].hex())
        #     logging.info(msg)
        #     print(msg)

        return bc_txn


if __name__ == "__main__":
    # my_address = '0x4dE801A18FaA4268eBe916F132CcD760b7C649B9'
    contract_address = "0x96807aD777850A9336B9aD9F9Bb625CaD4eC0e5a"
    owner_address = '0x42A5243D51176bdCED13F40E3C85b7259e84c113'
    mint_factory = MintFactory(contract_address, owner_address, network="ropsten")

    uri = "https://gateway.pinata.cloud/ipfs/Qmc7yWr8Q8j3fWJMK6zcwUEYPUcigeTDbBca857xD7Sg5Q"  # JSON
    return_hash = mint_factory.mint_nft(owner_address, uri)
    print(return_hash)
