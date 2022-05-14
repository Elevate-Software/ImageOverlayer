import ImageGen
import PinataUpload
import BuildTransaction

#   UNDER CONSTRUCTION!!!

# TODO: read CSV here
users = []

# TODO: call ImageGen.generate() for every name in list
# ex:
for name, _ in users:
    ImageGen.generate(name)

# TODO: upload all files to IPFS
uris = PinataUpload.pin_all_to_IPFS()   # note, the return is a TUPLE containing uris AND names

# TODO: create a new list of tuples of format: (address, uri)
new_list = []
for item in new_list:
    BuildTransaction.mint_nft(*item)

