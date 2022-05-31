# Description
# -------------
# Uploads an image to Pinata, then a metadata JSON with link to that image (IPFS)

# Resources
# -------------
# Pin File: https://docs.pinata.cloud/api-pinning/pin-file
# Pin JSON: https://docs.pinata.cloud/api-pinning/pin-json

import requests
import json
import os

psa_endpoint = 'https://api.pinata.cloud'  # pinata base URL

# TODO: change this to be an environment variable?
# read the JSON web token (bearer token) from json file
with open("JWT.json", 'r') as file:
    file_data = json.load(file)
    jwt = file_data['jwt']


def pin_all_to_IPFS():
    """
    Pins all files in /output directory to IPFS via Pinata API.

    :return: a list of the URIs created with names as a key so we know whose is whose.
    """
    list_of_uris = []

    filenames = ['output/' + fn for fn in os.listdir(os.getcwd() + '/output')]

    url = psa_endpoint + '/pinning/pinFileToIPFS'
    json_url = psa_endpoint + '/pinning/pinJSONToIPFS'
    headers = {'Authorization': 'Bearer ' + jwt}

    for f in filenames:

        # upload image to IPFS via Pinata API call
        files = {'file': open(f, "rb")}
        r = requests.post(url, headers=headers, files=files)

        # upload JSON metadata to IPFS via Pinata API call
        json_metadata = construct_metadata(f, r.json()['IpfsHash'])
        r = requests.post(json_url, headers=headers, json=json_metadata)

        # append link to a list to be returned
        list_of_uris.append(construct_output_tuple(f, r.json()['IpfsHash']))

    return list_of_uris


def process_name(filename):
    """
    Turns the provided filename back into the user's name.

    :param filename: the filename, format: 'output/First Last_diploma.png'
    :return: the user's name: ex.'First Last'
    """
    return filename.split('_')[0].split('/')[1]


def construct_metadata(filename, ipfs_hash):
    """
    Constructs the JSON metadata to be uploaded to IPFS and used as the NFT JSON link.

    :param filename: The image file path (gets converted back to person's First Last name).
    :param ipfs_hash: IPFS has returned by Pinata API call (used to create link to hosted image file).
    :return: formatted dictionary that will be passed as the JSON for uploading to IPFS.
    """
    name = process_name(filename)
    link = 'https://gateway.pinata.cloud/ipfs/' + ipfs_hash
    desc = f"This certifies that {name} has met the requirements for their exceptional performance in the " \
           "Fundamentals of Decentralised Finance / Digital Asset Portfolio Management curriculum."

    formatted_obj = {
        'name': name,
        'description': desc,
        'image_url': link
    }

    return formatted_obj


def construct_output_tuple(filename, ipfs_hash):
    """
    Creates the tuple needed for minting the NFT to the correct person.

    :param filename: Image file path (converted to the person's First Last name).
    :param ipfs_hash: Hash returned by Pinata representing the pinned JSON object (converted to URI of object).
    :return: Tuple of format (name, uri).
    """
    name = process_name(filename)
    uri = 'https://gateway.pinata.cloud/ipfs/' + ipfs_hash
    return name, uri


# tests pinning all files
if __name__ == "__main__":
    pin_all_to_IPFS()
