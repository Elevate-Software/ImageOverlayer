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

# contact address and contract abi for creating contract object
contract_address = "0x96807aD777850A9336B9aD9F9Bb625CaD4eC0e5a"
with open("contract_abi.json", "r") as f:
    contract_abi = json.load(f)

# create contract object
network = "ropsten"
w3 = Web3(Web3.HTTPProvider(f'https://{network}.infura.io/v3/4dd6cccb7c6c4c7a9a01f8b02b1ada03'))
nft_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# variables that need to be incremented internally
starting_id = nft_contract.functions.nextID().call()
id_counter = starting_id
starting_txn_count = w3.eth.get_transaction_count('0x42A5243D51176bdCED13F40E3C85b7259e84c113')
txn_count = starting_txn_count


# internally increments the token ID for each NFT
def new_id():
    global id_counter
    next_id = id_counter
    id_counter += 1
    return next_id


# internally increments the nonce for each NFT
def new_txn_count():
    global txn_count
    next_txn_count = txn_count
    txn_count += 1
    return next_txn_count


# mints an NFT
def mint_nft(to_address, uri):
    # get nonce and token id for transaction
    nonce = new_txn_count()
    token_id = new_id()

    mint_txn = nft_contract.functions.mint(
        to_address,  # owner of newly minted NFT
        token_id,  # unique identifier for the NFT
        uri,  # hosted link of JSON metadata
    ).buildTransaction({
        'gas': 700000,
        'gasPrice': w3.toWei('2', 'gwei'),
        'from': '0x42A5243D51176bdCED13F40E3C85b7259e84c113',
        'nonce': nonce,
    })

    # sign the transaction
    private_key = os.environ['PK']
    signed_txn = w3.eth.account.sign_transaction(mint_txn, private_key=private_key)

    # broadcast the transaction
    bc_txn = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return bc_txn


if __name__ == "__main__":
    # my_address = '0x4dE801A18FaA4268eBe916F132CcD760b7C649B9'
    my_address = '0x42A5243D51176bdCED13F40E3C85b7259e84c113'
    print(nft_contract.functions.balanceOf(my_address).call())
    uri = "https://gateway.pinata.cloud/ipfs/Qmc7yWr8Q8j3fWJMK6zcwUEYPUcigeTDbBca857xD7Sg5Q"  # JSON
    return_hash = mint_nft(my_address, uri)