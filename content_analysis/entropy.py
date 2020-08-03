import numpy as np
import xlrd
import pymysql


# 连接数据库

db = pymysql.connect("127.0.0.1",
                     "root",
                     "1011",
                     "apollo",
                     use_unicode=True,
                     charset="utf8"
                     )


#  从excel文件读取数据矩阵(去掉表头)
def readexcel(path):
    # 读数据并求熵
    sheetname = 'table_indicators'
    data = xlrd.open_workbook(path)
    table = data.sheet_by_name(sheetname)
    nrows = table.nrows
    data=[]
    for i in range(nrows):
        data.append(table.row_values(i))
    return np.array(data)


#  完成数据的归一化
def normal(data):

    # data = data.astype(np.float)
    # 每一列的最值
    maxium=np.max(data,axis=0)
    minium=np.min(data,axis=0)
    data= (data-minium)*1.0/(maxium-minium)
    return data


def entropy(data):

    # 样本数，指标个数
    n, m = np.shape(data)
    ##计算第j项指标，第i个样本占该指标的比重
    sumzb=np.sum(data,axis=0)
    data=data/sumzb
    #对ln0处理
    a=data*1.0
    a[np.where(data==0)]=0.0001
#    #计算每个指标的熵
    e=(-1.0/np.log(n))*np.sum(data*np.log(a),axis=0)
#    #计算权重
    w=(1-e)/np.sum(1-e)
    recodes=np.sum(data*w,axis=0)
    return recodes



def insert_weight(forum,weight):

    sql = "insert into weight (forums,weight_start_topics,weight_start_replies,weight_length_topics,weight_length_replies,weight_length_difference,weight_replies_kp, weight_replies_ka, weight_topics_kp,weight_topics_ka,weight_technical_jargon,weight_hacker_jargon, weight_ioc_shares, weight_topics_vkp,weight_topics_vka, weight_replies_vkp, weight_replies_vka) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
    insert_sql = sql % (forum,str(weight[0]),str(weight[1]),str(weight[2]),str(weight[3]),str(weight[4]),str(weight[5]),str(weight[6]),str(weight[7]),str(weight[8]),str(weight[9]),str(weight[10]),str(weight[11]),str(weight[12]),str(weight[13]),str(weight[14]),str(weight[15]))
    cursor = db.cursor()
    cursor.execute(insert_sql)
    db.commit()




if __name__ == '__main__':

    for forum in ['0x00sec', 'garage4hackers', 'hacktoday', 'SafeSkyHacks.com', 'hackthissite', 'antionline', 'sky-fraud.ru']:
        path = 'data/' + forum + '_indicators.xls'
        data = readexcel(path)
        data = normal(data)
        weight = entropy(data)
        weight = np.around(weight, decimals=4)
        insert_weight(forum,weight)