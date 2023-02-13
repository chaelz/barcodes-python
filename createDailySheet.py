import GSheets
import datetime
import os

# Sets the date
now = datetime.datetime.now()
currentDate = now.strftime("%A_%m-%d-%Y")
weekYear = now.strftime("%W-%Y")

# OS - Get current dir and set dir.
cwd = os.getcwd()
print(f"Current dir: {cwd}.")
os.chdir('C:\\py-barcodes')
print("Set dir to py-barcodes.")

# Creates the daily sheet
GSheets.createSheet(f"{currentDate}")
