import statistics
import asyncio
import sqlite3,time
import concurrent.futures
from itertools import groupby
import pygal
from multiprocessing.dummy import Pool as ThreadPool 

def multi(func,data,nbworker):
    with concurrent.futures.ThreadPoolExecutor(max_workers=nbworker) as executor:
        a=list(executor.map(func, data))
    return a

start=time.clock()
conn = sqlite3.connect('tout.db')
cursor = conn.cursor()
cursor.execute('''SELECT taux,nom,prix,date,lien FROM data''')
all_rows = cursor.fetchall()

def final(don,idd):
    don.sort(key=lambda x: x[idd])
    dataa=[]
    for key, group in groupby(don, lambda x: x[idd]):
        temp=[]
        for thing in group:
            temp.append(thing)
        dataa.append(temp)
    return dataa

databeta=[]
for row in all_rows:
    databeta.append((str(row[3]),(str(row[0])),row[1][0:2],row[1][0:5],int(row[2])))
print(len(databeta))
data=final(databeta,2)
matrice=[]
for x in data:
    matrice.append(final(x,0))
print(len(matrice))
print(len(matrice[75]))
#matrice ou [departement][date][donnees]
print(time.clock() - start)



ldep=[]

for x in range(1,95):
    ldep.append(format(x, '02d'))

class DataDept():
    def __init__(self,data,dept):
        self.AllData=data
        self.data=[]
        self.dept=dept
        self.SortedData=[]
        self.PrepData=[]
        self.DataLoad()
        self.DataGroup()
        self.Prep()

    def DataLoad(self):
        for row in self.AllData:
            if len(self.dept)==2:
                if row[1][0:2]==self.dept :
                    self.data.append((str(row[3]),(str(row[0])),row[1][0:2],row[1][0:5],int(row[2])))
            if len(self.dept)==5:
                if row[1][0:5]==self.dept :
                    self.data.append((str(row[3]),(str(row[0])),row[1][0:5],row[1][0:5],int(row[2])))

    def DataGroup(self):
        for key, group in groupby(self.data, lambda x: x[0]):
            temp=[]
            pp=[]
            for thing in group:
                temp.append((float(thing[1])))
                pp.append((int(thing[4])))
            self.SortedData.append((key,(statistics.mean(temp)),statistics.pvariance(temp)))
            #print("Date:",key," moyenne:",str(statistics.mean(temp))[0:5]," Var:",str(statistics.pvariance(temp))[0:5]," nb: ",len(temp)," moyenne:",str(int(statistics.mean(pp)))," Var:",str(statistics.pvariance(pp))[0:7])

        return(self.SortedData)

    def Prep(self):
        x1=[]
        x2=[]
        for x in self.SortedData:
            x1.append(x[0])
            x2.append(x[1])
        self.PrepData.append(x1)
        self.PrepData.append(x2)

class DataDeptBeta():
    def __init__(self,data,dept):
        self.AllData=data
        self.data=[]
        self.dept=dept
        self.SortedData=[]
        self.PrepData=[]
        self.DataGroup()
        self.Prep()

    def DataGroup(self):
        for key, group in groupby(self.data, lambda x: x[0]):
            temp=[]
            pp=[]
            for thing in group:
                temp.append((float(thing[1])))
                pp.append((int(thing[4])))
            self.SortedData.append((key,(statistics.mean(temp)),statistics.pvariance(temp)))
            #print("Date:",key," moyenne:",str(statistics.mean(temp))[0:5]," Var:",str(statistics.pvariance(temp))[0:5]," nb: ",len(temp)," moyenne:",str(int(statistics.mean(pp)))," Var:",str(statistics.pvariance(pp))[0:7])
        #print("donnee triees")
        return(self.SortedData)

    def Prep(self):
        x1=[]
        x2=[]
        for x in self.SortedData:
            x1.append(x[0])
            x2.append(x[1])
        self.PrepData.append(x1)
        self.PrepData.append(x2)


def momo(dp):
    return(DataDept(all_rows,str(dp)))

tt=((DataDept(all_rows,'13').data))
"""
faire des  generateur

pour chaque chose triee:
faire un calcul

etape 1 : tri

etap 2 calculs


etap3: dessins

que faire

tout 1 /2 /3

ou faire un pipeline e toutes les taches
tt=((DataDept(all_rows,'13').data))
print(len(tt))
print(tt[0])
things = [("13500", "bear"), ("animal", "duck"), ("13200", "cactus"), ("vehicle", "speed boat"), ("vehicle", "school bus")]

for key, group in groupby(tt, lambda x: x[2]):
    for thing in group:
        print("A %s is a %s." % (thing[1], key))
    print(" ")

 

tt=((DataDept(all_rows,'13').PrepData))
pp=DataDept(all_rows,'13').DataGroup()


print("a")
startt = time.clock()
multi(momo,ldep,4)
print(time.clock() - startt)

print("b")


start = time.clock()
for x in ldep:
    ((DataDept(all_rows,x).PrepData))
print(time.clock() - start)

starttt = time.clock()
pool = ThreadPool(8)
results = pool.map(momo, ldep)
pool.close() 
pool.join()
print(time.clock() - starttt)

"""





def graph(dep):
    tt=((DataDept(all_rows,'dep').PrepData))
    pp=[]
    for x in tt[0]:
        pp.append(x[8:])
    line_chart = pygal.Line()
    line_chart.title = 'Moyenne de variation des prix'
    line_chart.x_labels =pp
    line_chart.add("ttt",tt[1])
    line_chart.render_to_file(str(dep)+'.svg')
    



graph(13)

