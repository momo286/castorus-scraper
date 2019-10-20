import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect("toutf.db")
df = pd.read_sql_query("select * from data;", conn)




df['prix']=df['prix'].astype(float)
df['id']=df['id'].astype(float)
df['surface']=df['surface'].astype(float)
df['taux']=df['taux'].astype(float)
df['codepostal']=df['codepostal'].astype(float)
df['date'] = df['date'].astype('datetime64[ns]')




data_per_date = df.groupby(['type','date'])

print(data_per_date['taux'].mean())


data_per_date['taux'].mean().plot()

"""
print(df.info())
print(df.head())
print(df.iloc[0])
"""
