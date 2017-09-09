#!/usr/bin/env python3

import csv
import sys

print('running')

reader = csv.reader(sys.stdin)

for row in reader:
    print(row)
    break