
from bs4 import BeautifulSoup
import sqlite3,re,requests
from datetime import datetime

dbname="lol.db"

def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', str(text))

class Site():#prends les données brut html
    def __init__(self,url):
        self.url=url
        self.resultats=[]
        self.headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    def extraction(self): # on extrait le html
        response=requests.get(self.url,headers=self.headers)
        self.soup=BeautifulSoup(response.content)
 
    def tri(self):#on choisit les lignes
        for row in self.soup.find_all('tr'):
            self.resultats.append(row)

class Ligne():
        def __init__(self,ligne):
            self.ligne=ligne

        def trait(self):
            rex = re.compile(r'.*?<a href="(.*?)">.*?',re.S|re.M)#on extrait le lien
            match = rex.match(str(self.ligne))
            lien=match.groups()[0].strip()
            z=remove_tags(self.ligne).splitlines()
            variationprix=(z[2].lstrip().replace('%', '').replace('+', '')) #taux
            codepostal=(z[3][0:5]) #cp
            textannonce=(z[4].lstrip()) #description
            prix=(z[5].lstrip().split(" ")[0])#prix
            return [variationprix,codepostal,prix,lien,textannonce]

class DataSite():#traitement des données
    def __init__(self,rawdata):
        self.rawdata=rawdata
        self.resultats=[]
        self.tri()

    def tri(self): #enleve les doubles en se basant sur le hash extrait les données
        for row in self.rawdata:
            try:
                x=Ligne(row).trait()
                self.resultats.append(x)
            except Exception as inst:
                print(inst)
          
class InjectData():
    def __init__(self,data,dbname):
        self.data=data
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        i = datetime.now()
        self.temps=i.strftime('%Y/%m/%d') #date
        self.dbmaker()
        self.datainject()

    def dbmaker(self):
        self.cursor.execute("""
CREATE TABLE IF NOT EXISTS data(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     taux TEXT, 
     nom TEXT,
     prix TEXT,
     date TEXT,
     lien TEXT,
     codepostal TEXT )""")
        self.conn.commit()

    def datainject(self):
        for line in self.data:
            self.cursor.execute("INSERT INTO data(taux,nom,prix,date,lien,codepostal) VALUES(?, ?, ?, ?, ?,?)", (line[0],line[4],line[2],self.temps,line[3],line[1]))
        self.conn.commit()
        self.conn.close()

Castorus=Site("https://www.castorus.com/activite.php")
Castorus.extraction()
Castorus.tri()
Data=DataSite(Castorus.resultats)
Inject=InjectData(Data.resultats,dbname)
