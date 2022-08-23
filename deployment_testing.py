import csv
from web3 import Web3

# # Read CSV values into list
# with open("graduates.csv") as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     users = sorted([row for row in csv_reader])  # sorts by first value in sub-list
#
# print(sorted(users))
#
# with open("graduates.csv", "w", newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerows(users)

import os

dir = os.getcwd() + r'\output'

for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
