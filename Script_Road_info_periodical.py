import requests
import pandas as pd
import time
import schedule
import os.path

############### creating script to collect data periodically ###############
def script_info_periodially():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        'value': 'application/json, text/plain, */*',
        'accept': 'application/json, text/plain, */*',
        'cookie': '_ga=GA1.2.1272715160.1699462284; _gid=GA1.2.1647336826.1699462284; _ga_E8WJ6X0RYN=GS1.2.1699471615.3.0.1699471615.60.0.0; _ga_162SQ74LLR=GS1.2.1699471697.2.1.1699471698.0.0.0'
    }

    # https://eismoinfo.lt/#!/ information from page
    url = "https://eismoinfo.lt/eismoinfo-backend/osi-info-table"

    page = requests.get(url, headers=headers)

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

    ############### Saving periodical data as new CSV or adding new data on the same if it exsists ###############

    if os.path.isfile('CSV/Road_info_periodical.csv'):
        df.to_csv("CSV/Road_info_periodical.csv", mode='a', index=False, header=False)
        print("Data updated successfully!")
    else:
        df.to_csv("CSV/Road_info_periodical.csv", index=False, header=True)
        print("File Road_info_periodical was created successfully!")

# script_info_periodially()

############### setting schedule to collect data every 6 hours and putting sleep timer for the same period ###############

schedule.every().day.at("03:30").do(script_info_periodially)
schedule.every().day.at("09:30").do(script_info_periodially)
schedule.every().day.at("15:30").do(script_info_periodially)
schedule.every().day.at("21:30").do(script_info_periodially)

while True:
    schedule.run_pending()
    time.sleep(21600)