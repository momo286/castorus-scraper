from bs4 import BeautifulSoup
import urllib.request,sqlite3,re,hashlib
from datetime import datetime

conn = sqlite3.connect('toutdd.db')
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


url = "http://www.castorus.com/activite.php"
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html)

set=[]
i = datetime.now()
dd=i.strftime('%Y/%m/%d') #date


#statistiques
stat=0
surface=0
doublon=0
indefini=0

for row in soup.find_all('li',attrs={"class" : "nodeborde"}):
    stat=stat+1
    marqueur=0
    
    rex = re.compile(r'.*?<img.*?>(.*?)</span>.*?',re.S|re.M)
    match = rex.match(str(row))
    if match:
        text = match.groups()[0].strip()
        b=text[0:-1]#variation du prix
        
    rex = re.compile(r'.*?<a.*?>(.*?)</a>.*?',re.S|re.M)
    match = rex.match(str(row))
    if match:
        text = match.groups()[0].strip()
        rex = re.compile(r'.*?,(.*?)m2.*?',re.S|re.M)#on teste pour voir s'il y a des surfaces
        match = rex.match(str(text))
        if match:
            g=match.groups()[0].strip() #surface
        else:
            marqueur=1#pas de surface, pas d'injection
            surface=surface+1
        f=find_type(text) #on cherche le type d'appartement
        if f==0:
            print(text)
            indefini=indefini+1
            marqueur=1
        else:
            pass
        h=str(text[0:5]) #codepostal
        i = hashlib.md5((text).encode('utf-8')).hexdigest() #hash unique de description
        if i in set:#detection des doublons en se basant sur le hash
            doublon=doublon+1
            marqueur=1
        else:
            set.append(i)
        c=text #description
        
    rex = re.compile(r'.*?</strike>(.*?)</span></li>.*?',re.S|re.M)
    match = rex.match(str(row))
    if match:
        text = match.groups()[0].strip()
        d=text[5:-2] #prix
        
    rex = re.compile(r'.*?<a href="(.*?)">.*?',re.S|re.M)#on extrait le lien
    match = rex.match(str(row))


    if match:
        text = match.groups()[0].strip()
        e=text#lien
        if marqueur==0:
            cursor.execute("""INSERT INTO data(taux,nom,prix,date,lien,type,surface,codepostal,hash) VALUES(?, ?, ?, ?, ?,?,?,?,?)""", (b,c,d,dd,e,f,g,h,i))
            pass
        else:
            #cursor.execute("""INSERT INTO data(taux,nom,prix,date,lien,type,surface,codepostal,hash) VALUES(?, ?, ?, ?, ?,?,?,?,?)""", (b,c,d,dd,e,f,g,h,i))
            pass

conn.commit()
conn.close()



print("===========================")
print("Nombre de lignes: "+str(stat))
print("nombre de doublons: "+str(doublon))
print("nombre d'indefinis: "+str(indefini))
print("nombre de sans surface: "+str(surface))
print("taux de merdes: "+str(((doublon+indefini+surface)/stat)*100)[0:3]+"%")
print("===========================")


