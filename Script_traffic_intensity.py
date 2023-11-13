import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import schedule
import urllib.parse

############### Colecting Data ###############

token = "d23887006fb8447988a41075801339c913f1d71a0fd"
targetUrl = "https://eismoinfo.lt/traffic-intensity-service"

encoded_url = urllib.parse.quote(targetUrl)
url = "http://api.scrape.do?token={}&url={}".format(token, encoded_url)
response = requests.request("GET", url)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    'value': 'application/json, text/plain, */*',
    'accept': 'application/json, text/plain, */*',
    'cookie': '_ga=GA1.2.1272715160.1699462284; _gid=GA1.2.1647336826.1699462284; _ga_E8WJ6X0RYN=GS1.2.1699471615.3.0.1699471615.60.0.0; _ga_162SQ74LLR=GS1.2.1699471697.2.1.1699471698.0.0.0'
}

# https://eismoinfo.lt/#!/ information from page
url = "https://eismoinfo.lt/traffic-intensity-service"

page = requests.get(url, headers = headers)
# print(page.status_code)
data = page.json()

############### Creating DataFrames ###############

direction_positive = []
direction_negative = []

for i in range(len(data)):
    try:
        data2 = page.json()[i]['roadSegments'][0]
        data3 = page.json()[i]['roadSegments'][1]
        direction_positive.append(data2)
        direction_negative.append(data3)
    except IndexError:
        direction_positive.append({'direction': None, 'startX': None, 'startY': None, 'endX': None, 'endY': None, 'winterSpeed': 0, 'summerSpeed': 0, 'numberOfVehicles': 0, 'averageSpeed': 0, 'trafficType': 0})
        direction_negative.append({'direction': None, 'startX': None, 'startY': None, 'endX': None, 'endY': None, 'winterSpeed': 0, 'summerSpeed': 0, 'numberOfVehicles': 0, 'averageSpeed': 0, 'trafficType': 0})
        continue

df_info = pd.DataFrame(data)
df_positive = pd.DataFrame(direction_positive)
df_negative = pd.DataFrame(direction_negative)

# print(df_info)
# print(df_positive)
# print(df_negative)

############### DataFrame Clearance ###############

df_info['Date'] = df_info['date'].str.split(pat='.', n=0, expand=True)[0]
df_info['Date'] = df_info['Date'].str.replace('T', ' ')

df_info['Date'] = pd.to_datetime(df_info['Date'])
df_info['Date'] = df_info['Date'] + pd.Timedelta(hours=2)

df_info['Date'] = pd.to_datetime(df_info['Date']).dt.date
df_info['Time'] = pd.to_datetime(df_info['Date']).dt.time

df_info.drop(columns=['id', 'km', 'x', 'y', 'roadSegments', 'timeInterval', 'date'], inplace=True)
df_info.rename(columns={'name': 'Location', 'roadNr': 'Road', 'roadName': 'Road_Name'}, inplace=True)
df_info['Road_Name'] = df_info['Road_Name'].str.replace('*', '')

df_positive.drop(columns=['startX', 'startY', 'endX', 'endY', 'winterSpeed', 'summerSpeed'], inplace=True)
df_positive.rename(columns={'direction': 'Direction_Positive', 'numberOfVehicles': 'Number_of_Vehicles', 'averageSpeed': 'Average_Speed', 'trafficType':'Traffic_Type'}, inplace=True)

df_negative.drop(columns=['startX', 'startY', 'endX', 'endY', 'winterSpeed', 'summerSpeed'], inplace=True)
df_negative.rename(columns={'direction': 'Direction_Negative', 'numberOfVehicles': 'Number_of_Vehicles', 'averageSpeed': 'Average_Speed', 'trafficType':'Traffic_Type'}, inplace=True)

############### Joining DataFrames ###############

general = pd.concat([df_info, df_negative, df_positive], axis=1)
general.to_csv("Road_traffic_intensity_real_time.csv", index=False)

###############  ###############