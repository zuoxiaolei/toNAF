# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 10:56:11 2016

@author: zuoxiaolei
"""
from textToNAF import text2NAF
import pymysql.cursors
import hashlib
#获取数据库数据
connection = pymysql.connect(host='localhost',port=3306,user='root',password='cafo',db='investing_stock',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sql = 'SELECT * from news WHERE is_old = 0'
        cursor.execute(sql)
        news = cursor.fetchall()
    connection.commit()
    
    with connection.cursor() as cursor:
        sql = 'UPDATE news set is_old=1 WHERE is_old = 0'
        cursor.execute(sql)
    connection.commit()
finally:
    connection.close()
#数据整理
m = hashlib.md5()
for entity in news:
    content = entity[u'content']
    title = entity[u'title']
    url = entity[u'url']
    m.update(entity[u'content'])
    publicId = m.hexdigest()
    date = 
    text2NAF(content,date,title,publicId,url)
#转化为NAF
