import os
import json
import datetime

import psycopg2
import psycopg2.extras
from psycopg2 import pool

conn_pool = None

def json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

class Queries:
    @staticmethod
    def get_customers():
        return 'SELECT * FROM customers'
    
    @staticmethod
    def create_customer():
        return 'INSERT INTO customers (name, dob) VALUES(%s, %s)'
    
    @staticmethod
    def get_customer_by_id():
        pass

def connect_db():
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

def get_conn():
    return conn_pool.getconn()

def return_conn(conn):
    conn_pool.putconn(conn)

def format_result_date(row):
    new_row = row
    new_row['dob'] = new_row['dob'].strftime('%Y-%m-%d')
    new_row['updated_at'] = new_row['updated_at'].strftime('%Y-%m-%dT%H-%M-%S')
    return new_row

def query(querystring, params = ((),)):
    conn = get_conn()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(querystring, params)
    print(params)

    rows = cursor.fetchall()
    result = [dict(r) for r in rows]
    print(result)
    result = list(map(lambda row: format_result_date(row), result))
    
    if len(result) == 1:
        return result[0]
    else:
        return result

    cursor.close()
    return_conn(conn)
    return    

def query_mutate(querystring, params=((),)):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(querystring, params)
    print(params)

    conn.commit()
    cursor.close()
    return_conn(conn)


    
    