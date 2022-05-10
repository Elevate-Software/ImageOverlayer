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
    headers = {'Authorization': 'Bearer ' + jwt}

    for f in filenames:
        files = {'file': open(f, "rb")}
        r = requests.post(url, headers=headers, files=files)

        print(r.json())


if __name__ == "__main__":
    pin_all_to_IPFS()
