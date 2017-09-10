#!/usr/bin/env python3

import csv
import sys
from datetime import datetime
from datetime import timedelta

class Row():
    def __init__(self,
                 timestamp, 
                 address, 
                 zip_code, 
                 full_name, 
                 foo_duration, 
                 bar_duration, 
                 notes=None):
        self.timestamp = timestamp
        self.address = address
        self.zip_code = zip_code
        self.full_name = full_name.upper()
        self.foo_duration = foo_duration
        self.bar_duration = bar_duration
        self.total_duration = None
        self.notes = notes

    def utf_timestamp(self):
        pacific_time = self.timestamp + ' PST'
        time = datetime.strptime(pacific_time, '%m/%d/%y %I:%M:%S %p %Z')
        eastern_time = self.convert_to_eastern(time)
        return eastern_time.isoformat()

    def pad_zip_code(self):
        padded_zip = self.zip_code
        if len(padded_zip) < 5:
            padding = 5 - len(padded_zip)
            padded_zip = ('0'*padding) + padded_zip
        return padded_zip

    def convert_to_eastern(self, time):
        offset = timedelta(hours=3)
        return time + offset

def remove_header(reader):
    for row in reader:
        headers = row
        break
    return headers

def create_row_objects(reader):
    remove_header(reader)
    all_rows = []

    for row in reader:
        new_row = Row(row[0],
                      row[1],
                      row[2],
                      row[3],
                      row[4],
                      row[5],
                      row[7])
        new_row.utf_timestamp()
        all_rows.append(new_row)
    return all_rows


reader = csv.reader(sys.stdin)
for row in create_row_objects(reader):
    print(row.address)