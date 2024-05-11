import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def unix_stamp_to_date(ts):
    return datetime.fromtimestamp(ts)

def date_to_day(dt:datetime):
    return dt.days
def calculate():

    if start == True:
        start_time = datetime(2024, 2, 1)
    if end == True:
        end_time = datetime(2024, 2, 29)
    
def process(df:pd.DataFrame):
    time_col = df['timestamp'].apply(unix_stamp_to_date)
    td = df['billing_period'].apply(timedelta)
    df['start'] = time_col
    df['end'] = time_col + td
    print(df)
    df['start_before_feb'] = df['start'] < datetime(2024, 2, 1)
    #df['ends_after_feb'] = df['end'] > datetime(2024, 2, 29)
    df.loc[df['start_before_feb'],'start'] = datetime(2024, 2, 1)
    #df.loc[df['ends_after_feb'],'end'] = datetime(2024, 2, 29)
    #df.drop(columns=['start_before_feb',  'ends_after_feb'], inplace=True)

    df['days'] = (df['end'] - df['start']).apply(date_to_day)
    df['financial_input'] = df['billing_total_price_usd'] / df['billing_period'] * df['days']
    print(df)
    return 

     
df = pd.read_csv('C:\hse\year_1\contest\sample1.csv')
print(df)
process(df)

#df = df.sort_values('user_id')


users = pd.DataFrame(columns = ['user_id'])

print(df.groupby('user_id')['financial_input'].sum())
'''df = pd.read_csv("C:\hse\year_1\contest\sample_2.csv")
print(df)
print(process(df))'''

print()