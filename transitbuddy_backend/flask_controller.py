import time
from datetime import datetime
import pathlib

from flask import Flask, jsonify, request
from flask_cors import CORS

from comment import Comment
from line import Line
from mta import get_train_time
from user import User
from util import (
    all_stations,
    encrypt_password,
    get_stations,
    get_stop_id,
    get_weather_key,
)

dbpath = "./data/transit.db"
table3 = "comment"

app = Flask(__name__)
CORS(app)


__here__ = pathlib.Path(__file__).parent.resolve()

with open(__here__ / "apikey", "r") as file_object:
    api_key = file_object.readline().strip()


@app.route("/register", methods=["POST"])
def register():
    error_message = "There was an error creating your account! Please try again."

    data = request.get_json()
    f_name = data["f_name"]
    l_name = data["l_name"]
    username = data["username"]
    password = data["password"]
    email = data["email"]

    encrypted_password = encrypt_password(password)

    new_user = User(
        username=username,
        encrypted_password=encrypted_password,
        f_name=f_name,
        l_name=l_name,
        email=email,
        token="",
    )

    try:
        new_user.save()

    except:
        time.sleep(5)
        return jsonify({"error": error_message})
    finally:
        return jsonify({"Thank You:": new_user.username})


@app.route("/login", methods=["POST"])
def login():
    error_message = "Error: Invalid Credentials!"
    data = request.get_json()

    username = data["username"]
    password = data["password"]

    user_account = User.login(username, password)
    user_account.get_token()  # creates token when user logs in

    if user_account == False:
        return jsonify({"error": error_message})  # return to login'
    else:
        return jsonify({"token": user_account.token})


@app.route("/token/<token>", methods=["GET"])
def token_auth(token):
    user_account = User.select_token(f"""WHERE token =?""", (token,))

    user_account = {
        "pk": user_account.pk,
        "username": user_account.username,
        "f_name": user_account.f_name,
        "l_name": user_account.l_name,
        "token": user_account.token,
    }

    return jsonify({"userData": user_account})


@app.route("/logout", methods=["POST"])
def logout():
    data = request.get_json()
    user_account = User.select_one(
        f"""WHERE pk = {data["pk"]}"""
    )  # bugbug -- sql injection
    user_account.del_token()
    return jsonify({"response": "Logged out successfully!"})


# ------------------------------------------train,station and times
@app.route("/train/<letter>", methods=["POST", "GET"])
def get_train_stations(letter):
    if request.method == "POST":
        stations = get_stations(letter)
    # print(stations)

    if request.method == "GET":
        return {"stations": stations}
    return {"stations": stations}


@app.route("/incoming/time/<train>/<station>", methods=["GET"])
def get_time(train, station):
    stop_id = get_stop_id(station)

    get_times = []
    get_times = get_train_time(train, stop_id)
    print(get_times)
    return jsonify(get_times)


# -----------------------------------------------for user feeds and comment components
@app.route("/add/comment", methods=["POST"])
def add_comment():
    pass

    data = request.get_json()
    print(data)

    time = datetime.now()
    line = data["line"]["train"]
    token = data["token"]
    comment = data["comment"]
    line_record = Line.select_one(line)
    user = User.select_token(token)

    print(token)
    print(user.username)
    print(user.pk)

    # time = datetime.strptime(d, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %I:%M:%S %p")

    new_comment = Comment(
        comment=comment, time=time, line_pk=line_record["pk"], user_pk=user.pk
    )

    new_comment.save()

    return jsonify({"comment": "made a comment!"})


@app.route("/view/comments/<train>", methods=["GET"])
def view_comments(train):
    return jsonify(Comment.select_all_by_train(train))


@app.route("/weatherkey")
def get_openweather_key():
    weather_key = get_weather_key()

    time.sleep(5)
    return jsonify({"weather_key": weather_key})


# ---------------------------------------------------------station to list of trains
@app.route("/stationlist")
def get_station_list():
    subway_stations = all_stations()

    return subway_stations


if __name__ == "__main__":
    app.run(debug=True, port=5000)
