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
        E.g. 4/1/11 11:00:00 AM
        Returns: string
        """
        pacific_time = self.timestamp + ' PST'
        time = datetime.strptime(pacific_time, '%m/%d/%y %I:%M:%S %p %Z')
        eastern_time = self.convert_to_eastern(time)
        return eastern_time.isoformat()

    def pad_zip_code(self):
        """Left-pad a zip code with zeroes
        E.g. 21 returns 00021
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
        Returns: datetime object
        """
        offset = timedelta(hours=3)
        return time + offset

    def create_timedelta(self, duration):
        """Take an hour:minute:second string and return a timedelta object
        Args: duration, a string in hour:minute:second.millisecond format, e.g.
            31:23:32.123
        Returns: timedelta object
        """
        delta = [float(time) for time in duration.split(':')]
        return timedelta(hours=delta[0], minutes=delta[1], seconds=delta[2])

    def calc_total_duration(self):
        """Given two timedelta objects, calculate a total
        Returns: a timedelta object
        """
        foo_delta = self.create_timedelta(self.foo_duration)
        bar_delta = self.create_timedelta(self.bar_duration)

        return foo_delta + bar_delta

    def create_DTO(self):
        """Create a data transfer object for the write function
        Returns: list of strings
        """
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

def pop_header(reader):
    """Read the first row of a CSV file, i.e. the headers
    Args: reader, a CSV reader object
    Returns: a list of strings
    """
    for row in reader:
        headers = row
        break
    return headers

def create_row_objects(reader):
    """Create a list of Row objects
    Reads in the lines of a CSV file and creates a list of Row objects
    Args: reader, a CSV reader object
    Returns: a list of objects
    """
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

def write_rows(headers, rows):
    """Write the normalized verison of each string object to a new CSV file
    Args: headers, a list of strings
          rows, a list of row objects
    """
    with open('normalized.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, 
                            delimiter=',', 
                            quotechar='"', 
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row.create_DTO())

reader = csv.reader(sys.stdin)
headers = pop_header(reader)
all_rows = create_row_objects(reader)
write_rows(headers, all_rows)
