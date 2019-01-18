from bs4 import BeautifulSoup
import urllib.request
import re
from datetime import datetime
import sqlite3

conn = sqlite3.connect('tout.db')

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS data(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     taux TEXT,
     nom TEXT,
     prix TEXT,
     date TEXT,
     lien TEXT
     
)
""")
conn.commit()

url = "http://www.castorus.com/activite.php"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html)

i = datetime.now()

dd=i.strftime('%Y/%m/%d')

for row in soup.find_all('li',attrs={"class" : "nodeborde"}):
    rex = re.compile(r'.*?<img.*?>(.*?)</img>.*?',re.S|re.M)
    match = rex.match(str(row))
    if match:
        text = match.groups()[0].strip()
        b=text[0:-1]
    rex = re.compile(r'.*?<a.*?>(.*?)</a>.*?',re.S|re.M)
    match = rex.match(str(row))
    if match:
        text = match.groups()[0].strip()
        c=text
    rex = re.compile(r'.*?</strike>(.*?)</span></li>.*?',re.S|re.M)
    match = rex.match(str(row))
    if match:
        text = match.groups()[0].strip()
        d=text[5:-2]
    rex = re.compile(r'.*?<a href="(.*?)">.*?',re.S|re.M)
    match = rex.match(str(row))
    if match:
        text = match.groups()[0].strip()
        e=text
    cursor.execute("""INSERT INTO data(taux,nom,prix,date,lien) VALUES(?, ?, ?, ?, ?)""", (b,c,d,dd,e))

conn.commit()
conn.close()

