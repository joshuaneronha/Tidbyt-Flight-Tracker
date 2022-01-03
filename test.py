import numpy as np
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
import base64
from io import BytesIO
import json

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

schedule = requests.get('https://airlabs.co/api/v9/schedules?dep_iata=PVD&api_key=22bcdfcd-9201-4613-ad42-233868976072').json()
flights = schedule['response']

coords = pd.read_csv('airport-codes_csv.csv',usecols=['iata_code', 'coordinates'])

known_airlines = ['WN','B6','AA','DL','UA','MX','F9','G6']

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
        if next_flight['airline_iata'] in known_airlines:
            break

airline, flight_iata, dest, dep_time = next_flight['airline_iata'], next_flight['flight_iata'], next_flight['arr_iata'], next_flight['dep_time']

flight_iata_f = flight_iata[0:2] + ' ' + flight_iata[2:]

### new source

url = "https://aerodatabox.p.rapidapi.com/flights/airports/icao/KPVD/" + current_time_st + "/" + end_time_st

querystring = {"withLeg":"false","direction":"Departure","withCancelled":"false","withCodeshared":"false","withCargo":"false","withPrivate":"false","withLocation":"false"}

headers = {
    'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
    'x-rapidapi-key': "0c6cf1ab06mshef31a230c02dc4cp1a1d8fjsn87793b2dc24a"
    }

second_data = requests.request("GET", url, headers=headers, params=querystring).json()

aircraft_model

aircraft_model = ''

for i in second_data['departures']:
    if i['number'] == flight_iata_f:
        aircraft_model = i['aircraft']['model']

next_flight['aircraft'] = aircraft_model

next_flight['arr_iata']

out = generate_image('cropmap.png',get_coords('PVD'),get_coords(next_flight['arr_iata']))
buffered = BytesIO()
out.save(buffered, format="PNG")
buffered.seek(0)
img_str = base64.b64encode(buffered.getvalue()).decode()

next_flight['map'] = img_str

with open("next_flight.json", "w") as outfile:
    json.dump(next_flight,outfile)
