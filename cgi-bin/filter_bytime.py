#!/Python33/python

import cgi, sys
import json
import sqlite3
import collections
# -------------------------------
# Actually sending through script

# start_st_id, end_st_id and count

print("Content-type: json\n\n")
fs = cgi.FieldStorage()
City = fs["name"].value
Time_start = fs["time-start"].value
Time_end = fs["time-end"].value
Date_start = fs["date-start"].value
Date_end = fs["date-end"].value
sub_type = fs["user"].value
gender = fs["sex"].value
birthdate_start = fs["birthyear-start"].value
birthdate_end = fs["birthyear-end"].value
duration_start = fs["duration-start"].value
duration_end = fs["duration-end"].value

trips = {}

db_path = ""
# db_path = "data/capitalbikeshare.db"
# db_path = "data/hubway.db"

#print("Opened database successfully");
if City == "Boston":
	db_path = "data/hubway.db"
elif City == "Chicago":
	db_path = "data/divvy.db"
else:
	db_path = "data/capitalbikeshare.db"

conn = sqlite3.connect(db_path)

querystring = 'select trip_id,start_st_id,end_st_id from trips where start_date>=date("'+Date_start+'")'
if (Time_start!=""):
	querystring = querystring + ' and start_time>=time("'+Time_start+'")'
if (Time_end!=""):
        querystring = querystring+ ' and end_time<=time("'+Time_end +'")'
if (Date_end!=""):
	querystring = querystring + ' and end_date<=date("'+ Date_end +'")'
if (duration_start != ""):
        querystring = querystring + ' and duration>='+ duration_start
if (duration_end != ""):
        querystring = querystring + ' and duration<='+ duration_end
if (sub_type != "all"):
         querystring = querystring + ' and sub_type="' + sub_type + '"'
if (gender != "all"):
        querystring = querystring + ' and gender="' + gender + '"'
if (birthdate_start != "min"):
         querystring = querystring + ' and birth_date>='+ birthdate_start
if (birthdate_end != "max"):
         querystring = querystring + ' and birth_date<='+ birthdate_end


# querystring += " limit 100"

# print(querystring)
cursor = conn.execute(querystring)
for row in cursor:
	# print row
	if row[1] not in trips:
		trips[row[1]]={}
	if row[2] not in trips[row[1]]:
		trips[row[1]][row[2]] = 0
	trips[row[1]][row[2]] += 1 

max_weight = 0;

for key1 in trips:
        for key2 in trips[key1]:
                if(trips[key1][key2] > max_weight):
                        max_weight = trips[key1][key2]
to_send = {}
to_send["max_weight"] = max_weight
to_send["trips"] = trips
data = json.dumps(to_send)
print(data)
