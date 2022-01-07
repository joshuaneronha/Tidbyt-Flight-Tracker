import pandas as pd
import requests
from dateutil import parser

pvd_data = pd.read_html('https://webservice.prodigiq.com/wfids/PVD/full?page=1&type=departures&rows=100')[1]

pvd_data.head()

pvd_data['airline_iata'] = pvd_data.apply(lambda row : row['Flight No.'].split(' ')[0], axis=1)
pvd_data['flight_iata'] = pvd_data.apply(lambda row : row['Flight No.'].split(' ')[0] + row['Flight No.'].split(' ')[1], axis=1)
pvd_data['arr_iata'] = pvd_data.apply(lambda row : row['Destination'].split(')')[0][1:], axis=1)
pvd_data['datetime'] = pvd_data.apply(lambda row : parser.parse(row['Date'] + ' ' + row['Time']).strftime("%Y-%m-%dT%H:%M"), axis=1)
pvd_data['dep_gate'] = pvd_data['Gate']
pvd_data['status'] = pvd_data['Status']

pvd_data[['airline_iata','flight_iata', 'arr_iata', 'datetime', 'dep_gate', 'status']]
