# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import copy
import csv
import os

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class CsvPipeline(object):
    def process_item(self, item, spider):
        # 如果只保留正文
        if settings.get('ONLY_TEXT'):
            base_dir = '结果文件' + os.sep + 'only_text'
            if not os.path.isdir(base_dir):
                os.makedirs(base_dir)
            file_path = base_dir + os.sep + 'weibo_text.csv'
            first_write = not os.path.isfile(file_path)

            with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                if first_write:
                    writer.writerow(['微博正文'])
                writer.writerow([item['weibo'].get('text', '')])
            return item

        # 原来的完整写入逻辑
        base_dir = '结果文件' + os.sep + item['keyword']
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + item['keyword'] + '.csv'
        is_first = not os.path.isfile(file_path)

        with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if is_first:
                header = [
                    'id', 'bid', 'user_id', '用户昵称', '微博正文', '头条文章url',
                    '发布位置', '艾特用户', '话题', '转发数', '评论数', '点赞数',
                    '发布时间', '发布工具', '微博图片url', '微博视频url',
                    'retweet_id', 'ip', 'user_authentication', '会员类型', '会员等级'
                ]
                writer.writerow(header)
            writer.writerow([
                item['weibo'].get('id', ''),
                item['weibo'].get('bid', ''),
                item['weibo'].get('user_id', ''),
                item['weibo'].get('screen_name', ''),
                item['weibo'].get('text', ''),
                item['weibo'].get('article_url', ''),
                item['weibo'].get('location', ''),
                item['weibo'].get('at_users', ''),
                item['weibo'].get('topics', ''),
                item['weibo'].get('reposts_count', ''),
                item['weibo'].get('comments_count', ''),
                item['weibo'].get('attitudes_count', ''),
                item['weibo'].get('created_at', ''),
                item['weibo'].get('source', ''),
                ','.join(item['weibo'].get('pics', [])),
                item['weibo'].get('video_url', ''),
                item['weibo'].get('retweet_id', ''),
                item['weibo'].get('ip', ''),
                item['weibo'].get('user_authentication', ''),
                item['weibo'].get('vip_type', ''),
                item['weibo'].get('vip_level', 0)
            ])
        return item

class SQLitePipeline(object):
    def open_spider(self, spider):
        try:
            import sqlite3
            # 在结果文件目录下创建SQLite数据库
            base_dir = '结果文件'
            if not os.path.isdir(base_dir):
                os.makedirs(base_dir)
            db_name = settings.get('SQLITE_DATABASE', 'weibo.db')
            self.conn = sqlite3.connect(os.path.join(base_dir, db_name))
            self.cursor = self.conn.cursor()
            # 创建表
            sql = """
            CREATE TABLE IF NOT EXISTS weibo (
                id varchar(20) NOT NULL PRIMARY KEY,
                bid varchar(12) NOT NULL,
                user_id varchar(20),
                screen_name varchar(30),
                text varchar(2000),
                article_url varchar(100),
                topics varchar(200),
                at_users varchar(1000),
                pics varchar(3000),
                video_url varchar(1000),
                location varchar(100),
                created_at DATETIME,
                source varchar(30),
                attitudes_count INTEGER,
                comments_count INTEGER,
                reposts_count INTEGER,
                retweet_id varchar(20),
                ip varchar(100),
                user_authentication varchar(100),
                vip_type varchar(50),
                vip_level INTEGER
            )"""
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(f"SQLite数据库创建失败: {e}")
            spider.sqlite_error = True


    def process_item(self, item, spider):
        data = dict(item['weibo'])
        data['pics'] = ','.join(data['pics'])
        keys = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"""INSERT OR REPLACE INTO weibo ({keys}) 
                 VALUES ({placeholders})"""
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
        except Exception as e:
            print(f"SQLite保存出错: {e}")
            spider.sqlite_error = True
            self.conn.rollback()

    def close_spider(self, spider):
        self.conn.close()

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if len(item['weibo']['pics']) == 1:
            yield scrapy.Request(item['weibo']['pics'][0],
                                 meta={
                                     'item': item,
                                     'sign': ''
                                 })
        else:
            sign = 0
            for image_url in item['weibo']['pics']:
                yield scrapy.Request(image_url,
                                     meta={
                                         'item': item,
                                         'sign': '-' + str(sign)
                                     })
                sign += 1

    def file_path(self, request, response=None, info=None):
        image_url = request.url
        item = request.meta['item']
        sign = request.meta['sign']
        base_dir = '结果文件' + os.sep + item['keyword'] + os.sep + 'images'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        image_suffix = image_url[image_url.rfind('.'):]
        file_path = base_dir + os.sep + item['weibo'][
            'id'] + sign + image_suffix
        return file_path


class MyVideoPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item['weibo']['video_url']:
            yield scrapy.Request(item['weibo']['video_url'],
                                 meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        base_dir = '结果文件' + os.sep + item['keyword'] + os.sep + 'videos'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + item['weibo']['id'] + '.mp4'
        return file_path


class MongoPipeline(object):
    def open_spider(self, spider):
        try:
            from pymongo import MongoClient
            self.client = MongoClient(settings.get('MONGO_URI'))
            self.db = self.client['weibo']
            self.collection = self.db['weibo']
        except ModuleNotFoundError:
            spider.pymongo_error = True

    def process_item(self, item, spider):
        try:
            import pymongo

            new_item = copy.deepcopy(item)
            if not self.collection.find_one({'id': new_item['weibo']['id']}):
                self.collection.insert_one(dict(new_item['weibo']))
            else:
                self.collection.update_one({'id': new_item['weibo']['id']},
                                           {'$set': dict(new_item['weibo'])})
        except pymongo.errors.ServerSelectionTimeoutError:
            spider.mongo_error = True

    def close_spider(self, spider):
        try:
            self.client.close()
        except AttributeError:
            pass


class MysqlPipeline(object):
    def create_database(self, mysql_config):
        """创建MySQL数据库"""
        import pymysql
        sql = """CREATE DATABASE IF NOT EXISTS %s DEFAULT
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci""" % settings.get(
            'MYSQL_DATABASE', 'weibo')
        db = pymysql.connect(**mysql_config)
        cursor = db.cursor()
        cursor.execute(sql)
        db.close()

    def create_table(self):
        """创建MySQL表"""
        sql = """
                CREATE TABLE IF NOT EXISTS weibo (
                id varchar(20) NOT NULL,
                bid varchar(12) NOT NULL,
                user_id varchar(20),
                screen_name varchar(30),
                text varchar(2000),
                article_url varchar(100),
                topics varchar(200),
                at_users varchar(1000),
                pics varchar(3000),
                video_url varchar(1000),
                location varchar(100),
                created_at DATETIME,
                source varchar(30),
                attitudes_count INT,
                comments_count INT,
                reposts_count INT,
                retweet_id varchar(20),
                PRIMARY KEY (id),
                ip varchar(100),
                user_authentication varchar(100),
                vip_type varchar(50),
                vip_level INT
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
        self.cursor.execute(sql)

    def open_spider(self, spider):
        try:
            import pymysql
            mysql_config = {
                'host': settings.get('MYSQL_HOST', 'localhost'),
                'port': settings.get('MYSQL_PORT', 3306),
                'user': settings.get('MYSQL_USER', 'root'),
                'password': settings.get('MYSQL_PASSWORD', '123456'),
                'charset': 'utf8mb4'
            }
            self.create_database(mysql_config)
            mysql_config['db'] = settings.get('MYSQL_DATABASE', 'weibo')
            self.db = pymysql.connect(**mysql_config)
            self.cursor = self.db.cursor()
            self.create_table()
        except ImportError:
            spider.pymysql_error = True
        except pymysql.OperationalError:
            spider.mysql_error = True

    def process_item(self, item, spider):
        data = dict(item['weibo'])
        data['pics'] = ','.join(data['pics'])
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON
                     DUPLICATE KEY UPDATE""".format(table='weibo',
                                                    keys=keys,
                                                    values=values)
        update = ','.join([" {key} = {key}".format(key=key) for key in data])
        sql += update
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
        except Exception:
            self.db.rollback()
        return item

    def close_spider(self, spider):
        try:
            self.db.close()
        except Exception:
            pass


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['weibo']['id'] in self.ids_seen:
            raise DropItem("过滤重复微博: %s" % item)
        else:
            self.ids_seen.add(item['weibo']['id'])
            return item
