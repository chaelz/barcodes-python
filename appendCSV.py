import os
import csv

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

csvDir = os.environ.get("CSV_DIR")


def writeToCSV(csvBarcodeInfo, csvDateTime, csvDeviceName):
    header = ['Barcode', 'Date Time', 'Device Name']
    data = [csvBarcodeInfo, csvDateTime, csvDeviceName]
    csvPath = csvDir+"_All.csv"
    isExist = os.path.exists(csvDir)

    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(csvDir)
        print("The new directory is created!")

    csvExists = os.path.exists(csvPath)

    # open the file in the write mode
    with open(csvPath, 'a', newline='') as outFile:
        csvWriter = csv.writer(outFile)
        if not csvExists:
            csvWriter.writerow(header)
        csvWriter.writerow(data)

    print(csvBarcodeInfo, csvDateTime, csvDeviceName)
