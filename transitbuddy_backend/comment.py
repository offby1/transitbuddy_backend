import sqlite3
import string

from flask import Flask, jsonify, request
from user import User
from line import Line


class Comment:
    tablename = "comment"
    tablename2 = "line"
    dbpath = "./data/transit.db"

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.comment = kwargs.get("comment")
        self.time = kwargs.get("time")
        self.line_pk = kwargs.get("line_pk")
        self.user_pk = kwargs.get("user_pk")

    def save(self):  # saves file
        if self.pk is None:
            self._insert()
        else:
            self._update()

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            sql = """
            INSERT INTO {} (comment, time, line_pk, user_pk)
            VALUES(?,?,?,?);
            """.format(
                self.tablename
            )
            values = (self.comment, self.time, self.line_pk, self.user_pk)
            cur.execute(sql, values)

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            sql = """UPDATE {} SET
                     comment = ?,  time = ?
                     WHERE pk = ?;
            """.format(
                self.tablename
            )
            values = (self.comment, self.time, self.pk)
            cur.execute(sql, values)

    @classmethod
    def select_one(cls, user_pk):
        with sqlite3.connect(cls.dbpath) as conn:
            cur = conn.cursor()

            sql = """SELECT * FROM {cls.tablename} WHERE user_pk = ? """
            cur.execute(sql, (user_pk))
            comment = cur.fetchone()

            if not comment:
                return None
            comment = cls(**comment)
            return comment

    @classmethod
    def select_all_by_train(cls, train):
        line = Line.select_one(train)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            sql = f"""SELECT * FROM {cls.tablename} WHERE line_pk={line["pk"]}"""
            cur.execute(sql)
            rows = cur.fetchall()
            results = []

            for r in rows:
                user_comments = User.select_one(r["user_pk"])
                comment = {
                    "pk": r["pk"],
                    "comment": r["comment"],
                    "time": r["time"],
                    "line_pk": r["line_pk"],
                    "user_pk": r["user_pk"],
                    "username": user_comments.username,
                }
                results.append(comment)
            return results

    @classmethod
    def select_all(cls, where_clause="", values=tuple()):
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            sql = f"""SELECT * FROM {cls.tablename};"""
            cur.execute(sql, values)
            row = cur.fetchall()
            results = []

            for r in row:
                user_comments = User.select_one(r["user_pk"])
                comment = {
                    "pk": r["pk"],
                    "comment": r["comment"],
                    "time": r["time"],
                    "line_pk": r["line_pk"],
                    "user_pk": r["user_pk"],
                    "username": user_comments.username,
                }
                results.append(comment)

            return results


if __name__ == "__main__":
    app.run(debug=True)
