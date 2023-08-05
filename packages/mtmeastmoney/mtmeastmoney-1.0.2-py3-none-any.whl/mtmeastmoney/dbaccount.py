import sqlite3
import os
from .common import yestoday, today


class DBAccount:
    def __init__(self, database):
        self.database = database
        self.create_database(database=database)
        self.conn = sqlite3.connect(database, check_same_thread=False)

    def create_database(self, database):
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        try:
            cur.execute(f'''CREATE TABLE IF NOT EXISTS ACCOUNT
                (userId TEXT PRIMARY KEY NOT NULL,
                password TEXT NOT NULL,
                fromId TEXT NOT NULL,
                lastDate TEXT NOT NULL DEFAULT '20000101',
                dueDate TEXT NOT NULL,
                isNewBondMsgSend TEXT NOT NULL DEFAULT 'FALSE',
                isAutoSell TEXT NOT NULL DEFAULT 'FALSE',
                tag TEXT,
                api TEXT);''')
        except:
            print("创建失败")
        conn.commit()
        conn.close()
        return

    def insert(self, **kargs):
        if "userId" not in kargs:
            raise Exception("无UserID")
        userId = kargs["userId"]
        cur = self.conn.cursor()
        cursor = cur.execute(f"SELECT * from ACCOUNT where userId='{userId}'")
        if cursor.fetchone() is not None:
            return False
        names = ",".join(list(kargs.keys()))
        values = ",".join([f"'{i}'" for i in kargs.values()])
        cur.execute(f"INSERT INTO ACCOUNT ({names}) VALUES ({values})")
        self.conn.commit()
        return True

    def select(self, userId=None):
        cur = self.conn.cursor()
        if userId is None:
            cursor = cur.execute(f"SELECT * from ACCOUNT")
        else:
            cursor = cur.execute(f"SELECT * from ACCOUNT where userId={userId}")
        return cursor.fetchall()

    def update(self, userId, key, value):
        cur = self.conn.cursor()
        if isinstance(value, str):
            cur.execute(f"UPDATE ACCOUNT set {key} = '{value}' where userId={userId}")
        else:
            cur.execute(f"UPDATE ACCOUNT set {key} = {value} where userId={userId}")
        self.conn.commit()

    def execute(self, sql):
        cur = self.conn.cursor()
        cursor = cur.execute(sql)
        self.conn.commit()
        return cursor

    def __del__(self):
        self.conn.close()
