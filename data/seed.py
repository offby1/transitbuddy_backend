import os
import sqlite3
from csv import reader

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "transit.db")


def open_dataset(
    file="/home/richarda/Bootcamp/project_MTA/backend_app/stationdata.csv", header=True
):  # converts csv data to a list
    with open(file, "r") as f_object:
        read_file = reader(f_object)
        data = list(read_file)

        stop_id = [[x[0] for x in data]]
        station = [[y[1] for y in data]]

        station_dict = {}
        train_list = []

        for i in range(len(stop_id[0])):
            station_dict[stop_id[0][i]] = station[0][i]

        return station_dict, train_list


def seed(dbpath=DBPATH):
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()

        station_dict, train = open_dataset()
        del station_dict["GTFS Stop ID"]

        for k, v in station_dict.items():
            sql = """INSERT INTO station (stop_id, station_name) VALUES(?,?)"""
            values = (k, v)

            cur.execute(sql, values)
        # ------------------------------------------------------------
        trains = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "J",
            "L",
            "M",
            "N",
            "Q",
            "R",
            "W",
            "Z",
        ]

        for t in trains:
            sql = """INSERT INTO line (line_name) VALUES (?)"""
            values = t

            cur.execute(sql, values)


if __name__ == "__main__":
    seed()
