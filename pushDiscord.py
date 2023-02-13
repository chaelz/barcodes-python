from dotenv import load_dotenv, find_dotenv
import requests
import os

load_dotenv(find_dotenv())
discordUrl = os.environ.get("DISCORD_URL")
s_id = os.environ.get("SPREADSHEET_ID")
sheetURL = f"https://docs.google.com/spreadsheets/d/{s_id}/edit#gid=0"


def discordMessage(discordBarcodeInfo, discordDateTime, discordDeviceName):
    message = f"Barcode: {discordBarcodeInfo}\n \
		Time and date: {discordDateTime} \
		\nDevice: {discordDeviceName}\n \
		URL: {sheetURL}"
    embed = {
        "description": message,
        "title": "Barcode has been scanned",
        "color": "12574975"
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
