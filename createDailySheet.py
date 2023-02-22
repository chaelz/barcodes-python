import GSheets
import datetime
import os
import requests
from dotenv import load_dotenv, find_dotenv

# Sets the date
now = datetime.datetime.now()
currentDate = now.strftime("%A_%m-%d-%Y")
weekYear = now.strftime("%W-%Y")

# Creates the daily sheet
otherID = GSheets.createSheet(f"{currentDate}")

load_dotenv(find_dotenv())
discordUrl = os.environ["DISCORD_URL"]
sheetID = os.environ["SPREADSHEET_ID"]

sheetURL = f"https://docs.google.com/spreadsheets/d/{sheetID}/edit#gid={otherID}"
message_data = f"Dog_Log_Week-{weekYear}"
message = f"{message_data}\n \
    URL: {sheetURL}"

embed = {
    "description": message,
    "title": "Daily sheet created",
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
