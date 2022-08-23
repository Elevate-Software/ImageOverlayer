import ImageGen
import PinataUpload
from BuildTransaction import MintFactory
import csv
import os
from web3 import Web3

# DESC: coordinates project files to generate and mint an NFT to each user in graduates.csv.
# DEV: list 'users' and list 'pinned_uris' are both tuples sorted by user name (element 0)
#       so that we can correctly associate user address to IPFS file.

# initialize the mint factory
contract_address = '0x8d284785c5F5C2176e37665eb83354793FB3291B'
owner_address = '0xa93B0654999c1ae1eE4ad3D671E3a234B0420Ff7'
mint_factory = MintFactory(contract_address, owner_address, network='polygon-mainnet')

# delete files in image folder before running to avoid any issues
filenames = ['output/' + fn for fn in os.listdir(os.getcwd() + '/output')]
for file in filenames:
    os.remove(file)

# Read CSV values into list
with open("graduates.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    users = sorted([row for row in csv_reader])  # sorts by first value in sub-list

for u in users:
    if not Web3.isChecksumAddress(u[1]):
        try:
            u[1] = Web3.toChecksumAddress(u[1])
        except ValueError:
            print(f"could not convert {u} to checksum")
            users.remove(u)

print("CSV Loaded...")

# get starting token for generating contract images
next_token = mint_factory.token

# create diploma images for every name in list (discarding secondary value 'addr' with '_' char)
for name, _ in users:
    ImageGen.generate(name, next_token)
    next_token += 1

print("Images generated...")

# upload all files to IPFS
pinned_uris = PinataUpload.pin_all_to_IPFS()    # returns list of (name, uri) tuples
pinned_uris.sort()                              # sort by first value in tuple

print("Metadata pinned to IPFS...")

# create a new list of tuples of format: (address, uri)
new_list = [(users[i][1], pinned_uris[i][1]) for i, _ in enumerate(users)]

# build and call mint transactions for all
for i, item in enumerate(new_list):
    try:
        return_txn = mint_factory.mint_nft(*item)
        print(users[i][0], return_txn.hex())     # name, txn hash
    except:
        print("Error Caused by: ")
        print(item)

print("Minting finished.")

image_dir = os.getcwd() + r'\output'

for f in os.listdir(image_dir):
    os.remove(os.path.join(image_dir, f))

print("Image files removed.")
