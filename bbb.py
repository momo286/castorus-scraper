from bs4 import BeautifulSoup
import urllib.request,sqlite3,re,hashlib
from datetime import datetime


conn = sqlite3.connect('toutdd.db')

bien=0
pasbien=0

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS data(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     taux TEXT,
     nom TEXT,
     prix TEXT,
     date TEXT,
     lien TEXT,
     type INTEGER,
     surface INTEGER,
     codepostal TEXT,
     hash TEXT
     
)
""")
conn.commit()


def find_type(text):
    x=0
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


url = "http://www.castorus.com/activite.php"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html)

i = datetime.now()

dd=i.strftime('%Y/%m/%d')

for row in soup.find_all('li',attrs={"class" : "nodeborde"}):
    marqueur=0
    #print(row)
    rex = re.compile(r'.*?<img.*?>(.*?)</span>.*?',re.S|re.M)
    match = rex.match(str(row))
    if match:
        text = match.groups()[0].strip()
        #print(text)
        b=text[0:-1]
    rex = re.compile(r'.*?<a.*?>(.*?)</a>.*?',re.S|re.M)
    match = rex.match(str(row))
    if match:
        text = match.groups()[0].strip()
        rex = re.compile(r'.*?,(.*?)m2.*?',re.S|re.M)
        match = rex.match(str(text))
        if match:
            g=match.groups()[0].strip()
        else:
            marqueur=1
        f=find_type(text)
        h=str(text[0:5])
        i = hashlib.md5((text).encode('utf-8')).hexdigest()
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
        #print(text)
        e=text
        if marqueur==0:
            cursor.execute("""INSERT INTO data(taux,nom,prix,date,lien,type,surface,codepostal,hash) VALUES(?, ?, ?, ?, ?,?,?,?,?)""", (b,c,d,dd,e,f,g,h,i))
            bien=bien+1
        else:
            f=99
            cursor.execute("""INSERT INTO data(taux,nom,prix,date,lien,type,surface,codepostal,hash) VALUES(?, ?, ?, ?, ?,?,?,?,?)""", (b,c,d,dd,e,f,g,h,i))
            pasbien=pasbien+1
conn.commit()
conn.close()
print("taux de merdes: "+str((pasbien/bien)*100)[0:3]+"%")

