# -*- coding: utf-8 -*-
# @Project ：content_analysis2
# @Time    : 2020-08-17 20:41
# @Author  : honywen
# @FileName: verfiy.py
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



def get_content(username):

    content_sql = "SELECT * from forums_2 WHERE user = '%s'" % username
    result = sql_inquire(content_sql)
    all_content = ''
    for i in result:
        all_content = all_content + '\n' +  i[3].strip()
        # try:
        #     print(en_zn(i[3].strip()))
        # except:
        #     pass
    return all_content




def en_zn(content):

    translator = Translator(to_lang="chinese")
    translation = translator.translate(content)
    return translation




if __name__ == '__main__':

    all_content = get_content('K33P0')
    print(all_content)
    translation = en_zn(all_content)
    print(translation)


