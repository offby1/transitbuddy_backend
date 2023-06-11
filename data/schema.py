import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, "transit.db")


def schema(db=DBPATH):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()

        cur.execute("""DROP TABLE IF EXISTS user""")
        cur.execute(
            """
                CREATE TABLE user (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR UNIQUE,
                encrypted_password VARCHAR,
                email VARCHAR UNIQUE, 
                f_name VARCHAR,
                l_name VARCHAR,
                token VARCHAR
            );"""
        )

        cur.execute("""DROP TABLE IF EXISTS user_transit""")
        cur.execute(
            """     CREATE TABLE user_transit(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                line VARCHAR,
                station VARCHAR, 
                user_pk INTEGER,
                line_pk VARCHAR,
                FOREIGN KEY (user_pk) REFERENCES user(pk),
                FOREIGN KEY (line_pk) REFERENCES line(pk)
            );"""
        )

        cur.execute("""DROP TABLE IF EXISTS line""")
        cur.execute(
            """     CREATE TABLE line(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                line_name VARCHAR
            );"""
        )

        cur.execute("""DROP TABLE IF EXISTS station""")
        cur.execute(
            """     CREATE TABLE station(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                stop_id VARCHAR,
                station_name VARCHAR
                
            );"""
        )

        cur.execute("""DROP TABLE IF EXISTS comment""")
        cur.execute(
            """
                CREATE TABLE comment(
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
    schema()
