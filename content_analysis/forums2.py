# -*- coding: utf-8 -*-
# @Project ：content_analysis
# @Time    : 2020-08-02 15:34
# @Author  : honywen
# @FileName: forums2.py
# @Software: PyCharm


import nltk
import pymysql
import re

from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer


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


def user_name():

    username_list = []
    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    for i in forums_name_list:
        forum_username_list = []
        sql = "select distinct user from forums_2 where forum = '%s'" % i
        result = sql_inquire(sql)
        for k in result:
            username = k[0].strip()
            forum_username_list.append(username)
        username_list.append(forum_username_list)
    return username_list


#    获取论坛中的用户名
def get_user():

    forums_user = "select distinct user from forums"
    user_name_list = []
    result = sql_inquire(forums_user)
    for i in result:
        user_name_list.append(i[0])
    return user_name_list


def forums_name():

    forums_user = "select distinct forum from forums_2"
    forum_list = []
    result = sql_inquire(forums_user)
    for i in result:
        forum_list.append(i[0])
    return forum_list



def get_forums():

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    username_list = user_name()
    for forum in forums_name_list:
        forum_index = forums_name_list.index(forum)
        for username in username_list[forum_index]:
            username = pymysql.escape_string(username)
            # username = username.replace("\\", "\\\\")
            # username = username.replace("'", "\\'")
            # username = username.replace('"', "\\'")
            sql = "insert into indicators_2 (user_name,forums) values ('%s','%s')" % (username, forum)
            store_forum(sql)


#   统计每一个用户的创建帖子总数
def start_topics():

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    username_list = user_name()
    for forum in forums_name_list:
        forum_index = forums_name_list.index(forum)
        for username in username_list[forum_index]:
            username = pymysql.escape_string(username)
            # username = username.replace("\\", "\\\\")
            # username = username.replace("'", "\\'")
            # username = username.replace('"', "\\'")
            sql = "select content from forums_2 where user = '%s' and isorigin = 1 and forum = '%s'" % (username, forum)
            result = sql_inquire(sql)
            count = len(result)
            print(count)
            update_sql = "update indicators_2 set start_topics = '%s' where user_name = '%s' and forums = '%s'" % (count, username, forum)
            store_forum(update_sql)


# start_topics()



def start_replies():

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    username_list = user_name()
    for forum in forums_name_list:
        forum_index = forums_name_list.index(forum)
        for username in username_list[forum_index]:
            username = pymysql.escape_string(username)
            # username = username.replace("\\", "\\\\")
            # username = username.replace("'", "\\'")
            # username = username.replace('"', "\\'")
            sql = "select content from forums_2 where user = '%s' and isorigin <> 1 and forum = '%s'" % (username, forum)
            result = sql_inquire(sql)
            count = len(result)
            print(count)
            update_sql = "update indicators_2 set start_replies = '%s' where user_name = '%s' and forums = '%s'" % (count, username, forum)
            store_forum(update_sql)

# start_replies()


def count_word(str):

    str = str.lower()
    str1 = str.strip()  # 去掉头尾空格
    index = 0
    count = 0
    while index < len(str1):
        while str1[index] != " ":  # 有空格时结束当前循环
            index += 1
            if index == len(str1):  # 下标与字符串长度相等结束当前循环
                break
        count += 1  # 计算单词的个数
        if index == len(str1):  # 下标与字符串长度相等结束当前循环
            break
        while str1[index] == " ":  # 单词之间多个空格时，下标加1
            index += 1
    return count




def length_topic():

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    count = 0
    username_list = user_name()
    for forum in forums_name_list:
        forum_index = forums_name_list.index(forum)
        for username in username_list[forum_index]:
            username = pymysql.escape_string(username)
            # username = username.replace("\\", "\\\\")
            # username = username.replace("'", "\\'")
            # username = username.replace('"', "\\'")
            sql = "select content from forums_2 where user = '%s' and isorigin = 1 and forum = '%s'" % (username,forum)
            result = sql_inquire(sql)
            if(len(result) == 0):
                lg_topic = 0
            else:
                all_lg = 0
                num = len(result)
                for i in result:
                    content_lg = count_word(i[0])
                    all_lg = content_lg + all_lg
                lg_topic = format(float(all_lg) / float(num), '.2f')
            count = count + 1
            update_sql = "update indicators_2 set length_topics = '%s' where user_name = '%s' and forums = '%s'" %(lg_topic,username,forum)
            store_forum(update_sql)
            print(count)

# length_topic()


def length_replies():

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    count = 0
    username_list = user_name()
    for forum in forums_name_list:
        # forum_index = forums_name_list.index(forum)
        forum_index = 2
        for username in username_list[forum_index]:
            username = pymysql.escape_string(username)
            sql = "select content from forums_2 where user = '%s' and isorigin <> 1 and forum = '%s'" % (username,forum)
            result = sql_inquire(sql)
            if(len(result) == 0):
                lg_topic = 0
            else:
                all_lg = 0
                num = len(result)
                for i in result:
                    content_lg =  count_word(i[0])
                    all_lg = content_lg + all_lg
                lg_topic = format(float(all_lg) / float(num), '.2f')
            count = count + 1
            update_sql = "update indicators_2 set length_replies = '%s' where user_name = '%s' and forums = '%s'" %(lg_topic,username,forum)
            store_forum(update_sql)
            print(count)


length_replies()



def length_difference():

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    for forum in forums_name_list:
        select_sql = "select user_name,length_topics,length_replies from indicators where forums = '%s'" % forum
        result = sql_inquire(select_sql)
        for i in result:
            username = i[0]
            username = username.replace("\\", "\\\\")
            username = username.replace("'", "\\'")
            username = username.replace('"', "\\'")
            if(i[1] == '0' or i[2] == '0' or i[1] == '0.00' or i[2] == '0.00'):
                length_df = 0
            else:
                length_df = format(float(i[2]) / float(i[1]), '.2f')
            update_sql = "update indicators set length_difference = '%s' where user_name = '%s' and forums = '%s'" %(length_df,username,forum)
            store_forum(update_sql)


def read_dict(path):

    f = open(path)
    word_dict = []
    result = f.readlines()
    for i in result:
        i = i.strip()
        word_dict.append(i)
    return word_dict



#    对文本进行分词，词性还原，去标点等预处理
def nltk2word(record):

    list = []
    clean_word = []
    stem_word = []
    record = record.lower()
    comma = ['!','@','#','$','%','?',',','"','^','*','+','=','[',']','?','.',',',':','(',')',';',"'",'\\',"\'",'I','O','"'
             ,'if','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','it','would','the','this','like','it','one','time','know','in','lot','so','we','well']
    with open("/Users/blue/Documents/StackOverFlow/Txt_Analysis/Data/stopwords.txt","rb") as f:
        stopword = f.readlines()
    for stop in stopword:
        vl = stop.strip()
        comma.append(vl)

    pattern = r"""(?x)                       # set flag to allow verbose regexps 
    	              (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A. 
    	              |\d+(?:\.\d+)?%?       # numbers, incl. currency and percentages 
    	              |\w+(?:[-']\w+)*       # words w/ optional internal hyphens/apostrophe 
    	              |\.\.\.                # ellipsis 
    	              |(?:[.,;"'?():-_`])    # special characters with meanings 
    	            """

    #  基于正则表达式分词
    word = nltk.regexp_tokenize(record, pattern)
    #  词干提取
    snowball_stemmer = SnowballStemmer("english")
    for i in word:
        i = snowball_stemmer.stem(i)
        stem_word.append(i)
    #  词形还原
    wnl = WordNetLemmatizer()
    #  词性标注
    tagged_sent = pos_tag(word)
    ret = select_word(tagged_sent)
    lemmas_sent = []
    for tag in ret:
        tag = lemmatize_all(tag)
        lemmas_sent.append(tag)
        # wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        # lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos))
    # 去停词，标点以及其他符号
    stopworddic = set(stopwords.words('english'))
    for i in lemmas_sent:
        if i not in stopworddic:
            list.append(i)
    for i in list:
        if i not in comma:
            clean_word.append(i)
    return clean_word


#   获取单词的词性
def lemmatize_all(sentence):
    wnl = WordNetLemmatizer()
    special_word = ['xss','csrf','xxe','sql']
    for word, tag in pos_tag(sentence):
        if word in special_word:
            return word
        elif tag.startswith('NN'):
            return wnl.lemmatize(word, pos='n')
        elif tag.startswith('VB'):
            return wnl.lemmatize(word, pos='v')
        elif tag.startswith('JJ'):
            return wnl.lemmatize(word, pos='a')
        elif tag.startswith('R'):
            return wnl.lemmatize(word, pos='r')
        else:
            return word

#    保留特定词性的word
def select_word(pos_tags):
    tags = ['NN', 'NNS','NNP','NNPS', 'VB', 'JJ', 'VBN', 'VBP', 'VBZ', 'RP', 'RB', 'RBR', 'RBS', 'JJ', 'JJR', 'JJS', 'FW', 'NN', 'NNS','NNP', 'NNPS','CD','FW']
    ret = []
    for word, pos in pos_tags:
        if (pos in tags):
            rebuild = (word,pos)
            ret.append(rebuild)
    return ret



def kp_ka(query_sql,dict_txt,update_sql):

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    username_list = user_name()
    for forum in forums_name_list:
        forum_index = forums_name_list.index(forum)
        for username in username_list[forum_index]:
            username = username.replace("\\", "\\\\")
            username = username.replace("'", "\\'")
            username = username.replace('"', "\\'")
            sql = query_sql % (username, forum)
            result = sql_inquire(sql)
            if (len(result) == 0):
                word_count = 0
            else:
                content = ''
                for i in result:
                    content = content + ' ' + i[0]
                word_dict = read_dict(dict_txt)
                content = nltk2word(content)
                word_count = 0
                for word in word_dict:
                    count = content.count(word)
                    word_count = word_count + count
            print(word_count)
            update_sql_ = update_sql % (word_count,username,forum)
            store_forum(update_sql_)


def replies_ka():

    query_sql = "select content from forums where user = '%s' and isorigin <> 1 and forum = '%s'"
    dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/acquire.txt'
    update_sql = "update indicators set replies_ka = '%s' where user_name = '%s' and forums = '%s'"
    kp_ka(query_sql,dict_txt,update_sql)



def topics_ka():

    query_sql = "select content from forums where user = '%s' and isorigin =  1 and forum = '%s'"
    dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/acquire.txt'
    update_sql = "update indicators set topics_ka = '%s' where user_name = '%s' and forums = '%s'"
    kp_ka(query_sql, dict_txt, update_sql)



def replies_kp():

    query_sql = "select content from forums where user = '%s' and isorigin <> 1 and forum = '%s'"
    dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/provide.txt'
    update_sql = "update indicators set replies_kp = '%s' where user_name = '%s' and forums = '%s'"
    kp_ka(query_sql, dict_txt, update_sql)



def topics_kp():

    query_sql = "select content from forums where user = '%s' and isorigin = 1 and forum = '%s'"
    dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/provide.txt'
    update_sql = "update indicators set topics_kp = '%s' where user_name = '%s' and forums = '%s'"
    kp_ka(query_sql, dict_txt, update_sql)



def kp_ka_v(query_sql,dict_txt,update_sql):

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    username_list = user_name()
    count = 0
    for forum in forums_name_list:
        forum_index = forums_name_list.index(forum)
        for username in username_list[forum_index]:
            count = count + 1
            username = username.replace("\\", "\\\\")
            username = username.replace("'", "\\'")
            username = username.replace('"', "\\'")
            sql = query_sql % (username, forum)
            result = sql_inquire(sql)
            count_tiezi = len(result)
            if (count_tiezi == 0):
                kap_v = 0
            else:
                count_in_tiezi = 0
                word_dict = read_dict(dict_txt)
                for i in result:
                    content = i[0]
                    content = nltk2word(content)
                    for word in word_dict:
                        if word in content:
                            count_in_tiezi = count_in_tiezi + 1
                            break
                kap_v = format(float(count_in_tiezi) / float(count_tiezi), '.2f')
            print(count)
            update_sql_ = update_sql % (kap_v, username, forum)
            store_forum(update_sql_)



def replies_ka_v():

    query_sql = "select content from forums where user = '%s' and isorigin <> 1 and forum = '%s'"
    dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/acquire.txt'
    update_sql = "update indicators set replies_vka = '%s' where user_name = '%s' and forums = '%s'"
    kp_ka_v(query_sql,dict_txt,update_sql)


# replies_ka_v()


def topics_ka_v():

    query_sql = "select content from forums where user = '%s' and isorigin =  1 and forum = '%s'"
    dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/acquire.txt'
    update_sql = "update indicators set topics_vka = '%s' where user_name = '%s' and forums = '%s'"
    kp_ka_v(query_sql, dict_txt, update_sql)

# topics_ka_v()


def replies_kp_v():

    query_sql = "select content from forums where user = '%s' and isorigin <> 1 and forum = '%s'"
    dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/provide.txt'
    update_sql = "update indicators set replies_vkp = '%s' where user_name = '%s' and forums = '%s'"
    kp_ka_v(query_sql, dict_txt, update_sql)


# replies_kp_v()



def topics_kp_v():

    query_sql = "select content from forums where user = '%s' and isorigin = 1 and forum = '%s'"
    dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/provide.txt'
    update_sql = "update indicators set topics_vkp = '%s' where user_name = '%s' and forums = '%s'"
    kp_ka_v(query_sql, dict_txt, update_sql)


# topics_kp_v()



def it_word():

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    username_list = user_name()
    for forum in forums_name_list:
        forum_index = forums_name_list.index(forum)
        for username in username_list[forum_index]:
            username = username.replace("\\", "\\\\")
            username = username.replace("'", "\\'")
            username = username.replace('"', "\\'")
            query_sql = "select content from forums where user = '%s' and forum = '%s'"
            dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/ITWord.txt'
            dict_it = []
            word_dict = read_dict(dict_txt)
            word_dict = list(set(word_dict))
            for one in word_dict:
                one = one.lower()
                dict_it.append(one)
            sql = query_sql % (username, forum)
            result = sql_inquire(sql)
            if (len(result) == 0):
                word_count = 0
            else:
                content = ''
                for i in result:
                    content = content + ' ' + i[0]
                content = nltk2word(content)
                word_count = 0
                for word in dict_it:
                    count = content.count(word)
                    word_count = word_count + count
            update_sql = "update indicators set technical_jargon = '%s' where user_name = '%s' and forums = '%s'"
            update_sql_ = update_sql % (word_count, username, forum)
            store_forum(update_sql_)




# it_word()




def ioc_share():

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    username_list = user_name()
    for forum in forums_name_list:
        forum_index = forums_name_list.index(forum)
        for username in username_list[forum_index]:
            username = username.replace("\\", "\\\\")
            username = username.replace("'", "\\'")
            username = username.replace('"', "\\'")
            query_sql = "select content from forums where user = '%s' and forum = '%s'"
            sql = query_sql % (username, forum)
            result = sql_inquire(sql)
            if (len(result) == 0):
                count_ioc = 0
            else:
                content = ''
                for i in result:
                    content = content + ' ' + i[0]
                content = content.lower()
                cve = re.findall(r'cve-\d{4}-\d{4,7}', content)
                # print(cve)
                num_cve = len(cve)
                domain = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
                # print(domain)
                num_domain = len(domain)
                md5 =  re.findall(r'/([a-fA-F0-9]{32})/', content)
                # print(md5)
                num_md5 = len(md5)
                sha1 = re.findall(r'/([a-fA-F0-9]{40})/', content)
                # print(sha1)
                num_sha1 = len(sha1)
                sha256 = re.findall(r'/([a-fA-F0-9]{64})/', content)
                # print(sha256)
                num_sha256 = len(sha256)
                email =  re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', content)
                # print(email)
                num_email = len(email)
                icq = re.findall(r'/icq:.[0-9]{6,12}/', content)
                # print(icq)
                num_icq = len(icq)
                ipv4 = re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', content)
                # print(ipv4)
                num_ipv4 = len(ipv4)
                ipv6 = re.findall(r'^\s*((([0-9A-Fa-f]{1,4}:){7}(([0-9A-Fa-f]{1,4})|:))|(([0-9A-Fa-f]{1,4}:){6}(:|((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})|(:[0-9A-Fa-f]{1,4})))|(([0-9A-Fa-f]{1,4}:){5}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(([0-9A-Fa-f]{1,4}:){4}(:[0-9A-Fa-f]{1,4}){0,1}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(([0-9A-Fa-f]{1,4}:){3}(:[0-9A-Fa-f]{1,4}){0,2}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(([0-9A-Fa-f]{1,4}:){2}(:[0-9A-Fa-f]{1,4}){0,3}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(([0-9A-Fa-f]{1,4}:)(:[0-9A-Fa-f]{1,4}){0,4}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(:(:[0-9A-Fa-f]{1,4}){0,5}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})))(%.+)?\s*$', content)
                # print(ipv6)
                num_ipv6 = len(ipv6)
                count_ioc = num_cve + num_domain + num_email + num_icq + num_ipv4 + num_ipv6 + num_md5 + num_sha1 + num_sha256
            print(count_ioc)
            update_sql = "update indicators set ioc_shares = '%s' where user_name = '%s' and forums = '%s'"
            update_sql_ = update_sql % (count_ioc, username, forum)
            store_forum(update_sql_)


# ioc_share()





def hacker_word():

    forums_name_list = ['Zerodayforum', 'Raid', 'Nulled', 'HiddenAnswers', 'Hellboundhackers', 'Breachforum']
    username_list = user_name()
    for forum in forums_name_list:
        forum_index = forums_name_list.index(forum)
        for username in username_list[forum_index]:
            username = username.replace("\\", "\\\\")
            username = username.replace("'", "\\'")
            username = username.replace('"', "\\'")
            query_sql = "select content from forums where user = '%s' and forum = '%s'"
            dict_txt = '/Volumes/Study/课题/Hacker Figures/Code/content_analysis/dict/hacker.txt'
            sql = query_sql % (username, forum)
            result = sql_inquire(sql)
            if (len(result) == 0):
                word_count = 0
            else:
                content = ''
                for i in result:
                    content = content + ' ' + i[0]
                content = nltk2word(content)
                word_dict = read_dict(dict_txt)
                word_count = 0
                for word in word_dict:
                    count = content.count(word)
                    word_count = word_count + count
            print(word_count)
            update_sql = "update indicators set hacker_jargon = '%s' where user_name = '%s' and forums = '%s'"
            update_sql_ = update_sql % (word_count, username, forum)
            store_forum(update_sql_)