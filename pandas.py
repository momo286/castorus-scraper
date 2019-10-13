import pandas as pd
import sqlite3
conn = sqlite3.connect("toutf.db")
df = pd.read_sql_query("select * from data;", conn)
df
