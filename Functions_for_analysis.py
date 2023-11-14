import pandas as pd
import matplotlib.pyplot as plt

############### Function To Create Chosen Roads List ###############
def chosen_roads():
    roads = ['Vilnius–Kaunas–Klaipėda', 'Kaunas–Marijampolė–Suvalkai', 'Klaipėda–Liepoja', 'Antakalnis–Jieznas–Alytus–Merkinė', 'Jonava–Kėdainiai–Šeduva', 'Daugpilis–Rokiškis–Panevėžys', 'Kalvarija–Gražiškiai–Vištytis', 'Panevėžys–Šiauliai', 'Vilnius–Panevėžys', 'Vilnius–Varėna–Gardinas']
    return roads

############### Function To Create Chosen Roads Real Time Data CSV ###############
def chosen_roads_real_time_data():
    df_rt = pd.read_csv('Road_info_real_time.csv')

    roads_rt = chosen_roads()
    chosen_roads_rt = []
    for i in roads_rt:
        selecting_road_rt = df_rt.loc[df_rt['Road_Name'] == i]
        chosen_roads_rt.append(selecting_road_rt)

    df_chosen_roads_rt = pd.concat(chosen_roads_rt)
    df_chosen_roads_rt.to_csv('Chosen_roads_real_time.csv', index=False)

# chosen_roads_real_time_data()

############### Function To Create Chosen Roads Periodical Data CSV ###############
def chosen_roads_periodical_data():
    df_pd = pd.read_csv('Road_info_periodical.csv')

    roads_pd = chosen_roads()
    chosen_roads_pd = []
    for i in roads_pd:
        selecting_road_pd = df_pd.loc[df_pd['Road_Name'] == i]
        chosen_roads_pd.append(selecting_road_pd)

    df_chosen_roads_pd = pd.concat(chosen_roads_pd).reset_index()
    df_chosen_roads_pd.to_csv('Chosen_roads_periodical.csv', index=False)

# chosen_roads_periodical_data()

############### Averages From All Collected Data ###############
def avg_road_info_from_all_collected_data():
    chosen_roads_periodical_data()

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

# avg_road_info_from_all_collected_data()

############### Averages From All Collected Data By Selected Day ###############
def avg_on_the_road_from_collected_data_by_day():
    chosen_roads_periodical_data()
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

# avg_on_the_road_from_collected_data_by_day()