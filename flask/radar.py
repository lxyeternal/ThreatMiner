# -*-coding:utf-8-*-

import pymysql
import random

# 连接数据库
db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "hack_forums",
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
    reg_date = " 注册时间: " + year_date + "-" + mon_date + "-" + day_date
    if results[17] == 1:
        ishack = "角色 : 黑客"
    else:
        ishack = "角色 : 非黑客"

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

    pre_web = user_web/300
    pre_network = user_network/50
    pre_system = user_system/1200
    pre_database = user_database/50
    pre_mobloe = user_mobile/1800

    max_list = max(pre_database,pre_web,pre_mobloe,pre_network,pre_system)

    if pre_web == max_list:
        field = "研究领域 : web安全"
        word_list = [
            {
                "name": 'DVWA',
                "value": random.randint(6000,13000),
                "textStyle": {
                    "normal": {
                        "color": 'black'
                    },
                    "emphasis": {
                        "color": 'red'
                    }
                }
            },
            {
                "name": 'javascript',
                "value": random.randint(6000,13000)
            },
            {
                "name": 'php',
                "value": random.randint(6000,13000)
            },
            {
                "name": 'xss',
                "value": random.randint(6000,13000)
            },
            {
                "name": 'csrf',
                "value": random.randint(6000,13000)
            },
            {
                "name": 'http',
                "value": random.randint(6000,13000)
            },
            {
                "name": 'github',
                "value": random.randint(6000,13000)
            },
            {
                "name": 'torjan',
                "value": random.randint(6000,13000)
            },
            {
                "name": 'webshell',
                "value": random.randint(6000,13000)
            },
            {
                "name": 'upload files',
                "value": random.randint(6000,13000)
            }
        ]
    elif pre_network == max_list:
        field = "研究领域 : 网络安全"
        word_list = [
            {
                "name": 'network',
                "value": random.randint(6000, 13000),
                "textStyle": {
                    "normal": {
                        "color": 'black'
                    },
                    "emphasis": {
                        "color": 'red'
                    }
                }
            },
            {
                "name": 'http',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'DNS',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Router',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Switcher',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Hub',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Repeater',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Protocol',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'BGP',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'DHCP',
                "value": random.randint(6000, 13000)
            }
        ]
    elif pre_system == max_list:
        field = "研究领域 : 系统安全"
        word_list = [
            {
                "name": 'System',
                "value": random.randint(6000, 13000),
                "textStyle": {
                    "normal": {
                        "color": 'black'
                    },
                    "emphasis": {
                        "color": 'red'
                    }
                }
            },
            {
                "name": 'Linux',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Debug',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Reverse',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Binary',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Memory',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Oday',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'IDA',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'compile',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'link',
                "value": random.randint(6000, 13000)
            }
        ]
    elif pre_database == max_list:
        field = "研究领域 : 数据库安全"
        word_list = [
            {
                "name": 'Database',
                "value": random.randint(6000, 13000),
                "textStyle": {
                    "normal": {
                        "color": 'black'
                    },
                    "emphasis": {
                        "color": 'red'
                    }
                }
            },
            {
                "name": 'oracle',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Mysql',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'injection',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'table',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'mojondb',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'SQL-Server',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'phpmyadmin',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'root',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'primary key',
                "value": random.randint(6000, 13000)
            }
        ]
    else:
        field = "研究领域 : 移动安全"
        word_list = [
            {
                "name": 'Wifi attack Club',
                "value": random.randint(6000, 13000),
                "textStyle": {
                    "normal": {
                        "color": 'black'
                    },
                    "emphasis": {
                        "color": 'red'
                    }
                }
            },
            {
                "name": 'android',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'fingerprint',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Jurassic World',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Apple ios',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'google service',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'signature',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Pitch Perfect',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Bluetooth',
                "value": random.randint(6000, 13000)
            },
            {
                "name": 'Device',
                "value": random.randint(6000, 13000)
            }
        ]
    one_user_infor.append(user_name)
    one_user_infor.append(user_forums)
    one_user_infor.append(ishack)
    one_user_infor.append(field)
    one_user_infor.append(reg_date)
    one_user_infor.append(posts)
    one_user_infor.append(create_posts)

    user_forums_ = user_forums[:-2]
    return one_user_infor,user_forums_,word_list


def rank_hacker(username,forums):

    user_forums = "forum_" + forums
    sql = "select * from users where %s = 1 order by rank_page DESC" % user_forums
    user_name_list = []
    user_rank_list = []
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for user in results:
        user_name_list.append(user[1])

    hacker_order = user_name_list.index(username) + 1

    rank_1 = "第一名:" + results[0][1]
    rank_2 = "第二名:" + results[1][1]
    rank_3 = "第三名:" + results[2][1]
    rank_4 = "第四名:" + results[3][1]
    rank_5 = "第五名:" + results[4][1]
    rank_hack = "第" + str(hacker_order) + "名:" + username

    # page_rank_list = [100*results[0][5],100*results[1][5],100*results[2][5],100*results[3][5],100*results[4][5],100*results[hacker_order][5]]
    #
    user_rank_list.append(rank_1)
    user_rank_list.append(rank_2)
    user_rank_list.append(rank_3)
    user_rank_list.append(rank_4)
    user_rank_list.append(rank_5)
    user_rank_list.append(rank_hack)

    return user_rank_list

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