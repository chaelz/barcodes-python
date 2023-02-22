from __future__ import print_function

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys
import os
import datetime
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def connectSheetsSA():
    # Connection Variables
    secret_file = 'serviceaccount_pk.json'
    SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = service_account.Credentials.from_service_account_file(
        secret_file, scopes=SCOPE)
    service = build('sheets', 'v4', credentials=credentials)
    return service


def connectDriveSA():
    # Connection Variables
    secret_file = 'serviceaccount_pk.json'
    SCOPES = [
        "https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file"]
    credentials = service_account.Credentials.from_service_account_file(
        secret_file, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service


def create(title, sheetName):
    service = connectSheetsSA()
    try:
        # Create the spreadsheet.
        spreadsheet = {'properties': {'title': title}}
        spreadsheet = service.spreadsheets().create(
            body=spreadsheet, fields='spreadsheetId').execute()

        s_id = spreadsheet.get('spreadsheetId')

        # Adding header rows
        # Data Set
        values = [["Barcode", "Check In Time", "CI Device Name",
                   "Check Out Time", "CO Device Name"]]
        data = [{
                'range': "A1",
                'values': values
                }]
        body = {
            'valueInputOption': 'RAW',
            'data': data
        }

        # Update function
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=s_id, body=body).execute()

        # Spit out the URL
        print(
            f"Created spreadsheet ID: {s_id}. Adding to environmental variables.")
        s_url = f"https://docs.google.com/spreadsheets/d/{s_id}/edit#gid=0"
        print(f"Spreadsheet URL: {s_url}")

        sheetid = getSheetID(s_id, sheetName)

        # Updates Sheet1 to current date.
        # Let's define the new name for the sheet
        new_sheet_name = sheetName

        # Let's create a request to update the sheet's properties
        request = {"updateSheetProperties": {"properties": {
            "sheetId": sheetid, "title": new_sheet_name}, "fields": "title"}}

        # Let's execute the request
        response = service.spreadsheets().batchUpdate(spreadsheetId=s_id,
                                                      body={"requests": [request]}).execute()

        # Set Environmental Variable for WorkBook
        file_name = ".env"
        env = open(file_name, "r").readlines()
        append = True  # True and set false if update is necessary
        for line in env:
            if 'SPREADSHEET_ID' in line:
                env[env.index(line)] = f"SPREADSHEET_ID={s_id}\n"
                out = open(file_name, 'w')
                out.writelines(env)
                out.close()
                append = False

        if (append == True):
            with open('.env', 'a') as f:
                f.write(f"\nSPREADSHEET_ID={s_id}\n")

        # Sets Environmental Variable for Sheet ID
        file_name = ".env"
        env = open(file_name, "r").readlines()
        append = True  # True and set false if update is necessary
        for line in env:
            if 'GSHEET_ID' in line:
                env[env.index(line)] = f"GSHEET_ID={sheetid}\n"
                out = open(file_name, 'w')
                out.writelines(env)
                out.close()
                append = False

        if (append == True):
            with open('.env', 'a') as f:
                f.write(f"\nGSHEET_ID={sheetid}\n")

        return s_id
    # Exception in case there is an HTTP error
    except HttpError as error:
        print(
            f"An error occurred: {error}.")
        return error


def getSheetID(SPREADSHEET_ID, sheetName):
    service = connectSheetsSA()
    spreadsheet = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID).execute()
    sheet_id = None
    # Loops over existing sheets and searches for one with a matching name
    for _sheet in spreadsheet['sheets']:
        if _sheet['properties']['title'] == sheetName:
            sheet_id = _sheet['properties']['sheetId']
    return sheet_id


def createSheet(sheetName):
    service = connectSheetsSA()

    s_id = os.environ.get("SPREADSHEET_ID")
    now = datetime.datetime.now()
    currentDate = now.strftime("%A_%m-%d-%Y")

    requests = {
        "addSheet": {
            "properties": {
                "title": sheetName,
            }
        }
    }
    body = {
        'requests': requests
    }

    service.spreadsheets().batchUpdate(spreadsheetId=s_id, body=body).execute()
    sheetid = getSheetID(s_id, sheetName)

    # Adds Headers
    list = [["Barcode"], ["Check In Time"], ["CI Device Name"],
            ["Check Out Time"], ["CO Device Name"]]
    resource = {
        "majorDimension": "COLUMNS",
        "values": list
    }
    range = f"{currentDate}!A1:F1"
    service.spreadsheets().values().update(
        spreadsheetId=s_id, body=resource, range=range, valueInputOption="RAW").execute()

    # Sets Environmental Variable for Sheet ID
    file_name = ".env"
    env = open(file_name, "r").readlines()
    append = True  # True and set false if update is necessary
    for line in env:
        if 'GSHEET_ID' in line:
            env[env.index(line)] = f"GSHEET_ID={sheetid}\n"
            out = open(file_name, 'w')
            out.writelines(env)
            out.close()
            append = False

    if (append == True):
        with open('.env', 'a') as f:
            f.write(f"\nGSHEET_ID={sheetid}\n")

    return sheetid


def shareSheet(s_id):
    drive = connectDriveSA()
    emailAddresses = json.loads(os.environ["SHARE_ADDRESSES"])

    file_id = s_id
    for domain in emailAddresses:
        permission = {
            "type": "domain",
            "role": "writer",
            "domain": f"{domain}",
        }
        req = drive.permissions().create(fileId=file_id, body=permission).execute()
        print(req)


def getFileID(name):
    drive = connectDriveSA()

    results = drive.files().list(
        q=f"name='{name}'", fields="nextPageToken, files(id, name)").execute()
    files = results.get('files', [])
    for file in files:
        print(f"{file['name']} ({file['id']})")

    '''for file in files:
        file_id = file["id"]
        drive.files().delete(fileId=file_id).execute()'''
    return file['id']


def pushBarcode(barcodeData, deviceName, date_time):
    service = connectSheetsSA()
    s_id = os.environ.get("SPREADSHEET_ID")
    now = datetime.datetime.now()
    currentDate = now.strftime("%A_%m-%d-%Y")
    sheet_id = os.environ.get("GSHEET_ID")
    range_ = f"{currentDate}!A:F"

    # Read the data in the sheet
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=s_id, range=range_
        ).execute()
        values = result.get("values", [])
    except HttpError as error:
        print(f"An error occurred: {error}")
        values = []

    # Let's check if the string exists in column A
    column_A_values = [row[0] for row in values]

    if barcodeData in column_A_values:
        # If it does, let's find the row it's in and append the data to columns D to F
        row_index = column_A_values.index(barcodeData)
        range_to_update = f"{currentDate}!D{row_index + 1}:E{row_index + 1}"
        data = [{"range": range_to_update, "values": [
            [deviceName, date_time]]}]
    else:
        # If it doesn't, let's append the string and data to the next empty row in columns D to F
        range_to_update = f"{currentDate}!A{len(values) + 1}:C{len(values) + 1}"
        data = [{"range": range_to_update, "values": [
            [barcodeData, deviceName, date_time]]}]

    # Let's update the sheet with the new data
    body = {"valueInputOption": "USER_ENTERED", "data": data}
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=s_id, body=body
    ).execute()

    print(f"{result.get('totalUpdatedCells')} cells updated.")


def listFiles():
    service = connectDriveSA()

    # Call the Drive API's files().list() method to get a list of all files
    response = service.files().list().execute()
    files = response.get('files', [])

    # Print the ID and name of each file
    for file in files:
        print(f"File ID: {file['id']}, Name: {file['name']}")


def bigRedDeleteButton():
    service = connectDriveSA()
    # Call the Drive API's files().list() method to get a list of all files
    response = service.files().list().execute()
    files = response.get('files', [])

    # Iterate over the list of files and delete each one
    for file in files:
        try:
            # Execute the request to delete the file
            service.files().delete(fileId=file['id']).execute()
            print(f"Deleted file with ID {file['id']} and name {file['name']}")
        except HttpError as error:
            print(
                f"An error occurred while deleting file with ID {file['id']}: {error}")


if __name__ == 'connectSheetsSA':
    connectSheetsSA()

if __name__ == 'create':
    create(sys.argv[1], sys.argv[2])
