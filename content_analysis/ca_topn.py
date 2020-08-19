# -*- coding: utf-8 -*-
# @Project ：content_analysis2
# @Time    : 2020-08-18 11:51
# @Author  : honywen
# @FileName: ca_topn.py
# @Software: PyCharm




import pymysql


# 连接数据库

db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "hackrank",
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


def get_ca(forum):

    sql = "SELECT * from ability_2 WHERE forum = '%s'" % forum
    result = sql_inquire(sql)
    username_list = []
    ca_list = []
    for i in result:
        username_list.append(i[1])
        ca_list.append(float(i[3]))
    zipped = zip(username_list,ca_list)
    sort_zipped = sorted(zipped, key=lambda x: (x[1],x[0]))
    print(sort_zipped)


get_ca('Raid')




