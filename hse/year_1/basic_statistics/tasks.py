import pandas as pd
import numpy as np
import datetime
import json
'''
df = pd.DataFrame([[1,2,3],
                  [1,5,6],
                  [7,8,9]],
                  index=['a','b','c'],
                  columns = ['x','y','z'])
print(df)

df['Average'] = df.iloc[:, :].mean(axis=1)
print(df)

df=df.sort_values(['x', 'y'], ascending=[True, False])
print(df)

def iqr(x:pd.Series):
    return x.quantile(0.75) - x.quantile(0.25)
df.groupby(['col1','col2'])['property'].agg(iqr).unstack()

df.pivot(index='student', columns='course', values='grade')
df.pivot_table(index='student', columns='course', values='grade', aggfunc='min')

df.melt(id_vars='student', var_name='course', value_name='grade')

df.merge(table, left_on='col1', right_on='id', how='inner')
df.merge(table, left_on='col1', right_on='id', how='left/right/outer')
'''
def mult_table(n):
    nums = [[i*j for j in range(1, n+1)] for i in range(1, n+1)]
    return pd.DataFrame(nums, index=range(1, n+1), columns=range(1,n+1))

def get_rows_after_5(df, n):
    return df[4:4+n]

def between(df, n, m):
    return df.loc[n:m]

def get_grade(df:pd.DataFrame, lastname, firstname, course):
    return int(df[(df['Last Name'] == lastname) &
              (df['First Name'] == firstname)][course].iloc[0])

def contains_null(df:pd.DataFrame):
    return np.any(df.isnull())

def gpa_top(df:pd.DataFrame):
    df['GPA'] = df.iloc[:,2:].mean(axis=1)
    df.sort_values('GPA', ascending=False, inplace=True)
    return df[df['GPA']>=4]

def weight_grades(grades:pd.DataFrame, weights):
    return grades.dot(weights)

def standartize(df:pd.DataFrame):
    mu = df.mean(axis=0)
    std = df.std(axis=0)
    return (df-mu)/std

def sort_gradebook(gradebook):
    n = len(gradebook[0]) - 3
    cols=['first_name', 'last_name',]
    cols.extend([f'grade_{i+1}' for i in range(n)])
    cols.append('final_grade')

    sort_order = ['final_grade']
    sort_order.extend([f'grade_{i+1}' for i in range(n)])
    sort_order.extend(['last_name', 'first_name',])

    order = [False]*(n+3)
    order[-2] = True
    grades = pd.DataFrame(gradebook, columns=cols)
    grades.sort_values(sort_order, ascending=order,inplace=True)

    return(grades)

def mean_grade_dict(lst):
    df = pd.DataFrame(lst)
    df = df.mean(axis=0)
    return df.to_dict()

def mean_by_group(grades, groups):
    df = pd.DataFrame([grades, groups], index=['grade', 'group']).T
    means = df.groupby('group').mean().to_dict()['grade']
    return means

def check_table(df:pd.DataFrame):
    df['Money_spent']=df['Quantity'] * df['Price']
    spent = df.groupby('Customer')['Money_spent'].sum()
    revenue = df.groupby('Item')['Money_spent'].sum()
    return spent.to_dict(), revenue.to_dict()

def make_panel(df:pd.DataFrame):
    df.reset_index(drop=False, inplace=True)
    df = df.rename(columns={'index':'firm'})
    df = df.melt(id_vars='firm', var_name='year', value_name='value')
    df = df.reindex(columns=['year', 'firm', 'value'])
    df.sort_values(['firm','year'],inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def merge_gradebooks(gradebooks):
    df = pd.DataFrame()
    for (group, x) in gradebooks:
        some = pd.concat([x , pd.DataFrame([group]*len(x), index=x.index)], axis=1)
        df = pd.concat([df, some], axis=0)
    df.rename(columns={0:'group'}, inplace=True)
    return df

def check_table_merge(df, prices):
    df = df.merge(prices, how='left', left_on='Item', right_on='item_name')
    df['Money_spent']=df['Quantity'] * df['price']
    spent = df.groupby('Customer')['Money_spent'].sum()
    revenue = df.groupby('Item')['Money_spent'].sum()
    return spent.to_dict(), revenue.to_dict()

def winner_votes(results):
    results['Max'] = results.iloc[:,2:].idxmax(axis=1)
    results = results.groupby('Max')['electors'].sum()
    results.sort_index(inplace=True)
    return (results.idxmax(), results.max())

def merge_sectors(df_emp:pd.DataFrame, df_names:pd.DataFrame):
    df_emp['code2']=df_emp['code3'] // 10
    df_emp = df_emp.merge(df_names, on='code2', how='left')
    df_emp.drop(columns='code2', inplace=True)
    df_emp.rename(columns={'name':'group_name'}, inplace=True)
    return df_emp

def make_books(df_phone, df_address):
    df_phone['Full Name'] = df_phone['First Name']+' '+ df_phone['Last Name']
    book = pd.merge(left=df_phone, right=df_address, on=['Full Name', 'State'])
    book.drop(columns=['Full Name'], inplace=True)    
    book.dropna(axis=0, subset=['Phone','Address'], inplace=True)
    print(book)
    books = []
    for state in book['State'].unique():
        books.append(book[book['State']==state].reset_index(drop=True))
    return books

def totals(purchases, goods, discounts):
    df = pd.merge(left=goods, right = purchases, left_on='good', right_on='item', how='outer')
    df['total'] = df['quantity'] * df['price']
    df['total'].fillna(0.0, inplace=True)
    df['client'].fillna(df['client'][0], inplace=True)
    df.drop(columns=['item','quantity', 'price'], inplace=True)
    df = df.merge(discounts, on='client', how='left').fillna(0.0)
    df['total'] *= (1-df['discount']/100)
    df=df.pivot_table(values='total', index = 'client', columns='good', fill_value=0)
    return df

'''def final_grades(grades:pd.DataFrame, excuses:pd.DataFrame):
    grades = grades.reset_index().rename(columns={'index':'student'})
    grades = grades.melt(id_vars='student',var_name='date', value_name='mark').fillna(0)
    grades.set_index(keys=['student', 'date'], inplace=True, drop=True)
    excuses['reason'] =  excuses['reason'].str.contains('ill')
    excuses.set_index(keys=['student', 'date'], inplace=True, drop=True)
    grades = grades.merge(excuses, left_index=True, right_index=True, how='left')
    grades['reason'].fillna(False)
    #grades.loc[grades['reason']==True,'mark'] = pd.NA
    #grades.drop(columns='reason', inplace=True)
    #grades = grades.groupby('student')['mark'].mean()
    #grades = pd.Series(grades.to_dict())
    return grades'''

def final_grades(grades:pd.DataFrame, excuses:pd.DataFrame):
    excuses['reason'] = excuses['reason'].str.contains('ill')
    excuses = excuses.pivot(index='student', columns='date', values='reason').fillna(False)    
    grades.fillna(0.0, inplace=True)
    grades[grades[excuses] == 0] = pd.NA
    return grades.mean(axis=1)

if __name__ == '__main__':
    grades = pd.DataFrame([[5, np.nan, 7, np.nan],
                        [2, np.nan, np.nan, 4]], index=['Hannah', 'Ryan'],
                        columns=pd.date_range(start="2017-02-01", freq="W",
                                                periods=4))
    excuses = pd.DataFrame([['Hannah', datetime.datetime(2017, 2, 5),
                            'was ill'],
                            ['Hannah', datetime.datetime(2017, 2, 12),
                            'illness'],
                            ['Ryan', datetime.datetime(2017, 2, 19), 'family'],
                            ['Hurray',datetime.datetime(2017, 2, 19),
                            'sport']],
                        columns=['student', 'date', 'reason'])
    
    print(final_grades(grades, excuses))









    '''purch = pd.DataFrame([['Alice', 'sweeties', 4],
                          ['Bob', 'chocolate', 5],
                          ['Alice', 'chocolate', 3],
                          ['Claudia', 'juice', 2],],
                         columns=['client', 'item', 'quantity'])
    goods = pd.DataFrame([['sweeties', 15],
                          ['chocolate', 7],
                          ['juice', 8],
                          ['lemons', 3],],
                         columns=['good','price'])
    discounts = pd.DataFrame([['Alice', 10],
                          ['Bob', 5],
                          ['Patritia', 15],],
                         columns=['client','discount'])
    pd.testing.assert_frame_equal(
    totals(purch, goods, discounts).sort_index(axis=0).sort_index(axis=1),
    pd.DataFrame({'chocolate': {'Alice': 18.9, 'Bob': 33.25, 'Claudia': 0.0},
 'juice': {'Alice': 0.0, 'Bob': 0.0, 'Claudia': 16.0},
 'lemons': {'Alice': 0.0, 'Bob': 0.0, 'Claudia': 0.0},
 'sweeties': {'Alice': 54.0, 'Bob': 0.0, 'Claudia': 0.0}}).sort_index(axis=0).sort_index(axis=1),
    check_names=False)

    df = totals(purch, goods, discounts).sort_index(axis=0).sort_index(axis=1)
    print(df)
    df['juice'] = df['juice'].astype(float)
    for row in df.index:
        for col in df.columns:
            print(type(df.loc[row, col]), end=' ')
        print()'''