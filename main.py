import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import csv
from statistics import mean, median,variance,stdev
from datetime import datetime
import glob, re

## Import danych z pliku CSV
data = {
    'avd': pd.read_csv('data/air_visit_data.csv'),
    'asi': pd.read_csv('data/air_store_info.csv'),
    'hsi': pd.read_csv('data/hpg_store_info.csv'),
    'ar': pd.read_csv('data/air_reserve.csv'),
    'hr': pd.read_csv('data/hpg_reserve.csv'),
    'sir': pd.read_csv('data/store_id_relation.csv'),
    'ss': pd.read_csv('data/sample_submission.csv'),
    'di': pd.read_csv('data/date_info.csv')
    }

## Utworzenie bazy na tabelach rezerwacji w restauracjach z tabelą relacji pomiedzy restauracjami
data['hr'] = pd.merge(data['hr'], data['sir'], how='left', on=['hpg_store_id'])
data['ar'] = pd.merge(data['ar'], data['sir'], how='left', on=['air_store_id'])

## Rozdzielenie kolumn DateTime na Rok | Miesiąc | Data (format YYYY-MM-DD). Po rozdzieleniu usuniecie starych kolumn
## Dla daty wizyty w HPG
data['hr']['visit_datetime'] = pd.to_datetime(data['hr']['visit_datetime'])
data['hr']['visit_year'] = data['hr']['visit_datetime'].dt.year
data['hr']['visit_month'] = data['hr']['visit_datetime'].dt.month
data['hr']['visit_date'] = data['hr']['visit_datetime'].dt.date
data['hr'] = data['hr'].drop('visit_datetime',axis=1)

## Dla daty wizyty w AIR
data['ar']['visit_datetime'] = pd.to_datetime(data['ar']['visit_datetime'])
data['ar']['visit_year'] = data['ar']['visit_datetime'].dt.year
data['ar']['visit_month'] = data['ar']['visit_datetime'].dt.month
data['ar']['visit_date'] = data['ar']['visit_datetime'].dt.date
data['ar'] = data['ar'].drop('visit_datetime',axis=1)

## Dla rezerwacji w HPG
data['hr']['reserve_datetime'] = pd.to_datetime(data['hr']['reserve_datetime'])
data['hr']['reserve_year'] = data['hr']['reserve_datetime'].dt.year
data['hr']['reserve_month'] = data['hr']['reserve_datetime'].dt.month
data['hr']['reserve_date'] = data['hr']['reserve_datetime'].dt.date
data['hr'] = data['hr'].drop('reserve_datetime',axis=1)

## Dla rezerwacji w AIR
data['ar']['reserve_datetime'] = pd.to_datetime(data['ar']['reserve_datetime'])
data['ar']['reserve_year'] = data['ar']['reserve_datetime'].dt.year
data['ar']['reserve_month'] = data['ar']['reserve_datetime'].dt.month
data['ar']['reserve_date'] = data['ar']['reserve_datetime'].dt.date
data['ar'] = data['ar'].drop('reserve_datetime',axis=1)

## Dla daty wizyty w AIR
data['avd']['visit_datetime'] = pd.to_datetime(data['avd']['visit_date'])
data['avd']['visit_year'] = data['avd']['visit_datetime'].dt.year
data['avd']['visit_month'] = data['avd']['visit_datetime'].dt.month
data['avd']['visit_date'] = data['avd']['visit_datetime'].dt.date
data['avd'] = data['avd'].rename(columns={'visit_date':'visit_date'})
data['avd'] = data['avd'].drop('visit_datetime',axis=1)

## Podzielenie pliku date_info.csv przechowującego informacje o tym czy dana data jest świetem/weekendem, na tego samego typu wygląd co dane poprzednie
data['di']['visit_day'] = data['di']['calendar_date'].map(lambda x: (x.split('-')[2]))
data['di']['mnd_flg'] = data['di']['visit_day'].map(lambda x: 1 if int(x)>=25 else 0)
data['di']['calendar_datetime'] = pd.to_datetime(data['di']['calendar_date'])
data['di']['visit_year'] = data['di']['calendar_datetime'].dt.year
data['di']['visit_month'] = data['di']['calendar_datetime'].dt.month
data['di']['calendar_date'] = data['di']['calendar_datetime'].dt.date
data['di'] = data['di'].rename(columns={'calendar_date':'visit_date'})
data['di'] = data['di'].rename(columns={'calendar_datetime':'visit_datetime'})
non_bu = data['di'].apply((lambda x:(x.day_of_week=='Sunday' or x.day_of_week=='Saturday'or x.day_of_week=='Friday') or x.holiday_flg==1), axis=1)
data['di'] = data['di'].assign(non_buis_day = non_bu)
data['di'] = data['di'].drop('visit_datetime',axis=1)

''' Rozdzielenie kolumny ID z danych testowych na nastepujace kolumny
id_restauracji
data_wizyty
'''
data['ss']['air_store_id'] = data['ss']['id'].map(lambda x: '_'.join(x.split('_')[:2]))
data['ss']['visit_datetime'] = data['ss']['id'].map(lambda x: str(x).split('_')[2])
## Podzielenie daty w celu odpowiadania wyglądowi danym szkolącym
data['ss']['visit_datetime'] = pd.to_datetime(data['ss']['visit_datetime'])
data['ss']['visit_year'] = data['ss']['visit_datetime'].dt.year
data['ss']['visit_month'] = data['ss']['visit_datetime'].dt.month
data['ss']['visit_date'] = data['ss']['visit_datetime'].dt.date

data['ss'] = pd.merge(data['ss'], data['di'], how = 'left', on = ['visit_date','visit_year','visit_month'])
data['ss'] = pd.merge(data['ss'], data['sir'], how = 'left', on = ['air_store_id'])
data['ss'] = pd.merge(data['ss'], data['asi'], how = 'left', on = ['air_store_id'])
data['ss'] = pd.merge(data['ss'], data['hsi'], how = 'left', on = ['hpg_store_id'])
data['ss'] = data['ss'].drop('visitors',axis=1)

data['ss'] = data['ss'].fillna(0)
print('==================================================')
print("sample_submission1")
print(data['ss'])
print('==================================================')

data['avd'] = pd.merge(data['avd'], data['di'], how = 'left',on = ['visit_date','visit_year','visit_month'])
data['avd'] = pd.merge(data['avd'], data['sir'], how = 'left', on = ['air_store_id'])
data['avd'] = pd.merge(data['avd'], data['asi'], how = 'left', on = ['air_store_id'])
data['avd'] = pd.merge(data['avd'], data['hsi'], how = 'left', on = ['hpg_store_id'])

df_ah_dh = data['avd'].groupby(['air_store_id','holiday_flg','day_of_week'])['visitors'].median().reset_index()
df_ah_wh = data['avd'].groupby(['air_store_id','non_buis_day'])['visitors'].median().reset_index()


ss2 = pd.merge(data['ss'],df_ah_dh, how='left', on=['air_store_id','holiday_flg','day_of_week'])
print('==================================================')
print("sample_submission2")
print(ss2)
print(ss2.isnull().sum())
print('==================================================')

ss2_nan = ss2.visitors.isnull()
ss2_null = ss2[ss2_nan]
ss2_null = ss2_null.drop('visitors',axis=1)

ss3 = pd.merge(ss2_null,df_ah_wh, how='left', on=['air_store_id','non_buis_day'])
print('==================================================')
print("sample_submission3")
print(ss3)
print(ss3.isnull().sum())
print('==================================================')

ss2 = ss2.dropna()
ss3 = ss3.dropna()


sub = pd.concat([ss2,ss3],ignore_index = True)

submit = pd.concat([sub.id,sub.visitors],axis=1)
submit.columns = ['id','visitors']
print(submit)
submit.to_csv('submit.csv', index=False)