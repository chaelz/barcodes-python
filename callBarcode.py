"""
Python - Barcode Scanner - Import Barcodes
Handles the importing of the barcode data into multiple apps.

Written by Charlie Hall
charlie@chaelz.com
"""


import sys
import pushDiscord
import appendCSV
import GSheets
import datetime
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
s_id = os.environ.get("SPREADSHEET_ID")

# Barcode data
try:
    barcode = sys.argv[1]
except IndexError:
    print("You have not supplied enough arguments. Exiting")
    sys.exit()


now = datetime.datetime.now()
currentTime = now.strftime("%d/%m/%Y %H:%M:%S")
computerName = os.environ['COMPUTERNAME']

pushDiscord.discordMessage(sys.argv[1], currentTime, computerName)
appendCSV.writeToCSV(sys.argv[1], currentTime, computerName)
GSheets.pushBarcode(sys.argv[1], currentTime, computerName)
