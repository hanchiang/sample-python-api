import os

import psycopg2
from psycopg2 import pool

conn_pool = None

def connect():
    try:
        global conn_pool
        conn_pool = psycopg2.pool.SimpleConnectionPool(
            1,
            5,
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME')
        )
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)



