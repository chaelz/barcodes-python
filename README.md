# Barcode Scanner

Developed by Charlie for Pup Scouts Boarding and Daycamp.
Primarily functions to take a string and dump it in a few places - Discord, Google Sheets, and appends it to a CSV file for backup.

There are multiple functions of these items. General concept is that the primary script are the function scripts: -

1. GSheets.py - Google Sheets updates
   - Call: GSheets.pushBarcode(data, time and date, device)
2. pushDiscord.py - Discord Messages
   - Call: pushDiscord.discordMessage(data, time and date, device)
3. appendCSV.py - CSV log
   - Call: appendCSV.writeToCSV(data, time and date, device)

## callBarcode.py:

| Input                    | Output                                                                                       |
| ------------------------ | -------------------------------------------------------------------------------------------- |
| Barcode or scanned text. | The data being scanned, the number of cells updated, Discord webhook results, and any errors |

Functionality:

1. Sets up variables and pulls spreadsheet ID for Google Sheets from .env file.
2. Confirms parameters are present.
3. Sets time and date variable
4. Pushes a discord message of the passed argument, time and date, device, and google sheets URL using pushDiscord.py
5. Appends CSV with the passed argument, time and date, device using appendCSV.py
6. Pushes barcode info to Google Sheets with the passed argument, time and date, device.

## createDailySheet.py

| Input | Output               |
| ----- | -------------------- |
| None  | Location set message |

Functionality:

1. Calls GSheets.py to create sheet using the current date.
2. Date is formatted to standard to match weekly sheet.

## createWeeklyBook.py

| Input | Output                                        |
| ----- | --------------------------------------------- |
| None  | Spreadsheet ID, URL, and sharing permissions. |

Functionality:

1. Calls GSheets.py to create a weekly book using the current week, and current date to rename the default sheet.
2. Calls GSheets.py to share the sheet out.

Currently this repo is written around a Windows environment. Can be rewritten for Linux pretty easily.
