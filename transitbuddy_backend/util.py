import requests
import csv
from csv import reader
import bcrypt
import string
import random

# encoding libraries
import chardet
from collections import OrderedDict


url = "http://web.mta.info/developers/data/nyct/subway/Stations.csv"


# decode Data
def find_encoding(content):
    detected_encoding = chardet.detect(content)["encoding"]

    return detected_encoding


def decode_data(content):
    encoding = find_encoding(content)
    decoded_data = content.decode(encoding="cp1252")

    return decoded_data


# scrapes mta static csv
def scrape_data(url):
    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode("utf-8")

        data = csv.reader(decoded_content.splitlines(), delimiter=",")
        my_list = list(data)

        with open("stationlocations.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerows(my_list)


def open_dataset(
    file="stationlocations.csv", header=True
):  # converts csv data to a list
    with open(file, "r") as f_object:
        read_file = reader(f_object)
        data = list(read_file)
        # data = read_file

        if header:
            return data, data[1:], data[0]
        else:
            return data


all_data, data, header = open_dataset()
all_data = all_data


def station_data(all_data):
    stop_id = []
    station = []

    stop_id = [[x[2] for x in all_data]]
    station = [[y[5] for y in all_data]]
    train = [[z[7] for z in all_data]]

    stop_id = stop_id[0][1:]
    station = station[0][1:]

    station_id_data = stop_id + station + train

    # writes it to csv
    # with open('stationdata.csv', 'w') as file:
    #         writer = csv.writer(file)
    #         writer.writerows(station_id_data)

    train_list = []

    for i in train:
        for j in i:
            train_list.append(j.split())
    train_list = train_list[1:]

    stopid_train = dict(
        zip(stop_id, train_list)
    )  # dictionary of stop_id and corresponding trains for stops
    stopid_station = dict(
        zip(stop_id, station)
    )  # dictionary of stop_id and corresponding stations

    return (stopid_train, stopid_station)


def get_stations(train):
    stopid_train, stopid_station = station_data(all_data)

    stop_ids = []
    station_names = []
    for key, values in stopid_train.items():
        if train in values:
            stop_ids.append(key)

    for stop in stop_ids:
        station_names.append(stopid_station[stop])

    return station_names


def get_stop_id(station):
    stopid_train, stopid_station = station_data(all_data)

    routes_from_station = [
        route for route in stopid_station if stopid_station[route] == station
    ]
    stop_id = list(filter(lambda a: a in stopid_train, routes_from_station))
    return stop_id[0]


# encrypts password
def encrypt_password(password):
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_pw


def generate_token():
    key = string.digits + string.ascii_letters
    random_key = ["".join(random.choice(key) for i in range(20))]

    token = str(random_key)

    return token


def get_weather_key():
    with open("/home/richarda/apikeys/weatherkey", "r") as f_obj:
        weatherkey = f_obj.readline().strip()
        print(weatherkey)
    return weatherkey


# getting list of trains when user looks up the station-----------------------------------------


def all_stations():
    stopid_train, stopid_station = station_data(all_data)
    id_station = []

    id_station = [f"{key} - {value}" for key, value in stopid_station.items()]

    return id_station


def get_trains_for_station():
    stopid_train, stopid_station = station_data(all_data)
    id_trains = []

    id_trains = [f"{key} - {value}" for key, value in stopid_train.items()]

    return id_trains


if __name__ == "__main__":
    app.run(debug=True)
