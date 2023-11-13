import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import psycopg2



headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    'value': 'application/json, text/plain, */*',
    'accept': 'application/json, text/plain, */*',
    'cookie': '_ga=GA1.2.1272715160.1699462284; _gid=GA1.2.1647336826.1699462284; _ga_E8WJ6X0RYN=GS1.2.1699471615.3.0.1699471615.60.0.0; _ga_162SQ74LLR=GS1.2.1699471697.2.1.1699471698.0.0.0'
}
url = "https://osp.stat.gov.lt/analysis-portlet/services/api/v1/data/generate/table/hash/52b746af-9995-4168-8d27-1865a4ba4076"
page = requests.get(url, headers=headers)
ilgis = len(page.json()["data"]["itemMatrix"])
datas = page.json()
print(datas)
sarasas1 = []
sarasas2 = []
sarasas3 = []

for i in range(ilgis):
    data1 = page.json()["data"]["itemMatrix"][i][1]
    # data2 = page.json()["data"]["itemMatrix"][i][1]["value"]
    # laikotarpis = page.json()["data"]["sidebar"][i]["name"]
    sarasas1.append(data1)
    # sarasas2.append(data2)
    # sarasas3.append(laikotarpis)
    # print(data1, data2, laikotarpis)
print(sarasas1)


data = {
    "Old_Date": sarasas3,
    "Visi kelių eismo įvykiai": sarasas1,
    "Dėl neblaivių vairuotojų kaltės": sarasas2
}

df = pd.DataFrame(data)
#
# df['date'] = df['date].str.split(pat=' ', n=0, expand=True)[0]
# df['Time] = df['date].str.split(pat=' ', n=0, expand=True)[1]
# df.drop(columns=['Old_Date'], inplace=True)
#
# df = df.reindex(columns=['Year', 'Month', 'Visi kelių eismo įvykiai', 'Dėl neblaivių vairuotojų kaltės'])
#
# print(df)
# df.to_csv("Eismo ivykiai.csv", index=True)


# data["Pirmas_stulpelis"].append("data1")









# headers = {
# "User-Agent": "Chrome/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
# }
# url = "https://osp.stat.gov.lt/statistiniu-rodikliu-analize?hash=52b746af-9995-4168-8d27-1865a4ba4076#/"
# res = requests.get(url, headers=headers)
# # response = requests.get(url)
# soup = BeautifulSoup(res.content,"html.parser")
#
# #apacioje esanti eilute parodys tik teksta, be jokiu kodu, taip sakant nukopinam informacija is aruodo
# content_block = soup.find("div", class_="fluid-table-sidebar")
# # for content in content_block:
#
# print(content_block)




# url = "https://osp.stat.gov.lt/statistiniu-rodikliu-analize?hash=52b746af-9995-4168-8d27-1865a4ba4076#/"
# response = requests.get(url)
# soup = BeautifulSoup(response.content,"html.parser")
#
# #apacioje esanti eilute parodys tik teksta, be jokiu kodu, taip sakant nukopinam informacija is aruodo
# # content_block = soup.find('table', class_= "pb-center-column pb-right-column col-xs-12 col-sm-12 col-md-6 product-main-right")
# # for content in content_block:
#
#
# # flat_title = content_block.select('div''"h1", class_="name").text.strip()
# # flat_title = content_block.select_one("div.desktop-only h1").text.strip()
# ## turi buti grotazymes, jeigu ID
# # flat_title = soup.select_one("table#table")
# print(soup)