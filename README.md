The main scripts are :

-dailydata.py
It scrapes the castorus page which displays the changes for the last 24 hours and puts it into an sqlite file.The data that is scraped is: taux,nom,prix,date,lien,codepostal. Don't forget to set the database name!

Two notebooks are included for experiments with data:

"Per item" is a notebook that gives you a DataFrame where each line contains a property and all the price variations in a list.

"Per Tendency"  is a few graphs to follow price variation over time in different regions, based on the type of property.

