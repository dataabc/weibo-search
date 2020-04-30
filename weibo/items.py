# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    bid = scrapy.Field()
    user_id = scrapy.Field()
    screen_name = scrapy.Field()
    text = scrapy.Field()
    article_url = scrapy.Field()
    location = scrapy.Field()
    at_users = scrapy.Field()
    topics = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    created_at = scrapy.Field()
    source = scrapy.Field()
    pics = scrapy.Field()
    video_url = scrapy.Field()
    retweet_id = scrapy.Field()
