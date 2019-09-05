# -*-coding:utf-8-*-

'''
概览页面展示
'''

from main_hacker import *

# 连接数据库
db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "apollo",
                     use_unicode=True,
                     charset="utf8")

sql_one_entity = "select count(*) from %s"
sql_tablechart = "select time,user,type from events order by time DESC"


#  概览页面CVE实体统计
def one_entity(sql_inquery):

    cursor = db.cursor()
    cursor.execute(sql_inquery)
    result = cursor.fetchone()
    entity = result[0]
    return entity

def entity():

    list = ['cve','ip','email','domain','hash']
    entity_list = []
    for i in list:
        one_sql =  sql_one_entity % i
        count_one = one_entity(one_sql)
        entity_list.append(count_one)
    entity_list[0] = 245
    return entity_list

def tablechart():

    ten_list = []
    count = 0
    cursor = db.cursor()
    cursor.execute(sql_tablechart)
    result = cursor.fetchall()
    for i in result:
        if count < 10:
            one_list  = list(i)
            one_list[0] = time_str(str(one_list[0]))
            one_list[2] = type_events(one_list[2])
            ten_list.append(one_list)
            count = count + 1
        else:
            break
    return ten_list

def time_str(time_int):

    year_date = time_int[:4]
    mon_date = time_int[4:6]
    day_date = time_int[6:8]
    reg_date = year_date + "-" + mon_date + "-" + day_date
    return reg_date

def type_events(type):

    if type == 1:
        zn_type = "黑客市场交易"
    elif type == 2:
        zn_type = "黑客资产传播"
    elif type == 3:
        zn_type = "黑客网络攻击"
    else:
        zn_type = "安全事件讨论"
    return zn_type

def linechart():

    list_trade = [120, 132, 101, 134, 90, 230, 210]
    list_attack = [112, 45, 78, 134, 88, 110, 163]
    list_event = [220, 182, 191, 234, 290, 330, 310]
    list_asert = [820, 932, 901, 934, 1290, 1330, 1320]
    return [list_trade,list_attack,list_event,list_asert]

def main_hacker():

    all_source_main = getcsv_mian()
    end_class_main, user_list = networkclass_mian()  # end_class_main:前1000个黑客分类的格式化数据
    flask_source_main = source_main(all_source_main, user_list)
    return end_class_main, flask_source_main