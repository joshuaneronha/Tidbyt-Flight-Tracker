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
    url = "https://aerodatabox.p.rapidapi.com/flights/airports/icao/KPVD/" + current_time_st + "/" + end_time_st

    querystring = {"withLeg":"false","direction":"Departure","withCancelled":"false","withCodeshared":"false","withCargo":"false","withPrivate":"false","withLocation":"false"}

    headers = {
        'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
        }

    second_data = requests.request("GET", url, headers=headers, params=querystring).json()
except Exception as e:
    url = 'https://www.pushsafer.com/api'
    post_fields = {
    	"t" : 'Model Pull Failure',
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

with open("/home/pi/scripts/second_data.json", "w") as outfile:
    json.dump(second_data,outfile)

ftp_server = ftplib.FTP(HOST_NAME,FTP_USER,FTP_PASS)
filename = "/public_html/resources/second_data_ver.json"

with open("/home/pi/scripts/second_data.json", "rb") as upfile:
    ftp_server.storbinary(f"STOR {filename}", upfile)
