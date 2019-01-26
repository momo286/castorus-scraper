import statistics,sqlite3,pygal
from itertools import groupby

def final(don,idd,tri=0):#groupe selon l'index
    don.sort(key=lambda x: x[idd])
    data=[]
    for key, group in groupby(don, lambda x: x[idd]):
        temp=[]
        for thing in group:
            temp.append(thing)
        data.append(temp)
    return data

def SortCp(tab):#liste des tous les codes postaux dans les données
    set=[]
    for x in tab:
        y=x[1][0:5]
        if y in set:
            pass
        else:
            set.append(y) 
    #print("nombre de codes postaux dans les données:"+str(len(set)))
    set.sort()
    return set

def cDep():#liste des départements existants
    ldep=[]
    for x in range(1,96):
        ldep.append(format(x, '02d'))
    ldep.append(99)
    return ldep


def graph(dep):
    DataDept(all_rows,str(dep))

class DataDept():

    def __init__(self,data,dept):
        self.stat={} #tableau automatique ave les stats
        self.AllData=data #données de la BDD
        self.data=[]
        self.dept=dept
        self.listtab=[]
        self.DataLoad()#on charge les données  pour un departement ou un CP
        self.DataGroupAll(20,30,180) # on groupe les données en trois tableaux pour les trois périodes: 20 jours de données, 30 jours, 180 jours
        self.listprep=[]# contient les 3 data
        self.Prepall()
        self.graphAll()
        self.stat['dep']=self.dept
        print("--"+self.dept+"--" )
        #print(str(dept)+" "+str(self.stat['moy20']))
        

       
    def DataLoad(self): # on charge les données dans un tableau en les filtrant et en les triant que ce soit pour les departements ou Codes Postaux
        for row in self.AllData:
            if self.dept=="99":
                self.data.append((str(row[3]),(str(row[0])),row[1][0:2],row[1][0:5],int(row[2])))
                pass
            if len(self.dept)==2:
                if row[1][0:2]==self.dept :
                    self.data.append((str(row[3]),(str(row[0])),row[1][0:2],row[1][0:5],int(row[2])))
            if len(self.dept)==5:
                if row[1][0:5]==self.dept :
                    self.data.append((str(row[3]),(str(row[0])),row[1][0:5],row[1][0:5],int(row[2])))
        self.data.sort(key=lambda x: x[0])
        #print((self.data))

    def DataGroupAll(self,*args):
        [self.DataGroup(x) for x in args ]

    def DataGroup(self,nj): #on groupe les donnes par date avec les nj derniers jours, et ajoute au tableau
        buffer=[]
        fc=[]
        for key, group in groupby(self.data, lambda x: x[0]):
            temp=[]
            x=0
            for thing in group:
                temp.append((float(thing[1])))
                x=x+1
            buffer.append((key,(statistics.mean(temp)),statistics.pvariance(temp),x))
            #print("Date:",key," moyenne:",str(statistics.mean(temp))[0:5]," Var:",str(statistics.pvariance(temp))[0:5]," nb: ",len(temp),self.dept)
            
        for x in range(0,nj):
            try:
                fc.append(buffer.pop())
            except:
                pass
        self.listtab.append(fc)
        print("---")
        print(self.listtab)

        #print(fc)
        self.calc(fc) #calcul des stats
 
    def Prepall(self): # prepare les donnees
        for x in self.listtab:
            self.listprep.append(self.Prep(x)) 
    
    def Prep(self,tab): #prepare les donne spour pygal/ un tab avec les dates er les donnees
        temp=[]
        x1=[]
        x2=[]
        for x in tab:
            x1.append(x[0])
            x2.append(x[1])
        temp.append(x1)
        temp.append(x2)
        return  temp

    def calc(self,tab):#stats ajoutees au tableau
        temp=[]
        for x in tab:
            temp.append(x[1])
        self.stat["moy"+str(len(tab))]=statistics.mean(temp)
        

    def graphAll(self):
        for x in self.listprep:
            self.graph(x)
            
    def graph(self,tab):#realisation du graph
        temp=[]
        for x in tab[0]:
            temp.append(x[8:]) #on garde la fin des dates
        line_chart = pygal.Line()
        line_chart.title = 'Moyenne de variation des prix sur '+str(len(tab[0]))+' jours pour le departement'+str(self.dept)
        line_chart.x_labels =temp
        line_chart.add("ttt",tab[1])
        #line_chart.render_to_file('img/'+str(self.dept)+str(len(tab[0]))+'.svg')


#debut du porgrammes
conn = sqlite3.connect('toutdd.db')
cursor = conn.cursor()
cursor.execute('''SELECT taux,nom,prix,date,lien FROM data''')
all_rows = cursor.fetchall()

graph(75)
"""
#on obtient tous les codes postaux
ldep=cDep() #liste de tous les departements
SortCp(all_rows) #extractions de tous les codes postaux

for x in ldep: #pour chaque departement on lance les calculs
    (graph(x))




databeta=[]

for row in all_rows: # on charge le tableau
    databeta.append((str(row[3]),(str(row[0])),row[1][0:2],row[1][0:5],int(row[2])))
print("Taille des données "+str(len(databeta)))
data=final(databeta,2)#on trie les données par dept
print("Taille des par département "+str(len(data)))
data2=final(databeta,3)#on trie les données par CP
print("Taille des données par Code Postal "+str(len(data2)))

matrice=[]

for x in data: # on trie par date
    matrice.append(final(x,0))
#print(len(matrice[75]['2015/06/15']))
#matrice ou [departement][date][donnees]

"""





