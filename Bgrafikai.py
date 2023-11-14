import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import psycopg2
import numpy as np
from Apagrindinis import lietuvos_regionu_data




def lt_2023_grafikas():
    lt_2023 = pd.read_csv('Eismo ivykiai.csv')
    # def addlabels(x, y):
    #     for i in range(len(x)):
    #         plt.text(i, y[i], y[i], ha='center')


    plt.figure(figsize=(15, 10))
    plt.plot(lt_2023['Month'], lt_2023['Visi kelių eismo įvykiai'], color="green")
    plt.xlabel('Mėnesiai')
    plt.ylabel('Kelių eismo įvykių skaičius')
    plt.title('Lietuvos Respublikoje įvykusių eismo įvykių suma per mėnesį')
    # addlabels(lt_2023['Month'], lt_2023['Visi kelių eismo įvykiai'])
    plt.show()

lt_2023_grafikas()

KOMENTARAS##########################
gfgdfgd

def lietuvos_regionu_grafikas_22_23():
    lietuvos_regionu_data()

lietuvos_regionu_grafikas_22_23()


def europos_duomenys_20_21():
    df = pd.read_csv('Surusiuoti Europos duomenys.csv')
    def addlabels(x, y):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], ha='center')

    plt.figure(figsize=(15, 10))
    plt.bar(df['Country'], df['Amount of accidents 2021'], color="purple")
    plt.xlabel('Country')
    plt.ylabel('Amount')
    plt.title('Amount of deathly accidents 2021')
    addlabels(df['Country'], df['Amount of accidents 2021'])
    plt.show()

europos_duomenys_20_21()



