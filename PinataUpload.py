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

psa_endpoint = 'https://api.pinata.cloud'  # pinning services API endpoint

# read the JSON web token (bearer token) from json file
with open("JWT.json", 'r') as file:
    file_data = json.load(file)
    jwt = file_data['jwt']


def pin_all_to_IPFS():
    """
    Pins all files in /output directory to IPFS via Pinata API

    :return: a list of the URIs we created with names as a key so we know who's is who's
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


def construct_metadata(filename, hash):
    name = filename.split('_')[0].split('/')[1]
    link = 'https://gateway.pinata.cloud/ipfs/' + hash
    desc = f"This certifies that {name} has met the requirements for their exceptional performance in the " \
           "Fundamentals of Decentralised Finance / Digital Asset Portfolio Management curriculum."

    formatted_obj = {
        'name': name,
        'description': desc,
        'image_url': link
    }

    return formatted_obj


def construct_output_tuple(filename, hash):
    name = filename.split('_')[0].split('/')[1]
    uri = 'https://gateway.pinata.cloud/ipfs/' + hash
    return name, uri


if __name__ == "__main__":
    pin_all_to_IPFS()
