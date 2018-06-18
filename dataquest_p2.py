import csv
import datetime
import re
##change the census csv for the American to native american

f = open("guns.csv","r")
reader = csv.reader(f)

data = list(reader)

header = data [:1]
data = data [1:]

years = []
year_counts = {}
for row in data:
    years.append(row[1])
for row in years:
    if row in year_counts:
        year_counts[row] += 1
    else:
        year_counts[row] = 1

dates = [datetime.datetime(year=int(row[1]), month=int(row[2]), day = 1)
         for row in data]

dates
date_counts = {}

for date_data in dates:
    if (date_data in date_counts):
        date_counts[date_data] += 1
    else:
        date_counts[date_data] = 1

#print (date_counts)

sex_counts = {}
race_counts = {}
for row in data:
    if row[5] in sex_counts:
        sex_counts[row[5]] += 1
    else:
        sex_counts[row[5]] = 1

    if row[7] in race_counts:
        race_counts[row[7]] += 1
    else:
        race_counts[row[7]] = 1

#print(race_counts)
# print(sex_counts)

f = open("census.csv","r")
readCensus = csv.reader(f)

census = list(readCensus)

#print(census)
mapping = {}

head_data = census[0]
body_data = census[1]

# for head_val,body_val in zip(head_data,body_data):
#      print (head_val,body_val)



for key in race_counts:
    #print (key,race_counts[key])
    if re.search("/",key) is not None:
       key_val = key.split("/")
       #print(key_val)
       for row in key_val:
           for head_val, body_val in zip(head_data, body_data):
                try:
                   body_val = int(body_val)
                except Exception:
                   body_val = 0
                if re.search(row,head_val) is not None:
                    if key in mapping:
                        mapping[key] += int(body_val)
                    else:
                        mapping[key] = int(body_val)
    else:
        #print (key)
        for head_val, body_val in zip(head_data, body_data):
            try:
                body_val = int(body_val)
            except Exception:
                body_val = 0
            if re.search(key,head_val) is not None:
                if key in mapping:
                    mapping[key] += int(body_val)
                else:
                    mapping[key] = int(body_val)

# print(race_counts)
# print(mapping)
race_per_hundredk = {}
for key,value in race_counts.items():
    race_per_hundredk[key] = (value / mapping[key]) * 100000

print (race_per_hundredk)

intents = [row[3] for row in data]
races = [row[7] for row in data]

homicide_race_counts = {}
intents = [row[3] for row in data]
homicide_race_counts = {}
for i,race in enumerate(races):
    if race not in homicide_race_counts:
        homicide_race_counts[race] = 0
    if intents[i] == "Homicide":
        homicide_race_counts[race] += 1

race_per_hundredk = {}
for k,v in homicide_race_counts.items():
    race_per_hundredk[k] = (v / mapping[k]) * 100000

print("race_per_hundredk",race_per_hundredk)





