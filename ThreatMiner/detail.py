import traceback

import pymysql

# 连接数据库
db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "apollo",
                     use_unicode=True,
                     charset="utf8"
                     )



sql_detail = "select time,content,forum,url from forums where sequence = 1 and title = '%s'"
sql_countuser = "select count(distinct user) from forums where title = '%s'"
sql_startend = "select time from forums where title = '%s'"
sql_forums_id = "select id from forums where title = '%s'"
sql_timeline = "select sentence,time,user,tigger from events where title = '%s' order by time ASC"
sql_domain = "select domain,regi,create_time,expire_date,contact,DNS from domain where f_id = %d"
sql_ip = "select ip,is_malicious,location,des_kind,ip_kind from ip where f_id = %d"
sql_cve = "select cve,nvd_published_date,base_score,vulnerability_type,affected_configuration from cve where f_id = %d"
sql_hash = "select hash,scan_result_history_length,archived,rest_version,top_threat from hash where f_id = %d"
sql_email = "select email,user_name from email where f_id = %d"
sql_relation = "select title,time,tigger from events where user = '%s'"

def time_str(time_int):                      # 20190201 ---->   2019-02-01

    year_date = time_int[:4]
    mon_date = time_int[4:6]
    day_date = time_int[6:8]
    reg_date = year_date + "-" + mon_date + "-" + day_date
    return reg_date

def time_(time_int):                      # 20190201 ---->   2019-02-01

    year_date = time_int[:4]
    mon_date = time_int[5:7]
    day_date = time_int[8:10]
    reg_date = year_date + "-" + mon_date + "-" + day_date
    return reg_date


def time_detail(time_int):                   # 20190201 ---->   2019/02/01

    year_date = time_int[:4]
    mon_date = time_int[4:6]
    day_date = time_int[6:8]
    reg_date = year_date + "/" + mon_date + "/" + day_date
    return reg_date

def time_timeline(time_int):                    # 20190201 ---->   02-01    2019

    year_date = time_int[:4]
    mon_date = time_int[4:6]
    day_date = time_int[6:8]
    reg_date = mon_date + "-" + day_date
    return reg_date,year_date


def get_abstract(title):                         #  获取帖子主题，所属论坛，起止时间，参与人数，创建时间，摘要，url

    head_info = []
    sql_abstract = sql_detail % title
    cursor = db.cursor()
    try:
        db.ping(reconnect=True)  # 如果发现断线会自动重连，可不加 reconnect=True 默认就是。
    except:
        db.error(traceback.format_exc())
    cursor.execute(sql_abstract)
    result = cursor.fetchone()
    time = result[0]
    time = time_str(str(time))
    topic_abstract = result[1]
    topic_forums = result[2]
    topic_url = result[3]
    countuser = get_countuser(title)
    sta_end_time,start_time = get_startend_time(title)
    start_time = time_(start_time)
    head_info.append(title)
    head_info.append(topic_forums)
    head_info.append(sta_end_time)
    head_info.append(countuser)
    head_info.append(time)
    head_info.append(topic_abstract)
    head_info.append(topic_url)
    head_info.append(start_time)
    return head_info

def get_countuser(title):                                #  统计话题参与的总人数

    sql_abstract = sql_countuser % title
    cursor = db.cursor()
    try:
        db.ping(reconnect=True)  # 如果发现断线会自动重连，可不加 reconnect=True 默认就是。
    except:
        db.error(traceback.format_exc())
    cursor.execute(sql_abstract)
    result = cursor.fetchone()
    countuser = result[0]
    return countuser


def get_startend_time(title):                              #  处理话题起止时间

    time_list = []
    sql_startend_time = sql_startend % title
    cursor = db.cursor()
    try:
        db.ping(reconnect=True)  # 如果发现断线会自动重连，可不加 reconnect=True 默认就是。
    except:
        db.error(traceback.format_exc())
    cursor.execute(sql_startend_time)
    result = cursor.fetchall()
    for i in result:
        time_list.append(i[0])
    start_time = min(time_list)
    end_time = max(time_list)
    start_time = time_detail(str(start_time))
    end_time = time_detail(str(end_time))
    sta_end_time = start_time + '--' + end_time
    return sta_end_time,start_time

def timeline_detail(title):                                   #  时间轴所需数据处理

    all_events_list = []
    all_tigger = []
    all_user = []
    title = title.replace("'", "\\'")
    title = title.replace('"', "\\'")
    sql_event_timeline = sql_timeline % title
    cursor = db.cursor()
    try:
        db.ping(reconnect=True)  # 如果发现断线会自动重连，可不加 reconnect=True 默认就是。
    except:
        db.error(traceback.format_exc())
    cursor.execute(sql_event_timeline)
    result = cursor.fetchall()
    for i in result:
        one_list = []
        one_list.append(i[0])
        time_int = str(i[1])
        mon_day,year_date = time_timeline(time_int)
        one_list.append(mon_day)
        one_list.append(year_date)
        one_list.append(i[2])
        all_user.append(i[2])
        all_tigger.append(i[3])
        all_events_list.append(one_list)
    all_tigger = list(set(all_tigger))
    all_user = list(set(all_user))
    return all_events_list,all_tigger,all_user


def get_id(title):                                            #  获取话题所涉及到的所有的forums_id

    forums_id_list = []
    title = title.replace("'", "\\'")
    sql_id = sql_forums_id % title
    cursor = db.cursor()
    try:
        db.ping(reconnect=True)  # 如果发现断线会自动重连，可不加 reconnect=True 默认就是。
    except:
        db.error(traceback.format_exc())
    cursor.execute(sql_id)
    result = cursor.fetchall()
    for i in result:
        forums_id_list.append(i[0])
    return forums_id_list

def get_entity(forums_id_list,sql_entity):                      #    获取单个实体的详情

    entity_list = []
    for id in forums_id_list:
        sql_one = sql_entity % id
        cursor = db.cursor()
        try:
            db.ping(reconnect=True)  # 如果发现断线会自动重连，可不加 reconnect=True 默认就是。
        except:
            db.error(traceback.format_exc())
        cursor.execute(sql_one)
        result = cursor.fetchall()
        for i in result:
            entity_list.append(i)
    entity_list_set = list(set(entity_list))
    return entity_list_set

def get_allentity(title):                                        #  获取所有的情报实体

    forums_id_list = get_id(title)
    ip_list = get_entity(forums_id_list,sql_ip)
    domain_list = get_entity(forums_id_list,sql_domain)
    cve_list = get_entity(forums_id_list,sql_cve)
    hash_list = get_entity(forums_id_list,sql_hash)
    email_list = get_entity(forums_id_list,sql_email)
    return domain_list,ip_list,cve_list,hash_list,email_list

def get_relative_event(title):                                       # 用户事件关联

    all_events_list, all_tigger, all_user = timeline_detail(title)
    all_relation_event = []
    for user in all_user:
        sql_one_relation = sql_relation % user
        cursor = db.cursor()
        try:
            db.ping(reconnect=True)  # 如果发现断线会自动重连，可不加 reconnect=True 默认就是。
        except:
            db.error(traceback.format_exc())
        cursor.execute(sql_one_relation)
        result = cursor.fetchall()
        for one_re in result:
            try:
                if result[2] in all_tigger:
                    all_relation_event.append(one_re)
                else:
                    continue
            except:
                all_relation_event.append(one_re)
    all_relation_event = list(set(all_relation_event))
    return all_relation_event


timeline_detail("Windows for The Linux User - 0x00sec - The Home of the Hacker")