# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta

import scrapy

import weibo.utils.util as util
from weibo.items import WeiboItem
from weibo.utils.location import province_list


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['weibo.com']
    keyword_list = ['迪丽热巴']
    base_url = 'https://s.weibo.com'
    start_date = '2020-03-01'
    end_date = '2020-03-01'

    def start_requests(self):
        for keyword in self.keyword_list:
            url = 'https://s.weibo.com/weibo?q={}'.format(keyword)
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'keyword': keyword})

    def parse(self, response):
        keyword = response.meta.get('keyword')
        is_empty = response.xpath(
            '//div[@class="card card-no-result s-pt20b40"]')
        page_count = len(response.xpath('//ul[@class="s-scroll"]/li'))
        if is_empty:
            print('当前页面搜索结果为空')
        elif page_count < 50:
            # 解析当前页面
            for weibo in self.parse_weibo(response):
                yield weibo
            next_url = response.xpath(
                '//a[@class="next"]/@href').extract_first()
            if next_url:
                next_url = self.base_url + next_url
                yield scrapy.Request(url=next_url, callback=self.parse_page)
        else:
            start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            while start_date <= end_date:
                start_str = start_date.strftime('%Y-%m-%d') + '-0'
                start_date = start_date + timedelta(days=1)
                end_str = start_date.strftime('%Y-%m-%d') + '-0'
                url = 'https://s.weibo.com/weibo?q={}&typeall=1&suball=1&timescope=custom:{}:{}&page=1'.format(
                    keyword, start_str, end_str)
                # 获取一天的搜索结果
                yield scrapy.Request(url=url,
                                     callback=self.parse_by_day,
                                     meta={
                                         'keyword': keyword,
                                         'date': start_str[:-2]
                                     })

    def parse_by_day(self, response):
        """以天为单位筛选"""
        keyword = response.meta.get('keyword')
        is_empty = response.xpath(
            '//div[@class="card card-no-result s-pt20b40"]')
        date = response.meta.get('date')
        page_count = len(response.xpath('//ul[@class="s-scroll"]/li'))
        if is_empty:
            print('当前页面搜索结果为空')
        elif page_count < 50:
            # 解析当前页面
            for weibo in self.parse_weibo(response):
                yield weibo
            next_url = response.xpath(
                '//a[@class="next"]/@href').extract_first()
            if next_url:
                next_url = self.base_url + next_url
                yield scrapy.Request(url=next_url, callback=self.parse_page)
        else:
            start_date_str = date + '-0'
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d-%H')
            for i in range(1, 25):
                start_str = start_date.strftime('%Y-%m-%d-X%H').replace(
                    'X0', 'X').replace('X', '')
                start_date = start_date + timedelta(hours=1)
                end_str = start_date.strftime('%Y-%m-%d-X%H').replace(
                    'X0', 'X').replace('X', '')
                url = 'https://s.weibo.com/weibo?q={}&typeall=1&suball=1&timescope=custom:{}:{}&page=1'.format(
                    keyword, start_str, end_str)
                # 获取一小时的搜索结果
                yield scrapy.Request(url=url,
                                     callback=self.parse_by_hour,
                                     meta={
                                         'keyword': keyword,
                                         'start_time': start_str,
                                         'end_time': end_str
                                     })

    def parse_by_hour(self, response):
        """以小时为单位筛选"""
        keyword = response.meta.get('keyword')
        is_empty = response.xpath(
            '//div[@class="card card-no-result s-pt20b40"]')
        start_time = response.meta.get('start_time')
        end_time = response.meta.get('end_time')
        page_count = len(response.xpath('//ul[@class="s-scroll"]/li'))
        if is_empty:
            print('当前页面搜索结果为空')
        elif page_count < 50:
            # 解析当前页面
            for weibo in self.parse_weibo(response):
                yield weibo
            next_url = response.xpath(
                '//a[@class="next"]/@href').extract_first()
            if next_url:
                next_url = self.base_url + next_url
                yield scrapy.Request(url=next_url, callback=self.parse_page)
        else:
            for province in province_list:
                url = 'https://s.weibo.com/weibo?q={}&region=custom:{}:1000&typeall=1&suball=1&timescope=custom:{}:{}&page=1'.format(
                    keyword, province['id'], start_time, end_time)
                # 获取一小时一个省的搜索结果
                yield scrapy.Request(url=url,
                                     callback=self.parse_by_hour_province,
                                     meta={
                                         'keyword': keyword,
                                         'start_time': start_time,
                                         'end_time': end_time,
                                         'province': province
                                     })

    def parse_by_hour_province(self, response):
        """以小时和直辖市/省为单位筛选"""
        keyword = response.meta.get('keyword')
        is_empty = response.xpath(
            '//div[@class="card card-no-result s-pt20b40"]')
        start_time = response.meta.get('start_time')
        end_time = response.meta.get('end_time')
        province = response.meta.get('province')
        page_count = len(response.xpath('//ul[@class="s-scroll"]/li'))
        if is_empty:
            print('当前页面搜索结果为空')
        elif page_count < 50:
            # 解析当前页面
            for weibo in self.parse_weibo(response):
                yield weibo
            next_url = response.xpath(
                '//a[@class="next"]/@href').extract_first()
            if next_url:
                next_url = self.base_url + next_url
                yield scrapy.Request(url=next_url, callback=self.parse_page)
        else:
            for city in province['city_list']:
                url = 'https://s.weibo.com/weibo?q={}&region=custom:{}:{}&typeall=1&suball=1&timescope=custom:{}:{}&page=1'.format(
                    keyword, province['id'], city['id'], start_time, end_time)
                # 获取一小时一个城市的搜索结果
                yield scrapy.Request(url=url,
                                     callback=self.parse_page,
                                     meta={
                                         'keyword': keyword,
                                         'start_time': start_time,
                                         'end_time': end_time,
                                         'province': province,
                                         'city': city
                                     })

    def parse_page(self, response):
        """解析一页搜索结果的信息"""
        is_empty = response.xpath(
            '//div[@class="card card-no-result s-pt20b40"]')
        if is_empty:
            print('当前页面搜索结果为空')
        else:
            for weibo in self.parse_weibo(response):
                yield weibo
            next_url = response.xpath(
                '//a[@class="next"]/@href').extract_first()
            if next_url:
                next_url = self.base_url + next_url
                yield scrapy.Request(url=next_url, callback=self.parse_page)

    def parse_weibo(self, response):
        """解析网页中的微博信息"""
        for sel in response.xpath("//div[@class='card-wrap']"):
            info = sel.xpath(
                "div[@class='card']/div[@class='card-feed']/div[@class='content']/div[@class='info']"
            )
            if info:
                weibo = WeiboItem()
                weibo['id'] = sel.xpath('@mid').extract_first()

                weibo['user_id'] = info[0].xpath(
                    'div[2]/a/@href').extract_first().split('?')[0].split(
                        '/')[-1]
                weibo['nick_name'] = info[0].xpath(
                    'div[2]/a/@nick-name').extract_first()
                weibo['txt'] = sel.xpath('.//p[@class="txt"]')[0].xpath(
                    'string(.)').extract_first().replace('\u200b', '').replace(
                        '\ue627', '')
                reposts_count = sel.xpath(
                    './/a[@action-type="feed_list_forward"]/text()'
                ).extract_first()
                weibo['reposts_count'] = reposts_count
                reposts_count = re.findall(r'\d+.*', reposts_count)
                weibo['reposts_count'] = reposts_count[
                    0] if reposts_count else '0'
                comments_count = sel.xpath(
                    './/a[@action-type="feed_list_comment"]/text()'
                ).extract_first()
                comments_count = re.findall(r'\d+.*', comments_count)
                weibo['comments_count'] = comments_count[
                    0] if comments_count else '0'
                attitudes_count = sel.xpath(
                    './/a[@action-type="feed_list_like"]/em/text()'
                ).extract_first()
                weibo['attitudes_count'] = (attitudes_count
                                            if attitudes_count else '0')
                created_at = sel.xpath(
                    '(.//p[@class="from"])[last()]/a[1]/text()').extract_first(
                    ).replace(' ', '').replace('\n', '').split('前')[0]
                weibo['created_at'] = util.standardize_date(created_at)
                source = sel.xpath(
                    './/p[@class="from"]/a[2]/text()').extract_first()
                weibo['source'] = source
                print(weibo)
                yield weibo
