import pandas as pd
import requests
import matplotlib.pyplot as plt
import os.path
from bs4 import BeautifulSoup

############### function to scrape proxy list, since free proxies aren`t very usefull and we won`t scrape continously (mostly we create CSV) ###############
def get_proxy():
    url = "https://free-proxy-list.net"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    proxy_list = []

    table = soup.find('table', class_='table table-striped table-bordered')
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all('td')
            ip = columns[0].text.strip()
            port = columns[1].text.strip()
            proxy = f'https://{ip}:{port}'
            proxy_list.append(proxy)
    # print(proxy_list)
    return proxy_list

# get_proxy()

############### function to scrape road info real time ###############
def scrape_road_info_real_time():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        'value': 'application/json, text/plain, */*',
        'accept': 'application/json, text/plain, */*',
        'cookie': '_ga=GA1.2.1272715160.1699462284; _gid=GA1.2.1647336826.1699462284; _ga_E8WJ6X0RYN=GS1.2.1699471615.3.0.1699471615.60.0.0; _ga_162SQ74LLR=GS1.2.1699471697.2.1.1699471698.0.0.0'
    }

    # https://eismoinfo.lt/#!/ information from page
    url = "https://eismoinfo.lt/eismoinfo-backend/osi-info-table"

    page = requests.get(url, headers=headers)
    print(page.status_code)
    data = page.json()

    ############### creating DataFrame and cleaning ###############

    df = pd.DataFrame(data)

    ##### changing date time from timestamp to a normal date and time format, adjusting time zone (+2hours) #####

    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df['date'] = df['date'] + pd.Timedelta(hours=2)

    df['Date'] = pd.to_datetime(df['date']).dt.date
    df['Time'] = pd.to_datetime(df['date']).dt.time

    ##### dropping unnecessary columns and renaming them #####

    df.drop(columns=['color', 'importance', 'x', 'y', 'km', 'date'], inplace=True)
    df.rename(columns={'id': 'Measuring_Station_ID', 'name': 'Location', 'roadName': 'Road_Name', 'roadNr': 'Road', 'airTemperature': 'Air_Temperature', 'windDirection': 'Wind_Direction', 'windSpeed': 'Wind_Speed', 'precipitationType': 'Precipitation_Type', 'precipitationIntensity': 'Precipitation_Intensity', 'dewPoint': 'Dew_point', 'roadTemperature': 'Road_Surface_Temperature', 'surfaceCondition': 'Road_Surface_Condition', 'friction': 'Friction'}, inplace=True)
    df['Road_Name'] = df['Road_Name'].str.replace('*', '')

    ############### saving real time data as CSV ###############

    df.to_csv("CSV/Road_info_real_time.csv", index=False)

# scrape_road_info_real_time()

############### function to create chosen roads list (we can change it and get different graphs, CSV info) ###############
def chosen_roads():
    roads = ['Vilnius–Kaunas–Klaipėda', 'Kaunas–Marijampolė–Suvalkai', 'Klaipėda–Liepoja', 'Antakalnis–Jieznas–Alytus–Merkinė', 'Jonava–Kėdainiai–Šeduva', 'Daugpilis–Rokiškis–Panevėžys', 'Kalvarija–Gražiškiai–Vištytis', 'Panevėžys–Šiauliai', 'Vilnius–Panevėžys', 'Vilnius–Varėna–Gardinas']
    return roads

############### function to create chosen roads real time data CSV ###############
def chosen_roads_real_time_data():
    if os.path.isfile('CSV/Road_info_real_time.csv'):

        df_rt = pd.read_csv('CSV/Road_info_real_time.csv')

        ##### taking scraped real time data if it exists and leaving only our chosen roads #####

        roads_rt = chosen_roads()
        chosen_roads_rt = []
        for i in roads_rt:
            selecting_road_rt = df_rt.loc[df_rt['Road_Name'] == i]
            chosen_roads_rt.append(selecting_road_rt)

        ##### joining chosen roads to a new DataFrame and saving it as CSV #####

        df_chosen_roads_rt = pd.concat(chosen_roads_rt).reset_index()
        df_chosen_roads_rt.to_csv('CSV/Chosen_roads_real_time.csv', index=False)
    else:
        print("Seems like you don`t have 'Road_info_real_time.csv' file yet. Would you like to create it now? Enter Y for yes and N for no: ")
        create_or_not = input()

        ##### if where is no scraped data, we can create it and run this function again, or leave this function #####

        if create_or_not == 'Y':
            scrape_road_info_real_time()
            print("File 'Road_info_real_time.csv' was created successfully!")
            chosen_roads_real_time_data()
        elif create_or_not == 'N':
            print("File 'Road_info_real_time.csv' will not be created.")
        else:
            print("Wrong input! I`ll take it as a No.")

# chosen_roads_real_time_data()

############### real time conditions of the selected roads ###############
def chosen_roads_real_time_data():
    if os.path.isfile('CSV/Road_info_real_time.csv'):
        df_rt = pd.read_csv('CSV/Road_info_real_time.csv')

        ##### taking scraped real time data if it exists, and leaving only chosen roads #####

        roads_rt = chosen_roads()
        chosen_roads_rt = []
        for i in roads_rt:
            selecting_road_rt = df_rt.loc[df_rt['Road_Name'] == i]
            chosen_roads_rt.append(selecting_road_rt)

        ##### joining selected roads to a new DataFrame #####

        df_chosen_roads_rt = pd.concat(chosen_roads_rt)
        print(df_chosen_roads_rt)

        ##### drawing 3 graphs from a new DataFrame #####

        plt.figure(figsize=(10, 5))
        plt.bar(df_chosen_roads_rt['Road'], df_chosen_roads_rt['Air_Temperature'], color='gold')
        plt.title('Average temperature of chosen roads real time')
        plt.ylabel('Air temperature, °C')
        plt.xlabel('Road')
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.bar(df_chosen_roads_rt['Road'], df_chosen_roads_rt['Road_Surface_Temperature'], color='green')
        plt.title('Average road surface temperature of chosen roads real time')
        plt.ylabel('Road surface temperature, °C')
        plt.xlabel('Road')
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.bar(df_chosen_roads_rt['Road'], df_chosen_roads_rt['Wind_Speed'], color='firebrick')
        plt.title('Average wind speed of chosen roads real time')
        plt.ylabel('Wind speed, m/s')
        plt.xlabel('Road')
        plt.show()
    else:
        print(
            "Seems like you don`t have 'Road_info_real_time.csv' file yet. Would you like to create it now? Enter Y for yes and N for no: ")
        create_or_not = input()
        if create_or_not == 'Y':
            scrape_road_info_real_time()

            ##### if where is no scraped data, we can create it and run this function again, or leave this function #####

            print("File 'Road_info_real_time.csv' was created successfully!")
            chosen_roads_real_time_data()
        elif create_or_not == 'N':
            print("File 'Road_info_real_time.csv' will not be created.")
        else:
            print("Wrong input! I`ll take it as a No.")

# chosen_roads_real_time_data()

############### function to create chosen roads periodical data CSV ###############
def chosen_roads_periodical_data():
    if os.path.isfile('CSV/Road_info_periodical.csv'):
        df_pd = pd.read_csv('CSV/Road_info_periodical.csv')

        ##### taking scraped periodical data if it exists, and leaving only chosen roads #####

        roads_pd = chosen_roads()
        chosen_roads_pd = []
        for i in roads_pd:
            selecting_road_pd = df_pd.loc[df_pd['Road_Name'] == i]
            chosen_roads_pd.append(selecting_road_pd)

        ##### joining selected roads to a new DataFrame and creating CSV #####

        df_chosen_roads_pd = pd.concat(chosen_roads_pd).reset_index()
        df_chosen_roads_pd.to_csv('CSV/Chosen_roads_periodical.csv', index=False)
        print("File 'Chosen_roads_periodical.csv' was created successfully!")
    else:
        print("Sorry, you have not collected any periodical data yet! Try again after collecting some data with 'Script_Road_info_periodical'.")

        ##### we are not offered to create it instantly, because periodical data is automatically scraped every 6 hours #####

# chosen_roads_periodical_data()

############### creating function to get averages drom all collected data for chosen roads ###############
def avg_road_info_from_all_collected_data():
    if os.path.isfile('CSV/Chosen_roads_periodical.csv'):
        df = pd.read_csv('CSV/Chosen_roads_periodical.csv')

        ##### taking CSV with information about chosen roads if it exists #####
        ##### and grouping by the road, getting averages for all collected data #####

        mean_day_t_all_data = df.groupby('Road_Name')['Air_Temperature'].mean().round(1).reset_index()
        mean_day_t_all_data.drop(columns=['Road_Name'], inplace=True)
        mean_day_wind_all_data = df.groupby('Road')['Wind_Speed'].mean().round(1).reset_index()
        mean_day_road_surface_t = df.groupby('Road_Name')['Road_Surface_Temperature'].mean().round(1).reset_index()

        ##### joining grouped selected roads to a new DataFrame and rearranging columns order #####

        df_mean_of_all_data = pd.concat([mean_day_t_all_data, mean_day_wind_all_data, mean_day_road_surface_t], axis=1, join='inner')
        df_mean_of_all_data = df_mean_of_all_data[['Road_Name', 'Road', 'Air_Temperature', 'Road_Surface_Temperature', 'Wind_Speed']]
        print(df_mean_of_all_data)

        ##### drawing 3 graphs from a new DataFrame #####

        plt.figure(figsize=(10,5))
        plt.bar(df_mean_of_all_data['Road'], df_mean_of_all_data['Air_Temperature'], color='gold')
        plt.title('Average temperature of chosen roads from all collected data')
        plt.ylabel('Air temperature, °C')
        plt.xlabel('Road')
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.bar(df_mean_of_all_data['Road'], df_mean_of_all_data['Road_Surface_Temperature'], color='green')
        plt.title('Average road surface temperature of chosen roads from all collected data')
        plt.ylabel('Road surface temperature, °C')
        plt.xlabel('Road')
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.bar(df_mean_of_all_data['Road'], df_mean_of_all_data['Wind_Speed'],color='firebrick')
        plt.title('Average wind speed of chosen roads from all collected data')
        plt.ylabel('Wind speed, m/s')
        plt.xlabel('Road')
        plt.show()
    else:
        print("Seems like you don`t have 'Chosen_roads_periodical.csv' file yet. Would you like to create it now? Enter Y for yes and N for no: ")
        create_or_not = input()
        if create_or_not == 'Y':
            chosen_roads_periodical_data()

            ##### if where is no CSV with chosen roads periodical info #####
            ##### we can create it and run this function again, or leave this function #####

            print("Would you like to create file")
            avg_road_info_from_all_collected_data()
        elif create_or_not == 'N':
            print("File 'Chosen_roads_periodical.csv' will not be created.")
        else:
            print("Wrong input! I`ll take it as a No.")

# avg_road_info_from_all_collected_data()

############### averages from all collected data by selected day ###############
def avg_on_the_road_from_collected_data_by_day():
    if os.path.isfile('CSV/Chosen_roads_periodical.csv'):
        df_by_day = pd.read_csv('CSV/Chosen_roads_periodical.csv')

        ##### taking CSV with information about chosen roads if it exists #####
        ##### selecting a date of which we want to see info #####

        try:
            df_by_day.Date = pd.to_datetime(df_by_day.Date)
            choice = pd.to_datetime(input('Input date in mm-dd-yyyy format: '))
            chosen_day = df_by_day.loc[df_by_day['Date'] == choice]
            if chosen_day.empty:
                print("Where is no data about selected date!")
            else:
                avg_t_by_day = chosen_day.groupby('Road_Name')['Air_Temperature'].mean().round(1).reset_index()
                avg_wind_speed_by_day = chosen_day.groupby('Road')['Wind_Speed'].mean().round(1).reset_index()
                avg_rs_t_by_day = chosen_day.groupby('Road_Name')['Road_Surface_Temperature'].mean().round(1).reset_index()
                avg_rs_t_by_day.drop(columns=['Road_Name'], inplace=True)

                ##### grouping by the road, getting averages for all collected data #####
                ##### joining grouped selected roads to a new DataFrame and rearranging columns order #####

                df_by_day_avg = pd.concat([avg_t_by_day, avg_wind_speed_by_day, avg_rs_t_by_day], axis=1)
                df_by_day_avg = df_by_day_avg[['Road_Name', 'Road', 'Air_Temperature', 'Road_Surface_Temperature', 'Wind_Speed']]
                print(df_by_day_avg)

                ##### drawing 3 graphs from a new DataFrame #####

                plt.figure(figsize=(10, 5))
                plt.bar(df_by_day_avg['Road'], df_by_day_avg['Air_Temperature'], color='gold')
                plt.title('Average temperature of chosen roads for a selected day')
                plt.ylabel('Air temperature, °C')
                plt.xlabel('Road')
                plt.show()

                plt.figure(figsize=(10, 5))
                plt.bar(df_by_day_avg['Road'], df_by_day_avg['Road_Surface_Temperature'], color='green')
                plt.title('Average road surface temperature of chosen roads for a selected day')
                plt.ylabel('Road surface temperature, °C')
                plt.xlabel('Road')
                plt.show()

                plt.figure(figsize=(10, 5))
                plt.bar(df_by_day_avg['Road'], df_by_day_avg['Wind_Speed'], color='firebrick')
                plt.title('Average wind speed of chosen roads for a selected day')
                plt.ylabel('Wind speed, m/s')
                plt.xlabel('Road')
                plt.show()
        except:
            print("OOPS! Wrong date input!")
    else:
        print("Seems like you don`t have 'Chosen_roads_periodical.csv' file yet. Would you like to create it now? Enter Y for yes and N for no: ")
        create_or_not = input()
        if create_or_not == 'Y':
            chosen_roads_periodical_data()
            print("Would you like to create file")

            ##### if where is no CSV with chosen roads periodical info #####
            ##### we can create it and run this function again, or leave this function #####

            avg_on_the_road_from_collected_data_by_day()
        elif create_or_not == 'N':
            print("File 'Chosen_roads_periodical.csv' will not be created.")
        else:
            print("Wrong input! I`ll take it as a No.")

# avg_on_the_road_from_collected_data_by_day()

############### function to scrape road traffic intensity real time ###############
def scrape_road_traffic_intensity_real_time():
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
    data = page.json()

    ############### creating 2 list for DataFrames ###############

    direction_positive = []
    direction_negative = []

    ##### creating to list with information about traffic, since there are 2 directions of the road #####

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

            ##### for non existing values (one way street, malfunctio of the station) we insert empty data to keep DataFrame format #####

    ##### creating 3 DataFrames #####

    df_info = pd.DataFrame(data)
    df_positive = pd.DataFrame(direction_positive)
    df_negative = pd.DataFrame(direction_negative)

    ############### DataFrame clearance ###############

    df_info['Date'] = df_info['date'].str.split(pat='.', n=0, expand=True)[0]
    df_info['Date'] = df_info['Date'].str.replace('T', ' ')

    ##### changing date time from timestamp to a normal date and time format, adjusting time zone (+2hours) #####
    ##### separating date and time into two columns #####

    df_info['Date'] = pd.to_datetime(df_info['Date'])
    df_info['Date'] = df_info['Date'] + pd.Timedelta(hours=2)

    df_info['Time'] = pd.to_datetime(df_info['Date']).dt.time
    df_info['Date'] = pd.to_datetime(df_info['Date']).dt.date

    ##### dropping unnecessary columns and renaming them for the first DataFrame #####

    df_info.drop(columns=['id', 'km', 'x', 'y', 'roadSegments', 'date'], inplace=True)
    df_info.rename(columns={'name': 'Location', 'roadNr': 'Road', 'timeInterval': 'Time_Interval', 'roadName': 'Road_Name'}, inplace=True)
    df_info['Road_Name'] = df_info['Road_Name'].str.replace('*', '')

    ##### dropping unnecessary columns and renaming them for the second DataFrame #####

    df_positive.drop(columns=['startX', 'startY', 'endX', 'endY', 'winterSpeed', 'summerSpeed'], inplace=True)
    df_positive.rename(columns={'direction': 'Direction_Positive', 'numberOfVehicles': 'Number_of_Vehicles', 'averageSpeed': 'Average_Speed', 'trafficType':'Traffic_Type'}, inplace=True)

    ##### dropping unnecessary columns and renaming them for the third DataFrame #####

    df_negative.drop(columns=['startX', 'startY', 'endX', 'endY', 'winterSpeed', 'summerSpeed'], inplace=True)
    df_negative.rename(columns={'direction': 'Direction_Negative', 'numberOfVehicles': 'Number_of_Vehicles', 'averageSpeed': 'Average_Speed', 'trafficType':'Traffic_Type'}, inplace=True)

    ############### joining DataFrames and saving new CSV ###############

    general = pd.concat([df_info, df_negative, df_positive], axis=1)
    general.to_csv("CSV/Road_traffic_intensity_real_time.csv", index=False)

# scrape_road_traffic_intensity_real_time()


############################################################################

# Scraping Total Amount of Road Accidents per Month data from statistics departament  in Lithuania during 2023
# Using Json method
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

# Creating lists of scraped data
    sarasas1 = []
    sarasas2 = []
    sarasas3 = []

# Writing for loop to extract data from the source and appending it to previuosly created lists above
    for i in range(ilgis):
        data1 = page.json()["data"]["itemMatrix"][i][0]["value"]
        data2 = page.json()["data"]["itemMatrix"][i][1]["value"]
        laikotarpis = page.json()["data"]["sidebar"][i]["name"]
        sarasas1.append(data1)
        sarasas2.append(data2)
        sarasas3.append(laikotarpis)
        # print(data1, data2, laikotarpis)

# Creating dictionary to append to DataFrame later on in 349 line
    data = {
        "Old_Date": sarasas3,
        "Visi kelių eismo įvykiai": sarasas1,
        "Dėl neblaivių vairuotojų kaltės": sarasas2
    }

    df = pd.DataFrame(data)

# Formating DataFrame to desirable result. Splitting one collumn od data in to two, so that there would appear year and month in seperate columns
    df["Year"] = df["Old_Date"].str.split(pat='M', n=0, expand=True)[0]
    df["Month"] = df["Old_Date"].str.split(pat='M', n=0, expand=True)[1]
    df.drop(columns=['Old_Date'], inplace=True)

# Reindexing columns as well as filtering only year 2023 as well as moderarating collumn ['Visi kelių eismo įvykiai'] in order to avoid error in Run window using 'list(map(int)' method
    df = df.reindex(columns=['Year', 'Month', 'Visi kelių eismo įvykiai', 'Dėl neblaivių vairuotojų kaltės'])
    df = df.loc[df["Year"] == "2023"]
    df['Visi kelių eismo įvykiai'] = list(map(int, df['Visi kelių eismo įvykiai']))

    # print(df)

# Saving DataFrame to CSV in order to use the file in the following analysis and not scraping the website everytime the data is needed.
    df.to_csv("CSV/Road_Accidents_LT_2023.csv", index=False)


# lietuvos_duomenu_scraping()



# Scraping Total Amount of deathly Road Accidents data in selected EU countries in 2021 from OECD
# Using Json method
def oecd_data_scraping():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        'value': 'application/json, text/plain, */*',
        'accept': 'application/json, text/plain, */*',
        'cookie': '_ga=GA1.2.1272715160.1699462284; _gid=GA1.2.1647336826.1699462284; _ga_E8WJ6X0RYN=GS1.2.1699471615.3.0.1699471615.60.0.0; _ga_162SQ74LLR=GS1.2.1699471697.2.1.1699471698.0.0.0'
    }
    url = "https://stats.oecd.org/sdmx-json/data/DP_LIVE/.ROADACCID.DEATH.1000000HAB.A/OECD?json-lang=en&dimensionAtObservation=allDimensions&startPeriod=1970"

    page = requests.get(url, headers=headers)


# Setting a variable to declare the lenght of the rows in data table
    ilgis = len(page.json()["structure"]["dimensions"]["observation"][0]["values"])

# Creating lists of scraped data
    sarasiukas1 = []
    sarasiukas2 = []
    sarasiukas3 = []

# Writing for loop to extract data from the source and appending it to previuosly created lists above
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

# Creating dictionary to append to DataFrame later on in 414 line
    data = {
        "Country": sarasiukas1,
        "Amount of accidents 2020": sarasiukas2,
        "Amount of accidents 2021": sarasiukas3
    }

# Setting the function 'orient' to ensure that row in the right side of the table is not an index value as well as transposing DataFrame
    df = pd.DataFrame.from_dict(data, orient="index").transpose()
# Using .convert_dtypes() method to allow rounding of the values in the collumn "Amount of accidents 2021"
    df = df.loc[df["Amount of accidents 2021"] != "ok"].convert_dtypes().round(2)
    # print(df)

# Selecting countries from all data list, in other words filtered relevant data
    countries = ['Lithuania', 'Switzerland', 'Poland', 'Germany', 'France', 'Belgium', 'Italy', 'Sweden']

# Creating list of selected countries in order to run for loop and get relevant data table with only selected countries
    countries_from_list = []

# Writing for loop to extract data from the DataFrame above (with all countries in the table) and appending it to list with only selected countries
    for i in countries:
        selecting_countries = df.loc[df['Country'] == i]
        countries_from_list.append(selecting_countries)

# Concatenating data and saving to to CSV file format
    df = pd.concat(countries_from_list).reset_index()
    df.to_csv('CSV/Sorted_EU_data.csv', index=False)


# oecd_data_scraping()


# Creating a chart for Road Accidents Amount in Lithuania per month during 2023
def lt_2023_grafikas():
    if os.path.isfile('CSV/Road_Accidents_LT_2023.csv'):
        lt_2023 = pd.read_csv('CSV/Road_Accidents_LT_2023.csv')

        plt.figure(figsize=(15, 10))
        plt.plot(lt_2023['Month'], lt_2023['Visi kelių eismo įvykiai'], color="green")
        plt.xlabel('Months')
        plt.ylabel('Amount')
        plt.title(f"Road Accidents' amount per month during 2023 in Lithuania ")
        plt.show()
# Setting options to choose from if there is no scrapped and saved CSV file in order to create one and then extract needed data
    else:
        print("Seems like you don`t have 'Road_Accidents_LT_2023.csv' file yet. Would you like to create it now? Enter Y for yes and N for no: ")
        create_or_not = input()
        if create_or_not == 'Y':
            lietuvos_duomenu_scraping()
            print("File 'Road_Accidents_LT_2023.csv' was created successfully!")
            lt_2023_grafikas()
        elif create_or_not == 'N':
            print("File 'Road_Accidents_LT_2023.csv' will not be created.")
        else:
            print("Wrong input! I`ll take it as a No.")


# lt_2023_grafikas()


# Creating a chart for Road Accidents Amount in Lithuania per region and per month during 2022 or 2023
def lietuvos_regionu_grafikas_22_23():
    df = pd.read_csv("CSV/Road_Accidents_LT_22_23.csv")
    df = df[df['Administracinė teritorija'].notna()]

    df["Year"] = df["Laikotarpis"].str.split(pat='M', n=0, expand=True)[0]
    df["Month"] = df["Laikotarpis"].str.split(pat='M', n=0, expand=True)[1]

    df.drop(columns=['Rodiklis', 'Matavimo vienetai', 'Laikotarpis'], inplace=True)

    df = df.reindex(columns=['Year', 'Month', 'Administracinė teritorija', 'Reikšmė'])

# Here you can choose the year as the DataFrame contains values from 2022 or 2023
    pasirinkimas = input("Please choose date to analyze (either 2022 or 2023): ")

    # df.to_csv("CSV/Programiskai pakoreguotas failas.csv", index = False)
# Filtering and sorting data to extract only needed and without logical conflicts
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
    # df.to_csv("CSV/Programiskai pakoreguotas failas.csv", index=True)

# Adding labels to chart bars within addLabels function
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

# lietuvos_regionu_grafikas_22_23()



# Creating a chart for deathly Road Accidents Amount in selected EU countries during 2021
def europos_duomenys_20_21():
    if os.path.isfile('CSV/Sorted_EU_data.csv'):
        df = pd.read_csv('CSV/Sorted_EU_data.csv')

# Adding labels to the bars of the chart
        def addlabels(x, y):
            for i in range(len(x)):
                plt.text(i, y[i], y[i], ha='center')

        plt.figure(figsize=(15, 10))
        plt.bar(df['Country'], df['Amount of accidents 2021'], color="purple")
        plt.xlabel('Country')
        plt.ylabel('Amount')
        plt.title('Amount of deathly accidents 2021 in given Countries')
        addlabels(df['Country'], df['Amount of accidents 2021'])
        plt.show()

# Setting options to choose from if there is no scrapped and saved CSV file in order to create one and then extract needed data
    else:
        print("Seems like you don`t have 'Sorted_EU_data.csv' file yet. Would you like to create it now? Enter Y for yes and N for no: ")
        create_or_not = input()
        if create_or_not == 'Y':
            oecd_data_scraping()
            print("Sorted_EU_data.csv' was created successfully!")
            europos_duomenys_20_21()
        elif create_or_not == 'N':
            print("File 'Sorted_EU_data.csv' will not be created.")
        else:
            print("Wrong input! I`ll take it as a No.")


# europos_duomenys_20_21()




############### Meniu ###############
def meniu():
    print("--------------------Meniu--------------------")
    print("1. Create a csv with real time traffic intensity data in Lithunia.")
    print("2. Create a csv with real time information about roads condition.")
    print("3. Information about the road conditions on the selected roads in real time.")
    print("4. Information about the road conditions on the selected roads in all collected data.")
    print("5. Information about the road conditions on the selected roads in all collected data by selected day.")
    print("6. Total number of road accidents in Lithuania per month during 2023.")
    print("7. Total Number of road accidents per Region in 2022 or 2023.")
    print("8. Total number of deathly road accidents in given EU countries during 2021.")
    print("9. Exit ")
# meniu()

def meniu_controller():
    while True:
        meniu()
        pasirinkimas = input("Choose your action (1-9): ")
        if pasirinkimas == "1":
            scrape_road_traffic_intensity_real_time()
        elif pasirinkimas == "2":
            scrape_road_info_real_time()
        elif pasirinkimas == "3":
            chosen_roads_real_time_data()
        elif pasirinkimas == "4":
            avg_road_info_from_all_collected_data()
        elif pasirinkimas == "5":
            avg_on_the_road_from_collected_data_by_day()
        elif pasirinkimas == "6":
            lt_2023_grafikas()
        elif pasirinkimas == "7":
            lietuvos_regionu_grafikas_22_23()
        elif pasirinkimas == "8":
            europos_duomenys_20_21()
        elif pasirinkimas == "9":
            print("See you soon!")
            break
        else:
            print("OOPS! Wrong choice! Please choose between 1 and 9")

meniu_controller()





