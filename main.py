import csv
import pandas as pd
import numpy as np
import matplotlib as mtpllib

air_reserve = pd.read_csv('data/air_reserve.csv')
air_store_info = pd.read_csv('data/air_store_info.csv')
air_visit_data = pd.read_csv('data/air_visit_data.csv')
date_info = pd.read_csv('data/date_info.csv')
hpg_reserve = pd.read_csv('data/hpg_reserve.csv')
hpg_store_info = pd.read_csv('data/hpg_store_info.csv')
store_id_relation = pd.read_csv('data/store_id_relation.csv')

sample_submission = pd.read_csv('data/sample_submission.csv')
print(sample_submission)
##Pobranie z pliku Air_Reserver do tabeli air_reserve
'''air_reserve = []
with open('data/air_reserve.csv','r') as csvfile:
    next(csvfile,None)
    filereader = csv.reader(csvfile)
    for row in filereader:
        air_reserve.append({'air_store_id': row[0], 'visit_datetime': row[1], 'reserve_datetime': row[2], 'reserve_visitors': row[3]})

air_store_info = []
with open('data/air_store_info.csv','r') as csvfile:
    next(csvfile,None) #pominiecie nagłówka
    filereader = csv.reader(csvfile)
    for row in filereader:
        air_store_info.append({'air_store_id': row[0], 'air_genre_name': row[1], 'air_area_name': row[2], 'latitude': row[3], 'longitude': row[4]})
        

air_visit_data = []
with open('data/air_visit_data.csv','r') as csvfile:
    next(csvfile,None) #pominiecie nagłówka
    filereader = csv.reader(csvfile)
    for row in filereader:
        air_visit_data.append({'air_store_id': row[0], 'visit_date': row[1], 'visitors': row[2]})

date_info = []
with open('data/date_info.csv','r') as csvfile:
    next(csvfile,None) #pominiecie nagłówka
    filereader = csv.reader(csvfile)
    for row in filereader:
        date_info.append({'calendar_date': row[0], 'day_of_week': row[1], 'holiday_flg': row[2]})

hpg_reserve = []
with open('data/hpg_reserve.csv','r') as csvfile:
    next(csvfile,None)
    filereader = csv.reader(csvfile)
    for row in filereader:
        hpg_reserve.append({'hpg_store_id': row[0], 'visit_datetime': row[1], 'reserve_datetime': row[2], 'reserve_visitors': row[3]})

hpg_store_info = []
with open('data/hpg_store_info.csv','r') as csvfile:
    next(csvfile,None) #pominiecie nagłówka
    filereader = csv.reader(csvfile)
    for row in filereader:
        hpg_store_info.append({'hpg_store_id': row[0], 'hpg_genre_name': row[1], 'hpg_area_name': row[2], 'latitude': row[3], 'longitude': row[4]})

sample_submission = []
with open('data/sample_submission.csv','r') as csvfile:
    next(csvfile,None) #pominiecie nagłówka
    filereader = csv.reader(csvfile)
    for row in filereader:
        sample_submission.append({'id': row[0], 'visitors': row[1]})

store_id_relation = []
with open('data/store_id_relation.csv','r') as csvfile:
    next(csvfile,None) #pominiecie nagłówka
    filereader = csv.reader(csvfile)
    for row in filereader:
        store_id_relation.append({'air_store_id': row[0], 'hpg_store_id': row[1]})'''