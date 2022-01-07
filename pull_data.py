import numpy as np
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from dateutil import parser
from io import BytesIO
import json
from config import *
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import ftplib
import calendar

try:
    current_time = time.time()
    current_time_st = datetime.now().strftime("%Y-%m-%dT%H:%M")
    end_time_st = (datetime.now() + timedelta(hours=11.95)).strftime("%Y-%m-%dT%H:%M")

    # schedule = requests.get('https://airlabs.co/api/v9/schedules?dep_iata=PVD&api_key=' + AIRLABS_API_KEY).json()
    # first_data = schedule['response']

    pvd_data = pd.read_html('https://webservice.prodigiq.com/wfids/PVD/full?page=1&type=departures&rows=100')[1]

    pvd_data.head()

    pvd_data['airline_iata'] = pvd_data.apply(lambda row : row['Flight No.'].split(' ')[0], axis=1)
    pvd_data['flight_iata'] = pvd_data.apply(lambda row : row['Flight No.'].split(' ')[0] + row['Flight No.'].split(' ')[1], axis=1)
    pvd_data['arr_iata'] = pvd_data.apply(lambda row : row['Destination'].split(')')[0][1:], axis=1)
    pvd_data['datetime'] = pvd_data.apply(lambda row : parser.parse(row['Date'] + ' ' + row['Time']).strftime("%Y-%m-%dT%H:%M"), axis=1)
    pvd_data['dep_gate'] = pvd_data['Gate']
    pvd_data['status'] = pvd_data['Status']

    pvd_data[['airline_iata','flight_iata', 'arr_iata', 'datetime', 'dep_gate', 'status']].to_json(path_or_buf = '/home/pi/scripts/first_data.json',orient = 'index')
except Exception as e:
    url = 'https://www.pushsafer.com/api'
    post_fields = {
    	"t" : 'PVD Data Pull Fail',
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

ftp_server = ftplib.FTP(HOST_NAME,FTP_USER,FTP_PASS)
filename = "/public_html/resources/first_data_ver.json"

with open("/home/pi/scripts/first_data.json", "rb") as upfile:
    ftp_server.storbinary(f"STOR {filename}", upfile)
