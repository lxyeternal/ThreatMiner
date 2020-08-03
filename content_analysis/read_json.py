import json
import re
import pymysql






# 连接数据库

db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "apollo",
                     use_unicode=True,
                     charset="utf8"
                     )




def read_json(path):

    f = open(path)
    all_content = []
    result = f.readlines()
    for i in result:
        all_content.append(json.loads(i))
    return all_content



def time_convert(str):

    time = str[0:10]
    month = time[0:2]
    day = time[3:5]
    year = time[6:10]
    new_time = year + month +day
    try:
        new_time = int(new_time)
    except:
        new_time = 00000000
    return new_time



def time_convert1(str):

    time = str[0:10]
    month = time[5:7]
    day = time[8:10]
    year = time[0:4]
    new_time = year + month +day
    new_time = int(new_time)
    return new_time


def store_sql_no(id,user,content,isorigin,forum,url,title,sequence):

    sql = 'insert into forums_2 (id,user,content,isorigin,forum,url,title,sequence) values ("%d", "%s", "%s", "%d", "%s", "%s", "%s", "%d")' % (id,user,content,isorigin,forum,url,title,sequence)
    # print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()


def store_sql_time(id,time,user,content,isorigin,forum,url,title,sequence):

    sql = 'insert into forums_2 (id,time,user,content,isorigin,forum,url,title,sequence) values ("%d","%d","%s", "%s", "%d", "%s", "%s", "%s", "%d")' % (id,time,user,content,isorigin,forum,url,title,sequence)
    # print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()



def Zerodayforum():

    path = 'data/Zerodayforum.json'
    forum = 'Zerodayforum'
    ID = 2000000
    all_content = read_json(path)
    for thread in all_content:
        Thread_theme = thread['Thread_theme']
        Thread_title = thread['Thread_title']
        Thread_url = thread['Thread_url']
        author_content_pair = thread['author_content_pair']
        for one_content in author_content_pair:
            ID = ID + 1
            print(ID)
            content = one_content['content'].strip()
            content = pymysql.escape_string(content)
            author = one_content['author']
            sequence = author_content_pair.index(one_content) + 1
            if sequence == 1:
                isorigin = 1
            else:
                isorigin = 0
            store_sql_no(ID, author, content, isorigin, forum, Thread_url, Thread_title, sequence)


# Zerodayforum()


def Raid():

    path = 'data/Raid.json'
    forum = 'Raid'
    ID = 2003203
    all_content = read_json(path)
    for thread in all_content:
        Thread_theme = thread['Thread_theme']
        Thread_title = thread['Thread_title']
        Thread_url = thread['Thread_url']
        Thread_time = thread['Thread_time']
        Thread_time = time_convert(Thread_time)
        author_content_pair = thread['author_content_pair']
        for one_content in author_content_pair:
            ID = ID + 1
            print(ID)
            content = one_content['content'].strip()
            content = pymysql.escape_string(content)
            author = one_content['author']
            sequence = author_content_pair.index(one_content) + 1
            if sequence == 1:
                isorigin = 1
            else:
                isorigin = 0
            try:
                store_sql_time(ID,Thread_time, author, content, isorigin, forum, Thread_url, Thread_title, sequence)
            except:
                ascii = re.compile('[^a-zA-Z\s]')  # 删除非ascii字符
                Thread_title = ascii.sub(' ', Thread_title)
                store_sql_time(ID,Thread_time, author, content, isorigin, forum, Thread_url, Thread_title, sequence)

# Raid()



def Nulled():

    path = 'data/Nulled.json'
    forum = 'Nulled'
    ID = 2007522
    all_content = read_json(path)
    for thread in all_content:
        Thread_title = thread['Thread_title'].strip()
        Thread_url = thread['Thread_url']
        author_content_pair = thread['author_content_pair']
        for one_content in author_content_pair:
            ID = ID + 1
            print(ID)
            content = one_content['content'].strip()
            content = pymysql.escape_string(content)
            author = one_content['author']
            sequence = author_content_pair.index(one_content) + 1
            if sequence == 1:
                isorigin = 1
            else:
                isorigin = 0
            try:
                store_sql_no(ID, author, content, isorigin, forum, Thread_url, Thread_title, sequence)
            except:
                ascii = re.compile('[^a-zA-Z\s]')  # 删除非ascii字符
                content = ascii.sub(' ', content)
                Thread_title = ascii.sub(' ', Thread_title)
                store_sql_no(ID, author, content, isorigin, forum, Thread_url, Thread_title, sequence)


# Nulled()


def HiddenAnswers():

    path = 'data/HiddenAnswers.json'
    forum = 'HiddenAnswers'
    ID = 2238456
    all_content = read_json(path)
    for thread in all_content:
        Thread_title = thread['Thread_title'].strip()
        Thread_url = thread['Thread_url']
        author_content_pair = thread['author_content_pair']
        for one_content in author_content_pair:
            ID = ID + 1
            print(ID)
            date = one_content['date']
            date = time_convert1(date)
            content = one_content['content'].strip()
            content = pymysql.escape_string(content)
            author = one_content['author']
            sequence = author_content_pair.index(one_content) + 1
            if sequence == 1:
                isorigin = 1
            else:
                isorigin = 0
            try:
                store_sql_time(ID, date, author, content, isorigin, forum, Thread_url, Thread_title, sequence)
            except:
                ascii = re.compile('[^a-zA-Z\s]')  # 删除非ascii字符
                Thread_title = ascii.sub(' ', Thread_title)
                store_sql_time(ID, date, author, content, isorigin, forum, Thread_url, Thread_title, sequence)

# HiddenAnswers()


def Hellboundhackers():

    path = 'data/Hellboundhackers.json'
    forum = 'Hellboundhackers'
    ID = 2301162
    all_content = read_json(path)
    for thread in all_content:
        Thread_title = thread['Thread_title'].strip()
        Thread_url = thread['Thread_url']
        author_content_pair = thread['author_content_pair']
        for one_content in author_content_pair:
            ID = ID + 1
            print(ID)
            date = one_content['datetime']
            day = date[10:12]
            month = date[13:15]
            year = '20' + date[16:18]
            date = int(year + month + day)
            content = one_content['content'].strip()
            content = pymysql.escape_string(content)
            author = one_content['author']
            sequence = author_content_pair.index(one_content) + 1
            if sequence == 1:
                isorigin = 1
            else:
                isorigin = 0
            try:
                store_sql_time(ID, date, author, content, isorigin, forum, Thread_url, Thread_title, sequence)
            except:
                ascii = re.compile('[^a-zA-Z\s]')  # 删除非ascii字符
                Thread_title = ascii.sub(' ', Thread_title)
                content = ascii.sub(' ', content)
                store_sql_time(ID, date, author, content, isorigin, forum, Thread_url, Thread_title, sequence)

# Hellboundhackers()


def Breachforum():

    path = 'data/Breachforum.json'
    forum = 'Breachforum'
    ID = 2310455
    all_content = read_json(path)
    for thread in all_content:
        Thread_title = thread['Thread_title'].strip()
        Thread_url = thread['Thread_url']
        Thread_time = thread['Thread_time']
        Thread_time = time_convert(Thread_time)
        author_content_pair = thread['author_content_pair']
        for one_content in author_content_pair:
            ID = ID + 1
            print(ID)
            content = one_content['content'].strip()
            content = pymysql.escape_string(content)
            author = one_content['author']
            sequence = author_content_pair.index(one_content) + 1
            if sequence == 1:
                isorigin = 1
            else:
                isorigin = 0
            try:
                store_sql_time(ID, Thread_time, author, content, isorigin, forum, Thread_url, Thread_title, sequence)
            except:
                ascii = re.compile('[^a-zA-Z\s]')  # 删除非ascii字符
                Thread_title = ascii.sub(' ', Thread_title)
                store_sql_time(ID, Thread_time, author, content, isorigin, forum, Thread_url, Thread_title, sequence)

# Breachforum()





