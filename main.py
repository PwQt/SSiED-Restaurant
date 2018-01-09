import csv
import sys
import pandas as pd
import numpy as np
import matplotlib as mtpllib
from sklearn import *
from datetime import datetime
import re, glob


data = {
    'avd': pd.read_csv('data/air_visit_data.csv'),
    'asi': pd.read_csv('data/air_store_info.csv'),
    'hsi': pd.read_csv('data/hpg_store_info.csv'),
    'ar': pd.read_csv('data/air_reserve.csv'),
    'hr': pd.read_csv('data/hpg_reserve.csv'),
    'sir': pd.read_csv('data/store_id_relation.csv'),
    'ss': pd.read_csv('data/sample_submission.csv'),
    'di': pd.read_csv('data/date_info.csv').rename(columns={'calendar_date':'visit_date'})
    }

data['hr'] = pd.merge(data['hr'], data['sir'], how='inner', on=['hpg_store_id'])

print(data['ar'].head())
print('======================================')
print(data['hr'].head())
print('======================================')

for df in ['ar','hr']:
    data[df]['visit_datetime'] = pd.to_datetime(data[df]['visit_datetime'])
    data[df]['visit_datetime'] = data[df]['visit_datetime'].dt.date
    data[df]['reserve_datetime'] = pd.to_datetime(data[df]['reserve_datetime'])
    data[df]['reserve_datetime'] = data[df]['reserve_datetime'].dt.date
    data[df]['reserve_datetime_diff'] = data[df].apply(lambda r: (r['visit_datetime'] - r['reserve_datetime']).days, axis=1)

print(data['ar'].head())
print('======================================')

for df in ['ar','hr']:
    tmp1 = data[df].groupby(['air_store_id','visit_datetime'], as_index=False)[['reserve_datetime_diff', 'reserve_visitors']].sum().rename(columns={'visit_datetime':'visit_date', 'reserve_visitors':'rv1'})
    tmp2 = data[df].groupby(['air_store_id','visit_datetime'], as_index=False)[['reserve_datetime_diff', 'reserve_visitors']].mean().rename(columns={'visit_datetime':'visit_date', 'reserve_visitors':'rv2'})
    data[df] = pd.merge(tmp1, tmp2, how='inner', on=['air_store_id','visit_date'])


print(tmp1.head())
print('======================================')
print(tmp2.head())
print('======================================')

data['avd']['visit_date'] = pd.to_datetime(data['avd']['visit_date'])
data['avd']['dow'] = data['avd']['visit_date'].dt.dayofweek
data['avd']['year'] = data['avd']['visit_date'].dt.year
data['avd']['month'] = data['avd']['visit_date'].dt.month
data['avd']['visit_date'] = data['avd']['visit_date'].dt.date

data['ss']['visit_date'] = data['ss']['id'].map(lambda x: str(x).split('_')[2])
data['ss']['air_store_id'] = data['ss']['id'].map(lambda x: '_'.join(x.split('_')[:2]))
data['ss']['visit_date'] = pd.to_datetime(data['ss']['visit_date'])
data['ss']['dow'] = data['ss']['visit_date'].dt.dayofweek
data['ss']['year'] = data['ss']['visit_date'].dt.year
data['ss']['month'] = data['ss']['visit_date'].dt.month
data['ss']['visit_date'] = data['ss']['visit_date'].dt.date

unique_stores = data['ss']['air_store_id'].unique()
stores = pd.concat([pd.DataFrame({'air_store_id': unique_stores, 'dow': [i]*len(unique_stores)}) for i in range(7)], axis=0, ignore_index=True).reset_index(drop=True)

tmp = data['avd'].groupby(['air_store_id','dow'], as_index=False)['visitors'].min().rename(columns={'visitors':'min_visitors'})
stores = pd.merge(stores, tmp, how='left', on=['air_store_id','dow'])
tmp = data['avd'].groupby(['air_store_id','dow'], as_index=False)['visitors'].mean().rename(columns={'visitors':'mean_visitors'})
stores = pd.merge(stores, tmp, how='left', on=['air_store_id','dow'])
tmp = data['avd'].groupby(['air_store_id','dow'], as_index=False)['visitors'].median().rename(columns={'visitors':'median_visitors'})
stores = pd.merge(stores, tmp, how='left', on=['air_store_id','dow'])
tmp = data['avd'].groupby(['air_store_id','dow'], as_index=False)['visitors'].max().rename(columns={'visitors':'max_visitors'})
stores = pd.merge(stores, tmp, how='left', on=['air_store_id','dow'])
tmp = data['avd'].groupby(['air_store_id','dow'], as_index=False)['visitors'].count().rename(columns={'visitors':'count_observations'})

stores = pd.merge(stores, tmp, how='left', on=['air_store_id','dow'])
print(stores.head())
print('======================================')

stores = pd.merge(stores, data['asi'], how='left', on=['air_store_id'])
print(stores.head())
print('======================================')

lbl = preprocessing.LabelEncoder()
stores['air_genre_name'] = lbl.fit_transform(stores['air_genre_name'])
stores['air_area_name'] = lbl.fit_transform(stores['air_area_name'])
print(stores.head())
print('======================================')

data['di']['visit_date'] = pd.to_datetime(data['di']['visit_date'])
data['di']['day_of_week'] = lbl.fit_transform(data['di']['day_of_week'])
data['di']['visit_date'] = data['di']['visit_date'].dt.date
print(data['di'].head())
print('======================================')


train = pd.merge(data['avd'], data['di'], how='left', on=['visit_date'])
test = pd.merge(data['ss'], data['di'], how='left', on=['visit_date'])
print(train.head())
print('======================================')
print(test.head())
print('======================================')

for df in ['ar','hr']:
    train = pd.merge(train, data[df], how='left', on=['air_store_id','visit_date'])
    test = pd.merge(test, data[df], how='left', on=['air_store_id','visit_date'])
print(train.head())
print('======================================')
print(test.head())
print('======================================')

train['sir'] = train.apply(lambda r: '_'.join([str(r['air_store_id']), str(r['visit_date'])]), axis=1)
train['total_reserv_sum'] = train['rv1_x'] + train['rv1_y']
train['total_reserv_mean'] = (train['rv2_x'] + train['rv2_y']) / 2
test['total_reserv_sum'] = test['rv1_x'] + test['rv1_y']
test['total_reserv_mean'] = (test['rv2_x'] + test['rv2_y']) / 2

col = [c for c in train if c not in ['sir', 'air_store_id','visit_date','visitors']]
print(train.describe())
print('======================================')
print(train.head())
print('======================================')
print(train.columns)
print('======================================')

train = train.fillna(-1)
test = test.fillna(-1)

def RMSLE(y, pred):
    return metrics.mean_squared_error(y, pred)**0.5


from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(train[col], train['visitors'], test_size=0.33, random_state=42)
print(X_train.head())
print(len(X_train))
print(len(X_val))
print('======================================')

model1 = ensemble.GradientBoostingRegressor(learning_rate = 0.1, n_estimators = 375, max_depth = 6, min_samples_leaf = 2)

model1.fit(train[col], np.log1p(train['visitors'].values))

print('RMSE GradientBoostingRegressor: ', RMSLE(np.log1p(train['visitors'].values), model1.predict(train[col])))
print('======================================')
test['visitors'] = model1.predict(test[col])
test['visitors'] = np.expm1(test['visitors']).clip(lower=0.)
sub1 = test[['id','visitors']].copy()

print(sub1.head())
print('======================================')

sub1[['id', 'visitors']].to_csv('submission.csv', index=False)