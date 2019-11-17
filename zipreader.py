import zipfile
from pathlib import Path
import glob
import csv
import pandas as pd 

def extractor(file):
     zip=zipfile.ZipFile(file)
     dir_list=[]
     files_list=[]
     for x in zip.namelist():
          if x[-1]=="/":
               dir_list.append(x)
          else:
               files_list.append(Path(x).name)
     return(dir_list,files_list)

def comparator(list):
     testlist1=[]
     testlist2=[]
     for x in list:
          testlist1=testlist1+extractor(x)[0]
          testlist2=testlist2+extractor(x)[1]
     return(set(testlist1),set(testlist2))


in_list=glob.glob("./in/*.zip")

out_list=glob.glob("./out/*.zip")

print(comparator(in_list))
print(comparator(out_list))

newdir=comparator(out_list)[0].difference(comparator(in_list)[0])

newfiles=comparator(out_list)[1].difference(comparator(in_list)[1])
print(newfiles)
csvdata=[]
for x in newfiles:
     csvdata.append([x,"nouveau fichier"])
for x in newdir:
     csvdata.append([x,"nouveau repertoire"])

df = pd.DataFrame(csvdata)

print(df)

df.to_excel("data.xls", encoding='utf-8',header=False, index=False)

with open('person.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvdata)

csvFile.close()


"""
print("dif")

print(comparator(out_list)[0].difference(comparator(in_list)[0]))

print(comparator(out_list)[1].difference(comparator(in_list)[1]))
"""
