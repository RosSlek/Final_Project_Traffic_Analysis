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

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    'value': 'application/json, text/plain, */*',
    'accept': 'application/json, text/plain, */*',
    'cookie': '_ga=GA1.2.1272715160.1699462284; _gid=GA1.2.1647336826.1699462284; _ga_E8WJ6X0RYN=GS1.2.1699471615.3.0.1699471615.60.0.0; _ga_162SQ74LLR=GS1.2.1699471697.2.1.1699471698.0.0.0'
}

# https://eismoinfo.lt/#!/ information from page
url = "https://eismoinfo.lt/traffic-intensity-service"

page = requests.get(url, headers = headers)
print(page.status_code)
soup = BeautifulSoup(page.content, "html.parser")
print(soup)
direction_negative = soup.find_all("direction")
print(direction_negative)