#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
@Time    : 2020/2/31
@Author  : honywen
@File    : sql2excel.py
'''
# 从数据库中导出数据到excel数据表中
import xlwt
import pymysql
class MYSQL:
    def __init__(self):
        pass
    # def __del__(self):
    #   self._cursor.close()
    #   self._connect.close()
    def connectDB(self):
        """
        连接数据库
        :return:
        """
        try:
            self._connect = pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='1011',
            db='apollo',
            charset='utf8'
            )
            return 0
        except:
          return -1
    def export(self, table_name, forum, output_path):
        self._cursor = self._connect.cursor()
        sql = "select * from  %s where forums = '%s'" %(table_name,forum)
        count = self._cursor.execute(sql)
        # print(self._cursor.lastrowid)
        print(count)
        # 重置游标的位置
        self._cursor.scroll(0, mode='absolute')
        # 搜取所有结果
        results = self._cursor.fetchall()
        # 获取MYSQL里面的数据字段名称
        fields = self._cursor.description
        workbook = xlwt.Workbook()
        # 注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
        # cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
        sheet = workbook.add_sheet('table_'+table_name, cell_overwrite_ok=True)
        # 写上字段信息
        for field in range(0, len(fields)):
          sheet.write(0, field, fields[field][0])
        # 获取并写入数据段信息
        row = 1
        col = 0
        # [3, 4, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        for row in range(1,len(results)+1):
          for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % results[row-1][col])
        workbook.save(output_path)
if __name__ == '__main__':
  mysql = MYSQL()
  flag = mysql.connectDB()
  if flag == -1:
    print('数据库连接失败')
  else:
    print('数据库连接成功')
    for i in ['0x00sec', 'garage4hackers', 'hacktoday', 'SafeSkyHacks.com', 'hackthissite', 'antionline', 'sky-fraud.ru']:
        mysql.export('indicators',i ,'data/' + i + '_indicators.xls')

