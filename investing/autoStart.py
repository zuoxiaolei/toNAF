# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 10:17:36 2016

@author: aitech
"""
from setting import setFreq
import sys
import time
import random
import os
reload(sys)
sys.setdefaultencoding('utf8')
#导入配置
seconds = setFreq.secnods

while True:
    os.system(r"scrapy crawl autoInvesting")
    print '爬取网站新闻结束进入休眠状态'.encode('gb2312')
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'.encode('gb2312')
    start = time.clock()
    end = time.clock()
    #每隔10分钟爬虫
    while (end-start) < seconds:
        print '正在休眠'.encode('gb2312')
        time.sleep(int(10*random.random()))
        end = time.clock()
        print '休眠了%s秒'.encode('gb2312')%(end-start)
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'.encode('gb2312')