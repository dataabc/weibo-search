# settings.py
# -*- coding: utf-8 -*-

BOT_NAME = 'weibo'
SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'

COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False
LOG_LEVEL = 'ERROR'

# 访问完一个页面再访问下一个时需要等待的时间，默认为10秒
DOWNLOAD_DELAY = 10

DEFAULT_REQUEST_HEADERS = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cookie': 'SCF=Aq-KibgcfexCww1CL1YG-n6SZSbkzlQ9GF3Bmg7PKnJNuWBD_Lhlcjk3uy-ch2Cq2mc9i9JPWt-Ov7-G-JKtcFU.; XSRF-TOKEN=S6MgN82GsKv3W4dQ9My1ABs5; SUB=_2A25FLddKDeRhGeFG7FIY9SfIwj-IHXVmQ1aCrDV8PUNbmtAbLW3NkW9NeO75-14_F7JfgxkHKgxHiPrk4wY8G6Ue; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFbruNJuh6sTGaQgnopIFUg5NHD95QN1hM71K-4Sh.0Ws4DqcjHi--ci-i2iK.Ri--ci-i2iK.R1K2c; ALF=02_1750152218; WBPSESS=1dBqaYQOifgQXP1GqXCLSRGT4UAwkoGufHMuL9wkdV0K5BvZHmxviJ_T6ePKBq9io3yuLmEL9dSQ046txXOn6VElnDo8IS-7stpEfmL8FQsJFMGhLNI4pVQGlrjNgo6L-aJSelqBtQFGtAni9F0fNw=='
}

# 只保留微博正文的开关
ONLY_TEXT = True

ITEM_PIPELINES = {
    #'weibo.pipelines.DuplicatesPipeline': 300,
    'weibo.pipelines.CsvPipeline': 301,
    # 'weibo.pipelines.MysqlPipeline': 302,
    # 'weibo.pipelines.MongoPipeline': 303,
    # 'weibo.pipelines.MyImagesPipeline': 304,
    # 'weibo.pipelines.MyVideoPipeline': 305,
    # 'weibo.pipelines.SQLitePipeline': 306
}

# 要搜索的关键词列表，可写多个, 值可以是由关键词或话题组成的列表，也可以是包含关键词的txt文件路径，
# 如'keyword_list.txt'，txt文件中每个关键词占一行
KEYWORD_LIST = ['迪丽热巴']  # 或者 KEYWORD_LIST = 'keyword_list.txt'
# 要搜索的微博类型，0代表搜索全部微博，1代表搜索全部原创微博，2代表热门微博，3代表关注人微博，
# 4代表认证用户微博，5代表媒体微博，6代表观点微博
WEIBO_TYPE = 1

# 筛选结果微博中必需包含的内容，0代表不筛选，获取全部微博，
# 1代表搜索包含图片的微博，2代表包含视频的微博，3代表包含音乐的微博，
# 4代表包含短链接的微博
CONTAIN_TYPE = 0

# 筛选微博的发布地区，精确到省或直辖市，值不应包含“省”或“市”等字，
# 如想筛选北京市的微博请用“北京”而不是“北京市”，想要筛选安徽省的微博请用“安徽”而不是“安徽省”，
# 可以写多个地区，不筛选请用“全部”
REGION = ['全部']

# 搜索的起始日期，为yyyy-mm-dd形式，搜索结果包含该日期
START_DATE = '2020-03-01'
# 搜索的终止日期，为yyyy-mm-dd形式，搜索结果包含该日期
END_DATE = '2020-03-01'

# 进一步细分搜索的阈值，若结果页数大于等于该值，则认为结果没有完全展示，
# 数值越大速度越快，也越有可能漏掉微博；数值越小速度越慢，获取的微博越多
FURTHER_THRESHOLD = 46

# 爬取结果的数量限制，爬取到该数量的微博后自动停止，设置为0代表不限制
LIMIT_RESULT = 3

# 图片文件存储路径
IMAGES_STORE = './'
# 视频文件存储路径
FILES_STORE = './'

# MONGO_URI = 'localhost'
# MYSQL_HOST = 'localhost'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = '123456'
# MYSQL_DATABASE = 'weibo'
# SQLITE_DATABASE = 'weibo.db'
