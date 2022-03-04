"""
Download file from https://efile.fara.gov/ords/f?p=API:BULKDATA:0:
"""

import urllib.request
url = "https://efile.fara.gov/bulk/zip/FARA_All_Registrants.csv.zip?1618564234626.0645"
filename = "all_registrants.csv.zip"
urllib.request.urlretrieve(url, filename)

if __name__ == "__main__":
    pass

