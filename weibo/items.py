# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    user_id = scrapy.Field()
    nick_name = scrapy.Field()
    txt = scrapy.Field()
    comments_count = scrapy.Field()
