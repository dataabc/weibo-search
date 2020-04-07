## 功能
连续获取一个或多个**微博关键词搜索**结果，并将结果写入文件（可选）、数据库（可选）等。所谓微博关键词搜索即：**搜索正文中包含指定关键词的微博**，可以指定搜索的时间范围。举个栗子，比如你可以搜索包含关键词“迪丽热巴”且发布日期在2020-03-01和2020-03-16之间的微博。搜索结果数量巨大，对于非常热门的关键词，在一天的指定时间范围，可以获得**1000万**以上的搜索结果。注意这里的一天指的是时间筛选范围，具体多长时间将这1000万微博下载到本地还要看获取的速度。1000万只是一天时间范围可获取的微博数量，如果想获取更多微博，可以加大时间范围，比如10天，最多可以获得1亿条搜索结果。对于大多数关键词，微博一天产生的相关搜索结果应该低于1000万，因此可以说**本程序可以获取指定关键词的全部或近似全部的搜索结果**。本程序可以获得几乎全部的微博信息，如微博正文、发布者等，详情见[输出](#输出)部分。支持输出多种文件类型，具体如下：
- 写入**csv文件**（默认）
- 写入**MySQL数据库**（可选）
- 写入**MongoDB数据库**（可选）
- 下载微博中的**图片**（可选）
- 下载微博中的**视频**（可选）

## 输出
- 微博id：微博的id，为一串数字形式
- 微博bid：微博的bid，与[cookie版](https://github.com/dataabc/weiboSpider)中的微博id是同一个值
- 微博内容：微博正文
- 原始图片url：原创微博图片和转发微博转发理由中图片的url，若某条微博存在多张图片，则每个url以英文逗号分隔，若没有图片则值为''
- 视频url: 微博中的视频url和Live Photo中的视频url，若某条微博存在多个视频，则每个url以英文分号分隔，若没有视频则值为''
- 微博发布位置：位置微博中的发布位置
- 微博发布时间：微博发布时的时间，精确到天
- 点赞数：微博被赞的数量
- 转发数：微博被转发的数量
- 评论数：微博被评论的数量
- 微博发布工具：微博的发布工具，如iPhone客户端、HUAWEI Mate 20 Pro等，若没有则值为''
- 话题：微博话题，即两个#中的内容，若存在多个话题，每个url以英文逗号分隔，若没有则值为''
- @用户：微博@的用户，若存在多个@用户，每个url以英文逗号分隔，若没有则值为''
- 原始微博id：为转发微博所特有，是转发微博中那条被转发微博的id
- 结果文件：保存在当前目录“结果文件”文件夹下以关键词为名的文件夹里
- 微博图片：微博中的图片，保存在以关键词为名的文件夹下的images文件夹里
- 微博视频：微博中的视频，保存在以关键词为名的文件夹下的videos文件夹里

## 使用说明
### 1.下载脚本S
```bash
$ git clone https://github.com/dataabc/weibo-search.git
```
### 2.安装Scrapy
本程序依赖Scrapy，要想运行程序，需要安装Scrapy。如果系统中没有安装Scrapy，请根据自己的系统安装Scrapy。
### 3.配置程序
本程序的所有配置都在setting.py文件中完成，该文件位于“weibo-search\weibo\settings.py”，文件内容大致如下：
```
LOG_LEVEL = 'ERROR'
# 访问完一个页面再访问下一个时需要等待的时间，默认为10秒
DOWNLOAD_DELAY = 10
DEFAULT_REQUEST_HEADERS = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cookie': 'your cookie'
}
ITEM_PIPELINES = {
    'weibo.pipelines.DuplicatesPipeline': 300,
    'weibo.pipelines.CsvPipeline': 301,
    'weibo.pipelines.MysqlPipeline': 302,
    'weibo.pipelines.MongoPipeline': 303,
    'weibo.pipelines.MyImagesPipeline': 304,
    'weibo.pipelines.MyVideoPipeline': 305
}
# 要搜索的关键词列表，可写多个
KEYWORD_LIST = ['迪丽热巴']
# 搜索的起始日期，为yyyy-mm-dd形式，搜索结果包含该日期
START_DATE = '2020-03-01'
# 搜索的终止日期，为yyyy-mm-dd形式，搜索结果包含该日期
END_DATE = '2020-03-01'
# 图片文件存储路径
IMAGES_STORE = './结果文件'
# 视频文件存储路径
FILES_STORE = './结果文件'
# 配置MongoDB数据库
# MONGO_URI = 'localhost'
# 配置MySQL数据库，以下为默认配置，可以根据实际情况更改，程序会自动生成一个名为weibo的数据库，如果想换其它名字请更改MYSQL_DATABASE值
# MYSQL_HOST = 'localhost'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = '123456'
# MYSQL_DATABASE = 'weibo'
```
LOG_LEVEL代表日志的显示级别，“ERROR”意思是只有在程序出错时才显示日志；
DOWNLOAD_DELAY代表访问完一个页面再访问下一个时需要等待的时间，默认为10秒；
DEFAULT_REQUEST_HEADERS中的cookie是我们需要填的值，如何获取cookie详见[如何获取cookie](#如何获取cookie)，获取后将"your cookie"替换成真实的cookie即可；
ITEM_PIPELINES是我们可选的结果写入类型，第一个代表去重，第二个代表写入csv文件，第三个代表写入MySQL数据库，第四个代表写入MongDB数据库，第五个代表下载图片，第六个代表下载视频。后面的数字代表执行的顺序，数字越小优先级越高。如果你只要写入部分类型，可以把不需要的类型用“#”注释掉，以节省资源；
KEYWORD_LIST存储要搜索的关键词，可以写一个或多个；
START_DATE代表搜索的起始日期，END_DATE代表搜索的结束日期。程序会搜索包含关键词且发布时间在起始日期和结束日期之间的微博（包含边界），值为“yyyy-mm-dd”形式；
MONGO_URI是MongoDB数据库的配置；
MYSQL开头的是MySQL数据库的配置。
### 运行程序
```bash
$ scrapy crawl search -s JOBDIR=crawls/search
```
其实只运行“scrapy crawl search”也可以，只是上述方式在结束时可以保存进度，下次运行时会长程序上次的地方继续获取。注意，如果想要保存进度，请使用“Ctrl + C”**一次**，注意是**一次**。按下“Ctrl + C”一次后，程序会继续运行一会，主要用来保存获取的数据、保存进度等操作，请耐心等待。下次再运行时，只要再运行上面的指令就可以恢复上次的进度。
## 如何获取cookie
1.用Chrome打开<https://passport.weibo.cn/signin/login>；<br>
2.输入微博的用户名、密码，登录，如图所示：
![](https://picture.cognize.me/cognize/github/weibospider/cookie1.png)
登录成功后会跳转到<https://m.weibo.cn>;<br>
3.按F12键打开Chrome开发者工具，在地址栏输入并跳转到<https://weibo.cn>，跳转后会显示如下类似界面:
![](https://picture.cognize.me/cognize/github/weibospider/cookie2.png)
4.依此点击Chrome开发者工具中的Network->Name中的weibo.cn->Headers->Request Headers，"Cookie:"后的值即为我们要找的cookie值，复制即可，如图所示：
![](https://picture.cognize.me/cognize/github/weibospider/cookie3.png)
