#!/usr/bin/python
# Import Web Browser
import mechanize

# Import HTML Parser
from bs4 import BeautifulSoup

# For Downloading PDFs
import urllib2

# For Printing PDFs
import _winreg as winreg
import time, os, subprocess

print '''
                _        _____  _____  ______ _____      _       _
     /\        | |      |  __ \|  __ \|  ____|  __ \    (_)     | |
    /  \  _   _| |_ ___ | |__) | |  | | |__  | |__) | __ _ _ __ | |_ ___ _ __
   / /\ \| | | | __/ _ \|  ___/| |  | |  __| |  ___/ '__| | '_ \| __/ _ \ '__|
  / ____ \ |_| | || (_) | |    | |__| | |    | |   | |  | | | | | ||  __/ |
 /_/    \_\__,_|\__\___/|_|    |_____/|_|    |_|   |_|  |_|_| |_|\__\___|_|


AutoPDFPrinter  Copyright (C) 2016  Reilly Chase
This program comes with ABSOLUTELY NO WARRANTY; for details see 'LICENSE'.
This is free software, and you are welcome to redistribute it
under certain conditions; see 'LICENSE' included for details.

'''

# Dynamically get path to AcroRD32.exe
AcroRD32Path = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT,'Software\\Adobe\\Acrobat\Exe')
acroread = AcroRD32Path

# Download PDF Function
def download_file(download_url, pdf_name):
    response = urllib2.urlopen(download_url)
    file = open(pdf_name, 'wb')
    file.write(response.read())
    file.close()
    print("Downloaded PDF: " + pdf_name)

############################
# Setup Mechanize Defaults #
############################
br = mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

http_link = raw_input("Enter link to site: ")

attempts = 0
while attempts < 5:
    try:
        # User-Agent
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko')]
        r = br.open(http_link)
        page = r.read()
        soup = BeautifulSoup(page)
        anchor_links = soup.find_all("a", href=True)
        break

    except:
        print "ERROR: Connection failed to " + http_link
        attempts = attempts + 1

for link in anchor_links:
    if '.pdf' in link.get('href'):
        pdf_link = link.get('href')
        pdf_name = link.text

        # Download the PDF
        download_file(pdf_link, pdf_name)

        # The last set of double quotes leaves the printer blank, using the default printer
        cmd= '{0} /N /T "{1}" ""'.format(acroread, pdf_name)

        # See what the command line will look like before execution
        print(cmd)

        # Open command line in a different process
        proc = subprocess.Popen(cmd)

        # Wait for PDF to be sent to printer
        time.sleep(1)

        # Delete the PDF from file system after printing.
        os.remove(pdf_name)


# After all PDFs have printed, wait 1 second then kill Adobe Reader
time.sleep(1)

# Kill AcroRD32.exe from Task Manager
os.system("TASKKILL /F /IM AcroRD32.exe")
