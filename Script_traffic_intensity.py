import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import schedule
import urllib.parse



token = "d23887006fb8447988a41075801339c913f1d71a0fd"
targetUrl = "https://eismoinfo.lt/traffic-intensity-service"

encoded_url = urllib.parse.quote(targetUrl)
url = "http://api.scrape.do?token={}&url={}".format(token, encoded_url)
response = requests.request("GET", url)

############### Colecting Data ###############

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    'value': 'application/json, text/plain, */*',
    'accept': 'application/json, text/plain, */*',
    'cookie': '_ga=GA1.2.1272715160.1699462284; _gid=GA1.2.1647336826.1699462284; _ga_E8WJ6X0RYN=GS1.2.1699471615.3.0.1699471615.60.0.0; _ga_162SQ74LLR=GS1.2.1699471697.2.1.1699471698.0.0.0'
}

# https://eismoinfo.lt/#!/ information from page
url = "https://eismoinfo.lt/traffic-intensity-service"

page = requests.get(url)
# headers = headers)
print(page.status_code)
data = page.json()

list = []
for i in range(len(data)):
    data1 = page.json()[i]['roadSegments']
    list.append(data1)

# print(list)
print("########################################################################3")
# print(len(list))

direction_list = []

for x in range(len(list)):
    try:
        data2 = list[x][0]
        direction_list.append(data2)
    except:
        direction_list.append(0)
        continue


print(len(direction_list))

direction_negative = []
direction_positive = []

for y in range(len(direction_list)):
    try:
        data3 = direction_list[y][0]
        direction_positive.append(data3)
    except:
        direction_positive.append(0)
        continue

for u in range(len(direction_list)):
    try:
        data4 = direction_list[u][1]
        direction_negative.append(data4)
    except:
        direction_negative.append(0)
        continue


print(len(direction_negative))
print(direction_negative)
print("3333333333333333333333333333333333333333333333333333333333333333")
# print(direction_positive)
print(len(direction_positive))
print(direction_positive)
# df_info = pd.DataFrame(data)
# df_negative = pd.DataFrame(direction_negative)
# df_positive = pd.DataFrame(direction_positive)
#
# df_info['Date'] = df_info['date'].str.split(pat='.', n=0, expand=True)[0]
# df_info['Date'] = df_info['Date'].str.replace('T', ' ')
#
# df_info['Date'] = pd.to_datetime(df_info['Date'])
# df_info['Date'] = df_info['Date'] + pd.Timedelta(hours=2)
#
# df_info['Date'] = pd.to_datetime(df_info['Date']).dt.date
# df_info['Time'] = pd.to_datetime(df_info['Date']).dt.time
#
# df_info.drop(columns=['id', 'km', 'x', 'y', 'roadSegments', 'timeInterval', 'date'], inplace=True)
# df_info.rename(columns={'name': 'Location', 'roadNr': 'Road', 'roadName': 'Road_Name'}, inplace=True)
#df_info['Road_Name'] = df_info['Road_Name'].str.replace('*', '')

# print(df_info)
# print("###########################################################")
# df_positive.drop(columns=['startX', 'startY', 'endX', 'endY', 'winterSpeed', 'summerSpeed'], inplace=True)
# df_positive.rename(columns={'direction': 'Direction_Positive', 'numberOfVehicles': 'Number_of_Vehicles', 'averageSpeed': 'Average_Speed', 'trafficType':'Traffic_Type'}, inplace=True)
# print(df_positive)
# print("###########################################################")
# df_negative.drop(columns=['startX', 'startY', 'endX', 'endY', 'winterSpeed', 'summerSpeed'], inplace=True)
# df_negative.rename(columns={'direction': 'Direction_Negative', 'numberOfVehicles': 'Number_of_Vehicles', 'averageSpeed': 'Average_Speed', 'trafficType':'Traffic_Type'}, inplace=True)
# print(df_negative)
#
# general = pd.concat([df_info, df_negative, df_positive], axis=1)
# general.to_csv("Road_Traffic_intensity.csv", index=False)