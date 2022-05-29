import ImageGen
import PinataUpload
import BuildTransaction
import csv


# Read CSV values into list
with open("graduates.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    users = sorted([row for row in csv_reader])

# create diploma images for every name in list
for name, _ in users:
    ImageGen.generate(name)

# upload all files to IPFS
pinned_uris = PinataUpload.pin_all_to_IPFS()   # returns list of (name, uri) tuples
pinned_uris.sort()

# create a new list of tuples of format: (address, uri)
new_list = [(users[i][1], pinned_uris[i][1]) for i, _ in enumerate(users)]

# build transactions for all
for i, item in enumerate(new_list):
    return_txn = BuildTransaction.mint_nft(*item)
    print(users[i][0], return_txn)  # name, txn hash

