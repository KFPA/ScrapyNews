# ScrapyNews
采用scrapy框架抓取新闻的项目

详细使用方式，请看我的博客:
http://www.cnblogs.com/kfpa/
<br/>
最新也在更新关于此爬虫的扩展更多网站，能够轻而易举爬取不同类型的网站，大家可以关注我的公众号，更新我会及时通知。
<br/>

#### 我的微信公众号:

![](kfpa.jpg)
<br/>

# 项目依赖

## windows环境
1.安装Mysql数据库，可以直接去官网安装https://www.mysql.com/

2.安装Microsoft Visual c++ 14.0,可以从微软官网上下载exe安装，http://landinghub.visualstudio.com/visual-cpp-build-tools，scrapy中twisted需要此开发包支持

3.安装requests,chardet,web.py,gevent psutil: pip install requests chardet web.py sqlalchemy gevent psutil 

4.安装pywin32,scrapy，bs4,pillow,opencv-python,pymysql:pip install pywin32 scrapy bs4 pillow opencv-python pymysql

# 配置项目

1.启用ipproxypool项目
  ScrapyNews/IPProxyPool-master/config.py文件内的DB_CONFIG下修改'DB_CONFIG_STRING':'mysql+pymysql':'//username(mysql数据库用户名)：password(数据库密码)@localhost/数据库中创建的数据库名称?charset=utf8'
2.启用scrapynews项目
  ScrapyNews/Scrapywork/setting.py文件内的db={}中将user和passwd都修改为指定的mysql数据库的用户名和密码，并且创建一个article的数据库
 


##  注意:
	创建数据库是指定编码形式为utf-8；例 create database db default character set=utf8
# 特点：

1.采用IP池，防止目的网站封锁ip，IP池采用的是IPProxy开源项目，提供的ip很稳定，数目足够，完全可以满足个人或者小型的项目使用；

2.禁用爬虫代理，采用useragent代理池，防止网站根据代理封锁爬虫；

3.智能延迟，爬去网页间隔时间可以智能的调节；

4.数据存储采用MySQL数据库，并且通过mysql的查询进行增量式的爬取；

5.爬虫规则采用xml的形式自定义，可以满足不同形式的网站结构进行爬取新闻文章，而且可以根据scrapy框架提供的不同形式的spider做相应的类型扩展，也可以自己写不同形式的spider以满足各种不同的爬取需求而且一劳永逸；

6.基于scrapy爬虫框架，scrapy能做的它都是可以做的；

7.使用中间件，包括下载中间件和爬虫中间件；

8.采用邮件通知，可以随时随地的远程监控爬虫的工作状态；

9.打印日志文件，用户可以通过查看日志文件了解爬虫的工作过程；

10.自定义数据库字段，自定义爬取的文章字段；

# 扩展目标：

做可视化的爬虫生成器
这个爬虫工程算是通向可视化爬虫的一个台阶，一次性迈到可视化爬虫portia似乎步子太大，容易扯到蛋，通过这个项目能够更好的理解scrapy框架的工作原理，并且可以自定义通用的爬虫。
爬虫说来说去也就是那么几种，不同的就是每个爬虫爬取网站时数据提取时的规则，大家可以自定义的写自己的规则，就可以通过这类的爬虫爬取信息，写爬虫变成了写规则，这无疑是更方便的！

有一点需要注意portia项目它的可视化爬虫是通过可视化的界面写出一个规定的爬虫来，这个爬虫只能够做对应网站的数据爬取的！
这个项目如果做成可视化爬虫的话，他的目的不是生成一个爬虫，而是生成一个类型的爬虫规则，把这个规则输入到对应的爬虫中就可以爬取数据，这两者其实还是有区别的！

