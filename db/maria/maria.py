import mysql.connector
import signal
import time

def timeout_handler(signum, frame):
    raise Exception("Query time out!")

def mdb_connect():
    try:
        conn = mysql.connector.connect(
        host='10.1.1.164',
        port=3306,
        user='dev',
        password='dev',
        database='osvms_vds',
        connection_timeout=3  # 연결 타임아웃 5초
    )
        print("db open..")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Timeout error: {e}")

    finally:
        print("....")
        

mdb_connect()
