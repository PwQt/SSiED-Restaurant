import csv
import sys
import pandas as pd
import numpy as np
import matplotlib as mtpllib


air_reserve = pd.read_csv('data/air_reserve.csv', encoding='utf-8')
air_store_info = pd.read_csv('data/air_store_info.csv', encoding='utf-8')
air_visit_data = pd.read_csv('data/air_visit_data.csv', encoding='utf-8')
date_info = pd.read_csv('data/date_info.csv')
hpg_reserve = pd.read_csv('data/hpg_reserve.csv')
hpg_store_info = pd.read_csv('data/hpg_store_info.csv')
store_id_relation = pd.read_csv('data/store_id_relation.csv')

sample_submission = pd.read_csv('data/sample_submission.csv')

joined = air_reserve.set_index('air_store_id').join(air_store_info.set_index('air_store_id'))
air_data = joined.join(air_visit_data.set_index('air_store_id'))

with pd.option_context('display.max_rows', 10, 'display.max_columns', None):
    print(air_data)
    sys.stdin.read(1)