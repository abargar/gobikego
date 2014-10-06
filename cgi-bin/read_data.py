#!/usr/local/bin/python
'''
Created on Apr 4, 2014

@author: Martin
'''
import cgi, sys
import json
import numpy as np
import time
import sqlite3

def read_trip_info(trip_file_path, c):
    tripFile = open(trip_file_path)
    tripFileContent = tripFile.read()
    trip_file_dict_raw = json.loads(tripFileContent)
    trip_info_dict = {}
    index_tripid_lookup_table = {}
    index = 0
    for entry in trip_file_dict_raw:
        if not entry["start_time"].startswith('' + c + ':'):
            continue
        trip_id = entry['trip_id']
        trip_info_dict[trip_id] = entry
        index_tripid_lookup_table[index] = trip_id
        index += 1

    return trip_info_dict, index_tripid_lookup_table

def read_station_info(station_file_path):
    station_file = open(station_file_path)
    station_file_content = station_file.read()
    station_file_dict_raw = json.loads(station_file_content)
    station_info_dict = {}
    for entry in station_file_dict_raw:
        st_id = entry['st_id']
        station_info_dict[st_id] = entry
    return station_info_dict


def get_X_for_trip_start_end_station_time():
    trip_info_dict, station_info_dict, index_tripid_lookup_table = read_from_db()
    # if c == '--':
    #     # print 'from db'
    #     trip_info_dict, station_info_dict, index_tripid_lookup_table = read_from_db()
    # else:
    #     station_info_dict = read_station_info(station_file_path)
    #     trip_info_dict, index_tripid_lookup_table = read_trip_info(trip_file_path, c)
    num_trip = len(trip_info_dict)
    num_station = len(station_info_dict)
    X_trip_start_station = np.ones([num_trip, 2])
    X_trip_end_station = np.ones([num_trip, 2])
    X_trip_start_end_time = np.ones([num_trip, 2])
    for index in range(num_trip):
        trip_id = index_tripid_lookup_table[index]
        try:

            start_st_id = trip_info_dict[trip_id]['start_st_id']
            end_st_id = trip_info_dict[trip_id]['end_st_id']
            start_st_lat = station_info_dict[start_st_id]['st_lat']
            start_st_long = station_info_dict[start_st_id]['st_long']
    #         print end_st_id
            end_st_lat = station_info_dict[end_st_id]['st_lat']
            end_st_long = station_info_dict[end_st_id]['st_long']

            X_trip_start_station[index][0] = start_st_lat
            X_trip_start_station[index][1] = start_st_long
            X_trip_end_station[index][0] = end_st_lat
            X_trip_end_station[index][1] = end_st_long

            start_date_time = trip_info_dict[trip_id]['start_date'] + ' ' + trip_info_dict[trip_id]['start_time']
            end_date_time = trip_info_dict[trip_id]['end_date'] + ' ' + trip_info_dict[trip_id]['end_time']
            start_date_time = time.strptime(start_date_time, "%Y-%m-%d %H:%M:%S")
            end_date_time = time.strptime(end_date_time, "%Y-%m-%d %H:%M:%S")
            start_mk_time = time.mktime(start_date_time)
            end_mk_time = time.mktime(end_date_time)
            X_trip_start_end_time[index][0] = start_mk_time
            X_trip_start_end_time[index][1] = end_mk_time
        except KeyError:
            # print trip_id, trip_info_dict[trip_id]
            pass
    return X_trip_start_station, X_trip_end_station, X_trip_start_end_time, index_tripid_lookup_table, trip_info_dict

def read_from_db():


    # print "in"
    fs = cgi.FieldStorage()
    # print fs
    City = fs["name"].value
    Time_start = fs["time-start"].value
    Time_end = fs["time-end"].value
    Date_start = fs["date-start"].value
    Date_end = fs["date-end"].value
    sub_type = fs["user"].value
    gender = fs["sex"].value
    birthdate_start = fs["birthyear-start"].value
    birthdate_end = fs["birthyear-end"].value

    # print "{'city': '" + City + "'}"

    db_path = ""
    if City == "Boston":
        db_path = "data/hubway.db"
    elif City == "Chicago":
        db_path = "data/divvy.db"
    else:
        db_path = "data/capitalbikeshare.db"

    conn = sqlite3.connect(db_path)


    ############### trip


    trip_info_db = {}
    index_tripid_lookup_table = {}

    querystring = 'select * from trips where start_date>=date("'+Date_start+'")'
    if (Time_start!=""):
      querystring = querystring + ' and start_time>=time("'+Time_start+'")'
    if (Date_end!=""):
      querystring = querystring + ' and end_date<=date("'+ Date_end +'")'
      if (Time_end!=""):
        querystring = querystring+ ' and end_time<=time("'+Time_end +'")'
    if (sub_type != "all"):
            querystring = querystring + ' and sub_type="' + sub_type + '"'
    if (gender != "all"):
            querystring = querystring + ' and gender="' + gender + '"'
    # if (birthdate_start != ""):
    #         querystring = querystring + ' and birth_date>='+ birthdate_start
    # if (birthdate_end != ""):
    #         querystring = querystring + ' and birth_date<='+ birthdate_end


    # print "query: " + querystring
    cursor = conn.execute(querystring)
    index = 0

    for row in cursor:

        # {395268: {u'start_st_id': 32, u'end_date': u'2012-07-18', u'end_st_id': 56, u'start_time': u'04:11:00', u'sub_type': u'Registered', u'birth_date': 1979, u'end_time': u'04:27:00', u'gender': u'Male', u'duration': 961, u'zip_code': 2119, u'trip_id': 395268, u'start_date': u'2012-07-18', u'bike_nr': u'B00166'},
        # print row
        if row[2] == '' or row[3] == '' or row[4] == '' or row[5] == '' or row[6] == '' or row[7] == '':
            continue
        new_trip = {}
        new_trip['trip_id'] = row[0]
        new_trip['duration'] = row[1]
        new_trip['start_date'] = row[2]
        new_trip['start_time'] = row[3]
        new_trip['start_st_id'] = row[4]
        new_trip['end_date'] = row[5]
        new_trip['end_time'] = row[6]
        new_trip['end_st_id'] = row[7]
        trip_info_db[row[0]] = new_trip
        index_tripid_lookup_table[index] = row[0]
        index += 1

    ################ station

    querystring2 = 'select * from stations'

    station_info_db = {}
    cursor2 = conn.execute(querystring2)
    for row in cursor2:
        new_station = {}
        new_station['st_id'] = row[0]
        new_station['st_lat'] = row[2]
        new_station['st_long'] = row[3]
        new_station['st_name'] = row[1]
        station_info_db[row[0]] = new_station
        # new_station['st_lat'] =
        # print row[0], row[2], row[6], row[7]
        # id name lat long

    # print trip_info_db
    # print station_info_db
    # print index_tripid_lookup_table
    return trip_info_db, station_info_db, index_tripid_lookup_table



if __name__ == '__main__':
    trip_file_path = "../data/hubway_2011_trips_info.json"
    station_file_path = "../data/hubway_2011_stations_info.json"


    trip_info_dict, index_tripid_lookup_table = read_trip_info(trip_file_path, '--')

    # print "done"



    # {3: {u'st_id': 3, u'st_capacity': 15, u'st_lat': 42.340021, u'st_name': u'Colleges of the Fenway', u'st_long': -71.100812},
