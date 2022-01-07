import numpy as np
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from io import BytesIO
import json
from config import *
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import ftplib

try:
    current_time = time.time()
    current_time_st = datetime.now().strftime("%Y-%m-%dT%H:%M")
    end_time_st = (datetime.now() + timedelta(hours=11.95)).strftime("%Y-%m-%dT%H:%M")

    schedule = requests.get('https://airlabs.co/api/v9/schedules?dep_iata=PVD&api_key=' + AIRLABS_API_KEY).json()
    first_data = schedule['response']
except Exception as e:
    url = 'https://www.pushsafer.com/api'
    post_fields = {
    	"t" : 'Airlabs Pull Fail',
    	"m" : str(e),
    	"i" : 2,
        "c" : '#FF0000',
    	"d" : 'a',
    	"u" : 'https://www.pushsafer.com',
    	"ut" : 'Open Pushsafer',
    	"k" : PUSH_KEY,
    	}

    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()


with open("/home/pi/scripts/first_data.json", "w") as outfile:
    json.dump(first_data,outfile)

ftp_server = ftplib.FTP(HOST_NAME,FTP_USER,FTP_PASS)
filename = "/public_html/resources/first_data_ver.json"

with open("/home/pi/scripts/first_data.json", "rb") as upfile:
    ftp_server.storbinary(f"STOR {filename}", upfile)
