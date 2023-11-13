import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Road_info_real_time.csv')

# print(df)
# print(df.columns)

###### Informacija apie konkretu kelia ######



########### vidurkiai is visu duomenu ##############

vid_dienos_t_kelyje_viso = df.groupby('Road_Name')['Air_Temperature'].mean().round(1).reset_index()
vid_dienos_vejas_viso = df.groupby('Road_Name')['Wind_Speed'].mean().round(1).reset_index()
vid_dienos_pavirsiaus_t_viso = df.groupby('Road_Name')['Road_Surface_Temperature'].mean().round(1).reset_index()

df_visu_duomenu_vidurkiai = pd.concat([vid_dienos_t_kelyje_viso, vid_dienos_vejas_viso, vid_dienos_pavirsiaus_t_viso], axis=1, join='inner')

# df_visu_duomenu_vidurkiai.drop(columns=[3], inplace=True)

print(df_visu_duomenu_vidurkiai)
# df_visu_duomenu_vidurkiai.to_csv("Road_grafikam.csv", index=False)
# svarbiausi_keliai = df_visu_duomenu_vidurkiai.loc[df_visu_duomenu_vidurkiai['Road_Name'] == 'Vilnius–Kaunas–Klaipėda']
# print(svarbiausi_keliai)
# print(vid_dienos_pavirsiaus_t_viso)
#
# plt.figure(figsize=(15,10))
# plt.bar(vid_dienos_pavirsiaus_t_viso['Road_Name'], vid_dienos_pavirsiaus_t_viso['Road_Surface_Temperature'])
# plt.title('Viso duomenu rinkimo laikotarpio temperaturos vidurkis Lietuvos keliuose')
# plt.ylabel('Air_Temperature')
# plt.xlabel('Road_name')
# plt.show()


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



############ grafikai ###########

# plt.figure(figsize=(15,5))
# plt.bar(df['savaites_dienos'], df['paros_vidurkis'])
# plt.title('Paros temperaturos vidurkis Vilniuje')
# plt.ylabel('Temperatura')
# plt.xlabel('Savaites diena')
# plt.show()