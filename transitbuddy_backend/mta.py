from google.transit import gtfs_realtime_pb2
import requests 
import time
import os
from dotenv import load_dotenv, find_dotenv
from protobuf_to_dict import protobuf_to_dict
import json
import sqlite3 
import datetime

#encoding libraries
import chardet
from collections import OrderedDict


DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, 'transit.db')
tablename1 = "station"

load_dotenv(find_dotenv())

with open("/home/richarda/apikeys/mtapikey","r") as file_object:
    api_key = file_object.readline().strip()

def get_realtime_data(key, train): #GETS DATA FROM API AND PARSES  ALL lines
    feed = gtfs_realtime_pb2.FeedMessage()

    headers = {'x-api-key': key}

    one_to_six = ['1', '2', '3', '4', '5', '6']
    ace = ['A', 'C', 'E']
    nqrw = ['N', 'Q', 'R', 'W']
    bdfm = ['B', 'D', 'F', 'M']
    g = 'G'
    l = "L"
    jz = ['J', 'Z']
    seven = '7'

    if train in one_to_six:
        response = requests.get(url='https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs', headers = headers)
    elif train in ace:
        response = requests.get(url='https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace', headers = headers)
    elif train in nqrw:
        response = requests.get(url='https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw', headers = headers)
    elif train in bdfm:
        response = requests.get(url='https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm', headers = headers)
    elif train == g:
        response = requests.get(url='https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g', headers = headers)
    elif train in jz:
        response = requests.get(url='https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz', headers = headers)
    elif train == seven:
        response = requests.get(url='https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-7', headers = headers)
    elif train == l:
       response = requests.get(url='https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l', headers = headers)

    feed.ParseFromString(response.content)

    return  feed #type(trip_data)

# print(get_realtime_data(None, "F"))
# def get_realtime_data(key, train): #GETS DATA FROM API AND PARSES  ALL lines
#     feed = gtfs_realtime_pb2.FeedMessage()


#     one_to_six = ['1', '2', '3', '4', '5', '6']
#     ace = ['A', 'C', 'E']
#     nqrw = ['N', 'Q', 'R', 'W']
#     bdfm = ['B', 'D', 'F', 'M']
#     g = 'G'
#     l = "L"
#     jz = ['J', 'Z']
#     seven = '7'

#     if train in one_to_six:
#         response = requests.get(f'http://datamine.mta.info/mta_esi.php?key={key}&feed_id=1')
#     elif train in ace:
#         response = requests.get(f'http://datamine.mta.info/mta_esi.php?key={key}&feed_id=26')
#     elif train in nqrw:
#         response = requests.get(f'http://datamine.mta.info/mta_esi.php?key={key}&feed_id=16')
#     elif train in bdfm:
#         response = requests.get(f'http://datamine.mta.info/mta_esi.php?key={key}&feed_id=21')
#     elif train == g:
#         response = requests.get(f'http://datamine.mta.info/mta_esi.php?key={key}&feed_id=31')
#     elif train in jz:
#         response = requests.get(f'http://datamine.mta.info/mta_esi.php?key={key}&feed_id=36')
#     elif train == seven:
#         response = requests.get(f'http://datamine.mta.info/mta_esi.php?key={key}&feed_id=51')
#     elif train == l:
#        response = requests.get(f'http://datamine.mta.info/mta_esi.php?key={key}&feed_id=2')

#     feed.ParseFromString(response.content)

#     return  feed #type(trip_data)


def list_of_dict(train):            #converts  data to a list of dictionaries
    data_feed = get_realtime_data(api_key, train)
    subway_data = protobuf_to_dict(data_feed)
    header_data = subway_data['header']
    entity_data = subway_data['entity']

    # with open('/home/richarda/Bootcamp/project_MTA/backend_app/mtadata.json', 'w') as f_obj:
    #     json.dump(entity_data, f_obj, indent = 2)
    return entity_data


# def open_data(train, stop_code):
#      with open('/home/richarda/Bootcamp/project_MTA/backend_app/mtadata.json', 'r') as read_file:
#         data = json.load(read_file)

#         currentTime = time.time() #Might want to use this if times are earlier than current time
#         earliestTime_N = 2_147_483_647 #Max integer value that the time could be so this will be larger than all values found
#         earliestTime_S = 2_147_483_647

#         for trip in data: #Loop through the trips
#             if "trip_update" in trip: #Check that the trip update key is in a trip as some have vehicle keys instead
#                 if trip["trip_update"]["trip"]["route_id"] == train: #Checks train
#                     if "stop_time_update" in trip["trip_update"]: #Check trip has stops in it
#                         for stop in trip["trip_update"]["stop_time_update"]: #Loop through the stops on this trips
#                             if stop["stop_id"] ==  (stop_code+"N"): #Find check which the stop is. F05N and F05S are both station F05
#                             #if stop["stop_id"] == "B23N" or stop["stop_id"] == "B23S": #F05N and F05S are both same stations from diff bounds.
#                                 #if stop["arrival"]["time"] > currentTime: if i want to compare arrival time to current time
#                                 earliestTime_N = earliestTime_N if earliestTime_N < stop["arrival"]["time"] else stop["arrival"]["time"] #Use ternary opperator to find smallest value
#                             if stop["stop_id"] == (stop_code+"S"):
#                                 earliestTime_S = earliestTime_S if earliestTime_S < stop["arrival"]["time"] else stop["arrival"]["time"]
#         # arrival_time = datetime.datetime.fromtimestamp(
#         # int(earliestTime)).strftime('%H:%M:%S')

#         real_time_N = datetime.datetime.fromtimestamp(
#         int(earliestTime_N)).strftime('%I:%M:%S %p')

#         real_time_S = datetime.datetime.fromtimestamp(
#         int(earliestTime_S)).strftime('%I:%M:%S %p')


#         return real_time_N, "-------------", real_time_S 
       

def get_train_time(train, stop_code):
        data = list_of_dict(train)
        currentTime = time.time() 
        earliestTime_N = 2_147_483_647 
        earliestTime_S = 2_147_483_647 

        for trip in data: 
            if "trip_update" in trip: 
                if trip["trip_update"]["trip"]["route_id"] == train: 
                    if "stop_time_update" in trip["trip_update"]: 
                        for stop in trip["trip_update"]["stop_time_update"]: 
                            if stop["stop_id"] ==  (stop_code+"N"): 
                                earliestTime_N = earliestTime_N if earliestTime_N < stop["arrival"]["time"] else stop["arrival"]["time"]
                            if stop["stop_id"] == (stop_code+"S"):
                                 earliestTime_S = earliestTime_S if earliestTime_S < stop["arrival"]["time"] else stop["arrival"]["time"]
        # #24hr time
        # arrival_time = datetime.datetime.fromtimestamp(
        # int(earliestTime)).strftime('%H:%M:%S')

        #12hr time-ace
        real_time_N = datetime.datetime.fromtimestamp(
        int(earliestTime_N)).strftime('%I:%M:%S %p')

        real_time_S = datetime.datetime.fromtimestamp(
        int(earliestTime_S)).strftime('%I:%M:%S %p')
        return real_time_N, real_time_S
