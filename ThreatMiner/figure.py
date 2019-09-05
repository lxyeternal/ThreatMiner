# -*-coding:utf-8-*-

import pymysql

# 连接数据库
db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "apollo",
                     use_unicode=True,
                     charset="utf8")

def all_user_radar():

    all_user_value = []
    all_user_data = []
    all_name_list = []
    max_value = []
    cursor = db.cursor()
    sql = "select * from users"
    sql_web = "select * from users order by num_web DESC"
    sql_network = "select * from users order by num_network DESC"
    sql_system = "select * from users order by num_system DESC"
    sql_database = "select * from users order by num_database DESC"
    sql_mobile = "select * from users order by num_mobile DESC"

    cursor.execute(sql_web)
    results_web = cursor.fetchall()
    max_value.append(results_web[0][12])

    cursor.execute(sql_network)
    results_network = cursor.fetchall()
    max_value.append(results_network[0][13])

    cursor.execute(sql_system)
    results_system = cursor.fetchall()
    max_value.append(results_system[0][14])

    cursor.execute(sql_database)
    results_database = cursor.fetchall()
    max_value.append(results_database[0][15])

    cursor.execute(sql_mobile)
    results_mobile = cursor.fetchall()
    max_value.append(results_mobile[0][16])

    cursor.execute(sql)
    results = cursor.fetchall()

    for row in results:

        try:
            user_value = []
            user_dict = {}
            user_radar_list = []
            user_name = str(row[1])
            if(row[12] + 100>= 300):
                user_web = 300
            else:
                user_web = row[12] + 100
            if(row[13] + 10 >= 50):
                user_network = 50
            else:
                user_network = row[13] + 10
            if(row[14] + 500 >= 1200):
                user_system = 1200
            else:
                user_system = row[14] + 500
            if(row[15] + 10 >= 50):
                user_database = 50
            else:
                user_database = row[15] + 10
            if(row[16] + 800 >= 1800):
                user_mobile = 1800
            else:
                user_mobile = row[16] + 800
            pre_web = user_web / 300
            pre_network = user_network / 50
            pre_system = user_system / 1200
            pre_database = user_database / 50
            pre_mobloe = user_mobile / 1800

            max_list = max(pre_database, pre_web, pre_mobloe, pre_network, pre_system)

            if pre_web == max_list:
                field = " web安全"
            elif pre_network == max_list:
                field = "网络安全"
            elif pre_system == max_list:
                field = "系统安全"
            elif pre_database == max_list:
                field = "数据库安全"
            else:
                field = "移动安全"

            user_value.append(user_web)
            user_value.append(user_network)
            user_value.append(user_system)
            user_value.append(user_database)
            user_value.append(user_mobile)
            all_user_value.append(user_value)
            user_dict['name'] = user_name
            user_dict['value'] = user_value
            user_radar_list.append(user_dict)
            all_user_data.append(user_radar_list)
            all_name_list.append(user_name)

        except:
            continue

    return max_value,all_user_data,all_name_list


def one_user_radar(username):

    name = username
    all_user_value = []
    cursor = db.cursor()
    sql = "select * from users where user_name = '%s'"
    sql_radar = sql % name
    cursor.execute(sql_radar)
    row = cursor.fetchone()
    user_dict = {}
    try:
        user_value = []
        user_name = str(row[1])
        if (row[12] + 100 >= 300):
            user_web = 300
        else:
            user_web = row[12] + 100
        if (row[13] + 10 >= 50):
            user_network = 50
        else:
            user_network = row[13] + 10
        if (row[14] + 500 >= 1200):
            user_system = 1200
        else:
            user_system = row[14] + 500
        if (row[15] + 10 >= 50):
            user_database = 50
        else:
            user_database = row[15] + 10
        if (row[16] + 800 >= 1800):
            user_mobile = 1800
        else:
            user_mobile = row[16] + 800

        user_value.append(int(user_web))
        user_value.append(int(user_network))
        user_value.append(int(user_system))
        user_value.append(int(user_database))
        user_value.append(int(user_mobile))
        all_user_value.append(user_value)
        user_dict['value'] = user_value
        user_dict['name'] = user_name

    except:
        pass
    return [user_dict]

def user_information(name):

    sql = "select * from users where user_name = '%s'"
    sql_info = sql % name
    one_user_infor = []
    cursor = db.cursor()
    cursor.execute(sql_info)
    results = cursor.fetchone()
    user_name = results[1]
    create_posts = "创建话题数:" + str(results[3])
    posts = "总发言条数:" + str(results[2])
    date = results[18]
    year_date = date[:4]
    mon_date = date[4:6]
    day_date = date[6:8]
    reg_date = " 创建时间:" + year_date + "-" + mon_date + "-" + day_date

    if results[6] == 1:
        user_forums = "0x00sec论坛"
    if results[7] == 1:
        user_forums = "hackthissite论坛"
    if results[8] == 1:
        user_forums = "antionline论坛"
    if results[9] == 1:
        user_forums = "garage4hackers论坛"
    if results[10] == 1:
        user_forums = "hacktoday论坛"
    if results[11] == 1 :
        user_forums = "safeSkyHacks论坛"

    if (results[12] + 100 >= 300):
        user_web = 300
    else:
        user_web = results[12] + 100
    if (results[13] + 10 >= 50):
        user_network = 50
    else:
        user_network = results[13] + 10
    if (results[14] + 500 >= 1200):
        user_system = 1200
    else:
        user_system = results[14] + 500
    if (results[15] + 10 >= 50):
        user_database = 50
    else:
        user_database = results[15] + 10
    if (results[16] + 800 >= 1800):
        user_mobile = 1800
    else:
        user_mobile = results[16] + 800

    pre_web = user_web / 300
    pre_network = user_network / 50
    pre_system = user_system / 1200
    pre_database = user_database / 50
    pre_mobloe = user_mobile / 1800

    max_list = max(pre_database, pre_web, pre_mobloe, pre_network, pre_system)

    if pre_web == max_list:
        field = " web安全"
    elif pre_network == max_list:
        field = "网络安全"
    elif pre_system == max_list:
        field = "系统安全"
    elif pre_database == max_list:
        field = "数据库安全"
    else:
        field = "移动安全"

    one_user_infor.append(user_name)
    one_user_infor.append(user_forums)
    one_user_infor.append(reg_date)
    one_user_infor.append(posts)
    one_user_infor.append(create_posts)
    user_forums_ = user_forums[:-2]
    return one_user_infor,user_forums_,field


def rank_hacker(username,forums):

    username = username.lower()
    user_forums = "forum_" + forums
    sql = "select * from users where %s = 1 order by rank_page DESC" % user_forums
    user_name_list = []
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for user in results:
        user_name_list.append(user[1])
    hacker_order = user_name_list.index(username)

    user_rank_list = [username,results[4][1],results[3][1],results[2][1],results[1][1],results[0][1]]
    user_rank_value = [results[hacker_order][5],results[4][5],results[3][5],results[2][5],results[1][5],results[0][5]]
    user_rank_value = reflect_hundred(user_rank_value)
    return user_rank_list,user_rank_value

def user_post(username):

    sql = "select * from users where user_name = '%s'"
    sql_post = sql % username
    cursor = db.cursor()
    cursor.execute(sql_post)
    result_post = cursor.fetchone()
    post_list = [int(result_post[19]),int(result_post[20]),int(result_post[21]),int(result_post[22]),int(result_post[23]),int(result_post[24]),int(result_post[25]),int(result_post[26]),int(result_post[27]),int(result_post[28])]
    return post_list

def user_act(username,forums):

    forums = "forum_" + forums
    sql = "select sum(posts) from users where %s = 1" % (forums)
    sql2 = "select posts from users where user_name = '%s'" % username
    cursor = db.cursor()
    cursor.execute(sql)
    all_results = cursor.fetchone()[0]
    cursor.execute(sql2)
    one_result = cursor.fetchone()[0]
    info = int(one_result/all_results*100)+1

    return [info,100-info]


def user_rec_post(username):

    sql = "select * from forums where user = '%s' order by time DESC limit 3"
    act_list = []
    sql_act = sql % username
    cursor = db.cursor()
    cursor.execute(sql_act)
    result = cursor.fetchall()
    for row in result:
        date = str(row[1])
        year_date = date[:4]
        mon_date = date[4:6]
        day_date = date[6:8]
        reg_date = year_date + "-" + mon_date + "-" + day_date
        act_list.append([reg_date,row[3]])

    return act_list

def user_alive(username):

    sql = "select * from users where user_name = '%s'"
    sql_alive = sql % username
    cursor = db.cursor()
    cursor.execute(sql_alive)
    results = cursor.fetchone()
    posts = results[2]
    create_posts = results[3]

    return [posts,create_posts]

def time_str(time_int):

    date = str(time_int)
    year_date = date[:4]
    mon_date = date[4:6]
    day_date = date[6:8]
    reg_date = year_date + "-" + mon_date + "-" + day_date
    return reg_date


def reflect_hundred(value):

    k = 90 / (max(value) - min(value))
    transform_value = [k * (x - min(value)) + 10 for x in value]
    for i in transform_value:
        transform_value[transform_value.index(i)] = int(i)
    return transform_value

def hacker_events(username):

    sql_title = "select distinct title,time from forums where user = '%s' order by time DESC"
    sql = "select tigger from events where user= '%s' and title = '%s'"
    sql_user_title = sql_title % username
    count = 0
    event_list = []
    cursor = db.cursor()
    cursor.execute(sql_user_title)
    results = cursor.fetchall()
    for i in results:
        if count < 6:
            i = list(i)
            title = i[0]
            tigger_list = []
            title = title.replace("'", "\\'")
            sql_event = sql % (username,title)
            cursor = db.cursor()
            cursor.execute(sql_event)
            tigger = cursor.fetchall()
            for m in tigger:
                tigger_list.append(m[0])
            tigger_list = list(set(tigger_list))
            if len(tigger_list) >= 3:
                tigger_list = [tigger_list[0],tigger_list[1],tigger_list[2]]
            i.append(tigger_list)
            time = i[1]
            time = time_str(time)
            i[1] = time
            event_list.append(i)
            count = count + 1
        else:
            break

    return event_list
