from bs4 import BeautifulSoup
import urllib.request,sqlite3,re,hashlib
from datetime import datetime


class Site():#prends les données brut html
    def __init__(self,url):
        self.url=url
        self.resultats=[]

    def extraction(self): # on extrait le html
        self.soup=BeautifulSoup(urllib.request.urlopen(self.url).read()) 

    def tri(self):#on choisit les lignes
        for row in self.soup.find_all('li',attrs={"class" : "nodeborde"}):
            self.resultats.append(row)

class Ligne():
        def __init__(self,ligne):
            self.ligne=ligne

        def trait(self):
            rex = re.compile(r'.*?<img.*?>(.*?)</span>.*?',re.S|re.M)
            match = rex.match(str(self.ligne))
            text = match.groups()[0].strip()
            variationprix=text[0:-1]#variation du prix
            rex = re.compile(r'.*?<a.*?>(.*?)</a>.*?',re.S|re.M)
            match = rex.match(str(self.ligne))
            textannonce = match.groups()[0].strip()#text
            hashcp = hashlib.md5((textannonce).encode('utf-8')).hexdigest()
            codepostal=str(textannonce[0:5]) #codepostal
            rex = re.compile(r'.*?</strike>(.*?)</span></li>.*?',re.S|re.M)
            match = rex.match(str(self.ligne))
            text = match.groups()[0].strip()
            prix=text[5:-2] #prix
            rex = re.compile(r'.*?<a href="(.*?)">.*?',re.S|re.M)#on extrait le lien
            match = rex.match(str(self.ligne))
            text = match.groups()[0].strip()
            lien=text#lien
            return [variationprix,hashcp,codepostal,prix,lien,textannonce]

class DataSite():#traitement des données
    def __init__(self,rawdata):
        self.rawdata=rawdata
        self.resultats=[]
        self.set=[]
        self.tri()

    def tri(self): #enleve les doubles en se basant sur le hash extrait les données
        for row in self.rawdata:
            x=Ligne(row).trait()
            if x[1] in self.set:
                pass
            else:
                self.set.append(x[1])
                self.resultats.append(x)
        print("nombre de lignes extraites: "+ str(len(self.resultats)))
            
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
     codepostal TEXT,
     hash TEXT)""")
        self.conn.commit()
        print("aa")

    def datainject(self):
        print("ss")
        for line in self.data:
            self.cursor.execute("INSERT INTO data(taux,nom,prix,date,lien,codepostal,hash) VALUES(?, ?, ?, ?, ?,?,?)", (line[0],line[5],line[3],self.temps,line[4],line[2],line[1]))
        self.conn.commit()
        print("bb")
        self.conn.close()

Castorus=Site("http://www.castorus.com/activite.php")

Castorus.extraction()

Castorus.tri()

Data=DataSite(Castorus.resultats)

Inject=InjectData(Data.resultats,"/home/tgif/ppppp.db")

print (datetime.datetime.now())
