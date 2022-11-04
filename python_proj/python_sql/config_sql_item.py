import json
import random
import sys
import time
import traceback
from typing import List

#from time_log import time_log, error_log
import pyodbc
import multiprocessing
#from top_import_manager import is_config_sql_enable

json_sql_path = "configs/sql.json"
CONN_POOL_LEN = 10
CONN_MAX_COUNT = 12800


def read_sql_json():
    with open(json_sql_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class ConfigSqlItem:
    def __init__(self):
        self.id = ""
        self.sql = ""


class OdbcConnItem:
    def __init__(self):
        #time_log(conn)
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=127.0.0.1,1434;DATABASE=an_gang;UID=sa;PWD=6923263')
        self.cursor = self.conn.cursor()
        self.committing = False
        self.count = random.randint(0, CONN_MAX_COUNT / 16)


class SqlOperation:
    def __init__(self) -> None:
        self._locker = multiprocessing.Lock()
        #self._str_sql = read_sql_json()
        self._conns: List[OdbcConnItem] = []
        #for i in range(CONN_POOL_LEN):
        self._conns.append(OdbcConnItem())
        self._number = 0
        self.sqls: {str: str} = {}
        #for item in self._str_sql["sqls"]:
            #self.sqls[item["id"]] = " ".join(item["sql"])

    def acquire_cursor(self):
        retry_times = 0
        while True:
            with self._locker:
                if not self._conns:
                    return None
                for i in range(CONN_POOL_LEN):
                    self._number += 1
                    if self._number >= CONN_POOL_LEN:
                        self._number = 0
                    conn = self._conns[0]
                    if not conn.committing:
                        # sys.stdout.write("acquire conn.no {}\n".format(self._number))
                        conn.committing = True
                        return conn.cursor
            retry_times += 1
            #error_log("failed to acquire conn from pool: " + str(retry_times))
            if retry_times > 6:
                return None
            time.sleep(0.03)

    def release_cursor(self, cursor):
        conn: OdbcConnItem = None
        with self._locker:
            for item in self._conns:
                if item.cursor == cursor:
                    item.count += 1
                    if item.count > CONN_MAX_COUNT:
                        conn = item
                    else:
                        item.committing = False
                    break
        if conn is not None:
            # replace conn with a new
            with self._locker:
                self._conns.remove(conn)
            try:
                conn.conn.close()
            except:
                traceback.print_exc()
            try:
                conn = OdbcConnItem(self._str_sql["conn"])
            except:
                traceback.print_exc()
            with self._locker:
                self._conns.append(conn)

    def execute(self, key):#, *params):更新 插入
        cursor = self.acquire_cursor()
        try:
            cursor.execute(key)
            cursor.commit()
        finally:
            self.release_cursor(cursor)

    def fetch_all(self, key):#, *params):
        cursor = self.acquire_cursor()
        try:
            cursor.execute(key)
            return cursor.fetchall()
        finally:
            self.release_cursor(cursor)

    def fetch_one(self, key):#, *params):
        cursor = self.acquire_cursor()
        try:
            cursor.execute(key)
            return cursor.fetchone()
        finally:
            self.release_cursor(cursor)

    def close(self):
        while self._conns:
            #time_log("closing no {}".format(len(self._conns)))
            with self._locker:
                if not self._conns[-1].committing:
                    odbc = self._conns.pop()
                    try:
                        odbc.conn.close()
                    except:
                        traceback.print_exc()


#sql_executor = None
#if is_config_sql_enable():
sql_executor = SqlOperation()
