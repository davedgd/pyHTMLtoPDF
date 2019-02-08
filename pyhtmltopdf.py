# Notes:
# pip install pyppeteer

# Usage:
# pyhtmltopdf.py 'path/to/folder' --unzip

import os
import sys
from subprocess import call
import pathlib
import zipfile

import asyncio
from pyppeteer import launch

async def printpdf(fullFilePath, fullOutputPath):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(fullFilePath)
    #await page.screenshot({'path': 'example.png'})
    await page.emulateMedia('screen')
    await page.pdf({'path': fullOutputPath, 'format': 'A4', 'printBackground': 'true', 'margin': {'top': '0cm', 'left': '1cm', 'right': '1cm', 'bottom': '0cm'}})
    await browser.close()

if ("--unzip" in sys.argv):

    print("Unzipping as requested...")

    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if file.endswith(".zip"):
                theZipFile = os.path.join(root, file)
                theZipFile = zipfile.ZipFile(theZipFile, "r")
                theZipFile.extractall(root)
                theZipFile.close()

print("Processing PDFs...")

for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        if file.endswith(".html") or file.endswith(".htm"):

            theFile = os.path.join(root, file)
            theFileURI = pathlib.Path(os.path.abspath(theFile)).as_uri()

            print("Now processing:", theFile)

            outFile = os.path.abspath(os.path.splitext(theFile)[0] + ".pdf")
            asyncio.get_event_loop().run_until_complete(printpdf(theFileURI, outFile))
