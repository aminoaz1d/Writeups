#! /usr/bin/env python

import csv
from hashlib import sha256

with open('token_overview.csv', 'r') as ftoken:
    tokenreader = csv.reader(ftoken)
    for row in tokenreader:
        hash = sha256("{}\n".format(row[0]).encode()).hexdigest()
        print("{},{}".format(row[0],hash.upper()))

