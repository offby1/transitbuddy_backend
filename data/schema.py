import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "transit.db")


def create_tables(db=DBPATH):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS user (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR UNIQUE,
                encrypted_password VARCHAR,
                email VARCHAR UNIQUE,
                f_name VARCHAR,
                l_name VARCHAR,
                token VARCHAR
            );"""
        )

        cur.execute(
            """     CREATE TABLE IF NOT EXISTS user_transit(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                line VARCHAR,
                station VARCHAR,
                user_pk INTEGER,
                line_pk VARCHAR,
                FOREIGN KEY (user_pk) REFERENCES user(pk),
                FOREIGN KEY (line_pk) REFERENCES line(pk)
            );"""
        )

        cur.execute(
            """     CREATE TABLE IF NOT EXISTS line(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                line_name VARCHAR
            );"""
        )

        cur.execute(
            """     CREATE TABLE IF NOT EXISTS station(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                stop_id VARCHAR,
                station_name VARCHAR

            );"""
        )

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS comment(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                comment VARCHAR,
                time TIME,

                user_pk INTEGER,
                line_pk INTEGER,
                FOREIGN KEY (line_pk) REFERENCES line(pk),
                FOREIGN KEY (user_pk) REFERENCES user(pk)
            );"""
        )


if __name__ == "__main__":
    create_tables()
