import pandas as pd
import sqlite3,re,hashlib
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect("ddbt.db")
df = pd.read_sql_query("select * from data;", conn)

def find_type(text): # tries les annonces: 0 si rien, 1 si appartement, 2 si maison, 3 si terrain
    x=0 #si il n'y a rien dans l'annonce, ce n'est pas classé
    if "terrain" in text:
        x=3
    if "Terrain" in text:
        x=3
    if "Appartement" in text:
        x=1
    if "appartement" in text:
        x=1
    if "Studio" in text:
        x=1
    if "studio" in text:
        x=1
    if "maison" in text:
        x=2
    if "Maison" in text:
        x=2
    if "propriété" in text:
        x=2
    if "Propriété" in text:
        x=2
    return x

def hashmaker(text):
    return hashlib.md5((text).encode('utf-8')).hexdigest()

def surfacefinder(text):
    rex = re.compile(r'.*?,(.*?)m2.*?',re.S|re.M)
    matc = rex.match(str(text))
    if matc:
        return(matc.groups()[0].strip())
    else:
        return("0")


print(surfacefinder("aaaa11m2"))

df['prix']=df['prix'].astype(float)
df['id']=df['id'].astype(float)
df['taux']=df['taux'].astype(float)
df['date'] = df['date'].astype('datetime64[ns]')


#on catégorise l'appart
df['type'] = df['nom'].apply(find_type)


#on fait un hash
df['hash'] = df['lien'].apply(hashmaker)

df['surface'] = df['nom'].apply(surfacefinder)


print(df.iloc[0])
print(df.iloc[1])
"""

data_per_date = df.groupby(['type','date'])



xxx=data_per_date['taux'].mean()


test=df.loc[df.type==1]
print(test)
test2=df.loc[df.type==0]
print(test2)
test3=df.loc[df.type==2]
print(test3)

data_per_date2 = test.groupby(['date'])
xxx2=data_per_date2['taux'].mean()
print(xxx2)


data_per_date2['taux'].mean().plot()
plt.show()

print(df.info())
print(df.head())
print(df.iloc[0])
"""
