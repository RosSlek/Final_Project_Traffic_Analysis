import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import schedule

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
#
# print(data)
list = []
x = 0
for i in range(len(data)):
    data1 = page.json()[i]['roadSegments']
    print(data1[0])
print(data1)
print(type(data1))
print(len(data1))
# list.append(data1)

# print(list)


# df3 = pd.DataFrame(list)
# print(df3)
# for i in range():
#     data1 = page.json()["data"]["itemMatrix"][i][0]["value"]
# df1 = pd.DataFrame(data)
# print(data)
# traffic = []
# for i in range(len(data)):
#     df2 = data[i]['roadSegments']
#     # traffic.append(df2)
# df3 = pd.DataFrame(df2)
# print(df3)




# df1.drop(columns=['id', 'name', 'roadName', 'km', 'x', 'y', 'timeInterval'], inplace=True)
#
# df1.to_csv("Road_traffic_intensity.csv", index=False)

# df1.rename(columns={'id': 'Measuring_Station_ID', 'color': 'Traffic_Intensity'}, inplace=True)
# print(df1)
# df = pd.read_csv('Road_info_real_time.csv')
# # print(df)
# df3 = pd.merge(df, df1, on='Measuring_Station_ID', how='left')
# print(df3)
#
# df3 = pd.read_csv('Road_traffic_intensity.csv')
# print(df3)