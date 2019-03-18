# -*-coding:utf-8-*-

'''
首先分类，分出各个论坛的人物
分出各个论坛的网络邻接矩阵
画图
'''

import pymysql

# 连接数据库
db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "hack_forums",
                     use_unicode=True,
                     charset="utf8")

view_button = "查看"
delete_button = "删除"

sql_new = ['create_time','DESC']
sql_alive = ['rank_page','DESC']
sql_all = ['user_name','ASC']

sql_0x00sec = "select * from users where forum_0x00sec = 1 "
sql_hackthissite = "select * from users where forum_hackthissite = 1 "
sql_antionline = "select * from users where forum_antionline = 1 "
sql_garage4hackers = "select * from users where forum_garage4hackers = 1 "
sql_hacktoday = "select * from users where forum_hacktoday = 1 "
sql_SafeSkyHacks = "select * from users where forum_SafeSkyHacks = 1 "

new_sec_list = []
new_hackthissite_list = []
new_antionline_list = []
new_garage4hackers_list = []
new_hacktoday_list = []
new_SafeSkyHacks_list = []

alive_sec_list = []
alive_hackthissite_list = []
alive_antionline_list = []
alive_garage4hackers_list = []
alive_hacktoday_list = []
alive_SafeSkyHacks_list = []

all_sec_list = []
all_hackthissite_list = []
all_antionline_list = []
all_garage4hackers_list = []
all_hacktoday_list = []
all_SafeSkyHacks_list = []

def figure_users(sql_list,sql_forums):

    count = 0
    new_forums_list = []
    sql_in_forums = (sql_forums + "order by " + sql_list[0] + " " + sql_list[1])
    cursor = db.cursor()
    cursor.execute(sql_in_forums)
    results = cursor.fetchall()
    for row in results:
        if count <=5:
            user_list = []
            date = row[18]
            year_date = date[:4]
            mon_date = date[4:6]
            day_date = date[6:8]
            user_name = row[1]
            reg_date = year_date + "-" + mon_date + "-" + day_date
            count = count + 1
            user_list.append(user_name)
            user_list.append(reg_date)
            new_forums_list.append(user_list)
    # print(new_forums_list)
    return new_forums_list

def all_user(sql_list,sql_forums):

    all_forums_list = []
    sql_in_forums = (sql_forums + "order by " + sql_list[0] + " " + sql_list[1])
    cursor = db.cursor()
    cursor.execute(sql_in_forums)
    results = cursor.fetchall()
    for row in results:
        user_list = []
        date = row[18]
        year_date = date[:4]
        mon_date = date[4:6]
        day_date = date[6:8]
        user_name = row[1]
        reg_date = year_date + "-" + mon_date + "-" + day_date
        user_list.append(user_name)
        user_list.append(reg_date)
        all_forums_list.append(user_list)
    return all_forums_list

# if __name__ == "__main__":
#
#     new_sec_list = figure_users(sql_new,sql_0x00sec)
#     new_hackthissite_list = figure_users(sql_new,sql_hackthissite)
#     new_antionline_list = figure_users(sql_new,sql_antionline)
#     new_garage4hackers_list = figure_users(sql_new,sql_garage4hackers)
#     new_hacktoday_list = figure_users(sql_new,sql_hacktoday)
#     new_SafeSkyHacks_list = figure_users(sql_new,sql_SafeSkyHacks)
#
#     alive_sec_list = figure_users(sql_alive,sql_0x00sec)
#     alive_hackthissite_list = figure_users(sql_alive,sql_hackthissite)
#     alive_antionline_list = figure_users(sql_alive,sql_antionline)
#     alive_garage4hackers_list = figure_users(sql_alive,sql_garage4hackers)
#     alive_hacktoday_list = figure_users(sql_alive,sql_hacktoday)
#     alive_SafeSkyHacks_list = figure_users(sql_alive,sql_SafeSkyHacks)
#
#     all_sec_list = all_user(sql_all,sql_0x00sec)
#     all_hackthissite_list = all_user(sql_all,sql_hackthissite)
#     all_antionline_list = all_user(sql_all,sql_antionline)
#     all_garage4hackers_list = all_user(sql_all,sql_garage4hackers)
#     all_hacktoday_list = all_user(sql_all,sql_hacktoday)
#     all_SafeSkyHacks_list = all_user(sql_all,sql_SafeSkyHacks)
