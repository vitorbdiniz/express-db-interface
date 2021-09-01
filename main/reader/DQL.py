import pymysql

import pandas as pd
import numpy as np
import datetime as dt

import urllib3
import json

from os.path import realpath
from main.writer.database import env, tc_user
from main.generator.go_interface import *


'''
connecting to TC-Matrix's databank
'''
def connect_database():
    credentials = env()
    database = pymysql.connect(host=credentials.get_host(), user=credentials.get_user(), password=credentials.get_password(), db=credentials.get_dbname())
    return database

'''
execute a specific MySQL code
'''

def mysql_cursor(code, def_type='DQL'):
    database = connect_database()
    cursor = database.cursor()
    cursor.execute(query=code)
    if def_type != 'DQL':
        database.commit()
    return cursor

def execute_DML(code):
    cursor = mysql_cursor(code, 'DML')
    cursor.close()
    return None

def execute_query(query):
    cursor = mysql_cursor(query)
    df = pd.DataFrame(cursor.fetchall())
    cursor.close()
    return df

def get_mysql_code(path):
    return open(realpath(path), 'r').read()


def create_sql(table, def_type='query', enter_cols=True, dic=None):
    columns = tuple_to_str(dic.keys())
    values = tuple(dic.values())

    if def_type.lower() == 'insert':
        if enter_cols:
            code = f"INSERT INTO {table} ({columns}) VALUES {values};\n\n"
        else:
            code = f"INSERT INTO {table} VALUES {values};\n\n"

    code = none_to_null(code)
    return code


'''

funções de abstração da conexão com o BD 

'''




















'''
AUX
'''
def tuple_to_str(tup):
    string = ''
    for e in tup:
        string += str(e) + ','
    return string[0:len(string)-1]

def none_to_null(string:str):
    return string.replace('None', 'NULL')

def get_duration(VideoDuration):
    if pd.isna(VideoDuration):
        return 0
    d = VideoDuration.split(':')
    total_time = int(d[0])*3600 + int(d[1])*60 + int(d[2])
    return total_time

def add_to_backlog(code):
    backlog = open('./insert_backlog.sql', 'a')
    backlog.write(code)
    backlog.close()

def get_slug(string):
    string = str(string).lower()
    slug = ''
    for c in string:
        if c == 'à' or c == 'á' or c == 'â' or c == 'ã':
            c = 'a'
        elif c == 'è' or c == 'é' or c == 'ê' or c == 'ẽ':
            c = 'e'
        elif c == 'ì' or c == 'í' or c == 'î' or c == 'ĩ':
            c = 'i'
        elif c == 'ò' or c == 'ó' or c == 'ô' or c == 'õ':
            c = 'o'
        elif c == 'ù' or c == 'ú' or c == 'û' or c == 'ũ':
            c = 'u'
        elif c == 'ç':
            c = 'c'
        elif len(slug) > 0 and c == ' ' and slug[-1] != '-':
            c = '-'
        elif len(slug) > 0 and c == ' ' and slug[-1] == '-':
            continue
        slug += c
    return slug

