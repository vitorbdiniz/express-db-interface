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

def insert_trail(table, id=None, title='', description='', active=1, backgroundUrlBanner='', backgroundUrlDesktop='', backgroundUrlMobile='', createAt=None, updatedAt=None):
    if id is None:
        id = go_get_id()
    if createAt is None:
        createAt = get_date()
    new_line = {
        'Id':id,
        'Title':title, 
        'Description':description, 
        'Active':active, 
        'BackgroundUrlBanner':backgroundUrlBanner, 
        'BackgroundUrlDesktop':backgroundUrlDesktop, 
        'BackgroundUrlMobile':backgroundUrlMobile, 
        'CreateAt':createAt, 
        'UpdatedAt':updatedAt
    }
    code = create_sql(table,'insert', dic=new_line)
    execute_DML(code)
    add_to_backlog(code)
    return code

def insert_course(table, id=None, productId=0, courseSlug=None, title='', objective=None, certification=None,certificationActive=0, targetAudience=None, workload=None, timeAvailable=None, topics=None, backgroundUrl='', sequential=1, categoryId='', createAt=None, published=1,subscriptionsCount=0, active=1, dropoutPercentage=110, isOpenCourse=0, imgMobileUrl=None, imgBannerUrl=None):
    if id is None:
        id = go_get_id()
    if createAt is None:
        createAt = get_date()
    if courseSlug is None:
        courseSlug = get_slug(title)

    new_line = {
        'Id' : id, 
        'ProductId' : productId, 
        'CourseSlug' : courseSlug, 
        'Title' : title, 
        'Objective' : objective, 
        'Certification' : certification,
        'CertificationActive' : certificationActive, 
        'TargetAudience' : targetAudience, 
        'Workload' : workload, 
        'TimeAvailable' : timeAvailable, 
        'Topics' : topics, 
        'BackgroundUrl' : backgroundUrl, 
        'Sequential' : sequential, 
        'CategoryId' : categoryId, 
        'CreateAt' : createAt, 
        'Published' : published,
        'SubscriptionsCount' : subscriptionsCount, 
        'Active' : active, 
        'DropoutPercentage' : dropoutPercentage, 
        'IsOpenCourse' : isOpenCourse, 
        'ImgMobileUrl' : imgMobileUrl, 
        'ImgBannerUrl' : imgBannerUrl
    }
    code = create_sql(table,'insert', dic=new_line)
    execute_DML(code)
    add_to_backlog(code)
    return code

def insert_module(id=None, title='', order=0, courseId=None,courseName=None, active=1, activeTest=1):
    if id is None:
        id = go_get_id()
    if courseId is None and courseName is not None:
        courseId = execute_query(f"SELECT Id FROM Course WHERE Title='{courseName}';")[0].iloc[0]
    new_line = {
        'Id':id, 
        'Title':title, 
        'Order':order, 
        'CourseId':courseId,
        'Active':active, 
        'ActiveTest':activeTest
    }

    code = create_sql('Module','insert', enter_cols=False, dic=new_line)
    execute_DML(code)
    add_to_backlog(code)
    return code

def insert_lecture(Id=None, ModuleId=None, ModuleName='', CourseName='', LectureSlug=None, Tittle='', Description=None, CreatedAt=None, UpdatedAt=None, Question=None, Order=0, VideoId=0, Active=1, VideoDuration=None, EadboxLectureId=None, IsBonus=0):
    if Id is None:
        Id = go_get_id()
    if CreatedAt is None:
        CreatedAt = get_date()
    if LectureSlug is None:
        LectureSlug = get_slug(Tittle)
    if CourseName is not None and ModuleName is not None and ModuleId is None:
        query = f"""
                    SELECT *
                    FROM Module AS M 
                    WHERE CourseId IN ( SELECT Id FROM Course WHERE Title='{CourseName}') AND Title='{ModuleName}';
                """
        ModuleId = execute_query(query)[0].iloc[0]
    VideoDuration = get_duration(VideoDuration)

    new_line = {
        'Id':Id,
        'ModuleId':ModuleId,
        'LectureSlug':LectureSlug,
        'Tittle':Tittle,
        'Description':Description,
        'CreatedAt':CreatedAt,
        'UpdatedAt':UpdatedAt,
        'Question':Question,
        'Order':Order,
        'VideoId':VideoId,
        'Active':Active,
        'VideoDuration':VideoDuration,
        'EadboxLectureId':EadboxLectureId,
        'IsBonus':IsBonus
    }

    code = create_sql('Lecture','insert', enter_cols=False, dic=new_line)
    execute_DML(code)
    add_to_backlog(code)
    return code

def insert_product(Id=None, Title='', Description=None, ProductSlug=None, Active=1, CreateAt=None, UpdatedAt=None):
    if Id is None:
        Id = go_get_id()
    if CreateAt is None:
        CreateAt = get_date()
    if ProductSlug is None:
        ProductSlug = get_slug(Title)
    if Description is None:
        Description=Title

    new_line = {
        'Id':Id, 
        'Title':Title, 
        'Description':Description, 
        'ProductSlug':ProductSlug, 
        'Active':Active, 
        'CreateAt':CreateAt, 
        'UpdatedAt':UpdatedAt
    }
    code = create_sql('Product','insert', enter_cols=True, dic=new_line)
    execute_DML(code)
    add_to_backlog(code)
    return code

def insert_coursetrail(Id=None, CourseId=None, CourseName='',TrailId=None, TrailName='',CourseTrailOrder=0, CreateAt=None, UpdatedAt=None):
    if Id is None:
        Id = go_get_id()
    if CreateAt is None:
        CreateAt = get_date()
    if TrailId is None:
        TrailId = execute_query(f"SELECT Id FROM Trail WHERE Title='{TrailName}';")[0].iloc[0]
    if CourseId is None:
        CourseId = execute_query(f"SELECT Id FROM Course WHERE Title='{CourseName}';")[0].iloc[0]
        
    new_line = {
        'Id':Id,
        'CourseId':CourseId,
        'TrailId':TrailId,
        'CourseTrailOrder':CourseTrailOrder,
        'CreateAt':CreateAt,
        'UpdatedAt':UpdatedAt
    }
    code = create_sql('CourseTrail','insert', enter_cols=True, dic=new_line)
    execute_DML(code)
    add_to_backlog(code)
    return code

def insert_article(Id=None,LectureId=None,LectureName=None,CourseName=None, ModuleName=None, Title=None,Description='',WordpressUrl=None,Order=None):
    if Id is None:
        Id = execute_query('SELECT MAX(Id) FROM Article;')[0].iloc[0]+1
    if LectureId is None:
        query = f"""
                SELECT Id
                FROM Lecture
                WHERE ModuleId IN (
                                    SELECT Id
                                    FROM Module AS M 
                                    WHERE CourseId IN ( SELECT Id FROM Course WHERE Title='{CourseName}') AND Title='{ModuleName}'
                                    ) AND Tittle='{LectureName}';
        """
        LectureId = execute_query(query)[0].iloc[0]

    new_line ={
        'Id':Id,
        'LectureId':LectureId,
        'Title':Title,
        'Description':Description,
        'WordpressUrl':WordpressUrl,
        'Order':Order
    }

    code = create_sql('Article','insert', enter_cols=False, dic=new_line)
    execute_DML(code)
    add_to_backlog(code)
    return code


def insert_refference(Id=None, LectureId=None, CourseName=None, ModuleName=None, LectureName=None, ReffUrl=None, Order=None, Title=None, Description=None):
    if Id is None:
        Id = go_get_id()

    if LectureId is None:
        query = f"""
                SELECT Id
                FROM Lecture
                WHERE ModuleId IN (
                                    SELECT Id
                                    FROM Module AS M 
                                    WHERE CourseId IN ( SELECT Id FROM Course WHERE Title='{CourseName}') AND Title='{ModuleName}'
                                    ) AND Tittle='{LectureName}';
        """
        LectureId = execute_query(query)[0].iloc[0]

    new_line ={
        'Id':Id,
        'LectureId':LectureId,
        'ReffUrl':ReffUrl,
        'Order':Order,
        'Title':Title,
        'Description':Description
    }

    code = create_sql('Refference','insert', enter_cols=False, dic=new_line)
    execute_DML(code)
    add_to_backlog(code)
    return code


def file_get_infos(data):
    result = []
    for i in range(data.shape[0]):
        if pd.isna(data['Nome Download'].iloc[i]) or data['Nome Download'].iloc[i] == '':
            continue
        if i==0 or data['Nome Aula'].iloc[i-1]!=data['Nome Aula'].iloc[i]:
            order = 1
        elif pd.isna(data['Nome Download'].iloc[i-1]) or data['Nome Download'].iloc[i-1] == '':
            order = 1
        else:
            order += 1

        name = data['Nome Download'].iloc[i]
        CourseName =  data['Curso'].iloc[0]
        LectureName = data['Nome Aula'].iloc[i]
        ModuleName = data['Nome Módulo'].iloc[i]

        query = f"""
                SELECT Id
                FROM Lecture
                WHERE ModuleId IN (
                                    SELECT Id
                                    FROM Module AS M 
                                    WHERE CourseId IN ( SELECT Id FROM Course WHERE Title='{CourseName}') AND Title='{ModuleName}'
                                    ) AND Tittle='{LectureName}';
        """
        lecture_id = execute_query(query)
        lecture_id = lecture_id[0].iloc[0]

        agg = {'lecture_id':lecture_id, 'order':order, 'title':name}
        print(agg)
        js = json.dumps(agg, indent = 4).encode('utf-8')
        f = open(f'{CourseName} - {name}.json', 'wb')
        f.write(js)

        result.append( agg )
    return result


def insert_file(env='hml', lecture_id=None, CourseName=None, LectureName=None, order=1, title=None, file='./', ext=None):
    if ext is None:
        ext = file.split('.')[-1]
    if lecture_id is None:
        query = f"""
                SELECT Id
                FROM Lecture
                WHERE ModuleId IN (
                                    SELECT Id
                                    FROM Module AS M 
                                    WHERE CourseId IN ( SELECT Id FROM Course WHERE Title='{CourseName}') AND Title='{ModuleName}'
                                    ) AND Tittle='{LectureName}';
        """
        lecture_id = execute_query(query)[0].iloc[0]


    user = tc_user(env)

    headers = {'Authorization': f'Bearer {user.get_token()}'}
    headers = json.dumps(headers, indent = 4).encode('utf-8')
    
    file_data = open(file, 'rb')
    fields = {
        "composite_attributes[type]": "File",
        "composite_attributes[file]": (f'{title}.{ext}', file_data, f'application/{ext}')
    }
    fields = json.dumps(fields, indent = 4).encode('utf-8')

    body = {
        'lecture_id': lecture_id,
        'order': order,
        'title': title
    }
    body = json.dumps(body, indent = 4).encode('utf-8')

    
    http = urllib3.PoolManager()
    resp = http.request(headers=headers, body=body, fields=fields)

    return resp



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

