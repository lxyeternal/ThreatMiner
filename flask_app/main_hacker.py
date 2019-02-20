# -*-coding:utf-8-*-

import csv
import pymysql
import itertools

# 连接数据库
db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "user",
                     use_unicode=True,
                     charset="utf8")

over_hacker_order = list(itertools.combinations([6,7,8,9,10,11],2))

# 对黑客关系邻接矩阵进行处理
def getcsv_mian():
    all_user = []
    all_source = []
    num = 0
    csvpath = 'sqldata/network.csv'
    csvpath_num = 'sqldata/network_num.csv'
    csv_file = csv.reader(open(csvpath, 'r'))
    csv_file_num = csv.reader(open(csvpath_num, 'r'))

    for i in csv_file:
        all_user.append(i[0])
    all_user.pop(0)                           # all_user为所有的黑客用户名

    # one_source为网络图中的每一条边，代表两个黑客之间有关系
    # {source: '奥巴马', target: '乔布斯', weight: 1}
    # all_source为所有关系组成的集合
    # source：为起点
    # target：为指向的终点
    # weight：权重

    for k in csv_file_num:
        for j in range(len(k)):
            one_source = []
            one_source_dict = {}
            if k[j] == '0':
                continue
            one_source.append(all_user[num])
            one_source.append(all_user[j])
            one_source.append(k[j])
            one_source_dict['source'] = one_source[0]
            one_source_dict['target'] = one_source[1]
            # one_source_dict['weight'] = int(one_source[2])
            one_source_dict['weight'] = 1
            all_source.append(one_source_dict)
        num = num + 1

    return all_source

# 该函数为对所有的用户进行分类，标明用户所属的论坛
# 数据格式要求：{category: 2, name: 'cwefew'}，2：表示用户来自于第二个论坛即forum_hackthissite_list
def networkclass_mian():

    user_num = 0
    end_class = []                   # 所有分类的用户组成的列表
    forum_0x00sec_list = []          # 属于该论坛的黑客（用户名组成的列表）
    forum_hackthissite_list = []
    forum_antionline_list = []
    forum_garage4hackers_list = []
    forum_hacktoday_list = []
    forum_SafeSkyHacks_list = []
    over_hacker_name_list = []
    class_over_hacker_name_list = []

    cursor = db.cursor()

    sql = "select * from users order by rank_page DESC"

    cursor.execute(sql)
    results = cursor.fetchall()

    for row in results:

        user_num = user_num + 1
        flag = 0
        #   user_value表示网络图中圆圈的大小，值越大圈越大，越明显

        if row[5] >= 0.0007872425:
            user_value = 50
            user_symbolSize = 20
        elif row[5] >= 0.000453549:
            user_value = 30
            user_symbolSize = 16
        elif row[5] >= 0.0002265917:
            user_value = 20
            user_symbolSize = 13
        elif row[5] >= 0.0001289066:
            user_value = 10
            user_symbolSize = 10
        elif row[5] >= 0.0000544649:
            user_value = 5
            user_symbolSize = 6
        else:
            user_value = 3
            user_symbolSize = 3

        try:
            if user_num <= 100:

                one_class_dict = {}                         #  对每一行数据按照flask要求进行格式化

                for k in over_hacker_order:
                    if row[k[0]] == 1 and row[k[1]] == 1:
                        flag = 1
                        over_hacker_name_list.append(str(row[1]))
                        one_class_dict['category'] = 0  # 黑客的所属论坛的分类
                        one_class_dict['name'] = str(row[1])  # 黑客的用户名
                        one_class_dict['value'] = user_value  # 黑客对应的权重大小
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        class_over_hacker_name_list.append(one_class_dict)
                        break

                if flag == 1:
                    continue

                if row[6] == 1:
                    forum_0x00sec_list.append(str(row[1]))
                    one_class_dict['category'] = 1          #   黑客的所属论坛的分类
                    one_class_dict['name'] = str(row[1])    #   黑客的用户名
                    one_class_dict['value'] = user_value    #   黑客对应的权重大小
                    one_class_dict['symbolSize'] = user_symbolSize
                    end_class.append(one_class_dict)
                    continue
                if row[7] == 1:
                    forum_hackthissite_list.append(str(row[1]))
                    one_class_dict['category'] = 2
                    one_class_dict['name'] = str(row[1])
                    one_class_dict['value'] = user_value
                    one_class_dict['symbolSize'] = user_symbolSize
                    end_class.append(one_class_dict)
                    continue
                if row[8] == 1:
                    if row[1] == u'\u59afpy\u5c55ght':
                        forum_antionline_list.append('妯py展ght')
                        one_class_dict['category'] = 3
                        one_class_dict['name'] = '妯py展ght'
                        one_class_dict['value'] = user_value
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        continue
                    if row[1] == u'\u4e09he\u53c8pe\u59c6alist':
                        forum_antionline_list.append('三he又pe姆alist')
                        one_class_dict['category'] = 3
                        one_class_dict['name'] = '三he又pe姆alist'
                        one_class_dict['value'] = user_value
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        continue
                    if row[1] == u'\xa9opy\xaeight':
                        forum_antionline_list.append('©opy®ight')
                        one_class_dict['category'] = 3
                        one_class_dict['name'] = '©opy®ight'
                        one_class_dict['value'] = user_value
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        continue
                    else:
                        forum_antionline_list.append(str(row[1]))
                        one_class_dict['category'] = 3
                        one_class_dict['name'] = str(row[1])
                        one_class_dict['value'] = user_value
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        continue
                if row[9] == 1:
                    if row[1] == u'\u0443\u043b\u044b\u0431\u0430\u0439\u0441\u044f':
                        forum_garage4hackers_list.append('улыбайся')
                        one_class_dict['category'] = 4
                        one_class_dict['name'] = 'улыбайся'
                        one_class_dict['value'] = user_value
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        continue
                    if row[1] == u'\xabspeed|light\xbb':
                        forum_garage4hackers_list.append('«speed | light»')
                        one_class_dict['category'] = 4
                        one_class_dict['name'] = '«speed | light»'
                        one_class_dict['value'] = user_value
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        continue
                    else:
                        forum_garage4hackers_list.append(str(row[1]))
                        one_class_dict['category'] = 4
                        one_class_dict['name'] = str(row[1])
                        one_class_dict['value'] = user_value
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        continue

                if row[10] == 1:
                    forum_hacktoday_list.append(str(row[1]))
                    one_class_dict['category'] = 5
                    one_class_dict['name'] = str(row[1])
                    one_class_dict['value'] = user_value
                    one_class_dict['symbolSize'] = user_symbolSize
                    end_class.append(one_class_dict)
                    continue
                if row[11] == 1:
                    try:
                        forum_SafeSkyHacks_list.append(str(row[1]))
                        one_class_dict['category'] = 6
                        one_class_dict['name'] = str(row[1])
                        one_class_dict['value'] = user_value
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        continue
                    except:
                        forum_SafeSkyHacks_list.append(str(row[1][0]))
                        one_class_dict['category'] = 6
                        one_class_dict['name'] = str(row[1][0])
                        one_class_dict['value'] = user_value
                        one_class_dict['symbolSize'] = user_symbolSize
                        end_class.append(one_class_dict)
                        continue
        except:
            print ('*******error********')
            print ('\n')
            break

    db.close()
    user_list = forum_0x00sec_list + forum_hackthissite_list + forum_antionline_list +  forum_garage4hackers_list + forum_hacktoday_list + forum_SafeSkyHacks_list

    return end_class,user_list


def source_main(all_source,class_user):

    flask_source_main = []

    for k in range(len(all_source)):

        if all_source[k]['source'] in class_user and all_source[k]['target'] in class_user:
            flask_source_main.append(all_source[k])

    return flask_source_main









