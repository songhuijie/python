# -*- coding: utf-8 -*-
import csv
import time


def SaveCsv():
    with open("tests.csv", "a", newline="") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        csvwriter.writerow(['当前时间',time.time()])
    return 'true'

if __name__ == '__main__':
    print(SaveCsv())
    exit()