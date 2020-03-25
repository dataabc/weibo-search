# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# class WeiboPipeline(object):
# def process_item(self, item, spider):
#     return item
import csv


class CsvPipeline(object):
    def __init__(self):
        file_path = 'result.csv'

        self.file = open(file_path, 'a', encoding="utf-8-sig", newline='')
        self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        if item['id']:
            self.writer.writerow([item[key] for key in item.keys()])
        return item

    def close_spider(self, spider):
        self.file.close()
