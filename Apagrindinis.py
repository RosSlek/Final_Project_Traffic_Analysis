import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import psycopg2
import numpy as np





def lietuvos_duomenu_scraping():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        'value': 'application/json, text/plain, */*',
        'accept': 'application/json, text/plain, */*',
        'cookie': '_ga=GA1.2.1272715160.1699462284; _gid=GA1.2.1647336826.1699462284; _ga_E8WJ6X0RYN=GS1.2.1699471615.3.0.1699471615.60.0.0; _ga_162SQ74LLR=GS1.2.1699471697.2.1.1699471698.0.0.0'
    }
    url = "https://osp.stat.gov.lt/analysis-portlet/services/api/v1/data/generate/table/hash/52b746af-9995-4168-8d27-1865a4ba4076"
    page = requests.get(url, headers=headers)
    ilgis = len(page.json()["data"]["itemMatrix"])

    sarasas1 = []
    sarasas2 = []
    sarasas3 = []

    for i in range(ilgis):
        data1 = page.json()["data"]["itemMatrix"][i][0]["value"]
        data2 = page.json()["data"]["itemMatrix"][i][1]["value"]
        laikotarpis = page.json()["data"]["sidebar"][i]["name"]
        sarasas1.append(data1)
        sarasas2.append(data2)
        sarasas3.append(laikotarpis)
        # print(data1, data2, laikotarpis)


    data = {
        "Old_Date": sarasas3,
        "Visi kelių eismo įvykiai": sarasas1,
        "Dėl neblaivių vairuotojų kaltės": sarasas2
    }

    df = pd.DataFrame(data)

    df["Year"] = df["Old_Date"].str.split(pat='M', n=0, expand=True)[0]
    df["Month"] = df["Old_Date"].str.split(pat='M', n=0, expand=True)[1]
    df.drop(columns=['Old_Date'], inplace=True)

    df = df.reindex(columns=['Year', 'Month', 'Visi kelių eismo įvykiai', 'Dėl neblaivių vairuotojų kaltės'])
    df = df.loc[df["Year"] == "2023"]
    df['Visi kelių eismo įvykiai'] = list(map(int, df['Visi kelių eismo įvykiai']))

    # print(df)
    df.to_csv("Eismo ivykiai.csv", index=False)

# lietuvos_duomenu_scraping()





########################################################################################################################





def oecd_data_scraping():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        'value': 'application/json, text/plain, */*',
        'accept': 'application/json, text/plain, */*',
        'cookie': '_ga=GA1.2.1272715160.1699462284; _gid=GA1.2.1647336826.1699462284; _ga_E8WJ6X0RYN=GS1.2.1699471615.3.0.1699471615.60.0.0; _ga_162SQ74LLR=GS1.2.1699471697.2.1.1699471698.0.0.0'
    }
    url = "https://stats.oecd.org/sdmx-json/data/DP_LIVE/.ROADACCID.DEATH.1000000HAB.A/OECD?json-lang=en&dimensionAtObservation=allDimensions&startPeriod=1970"
    page = requests.get(url, headers=headers)

    ilgis = len(page.json()["structure"]["dimensions"]["observation"][0]["values"])

    sarasiukas1 = []
    sarasiukas2 = []
    sarasiukas3 = []


    for i in range(ilgis):
        try:
            data1 = page.json()["structure"]["dimensions"]["observation"][0]["values"][i]["name"]
            sarasiukas1.append(data1)
            data2 = page.json()["dataSets"][0]["observations"][f"{i}:0:0:0:0:27"][0]
            sarasiukas2.append(data2)
            data3 = page.json()["dataSets"][0]["observations"][f"{i}:0:0:0:0:26"][0]
            sarasiukas3.append(data3)
            # print(data1, data2)
        except KeyError:
            sarasiukas2.append("ok")
            sarasiukas3.append("ok")
            continue



    data = {
        "Country": sarasiukas1,
        "Amount of accidents 2020": sarasiukas2,
        "Amount of accidents 2021": sarasiukas3
    }


    df = pd.DataFrame.from_dict(data, orient="index").transpose()
    df = df.loc[df["Amount of accidents 2021"] != "ok"].convert_dtypes().round(2)
    print(df)
    df.to_csv("xxEuropos duomenys.csv", index=True)


# oecd_data_scraping()



def europos_duomenu_surusiavimas():
    df_pd = pd.read_csv('xxEuropos duomenys.csv')

    roads_pd = ['Lithuania', 'Switzerland', 'Poland', 'Germany', 'France', 'Belgium', 'Italy', 'Sweden']
    important_roads_pd = []
    for i in roads_pd:
        selecting_road_pd = df_pd.loc[df_pd['Country'] == i]
        important_roads_pd.append(selecting_road_pd)

    df_important_roads_pd = pd.concat(important_roads_pd).reset_index()
    df_important_roads_pd.to_csv('Surusiuoti Europos duomenys.csv', index=False)

# europos_duomenu_surusiavimas()






def lietuvos_regionu_data():
    df = pd.read_csv("LT duomenys 22-23.csv")
    df = df[df['Administracinė teritorija'].notna()]

    df["Year"] = df["Laikotarpis"].str.split(pat='M', n=0, expand=True)[0]
    df["Month"] = df["Laikotarpis"].str.split(pat='M', n=0, expand=True)[1]

    df.drop(columns=['Rodiklis', 'Matavimo vienetai', 'Laikotarpis'], inplace=True)

    df = df.reindex(columns=['Year', 'Month', 'Administracinė teritorija', 'Reikšmė'])


    pasirinkimas = input("Pasirinkite analizuojamus metus (2022 arba 2023): ")

    # df.to_csv("Programiskai pakoreguotas failas.csv", index = False)
    df = df.loc[df['Year'] == pasirinkimas]
    df = df.loc[df['Administracinė teritorija'] != 'Lietuvos Respublika']
    df = df.loc[df['Administracinė teritorija'] != 'Vidurio ir vakarų Lietuvos regionas']
    df = df.loc[df['Administracinė teritorija'] != 'Sostinės regionas']
    df = df.groupby(['Administracinė teritorija']).sum('Reikšmė').sort_values(by="Reikšmė", ascending=False).reset_index()
    # min = df.loc[df["Reikšmė"] == df["Reikšmė"].min()]
    # min = df["Reikšmė"].min()
    # max = df["Max"] = df.loc[df["Reikšmė"] == df["Reikšmė"].max()]
    # max = df["Reikšmė"].max()


    # print(df)
    df.to_csv("Programiskai pakoreguotas failas.csv", index=True)


    def addlabels(x, y):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], ha='center')

    plt.figure(figsize=(15, 10))
    plt.bar(df['Administracinė teritorija'], df['Reikšmė'], color="green")
    plt.title(f"Total Number of Road Accidents per Region in {pasirinkimas}")
    plt.ylabel(f'Amount in {pasirinkimas}')
    addlabels(df['Administracinė teritorija'], df['Reikšmė'])
    plt.xticks(rotation=10, ha='right')
    plt.xlabel('')
    plt.show()


# lietuvos_regionu_data()









# print(type(df["Amount of accidents 2022"]))















