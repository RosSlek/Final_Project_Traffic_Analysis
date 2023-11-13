import requests
import json
import psycopg2
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time
import schedule
import os.path


df3 = pd.read_csv('Road_traffic_intensity.csv')
print(df3)
df = df3.values.tolist()
# print(df)
print(len(df))
tuscia = []
for i in range df:
    data = df[i]['startX']

print(data)