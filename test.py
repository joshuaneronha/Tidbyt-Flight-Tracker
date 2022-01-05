import numpy as np
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
import base64
from io import BytesIO
import json
import ftplib
from config import *

import matplotlib.pyplot as plt

lat_top = 47.34
lat_bottom = 23.95
lon_left = -93.16
lon_right = -68.66

lat_space = np.linspace(lat_top, lat_bottom, 32)
lon_space = np.linspace(lon_left, lon_right, 28)

current_time = time.time()
current_time_st = datetime.now().strftime("%Y-%m-%dT%H:%M")
end_time_st = (datetime.now() + timedelta(hours=11.95)).strftime("%Y-%m-%dT%H:%M")

schedule = requests.get('https://airlabs.co/api/v9/schedules?dep_iata=PVD&api_key=' + AIRLABS_API_KEY).json()
flights = schedule['response']

coords = pd.read_csv('airport-codes_csv.csv',usecols=['iata_code', 'coordinates'])

known_airlines = ['WN','B6','AA','DL','UA','MX','F9','G4']

def generate_image(base_map, origin, dest):
    im = Image.open(base_map)
    draw = ImageDraw.Draw(im)

    origin_x_point = np.abs(np.array([x - origin[0] for x in lat_space])).argmin() + 1
    origin_y_point = np.abs(np.array([x - origin[1] for x in lon_space])).argmin() + 1
    dest_x_point = np.abs(np.array([x - dest[0] for x in lat_space])).argmin() + 1
    dest_y_point = np.abs(np.array([x - dest[1] for x in lon_space])).argmin() + 1

    draw.line((origin_y_point,origin_x_point, dest_y_point,dest_x_point),width=1,fill='orange')

    return im

def get_coords(airport):
    extracted = coords[coords['iata_code'] == airport]['coordinates'].iloc[0].split(', ')
    extracted.reverse()
    return tuple([float(x) for x in extracted])

for next_flight in flights:
    if float(next_flight['dep_time_ts']) > current_time:
        if (next_flight['airline_iata'] in known_airlines) & (next_flight['status'] != 'cancelled'):
            break

airline, flight_iata, dest, dep_time = next_flight['airline_iata'], next_flight['flight_iata'], next_flight['arr_iata'], next_flight['dep_time']

flight_iata_f = flight_iata[0:2] + ' ' + flight_iata[2:]

### new source

aircraft_model

flights

url = "https://aerodatabox.p.rapidapi.com/flights/airports/icao/KPVD/" + current_time_st + "/" + end_time_st

querystring = {"withLeg":"false","direction":"Departure","withCancelled":"false","withCodeshared":"false","withCargo":"false","withPrivate":"false","withLocation":"false"}

headers = {
    'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
    'x-rapidapi-key': RAPIDAPI_KEY
    }

second_data = requests.request("GET", url, headers=headers, params=querystring).json()

flight_iata_f

second_data['departures']

aircraft_model = ''

for i in second_data['departures']:
    if i['number'] == flight_iata_f:
        aircraft_model = i['aircraft']['model']
        if 'Canadair' in aircraft_model:
            aircraft_model = 'CRJ' + aircraft_model[-3:]
        if 'Boeing' in aircraft_model:
            aircraft_model = aircraft_model.split('Boeing ')[1][:-2]
        if 'Airbus' in aircraft_model:
            aircraft_model = aircraft_model.split('Airbus ')[1]
        if 'Embraer' in aircraft_model:
            aircraft_model = 'E' + aircraft_model.split('Embraer ')

next_flight['aircraft'] = aircraft_model



next_flight['short_time'] = next_flight['dep_time'][-5:]

out = generate_image('cropmap.png',get_coords('PVD'),get_coords(next_flight['arr_iata']))
buffered = BytesIO()
out.save(buffered, format="PNG")
buffered.seek(0)
img_str = base64.b64encode(buffered.getvalue()).decode()

next_flight

next_flight['map'] = img_str
next_flight['marquee'] = next_flight['short_time'] + '     ' + next_flight['aircraft'] + '     Gate' + next_flight['dep_gate']

next_flight

with open("next_flight.json", "w") as outfile:
    json.dump(next_flight,outfile)

ftp_server = ftplib.FTP(HOST_NAME,FTP_USER,FTP_PASS)
filename = "/public_html/resources/next_flight.json"

with open("next_flight.json", "rb") as upfile:
    ftp_server.storbinary(f"STOR {filename}", upfile)
