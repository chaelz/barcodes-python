import GSheets
from dotenv import load_dotenv, find_dotenv
import datetime
import os
import requests

# Sets the date
now = datetime.datetime.now()
currentDate = now.strftime("%A_%m-%d-%Y")
weekYear = now.strftime("%W-%Y")

# OS - Get current dir and set dir.
cwd = os.getcwd()
print(f"Current dir: {cwd}.")
os.chdir('C:\\py-barcodes')
print("Set dir to py-barcodes.")

# Creates the Google Book
sheetID = GSheets.create(f"Dog_Log_Week-{weekYear}", f"{currentDate}")
GSheets.shareSheet(sheetID)

# Spits out a discord message.
load_dotenv(find_dotenv())
discordUrl = os.environ.get("DISCORD_URL")
s_id = os.environ.get("SPREADSHEET_ID")
sheetURL = f"https://docs.google.com/spreadsheets/d/{s_id}/edit#gid=0"

message_data = f"Dog_Log_Week-{weekYear}"
message = f"{message_data}\n \
    URL: {sheetURL}"
embed = {
    "description": message,
    "title": "Weekly sheet created",
    "color": "11174089"
}

data = {
    "embeds": [
        embed
    ],
}

headers = {
    "Content-Type": "application/json"
}

result = requests.post(discordUrl, json=data, headers=headers)
if 200 <= result.status_code < 300:
    print(f"Discord webhook sent {result.status_code}")
else:
    print(
        f"Discord webhook: Not sent with {result.status_code}, response:\n{result.json()}")
