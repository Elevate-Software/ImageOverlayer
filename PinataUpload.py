# Description
# -------------
# Uploads an image to Pinata (IPFS)

# Resources
# -------------
# https://docs.pinata.cloud/api-pinning/pinning-services-api

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

    :return:
    """

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


def construct_metadata(filename, hash):
    name = filename.split('_')[0].split('/')[1]
    link = 'https://gateway.pinata.cloud/ipfs/' + hash
    desc = f"This certifies that {name} has met the requirements for their exceptional performance in the " \
           "Fundamentals of Decentralised Finance / Digital Asset Portfolio Management curriculum."

    formatted_obj = {
        'name': name,
        'image_url': link,
        'description': desc
    }

    return formatted_obj


if __name__ == "__main__":
    pin_all_to_IPFS()
