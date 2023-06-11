import sqlite3
import string

from flask import Flask, jsonify, request


class Line:
    tablename = "line"
    dbpath = "./data/transit.db"

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.line_name = kwargs.get("line_name")

    def save(self):  # saves file
        if self.pk is None:
            self._insert()
        else:
            self._update()

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            sql = """
            INSERT INTO {tablename} (line_name)
            VALUES(?);
            """.format(
                self.tablename
            )

            values = self.line_name
            cur.execute(sql, values)

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            sql = """UPDATE {} SET
                     line_name = ?
                     WHERE pk = ?;
            """.format(
                self.tablename
            )
            values = (self.line_name, self.pk)
            cur.execute(sql, values)

    @classmethod
    def select_one(cls, line_name):
        with sqlite3.connect(cls.dbpath) as conn:
            cur = conn.cursor()
            # print('select_one', line_name)
            sql = f"""SELECT * FROM {cls.tablename} WHERE line_name = ?;"""
            cur.execute(sql, (line_name))
            line = cur.fetchone()
            if not line:
                return None
            return {"pk": line[0], "line_name": line[1]}

    @classmethod
    def select_all(cls, where_clause="", values=tuple()):
        # selects one entry from the database
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            print(values, "VALUES----------------------")
            sql = f"""SELECT * FROM {cls.tablename};"""
            cur.execute(sql, values)
            row = cur.fetchall()
            return cls(**row)


if __name__ == "__main__":
    app.run(debug=True)
