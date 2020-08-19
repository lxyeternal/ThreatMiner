# -*- coding: utf-8 -*-
# @Project ：content_analysis2
# @Time    : 2020-08-17 22:35
# @Author  : honywen
# @FileName: degree.py
# @Software: PyCharm



import pymysql
from translate import Translator


# 连接数据库

db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "apollo",
                     use_unicode=True,
                     charset="utf8"
                     )


def sql_inquire(sql):

    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def store_forum(sql):

    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()


def in_degree(username):

    content_sql = "SELECT * from forums_2 WHERE user = '%s' and isorigin = 1" % username
    inquery_url = "SELECT * from forums_2 WHERE isorigin <> 1 and url = '%s'"
    result = sql_inquire(content_sql)
    count = 0
    for i in result:
        url = i[6]
        inqueryurl = inquery_url % url
        indegree = sql_inquire(inqueryurl)
        count = count + len(indegree)
    return count



def out_degree(username):

    content_sql = "SELECT * from forums_2 WHERE user = '%s' and isorigin <> 1" % username
    result = sql_inquire(content_sql)
    return len(result)



if __name__ == '__main__':

    print("username\t入度\t出度\t")
    for username in ['Zaida','Veterun','Psych0path','K33P0','Nord','Anadia','H4ppy']:
        idegree = in_degree(username)
        outdegree = out_degree(username)
        print(username,idegree,outdegree)