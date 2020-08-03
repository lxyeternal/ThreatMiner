# -*- coding: utf-8 -*-
# @Project ：content_analysis2
# @Time    : 2020-08-03 16:20
# @Author  : honywen
# @FileName: ability.py
# @Software: PyCharm


import pymysql


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


def get_weight(forum):

    weight = []
    sql = "select * from weight where forums = '%s'" % forum
    result = sql_inquire(sql)
    for i in range(2,18):
        weight.append(float(result[0][i]))
    return weight


def get_user_indicator(forum,weight):

    sql = "select * from indicators where forums = '%s'" % forum
    result = sql_inquire(sql)
    user_value_list = []
    for user in result:
        one_value = []
        for index in [3, 4, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
            one_value.append(float(user[index]))
        content_value = sum([a * b for a, b in zip(weight, one_value)])
        content_value = round(content_value, 4)
        user_value_list.append((user[1],content_value))
    return user_value_list


def insert_user_ability(username,forum,value):

    username = username.replace("\\", "\\\\")
    username = username.replace("'", "\\'")
    username = username.replace('"', "\\'")
    sql = "insert into ability (username,forum,content_value) values ('%s','%s','%s')" % (username, forum, value)
    store_forum(sql)



if __name__ == '__main__':

    forum_list = ['0x00sec', 'garage4hackers', 'hacktoday', 'SafeSkyHacks.com', 'hackthissite', 'antionline', 'sky-fraud.ru']
    for forum in forum_list:
        weight = get_weight(forum)
        user_value_list = get_user_indicator(forum,weight)
        for i in user_value_list:
            insert_user_ability(i[0],forum,str(i[1]))