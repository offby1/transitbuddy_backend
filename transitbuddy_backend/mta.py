import datetime
import os

import dotenv
import platformdirs
import requests
from google.transit import gtfs_realtime_pb2
from protobuf_to_dict import protobuf_to_dict

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "transit.db")
tablename1 = "station"

dotenv.load_dotenv(dotenv_path=platformdirs.user_config_dir(appname="com.github.ra1993.transitbuddy"))
# https://api.mta.info/#/AccessKey

api_key = os.environ.get("MTA_API_KEY", "")


def get_realtime_data(key, train):  # GETS DATA FROM API AND PARSES  ALL lines
    feed = gtfs_realtime_pb2.FeedMessage()

    headers = {"x-api-key": key}

    one_to_six = ["1", "2", "3", "4", "5", "6"]
    ace = ["A", "C", "E"]
    nqrw = ["N", "Q", "R", "W"]
    bdfm = ["B", "D", "F", "M"]
    g = "G"
    l = "L"
    jz = ["J", "Z"]
    seven = "7"

    if train in one_to_six:
        response = requests.get(
            url="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
            headers=headers,
        )
    elif train in ace:
        response = requests.get(
            url="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace",
            headers=headers,
        )
    elif train in nqrw:
        response = requests.get(
            url="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
            headers=headers,
        )
    elif train in bdfm:
        response = requests.get(
            url="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm",
            headers=headers,
        )
    elif train == g:
        response = requests.get(
            url="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g",
            headers=headers,
        )
    elif train in jz:
        response = requests.get(
            url="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz",
            headers=headers,
        )
    elif train == seven:
        response = requests.get(
            url="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-7",
            headers=headers,
        )
    elif train == l:
        response = requests.get(
            url="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l",
            headers=headers,
        )

    feed.ParseFromString(response.content)

    return feed  # type(trip_data)


def list_of_dict(train):  # converts  data to a list of dictionaries
    data_feed = get_realtime_data(api_key, train)
    subway_data = protobuf_to_dict(data_feed)
    entity_data = subway_data["entity"]

    return entity_data


def get_train_time(train, stop_code):
    data = list_of_dict(train)

    earliestTime_N = 2_147_483_647
    earliestTime_S = 2_147_483_647

    for trip in data:
        if "trip_update" in trip:
            if trip["trip_update"]["trip"]["route_id"] == train:
                if "stop_time_update" in trip["trip_update"]:
                    for stop in trip["trip_update"]["stop_time_update"]:
                        if stop["stop_id"] == (stop_code + "N"):
                            earliestTime_N = (
                                earliestTime_N
                                if earliestTime_N < stop["arrival"]["time"]
                                else stop["arrival"]["time"]
                            )
                        if stop["stop_id"] == (stop_code + "S"):
                            earliestTime_S = (
                                earliestTime_S
                                if earliestTime_S < stop["arrival"]["time"]
                                else stop["arrival"]["time"]
                            )
    # 12hr time-ace
    real_time_N = datetime.datetime.fromtimestamp(int(earliestTime_N)).strftime(
        "%I:%M:%S %p"
    )

    real_time_S = datetime.datetime.fromtimestamp(int(earliestTime_S)).strftime(
        "%I:%M:%S %p"
    )
    return real_time_N, real_time_S
