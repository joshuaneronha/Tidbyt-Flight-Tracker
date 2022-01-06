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

try:
    current_time = time.time()
    current_time_st = datetime.now().strftime("%Y-%m-%dT%H:%M")
    end_time_st = (datetime.now() + timedelta(hours=11.95)).strftime("%Y-%m-%dT%H:%M")

    schedule = requests.get('https://airlabs.co/api/v9/schedules?dep_iata=PVD&api_key=' + AIRLABS_API_KEY).json()
    first_data = schedule['response']
except:
    url = 'https://www.pushsafer.com/api'
    post_fields = {
    	"t" : 'Critical API Failure',
    	"m" : 'AirLabs Pull',
    	"i" : 2,
        "c" : '#FF0000',
    	"d" : 'a',
    	"u" : 'https://www.pushsafer.com',
    	"ut" : 'Open Pushsafer',
    	"k" : PUSH_KEY,
    	}

    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()

try:
    url = "https://aerodatabox.p.rapidapi.com/flights/airports/icao/KPVD/" + current_time_st + "/" + end_time_st

    querystring = {"withLeg":"false","direction":"Departure","withCancelled":"false","withCodeshared":"false","withCargo":"false","withPrivate":"false","withLocation":"false"}

    headers = {
        'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
        }

    second_data = requests.request("GET", url, headers=headers, params=querystring).json()
except:
    url = 'https://www.pushsafer.com/api'
    post_fields = {
    	"t" : 'Critical API Failure',
    	"m" : 'RapidAPI Pull',
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

with open("/home/pi/scripts/second_data.json", "w") as outfile:
    json.dump(second_data,outfile)
