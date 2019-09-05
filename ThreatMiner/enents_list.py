import pymysql
import random

# 连接数据库
db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "apollo",
                     use_unicode=True,
                     charset="utf8"
                     )


sql_new_list = "select distinct title,time from forums order by time DESC"
sql_detail = "select time,content from forums where sequence = 1 and title = '%s'"
sql_all_list = "select distinct title,time from forums order by time ASC"


def time_str(time_int):

    year_date = time_int[:4]
    mon_date = time_int[4:6]
    day_date = time_int[6:8]
    reg_date = year_date + "-" + mon_date
    return reg_date,day_date

def combine(odd_list,even_list):

    combine_list = []
    for i in range(min(len(odd_list),len(even_list))):
        one_new_list = []
        for k in odd_list[i]:
            one_new_list.append(k)
        for m in even_list[i]:
            one_new_list.append(m)
        combine_list.append(one_new_list)

    return combine_list

def random_type():

    a1 = random.randint(0, 3)
    a2 = random.randint(0, 3)
    ran_int = [a1]
    while True:
        if a2 in ran_int:
            a2 = random.randint(0, 3)
        else:
            ran_int.append(a2)
            break
    return ran_int


def new_list():           #  最新事件列表

    count = 0
    even_news_list = []
    odd_news_list = []
    type_list = ["黑客市场交易","黑客网络攻击","安全事件讨论","黑客资产传播"]
    cursor  = db.cursor()
    cursor.execute(sql_new_list)
    results = cursor.fetchall()
    for i in results:
        if count < 8:
            one_list = []
            title = i[0]
            time = i[1]
            sql_one_detail = sql_detail % title
            cursor.execute(sql_one_detail)
            try:
                one_detail_result = cursor.fetchone()
                k = one_detail_result
                ye_mon,day = time_str(str(time))
                ioc = "IOC " + str(random.randint(1, 6))
                a1,a2 = random_type()
                event_type1 = type_list[a1]
                event_type2 = type_list[a2]
                one_list.append(day)
                one_list.append(ye_mon)
                one_list.append(title)
                one_list.append(k[1])
                one_list.append(ioc)
                one_list.append(event_type1)
                one_list.append(event_type2)
                if count % 2 == 0:
                    even_news_list.append(one_list)
                else:
                    odd_news_list.append(one_list)
                count = count + 1
            except:
                continue
        else:
            break
    combine_new_list = combine(even_news_list,odd_news_list)
    return combine_new_list


def all_news_list():            #  全部事件列表

    count = 0
    odd_all_list = []
    even_all_list = []
    type_list = ["黑客市场交易","黑客网络攻击","安全事件讨论","黑客资产传播"]
    cursor = db.cursor()
    cursor.execute(sql_all_list)
    results = cursor.fetchall()
    for i in results:
        if count < 60:
            one_list = []
            title = i[0]
            sql_one_detail = sql_detail % title
            try:
                cursor.execute(sql_one_detail)
                one_detail_result = cursor.fetchone()
                k = one_detail_result
                ye_mon, day = time_str(str(k[0]))
                ioc = "IOC " + str(random.randint(1, 6))
                a1, a2 = random_type()
                event_type1 = type_list[a1]
                event_type2 = type_list[a2]
                one_list.append(day)
                one_list.append(ye_mon)
                one_list.append(title)
                one_list.append(k[1])
                one_list.append(ioc)
                one_list.append(event_type1)
                one_list.append(event_type2)
                if count % 2 == 0:
                    even_all_list.append(one_list)
                else:
                    odd_all_list.append(one_list)
                count = count + 1
            except:
                continue
    combine_all_list = combine(even_all_list,even_all_list)
    return combine_all_list