# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os

from scrapy.exceptions import DropItem


class CsvPipeline(object):
    def process_item(self, item, spider):
        file_path = item['keyword'] + '.csv'
        if not os.path.isfile(file_path):
            is_first_write = 1
        else:
            is_first_write = 0
        if item:
            with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                if is_first_write:
                    header = [
                        'id', 'bid', 'user_id', '用户昵称', '微博正文', '发布位置', '艾特用户',
                        '话题', '转发数', '评论数', '点赞数', '发布时间', '发布工具', '微博图片url',
                        '微博视频url'
                    ]
                    writer.writerow(header)
                writer.writerow(
                    [item['weibo'][key] for key in item['weibo'].keys()])
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['weibo']['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['weibo']['id'])
            return item
