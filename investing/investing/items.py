# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InvestingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url,title,date,source,content = (scrapy.Field(),)*5
    pass
