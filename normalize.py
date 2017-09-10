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

    def iso_timestamp(self):
        """Converts a string to a ISO-8601 timestamp
        returns: string
        """
        pacific_time = self.timestamp + ' PST'
        time = datetime.strptime(pacific_time, '%m/%d/%y %I:%M:%S %p %Z')
        eastern_time = self.convert_to_eastern(time)
        return eastern_time.isoformat()

    def pad_zip_code(self):
        """Left-pad a zip code with zeroes
        Returns: string
        """
        padded_zip = self.zip_code
        if len(padded_zip) < 5:
            padding = 5 - len(padded_zip)
            padded_zip = ('0'*padding) + padded_zip
        return padded_zip

    def convert_to_eastern(self, time):
        """Convert a datetime to US Eastern
        Args: time (datetime) a datetime object in PST
        """
        offset = timedelta(hours=3)
        return time + offset

    def create_timedelta(self, duration):
        """
        """
        delta = [float(time) for time in duration.split(':')]
        return timedelta(hours=delta[0], minutes=delta[1], seconds=delta[2])

    def calc_total_duration(self):
        foo_delta = self.create_timedelta(self.foo_duration)
        bar_delta = self.create_timedelta(self.bar_duration)

        return foo_delta + bar_delta

    def create_DTO(self):
        DTO = []
        DTO.append(self.iso_timestamp())
        DTO.append(self.address)
        DTO.append(self.pad_zip_code())
        DTO.append(self.full_name)
        DTO.append(self.create_timedelta(self.foo_duration).total_seconds())
        DTO.append(self.create_timedelta(self.bar_duration).total_seconds())
        DTO.append(self.calc_total_duration())
        DTO.append(self.notes)
        return DTO

def remove_header(reader):
    for row in reader:
        headers = row
        break
    return headers

def create_row_objects(reader):
    all_rows = []
    for row in reader:
        new_row = Row(row[0],
                      row[1],
                      row[2],
                      row[3],
                      row[4],
                      row[5],
                      row[7])
        new_row.iso_timestamp()
        all_rows.append(new_row)
    return all_rows

reader = csv.reader(sys.stdin)
headers = remove_header(reader)
all_rows = create_row_objects(reader)

with open('normalized.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, 
                        delimiter=',', 
                        quotechar='"', 
                        quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headers)
    for row in all_rows:
        writer.writerow(row.create_DTO())