import csv
import sys
import pandas as pd 
import numpy as np #Wymagana zależność dla pandas
import matplotlib.pyplot as plt # Wykresy

#Import danych szkoleniowych z pliku do struktur DataFrames
air_reserve = pd.read_csv('data/air_reserve.csv', encoding='utf-8')
air_store_info = pd.read_csv('data/air_store_info.csv', encoding='utf-8')
air_visit_data = pd.read_csv('data/air_visit_data.csv', encoding='utf-8')
date_info = pd.read_csv('data/date_info.csv')
hpg_reserve = pd.read_csv('data/hpg_reserve.csv')
hpg_store_info = pd.read_csv('data/hpg_store_info.csv')
store_id_relation = pd.read_csv('data/store_id_relation.csv')

#Tu jest nasz zbiór testowy z datami
sample_submission = pd.read_csv('data/sample_submission.csv')

#Łączenie struktur testowych do jednego DataFrame
joined = air_reserve.set_index('air_store_id').join(air_store_info.set_index('air_store_id'))
air_data = joined.join(air_visit_data.set_index('air_store_id'))

#Przykładowy wykres uzyskany z istniejących danych
plt.plot(air_data['visit_date'][0:100], air_data['visitors'][0:100])
plt.title('Wizyty')
plt.show()