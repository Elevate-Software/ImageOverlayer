import ImageGen
import PinataUpload
from BuildTransaction import MintFactory
import csv
import os


# delete files in image folder before running to avoid any issues
filenames = ['output/' + fn for fn in os.listdir(os.getcwd() + '/output')]
for file in filenames:
    os.remove(file)

# Read CSV values into list
with open("graduates.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    users = sorted([row for row in csv_reader])  # sorts by first value in sub-list

# create diploma images for every name in list (discarding secondary value 'addr' with '_' char)
for name, _ in users:
    ImageGen.generate(name)

# upload all files to IPFS
pinned_uris = PinataUpload.pin_all_to_IPFS()    # returns list of (name, uri) tuples
pinned_uris.sort()                              # sort by first value in tuple

# create a new list of tuples of format: (address, uri)
new_list = [(users[i][1], pinned_uris[i][1]) for i, _ in enumerate(users)]

# create the MintFactory object
contract_address = '0x96807aD777850A9336B9aD9F9Bb625CaD4eC0e5a'
owner_address = '0x42A5243D51176bdCED13F40E3C85b7259e84c113'
mint_factory = MintFactory(contract_address, owner_address, network='ropsten')

# build transactions for all
for i, item in enumerate(new_list):
    return_txn = mint_factory.mint_nft(*item)
    print(users[i][0], return_txn.hex())     # name, txn hash
