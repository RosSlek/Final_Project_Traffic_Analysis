import pandas as pd
import requests
import matplotlib.pyplot as plt
import os.path

############### Function To Scrape Road Info Real Time ###############
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

    data = page.json()

    ############### DataFrame Clearance ###############

    df = pd.DataFrame(data)

    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df['date'] = df['date'] + pd.Timedelta(hours=2)

    df['Date'] = pd.to_datetime(df['date']).dt.date
    df['Time'] = pd.to_datetime(df['date']).dt.time

    df.drop(columns=['color', 'importance', 'x', 'y', 'km', 'date'], inplace=True)
    df.rename(columns={'id': 'Measuring_Station_ID', 'name': 'Location', 'roadName': 'Road_Name', 'roadNr': 'Road', 'airTemperature': 'Air_Temperature', 'windDirection': 'Wind_Direction', 'windSpeed': 'Wind_Speed', 'precipitationType': 'Precipitation_Type', 'precipitationIntensity': 'Precipitation_Intensity', 'dewPoint': 'Dew_point', 'roadTemperature': 'Road_Surface_Temperature', 'surfaceCondition': 'Road_Surface_Condition', 'friction': 'Friction'}, inplace=True)
    df['Road_Name'] = df['Road_Name'].str.replace('*', '')

    ############### Saving Real Time Data as CSV ###############

    df.to_csv("Road_info_real_time.csv", index=False)

# scrape_road_info_real_time()

############### Function To Create Chosen Roads List ###############
def chosen_roads():
    roads = ['Vilnius–Kaunas–Klaipėda', 'Kaunas–Marijampolė–Suvalkai', 'Klaipėda–Liepoja', 'Antakalnis–Jieznas–Alytus–Merkinė', 'Jonava–Kėdainiai–Šeduva', 'Daugpilis–Rokiškis–Panevėžys', 'Kalvarija–Gražiškiai–Vištytis', 'Panevėžys–Šiauliai', 'Vilnius–Panevėžys', 'Vilnius–Varėna–Gardinas']
    return roads

############### Function To Create Chosen Roads Real Time Data CSV ###############
def chosen_roads_real_time_data():

    if os.path.isfile('Road_info_real_time.csv'):

        df_rt = pd.read_csv('Road_info_real_time.csv')

        roads_rt = chosen_roads()
        chosen_roads_rt = []
        for i in roads_rt:
            selecting_road_rt = df_rt.loc[df_rt['Road_Name'] == i]
            chosen_roads_rt.append(selecting_road_rt)

        df_chosen_roads_rt = pd.concat(chosen_roads_rt)
        df_chosen_roads_rt.to_csv('Chosen_roads_real_time.csv', index=False)
    else:
        print("Seems like you don`t have 'Road_info_real_time.csv' file yet. Would you like to create it now? Enter Y for yes and N for no: ")
        create_or_not = input()
        if create_or_not == 'Y':
            scrape_road_info_real_time()
            print("File 'Road_info_real_time.csv' was created successfully!")
        elif create_or_not == 'N':
            print("File 'Road_info_real_time.csv' will not be created.")
        else:
            print("Wrong input! I`ll take it as a No.")

# chosen_roads_real_time_data()

############### Function To Create Chosen Roads Periodical Data CSV ###############
def chosen_roads_periodical_data():
    if os.path.isfile('Road_info_periodical.csv'):
        df_pd = pd.read_csv('Road_info_periodical.csv')

        roads_pd = chosen_roads()
        chosen_roads_pd = []
        for i in roads_pd:
            selecting_road_pd = df_pd.loc[df_pd['Road_Name'] == i]
            chosen_roads_pd.append(selecting_road_pd)

        df_chosen_roads_pd = pd.concat(chosen_roads_pd).reset_index()
        df_chosen_roads_pd.to_csv('Chosen_roads_periodical.csv', index=False)
        print("File 'Chosen_roads_periodical.csv' was created successfully!")
    else:
        print("Sorry, you have not collected any periodical data yet! Try again after collecting some data with 'Script_Road_info_periodical'.")

# chosen_roads_periodical_data()

############### Averages From All Collected Data ###############
def avg_road_info_from_all_collected_data():
    if os.path.isfile('Chosen_roads_periodical.csv'):
        df = pd.read_csv('Chosen_roads_periodical.csv')

        mean_day_t_all_data = df.groupby('Road_Name')['Air_Temperature'].mean().round(1).reset_index()
        mean_day_t_all_data.drop(columns=['Road_Name'], inplace=True)
        mean_day_wind_all_data = df.groupby('Road')['Wind_Speed'].mean().round(1).reset_index()
        mean_day_road_surface_t = df.groupby('Road_Name')['Road_Surface_Temperature'].mean().round(1).reset_index()

        df_mean_of_all_data = pd.concat([mean_day_t_all_data, mean_day_wind_all_data, mean_day_road_surface_t], axis=1, join='inner')
        df_mean_of_all_data = df_mean_of_all_data[['Road_Name', 'Road', 'Air_Temperature', 'Road_Surface_Temperature', 'Wind_Speed']]
        print(df_mean_of_all_data)

        plt.figure(figsize=(10,5))
        plt.bar(df_mean_of_all_data['Road'], df_mean_of_all_data['Road_Surface_Temperature'], color='gold')
        plt.title('Average temperature of chosen roads from all collected data')
        plt.ylabel('Air temperature')
        plt.xlabel('Road')
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.bar(df_mean_of_all_data['Road'], df_mean_of_all_data['Road_Surface_Temperature'], color='green')
        plt.title('Average road surface temperature of chosen roads from all collected data')
        plt.ylabel('Road surface temperature')
        plt.xlabel('Road')
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.bar(df_mean_of_all_data['Road'], df_mean_of_all_data['Wind_Speed'],color='firebrick')
        plt.title('Average wind speed of chosen roads from all collected data')
        plt.ylabel('Wind speed')
        plt.xlabel('Road')
        plt.show()
    else:
        print("Seems like you don`t have 'Chosen_roads_periodical.csv' file yet. Would you like to create it now? Enter Y for yes and N for no: ")
        create_or_not = input()
        if create_or_not == 'Y':
            chosen_roads_periodical_data()
            print("Would you like to create file")
            avg_road_info_from_all_collected_data()
        elif create_or_not == 'N':
            print("File 'Chosen_roads_periodical.csv' will not be created.")
        else:
            print("Wrong input! I`ll take it as a No.")

# avg_road_info_from_all_collected_data()

############### Averages From All Collected Data By Selected Day ###############
def avg_on_the_road_from_collected_data_by_day():
    if os.path.isfile('Chosen_roads_periodical.csv'):
        df_by_day = pd.read_csv('Chosen_roads_periodical.csv')
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

                df_by_day_avg = pd.concat([avg_t_by_day, avg_wind_speed_by_day, avg_rs_t_by_day], axis=1)
                df_by_day_avg = df_by_day_avg[['Road_Name', 'Road', 'Air_Temperature', 'Road_Surface_Temperature', 'Wind_Speed']]
                print(df_by_day_avg)

                plt.figure(figsize=(10, 5))
                plt.bar(df_by_day_avg['Road'], df_by_day_avg['Air_Temperature'], color='gold')
                plt.title('Average temperature of chosen roads for a selected day')
                plt.ylabel('Air temperature')
                plt.xlabel('Road')
                plt.show()

                plt.figure(figsize=(10, 5))
                plt.bar(df_by_day_avg['Road'], df_by_day_avg['Road_Surface_Temperature'], color='green')
                plt.title('Average road surface temperature of chosen roads for a selected day')
                plt.ylabel('Road surface temperature')
                plt.xlabel('Road')
                plt.show()

                plt.figure(figsize=(10, 5))
                plt.bar(df_by_day_avg['Road'], df_by_day_avg['Wind_Speed'], color='firebrick')
                plt.title('Average wind speed of chosen roads for a selected day')
                plt.ylabel('Wind speed')
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
            avg_on_the_road_from_collected_data_by_day()
        elif create_or_not == 'N':
            print("File 'Chosen_roads_periodical.csv' will not be created.")
        else:
            print("Wrong input! I`ll take it as a No.")

# avg_on_the_road_from_collected_data_by_day()