import pymysql

# 连接数据库
db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "apollo",
                     use_unicode=True,
                     charset="utf8"
                     )


sql_allurl = "select distinct forums_url from events"
sql_detail = "select title from forums where url = '%s'"
sql_update = "update events set title = '%s' where forums_url = '%s'"
sql_update1 = "update events set title = %s where forums_url = %s"


def get_allurl():

    allurl_list = []
    cursor = db.cursor()
    cursor.execute(sql_allurl)
    result = cursor.fetchall()
    for i in result:
        allurl_list.append(i[0])
    return allurl_list

def get_title():

    allurl_list = get_allurl()
    for i in allurl_list:
        sql_one = sql_detail % i
        cursor = db.cursor()
        cursor.execute(sql_one)
        result = cursor.fetchone()
        title = result[0]
        update_data(title,i)
        print('ok')


def update_data(title,url):


    title = title.replace("'", "\\'")
    url = url.replace("'", "\\'")
    sql_one = sql_update % (title,url)
    cursor = db.cursor()
    cursor.execute(sql_one)
    db.commit()

get_title()