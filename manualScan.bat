@ECHO off
:START
set /p "BARCODE=Scan barcode: "
aws s3 cp s3://codedumps/.env C:\py-barcodes\.env > nul 2>&1
python "callBarcode.py" "%BARCODE%"
GOTO START