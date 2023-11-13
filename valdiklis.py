import pandas as pd
from datetime import datetime
df = pd.read_csv('Road_info_real_time.csv')

# print(df)
# print(df.columns)

###### Informacija apie konkretu kelia ######



########### vidurkiai is visu duomenu ##############

# vid_dienos_t_kelyje_viso = df.groupby('Road_Name')['Air_Temperature'].mean().round(1)
# vid_dienos_vejas_viso = df.groupby('Road_Name')['Wind_Speed'].mean().round(1)
# vid_dienos_pavirsiaus_t_viso = df.groupby('Road_Name')['Road_Surface_Temperature'].mean().round(1)
# df1 = pd.concat([vid_dienos_t_kelyje_viso, vid_dienos_vejas_viso, vid_dienos_pavirsiaus_t_viso], axis=1)
# print(df1)

############ vidurkiai konkrecios datos ###########

# try:
#     df.Date = pd.to_datetime(df.Date)
#     pasirinkimas = pd.to_datetime(input('Input date in mm-dd-yyyy format: '))
#     pasirinktos_dienos = df.loc[df['Date'] == pasirinkimas]
#     #print(pasirinktos_dienos)
#     if pasirinktos_dienos.empty:
#         print("Where is no data about selected date!")
#     else:
#         vid_dienos_t_kelyje = pasirinktos_dienos.groupby('Road_Name')['Air_Temperature'].mean().round(1)
#         vid_dienos_vejas = pasirinktos_dienos.groupby('Road_Name')['Wind_Speed'].mean().round(1)
#         vid_dienos_pavirsiaus_t = pasirinktos_dienos.groupby('Road_Name')['Road_Surface_Temperature'].mean().round(1)
#         df2 = pd.concat([vid_dienos_t_kelyje, vid_dienos_vejas, vid_dienos_pavirsiaus_t], axis=1)
#         print(df2)
# except:
#     print("Wrong date input!")



