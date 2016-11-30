# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import time
from bs4 import BeautifulSoup
from investing.items import InvestingItem
import re
import pymysql
import sys
import logging
from scrapy.utils.log import configure_logging
reload(sys)
sys.setdefaultencoding('utf8')

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO)
logger = logging.getLogger('mycustomlogger')

class InvestingSpider(scrapy.Spider):
    name = 'autoInvesting'
    start_urls =[u'http://www.investing.com/news/stock-market-news']
    #第一层网页解析
    def parse(self,response):
        logger.info('***************start parsing the first class web page****************')


        headUrl = u"http://www.investing.com/news/forex-news/"
        soup = BeautifulSoup(response.body,'lxml')
        target = soup.find('div','midDiv inlineblock')
        strNumber = target.find_all('a')[-1].get_text()
        logger.info('it contain %d url',int(strNumber))

        number = int(strNumber)
        for i in xrange(number):
            url = headUrl+str(i+1)
            yield Request(url,callback=self.parse2)
        time.sleep(0.01)
        logger.info('***************end parsing the first class web page****************')

    #第二层网页解析       
    def parse2(self,response):
        logger.info('***************start parsing the second class web page****************')

        soup = BeautifulSoup(response.body,'lxml')
        target = soup.find_all('div','largeTitle')
        for item in target:
            urlPart = item.find('a').get('href')
            urlHeader = u'http://www.investing.com'
            url = urlHeader+urlPart
            myitem= InvestingItem()
            myitem[u'url'] = url.encode('utf8')

            with open('filter/urlFilter.txt','r') as fh:
                urls = [line.rstrip() for line in fh]
            if url in set(urls):
                continue
            else:
                with open('filter/urlFilter.txt','a') as fh:
                    fh.write(url+u'\n')
                meta = {"item":myitem}
                yield Request(url,callback=self.parse3,meta=meta)
                time.sleep(0.01)
        logger.info('***************end parsing the second class web page****************')

    #第三层网页解析
    def parse3(self,response):
        logger.info('***************start parsing the third class web page****************')
        soup = BeautifulSoup(response.body,'lxml')
        item = response.meta['item']
       
        #获取新闻title
        title = soup.find('h1','articleHeader').get_text()
        
        #获取日期
        date = soup.find('div','contentSectionDetails').find('span').get_text()
        if u"(" in date:
            reobj = re.compile(ur'(.*)')
            date,_ = reobj.subn(u'',date)
        else:
            pass
        #日期转化为时间戳
        date = date.replace(u'ET',u'').rstrip()
        date = str(int(time.mktime(time.strptime(date,'%b %d, %Y %I:%M%p'))))
        
        #获取新闻内容
        temp = soup.find('div','arial_14 clear WYSIWYG newsPage')
        temp = temp.get_text().split(u'\n')
        content = u''
        source = u''
        for p in temp:
            if u' - ' in p:
                source = p.split(u' - ')[0]
            if p.strip==u'' or p==u"                googletag.cmd.push(function() { googletag.display('div-gpt-ad-1466339494851-0'); });":
                pass
            else:
                if content == u'':
                    content = p
                else:
                    content = content+p
        
        item[u'title'] = title.encode('utf8')
        item[u'date'] = date.encode('utf8')
        item[u'source'] = source.encode('utf8')
        item[u'content'] = content.encode('utf8')

        with open('news.txt','a') as fh:
            fh.write(unicode(item[u'url']).replace(u"\n",u'')+u"\t\t"+title.replace(u"\n",u'')+u"\t\t"+date.replace(u"\n",u'')+u"\t\t"+source.replace(u"\n",u'')+u"\t\t"+content.replace(u"\n",u'')+u"\n")
        logger.info(u"*******************************write to file success**************************************************")
        #test
        #print 'this is content:%s'%(content)
        #连接数据库写入数据
        connection = pymysql.connect(host='localhost',port=3306,user='root',password='cafo',db='investing_stock',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = 'INSERT IGNORE INTO news (url, date, source, title,content) VALUES (%s, %s, %s, %s, %s)'
                cursor.execute(sql,(item[u'url'],item[u'date'],item[u'source'],item[u'title'],item[u'content']))
            connection.commit()
        finally:
            connection.close()
        logger.info('***************end parsing the third class web page****************')
        time.sleep(0.01)
        return item
