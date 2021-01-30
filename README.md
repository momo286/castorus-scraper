The main script is :

-dailydata.py
It scrapes the castorus page which displays the changes for the last 24 hours and puts it into an sql file.

It doesn't modify the data, except for two things in order to have clean data:
  -It removes duplicates: sometimes for the same property you'll see the same variation more than once, it keeps just one of them
  -Some properties have variations that are equal to 0, those lines are deleted

-dailydataobjectversion.py is an object version

Two notebooks are included for experiments with data
:
"Per item" is a notebook that gives you a DataFrame where each line contains a property and all the price variations in a list


"Per Tendency"  is a few graphs to folloew price variation over time in different regions, based on the type of property

