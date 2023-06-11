import sqlite3
import bcrypt
import string
import random

from util import generate_token

from flask import Flask, jsonify, request, render_template


class User:

    tablename = "user"
    dbpath = "./data/transit.db"

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.username = kwargs.get("username")
        self.encrypted_password = kwargs.get("encrypted_password")
        self.f_name = kwargs.get("f_name")
        self.l_name = kwargs.get("l_name")
        self.email = kwargs.get('email')
        self.token = kwargs.get('token')

    def save(self):     #saves file
        if self.pk is None:
            self._insert()
        else:
            self._update()
    
    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            sql = """
            INSERT INTO {} (username, encrypted_password, f_name, l_name,  email, token)
            VALUES(?,?,?,?,?,?);
            """.format(self.tablename)

            values = (self.username, self.encrypted_password, self.f_name, self.l_name, self.email, self.token)
            cur.execute(sql, values)

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            sql = """UPDATE {} SET
                     username = ?, encrypted_password = ?, f_name = ?, l_name = ?, email = ?, token = ?
                     WHERE pk = ?;
            """.format(self.tablename)
            values = (self.username, self.encrypted_password, self.f_name, self.l_name, self.email, self.token, self.pk)
            cur.execute(sql, values)
  
    @classmethod
    def login(cls, username, password):

        # return cls.select_one_where("WHERE username=? AND password=?", username, crypted_password)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            sql= f"""SELECT * FROM {cls.tablename} WHERE username == ?
            """

            cur.execute(sql, (username,)) 
            row = cur.fetchone()
            if row is None:
                return False
            
            user_account = cls(**row)

            if not bcrypt.checkpw(password.encode('utf-8'),user_account.encrypted_password): #checking password against crypt password
                return False
            else:
                return user_account

    def get_token(self):
        
        repeat = True
        self.token = generate_token()

        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()

           
            while repeat is True:
                sql = f"""SELECT pk FROM {self.tablename} WHERE token == ?"""
                cur.execute(sql, (self.token,))
                instance = cur.fetchone()

                if instance is None:
                    repeat = False
                else:
                    self.token = generate_token()
            
            sql = f"""UPDATE {self.tablename} SET token = "{self.token}"
                WHERE pk = {self.pk}"""
            cur.execute(sql)



    def del_token(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            sql = f"""UPDATE {self.tablename} SET token="" 
                WHERE pk={self.pk}"""
            cur.execute(sql)


    @classmethod
    def select_one(cls, pk):
        #selects one entry from the database
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            sql = f"""SELECT * FROM {cls.tablename} WHERE pk =?;"""
            cur.execute(sql, (pk,))
            row = cur.fetchone()
            return cls(**row)

    @classmethod
    def select_token(cls, where_clause = "", values = tuple()):
        #selects one entry from the database
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            print(values, "VALUES----------------------")
            sql = f"""SELECT * FROM {cls.tablename} {where_clause};"""
            print(sql)
            cur.execute(sql, values)
            row = cur.fetchone()
            return cls(**row)

if __name__ == "__main__":
    app.run(debug=True)
    
