@ECHO off
:START
set /p "BARCODE=Scan barcode: "
python "callBarcode.py" "%BARCODE%"
GOTO START